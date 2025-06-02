<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreChatSessionRequest;
use App\Http\Requests\UpdateChatSessionRequest;
use App\Models\ChatSession;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;
use Inertia\Response;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Support\Facades\Config;

class ChatSessionController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(): Response
    {
        $sessions = Auth::user()->chatSessions()
            ->select('id', 'title', 'created_at', 'ai_configuration_key') // Also select the key
            ->latest()
            // ->withCount('messages') // Optional: Count messages for display
            ->paginate(15); // Paginate results

        // Get AI configurations from config file
        $aiConfigs = Config::get('ai_configurations', []);
        // Prepare for frontend dropdown (key -> name)
        $availableAiConfigs = collect($aiConfigs)->mapWithKeys(function ($config, $key) {
            return [$key => $config['name'] ?? $key];
        })->all();

        return Inertia::render('ChatSessions/Index', [
            'sessions' => $sessions,
            'availableAiConfigs' => $availableAiConfigs, // Pass configurations to the view
        ]);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        // Typically not needed for SPA if creation is just a button click
        // Redirect to store method or handle directly in index view
        return Redirect::route('chat-sessions.store');
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreChatSessionRequest $request): RedirectResponse
    {
        // Get validated data, including the optional ai_configuration_key
        $validatedData = $request->validated();

        // If the key isn't provided or is null, the database default ('default') will be used.
        // We merge the user_id here as it's not part of the form request usually.
        $session = Auth::user()->chatSessions()->create(
            array_merge($validatedData, ['user_id' => Auth::id()])
        );

        // Redirect to the show view for the newly created session
        return Redirect::route('chat-sessions.show', $session->id)
            ->with('success', 'New chat session started.');
    }

    /**
     * Display the specified resource.
     */
    public function show(ChatSession $chatSession): Response
    {
        // Authorize: Ensure the session belongs to the logged-in user
        if ($chatSession->user_id !== Auth::id()) {
            abort(403);
        }

        // Pass session ID and Title
        return Inertia::render('SupportChat', [
            'chatSessionId' => $chatSession->id,
            'chatSessionTitle' => $chatSession->title ?? ('Chat #' . $chatSession->id) // Pass title or default
        ]);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(ChatSession $chatSession)
    {
        // Might not be needed for SPA, could edit name inline?
        // If needed, pass session to an edit view
        abort(501); // Not implemented
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(UpdateChatSessionRequest $request, ChatSession $chatSession): RedirectResponse
    {
        // Authorize
        if ($chatSession->user_id !== Auth::id()) {
            abort(403);
        }

        // Validate (UpdateChatSessionRequest should define rules for 'title')
        $validated = $request->validated();

        $chatSession->update($validated);

        // Use inertia redirect for SPA update without full page reload
        // Or return JSON response if handling via direct API call from component
        return Redirect::back()->with('success', 'Chat session renamed.');
        // If using inline edit, might return json instead:
        // return response()->json(['success' => true, 'new_title' => $validated['title']]);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(ChatSession $chatSession): RedirectResponse
    {
        // Authorize
        if ($chatSession->user_id !== Auth::id()) {
            abort(403);
        }

        $chatSession->delete();

        return Redirect::route('chat-sessions.index')
            ->with('success', 'Chat session deleted successfully.');
    }
}
