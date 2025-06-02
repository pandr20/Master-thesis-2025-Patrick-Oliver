<?php

namespace App\Http\Controllers;

use App\Models\ChatSession; // Import ChatSession
use Illuminate\Http\Request;
// Remove Provider enum import if no longer needed, or keep if used elsewhere
// use Prism\Prism\Enums\Provider; 
use Prism\Prism\Prism;
use Illuminate\Support\Facades\Auth; // Import Auth facade
use App\Models\ChatMessage; // Import ChatMessage
use Illuminate\Validation\Rule; // Import Rule
use Illuminate\Support\Facades\Config; // Import Config facade
use Illuminate\Support\Facades\View; // Import View facade

class AiSupportController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        //
    }

    // Method to get chat history for a specific session
    public function getHistory(Request $request)
    {
        $request->validate([
            'session_id' => 'required|integer|exists:chat_sessions,id'
        ]);

        $sessionId = $request->input('session_id');
        $user = Auth::user();

        // Find the requested session and verify ownership
        $session = ChatSession::where('id', $sessionId)
            ->where('user_id', $user->id)
            ->firstOrFail(); // Fails if not found or not owned

        // Eager load feedback relationship
        $messages = $session->messages()->with('feedback')->orderBy('created_at', 'asc')->get();

        // Format messages (same as before)
        $formattedMessages = $messages->map(function ($message) use ($user) { // Pass user
            $feedbackRating = null;
            if ($message->sender === 'ai' && $message->feedback) {
                // Check if the feedback belongs to the current user
                if ($message->feedback->user_id === $user->id) {
                    $feedbackRating = $message->feedback->rating;
                }
            }
            return [
                'db_id' => $message->id,
                'sender' => $message->sender,
                'text' => $message->message,
                'created_at' => $message->created_at->toDateTimeString(),
                'feedbackGiven' => $feedbackRating,
            ];
        });

        return response()->json(['messages' => $formattedMessages]);
    }

    // Add the chat method
    public function chat(Request $request)
    {
        $request->validate([
            'message' => 'required|string|max:1000',
            'session_id' => 'required|integer|exists:chat_sessions,id',
        ]);

        $sessionId = $request->input('session_id');
        $user = Auth::user();

        // Find the requested session and verify ownership
        $session = ChatSession::where('id', $sessionId)
            ->where('user_id', $user->id)
            ->firstOrFail(); // Ensures user owns the session

        $userMessageText = $request->input('message');

        // Save user message
        $userChatMessage = $session->messages()->create([
            'sender' => 'user',
            'message' => $userMessageText,
        ]);

        // --- Title Generation (unchanged, uses default AI settings for simplicity) ---
        if (is_null($session->title)) {
            try {
                $titlePrompt = "Generate a very short title (max 5 words) for a chat based on this first user message: \"" . $userMessageText . "\"";
                $defaultConfig = Config::get('ai_configurations.default');
                $titleResponse = Prism::text()
                    ->using($defaultConfig['provider'], $defaultConfig['model'])
                    ->withPrompt($titlePrompt)
                    ->asText();
                $generatedTitle = trim($titleResponse->text, " \t\n\r\0\x0B\"'");
                $generatedTitle = mb_substr($generatedTitle, 0, 100);
                if (!empty($generatedTitle)) {
                    $session->update(['title' => $generatedTitle]);
                }
            } catch (\Exception $e) {
                logger()->error('Chat title generation failed: ' . $e->getMessage());
            }
        }
        // --- End Title Generation ---

        // --- Get AI Configuration based on Session ---
        $configKey = $session->ai_configuration_key ?? 'default';
        $aiConfig = Config::get("ai_configurations.{$configKey}");

        // Fallback to default if the key is invalid or config missing
        if (!$aiConfig) {
            logger()->warning("Invalid ai_configuration_key '{$configKey}' for session {$session->id}. Falling back to default.");
            $configKey = 'default';
            $aiConfig = Config::get("ai_configurations.default");
        }

        // Further fallback if even default is somehow missing
        if (!$aiConfig) {
            logger()->error("Default AI configuration ('ai_configurations.default') is missing.");
            return response()->json(['error' => 'Server configuration error.'], 500);
        }

        $aiProvider = $aiConfig['provider'];
        $aiModel = $aiConfig['model'];
        $systemPromptView = $aiConfig['system_prompt_view'];
        $systemPrompt = '';

        // Validate and render the system prompt view
        if (View::exists($systemPromptView)) {
            $systemPrompt = View::make($systemPromptView)->render();
        } else {
            logger()->error("System prompt view '{$systemPromptView}' not found for AI config key '{$configKey}'. Using empty prompt.");
            // Decide if you want to fallback to a default prompt here instead of empty
            // $systemPrompt = View::make(Config::get('ai_configurations.default.system_prompt_view'))->render();
        }
        // --- End Get AI Configuration ---

        $aiResponseText = null;
        $aiMessageId = null;

        try {
            // --- Call AI using selected configuration ---
            $response = Prism::text()
                ->using($aiProvider, $aiModel)
                ->withSystemPrompt($systemPrompt)
                ->withPrompt($userMessageText)
                ->asText();
            $aiResponseText = $response->text;

            // Save AI response
            $aiMessage = $session->messages()->create([
                'sender' => 'ai',
                'message' => $aiResponseText,
                // Optional: could also save the $configKey here if needed for message-level analysis
            ]);
            $aiMessageId = $aiMessage->id;

        } catch (\Exception $e) {
            logger()->error("AI API Error (Config: {$configKey}, Provider: {$aiProvider}, Model: {$aiModel}): " . $e->getMessage(), ['exception' => $e]);
            // Save error message
            $session->messages()->create([
                'sender' => 'ai',
                'message' => '[Error fetching response]',
            ]);
            return response()->json(['error' => 'Sorry, I encountered an error trying to respond.'], 500);
        }

        // Return the reply
        return response()->json([
            'reply' => $aiResponseText,
            'ai_message_id' => $aiMessageId,
            'session_title' => $session->refresh()->title,
        ]);
    }

    // Method to handle feedback submission
    public function submitFeedback(Request $request)
    {
        $request->validate([
            'message_id' => 'required|integer|exists:chat_messages,id',
            'rating' => ['required', Rule::in(['positive', 'negative'])],
            'comment' => 'nullable|string|max:1000',
        ]);

        $user = Auth::user();
        $messageId = $request->input('message_id');

        // Optional: Verify the message belongs to the user's session 
        // or is an AI message from a session they participated in.
        $message = ChatMessage::findOrFail($messageId);
        // Add authorization check here if needed (e.g., ensure message sender is 'ai')
        if ($message->sender !== 'ai') {
            return response()->json(['error' => 'Feedback can only be submitted for AI messages.'], 403);
        }
        // Add check to ensure message belongs to one of the user's sessions if necessary

        // Use updateOrCreate to handle potential unique constraint violations gracefully
        // (if user tries to submit feedback for the same message twice)
        $feedback = $message->feedback()->updateOrCreate(
            [
                'chat_message_id' => $messageId, // Technically redundant as we query via relationship
                'user_id' => $user->id,
            ],
            [
                'rating' => $request->input('rating'),
                'comment' => $request->input('comment'),
            ]
        );

        return response()->json(['success' => true, 'feedback_id' => $feedback->id]);
    }
}
