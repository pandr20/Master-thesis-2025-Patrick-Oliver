<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue';
import type { PaginatedResponse } from '@/types';
import { Link } from '@inertiajs/vue3';
import { ExternalLink, ThumbsDown, ThumbsUp } from 'lucide-vue-next';
import { defineProps } from 'vue';

// Define interfaces for the data passed from controller
interface Stats {
    total: number;
    positive: number;
    negative: number;
    positivePercentage: number;
    totalSessions: number;
}

interface ChatMessage {
    id: number;
    message: string;
    chat_session_id: number;
}

interface User {
    id: number;
    name: string;
}

interface FeedbackEntry {
    id: number;
    rating: 'positive' | 'negative';
    comment: string | null;
    created_at: string;
    chat_message: ChatMessage | null;
    user: User | null;
}

defineProps<{
    stats: Stats;
    recentFeedback: PaginatedResponse<FeedbackEntry>;
}>();

// Helper to format dates (optional)
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
};
</script>

<template>
    <AppLayout title="Feedback Dashboard">
        <div class="container mx-auto p-4 sm:p-6 lg:p-8">
            <h1 class="mb-6 text-2xl font-semibold text-gray-900 dark:text-white">AI Chat Feedback</h1>

            <!-- Stats Section -->
            <div class="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5">
                <div class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6 dark:bg-gray-800">
                    <dt class="truncate text-sm font-medium text-gray-500 dark:text-gray-400">Total Feedback</dt>
                    <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white">{{ stats.total }}</dd>
                </div>
                <div class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6 dark:bg-gray-800">
                    <dt class="truncate text-sm font-medium text-gray-500 dark:text-gray-400">Positive Ratings</dt>
                    <dd class="mt-1 text-3xl font-semibold tracking-tight text-green-600">{{ stats.positive }}</dd>
                </div>
                <div class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6 dark:bg-gray-800">
                    <dt class="truncate text-sm font-medium text-gray-500 dark:text-gray-400">Negative Ratings</dt>
                    <dd class="mt-1 text-3xl font-semibold tracking-tight text-red-600">{{ stats.negative }}</dd>
                </div>
                <div class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6 dark:bg-gray-800">
                    <dt class="truncate text-sm font-medium text-gray-500 dark:text-gray-400">Positive Rate</dt>
                    <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white">{{ stats.positivePercentage }}%</dd>
                </div>
                <div class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6 dark:bg-gray-800">
                    <dt class="truncate text-sm font-medium text-gray-500 dark:text-gray-400">Total Chats</dt>
                    <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900 dark:text-white">{{ stats.totalSessions }}</dd>
                </div>
            </div>

            <!-- Recent Feedback Table -->
            <h2 class="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Recent Feedback</h2>
            <div class="overflow-hidden rounded-lg bg-white shadow dark:bg-gray-800">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-700">
                            <tr>
                                <th
                                    scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-300"
                                >
                                    Rating
                                </th>
                                <th
                                    scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-300"
                                >
                                    AI Message
                                </th>
                                <th
                                    scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-300"
                                >
                                    Comment
                                </th>
                                <th
                                    scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-300"
                                >
                                    User
                                </th>
                                <th
                                    scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-300"
                                >
                                    Date
                                </th>
                                <th
                                    scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-300"
                                >
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-800">
                            <tr v-if="recentFeedback.data.length === 0">
                                <td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">No feedback submitted yet.</td>
                            </tr>
                            <tr v-for="feedback in recentFeedback.data" :key="feedback.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                                <td class="px-6 py-4 text-sm whitespace-nowrap">
                                    <span v-if="feedback.rating === 'positive'" class="inline-flex items-center text-green-600">
                                        <ThumbsUp class="mr-1 h-4 w-4" /> Positive
                                    </span>
                                    <span v-else class="inline-flex items-center text-red-600"> <ThumbsDown class="mr-1 h-4 w-4" /> Negative </span>
                                </td>
                                <td
                                    class="max-w-md truncate overflow-hidden px-6 py-4 text-sm text-gray-500 dark:text-gray-300"
                                    :title="feedback.chat_message?.message"
                                >
                                    {{ feedback.chat_message?.message || '[Message Unavailable]' }}
                                </td>
                                <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-300">{{ feedback.comment || '-' }}</td>
                                <td class="px-6 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-300">
                                    {{ feedback.user?.name || '[User Unavailable]' }}
                                </td>
                                <td class="px-6 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-300">
                                    {{ formatDate(feedback.created_at) }}
                                </td>
                                <td class="px-6 py-4 text-center text-sm">
                                    <Link
                                        v-if="feedback.chat_message?.chat_session_id"
                                        :href="route('chat-sessions.show', feedback.chat_message.chat_session_id)"
                                        class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                                        title="View Chat Session"
                                    >
                                        <ExternalLink class="inline h-5 w-5" />
                                    </Link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- Add Pagination Links if needed -->
            <!-- <Pagination :links="recentFeedback.links" class="mt-6" /> -->
        </div>
    </AppLayout>
</template>
