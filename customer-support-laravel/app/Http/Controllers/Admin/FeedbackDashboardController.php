<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\ChatFeedback;
use App\Models\ChatSession;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

class FeedbackDashboardController extends Controller
{
    /**
     * Display the feedback dashboard.
     */
    public function index(Request $request): Response
    {
        // Calculate overall stats
        $totalFeedback = ChatFeedback::count();
        $positiveFeedback = ChatFeedback::where('rating', 'positive')->count();
        $negativeFeedback = ChatFeedback::where('rating', 'negative')->count();

        $positivePercentage = $totalFeedback > 0 ? round(($positiveFeedback / $totalFeedback) * 100, 1) : 0;

        // Get total chat sessions count
        $totalSessions = ChatSession::count();

        // Fetch recent feedback entries with associated message
        $recentFeedback = ChatFeedback::with(['chatMessage', 'user'])
            ->latest()
            ->paginate(20);

        // Explicitly map needed data, including session ID
        $formattedFeedback = $recentFeedback->through(function ($feedback) {
            return [
                'id' => $feedback->id,
                'rating' => $feedback->rating,
                'comment' => $feedback->comment,
                'created_at' => $feedback->created_at,
                'user' => $feedback->user ? [
                    'id' => $feedback->user->id,
                    'name' => $feedback->user->name,
                ] : null,
                'chat_message' => $feedback->chatMessage ? [
                    'id' => $feedback->chatMessage->id,
                    'message' => $feedback->chatMessage->message,
                    // Include the session ID directly for easier linking
                    'chat_session_id' => $feedback->chatMessage->chat_session_id,
                ] : null,
            ];
        });

        // Render the main Dashboard view with the data
        return Inertia::render('Dashboard', [
            'stats' => [
                'total' => $totalFeedback,
                'positive' => $positiveFeedback,
                'negative' => $negativeFeedback,
                'positivePercentage' => $positivePercentage,
                'totalSessions' => $totalSessions,
            ],
            'recentFeedback' => $formattedFeedback,
        ]);
    }
}
