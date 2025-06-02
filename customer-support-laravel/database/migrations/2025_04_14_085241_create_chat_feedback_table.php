<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('chat_feedback', function (Blueprint $table) {
            $table->id();
            // Link to the specific AI message being reviewed
            $table->foreignId('chat_message_id')->constrained()->onDelete('cascade');
            // Link to the user providing feedback
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->enum('rating', ['positive', 'negative']); // Simple thumbs up/down
            $table->text('comment')->nullable(); // Optional free-text comment
            $table->timestamps();

            // Ensure a user can only rate a specific message once
            $table->unique(['chat_message_id', 'user_id']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('chat_feedback');
    }
};
