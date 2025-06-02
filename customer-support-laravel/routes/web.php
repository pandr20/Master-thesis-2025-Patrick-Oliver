<?php

use App\Http\Controllers\AiSupportController;
use App\Http\Controllers\ChatSessionController;
use App\Http\Controllers\Admin\FeedbackDashboardController;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    return Inertia::render('Welcome');
})->name('home');

Route::get('dashboard', [FeedbackDashboardController::class, 'index'])
    ->middleware(['auth', 'verified'])->name('dashboard');

Route::post('/api/chat', [AiSupportController::class, 'chat'])->middleware('auth');

// Add route for fetching chat history
Route::get('/api/chat/history', [AiSupportController::class, 'getHistory'])->middleware('auth')->name('api.chat.history');

// Add the route for the support chat page
Route::get('/support-chat', function () {
    return Inertia::render('SupportChat');
})->middleware(['auth', 'verified'])->name('support.chat');

// Add route for submitting feedback
Route::post('/api/chat/feedback', [AiSupportController::class, 'submitFeedback'])
    ->middleware('auth')
    ->name('api.chat.feedback');

// Routes for managing Chat Sessions (CRUD)
Route::resource('chat-sessions', ChatSessionController::class)
    ->middleware(['auth', 'verified']);

require __DIR__ . '/settings.php';
require __DIR__ . '/auth.php';
