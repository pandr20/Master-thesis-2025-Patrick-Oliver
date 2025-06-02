<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue';
import type { PaginatedResponse } from '@/types'; // Assuming a type for pagination
import { Link, router } from '@inertiajs/vue3';
import { Bot, ChevronDown, Clock, MessageSquarePlus, Trash2 } from 'lucide-vue-next';
import { ref } from 'vue'; // Import ref

interface ChatSession {
    id: number;
    created_at: string; // Or format as needed
    title: string | null; // Add title
    ai_configuration_key: string; // Add the key here
}

// Define props including the new AI configs map
defineProps<{
    sessions: PaginatedResponse<ChatSession>;
    availableAiConfigs: { [key: string]: string }; // key -> display name
}>();

// Ref to hold the selected AI configuration key
const selectedAiConfigKey = ref<string>('default'); // Default to 'default'

const createNewSession = () => {
    // Include the selected key in the POST data
    router.post(route('chat-sessions.store'), {
        ai_configuration_key: selectedAiConfigKey.value,
    });
};

const deleteSession = (sessionId: number) => {
    if (confirm('Are you sure you want to delete this chat session and all its messages?')) {
        router.delete(route('chat-sessions.destroy', sessionId), {
            preserveScroll: true, // Keep scroll position on page reload
        });
    }
};

// Enhanced date formatting function
const formatRelativeDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return rtf.format(-minutes, 'minute');
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return rtf.format(-hours, 'hour');
    } else if (diffInSeconds < 604800) {
        const days = Math.floor(diffInSeconds / 86400);
        return rtf.format(-days, 'day');
    } else {
        // For older dates, show the actual date
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    }
};
</script>

<template>
    <AppLayout title="My Chat Sessions">
        <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-gray-900 dark:to-gray-800">
            <div class="container mx-auto px-4 py-8 sm:px-6 lg:px-8">
                <!-- Header Section -->
                <div class="mb-8">
                    <div class="flex items-center justify-between">
                        <div>
                            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Chat Sessions</h1>
                            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">Manage your AI conversations and start new chats</p>
                        </div>
                        <div class="flex items-center gap-3">
                            <!-- AI Configuration Dropdown -->
                            <div class="relative">
                                <label for="ai-config-select" class="sr-only">AI Model</label>
                                <div class="relative">
                                    <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                        <Bot class="h-4 w-4 text-gray-400 dark:text-gray-500" />
                                    </div>
                                    <select
                                        id="ai-config-select"
                                        v-model="selectedAiConfigKey"
                                        class="focus:ring-opacity-25 block w-full appearance-none rounded-xl border-gray-300 bg-white py-2.5 pr-10 pl-10 text-sm font-medium shadow-sm transition-all duration-200 hover:border-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:border-gray-500 dark:focus:border-blue-400 dark:focus:ring-blue-400"
                                    >
                                        <option v-for="(name, key) in availableAiConfigs" :key="key" :value="key">
                                            {{ name }}
                                        </option>
                                    </select>
                                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                        <ChevronDown class="h-4 w-4 text-gray-400 dark:text-gray-500" />
                                    </div>
                                </div>
                            </div>
                            <!-- New Chat Button -->
                            <button
                                @click="createNewSession"
                                class="inline-flex items-center rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-2.5 text-sm font-semibold text-white shadow-lg transition-all duration-200 hover:from-blue-700 hover:to-blue-800 hover:shadow-xl focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none dark:focus:ring-offset-gray-800"
                            >
                                <MessageSquarePlus class="mr-2 h-5 w-5" />
                                New Chat
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Chat Sessions Grid -->
                <div v-if="sessions.data.length > 0" class="grid gap-4 sm:gap-6">
                    <div
                        v-for="session in sessions.data"
                        :key="session.id"
                        class="group relative overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 hover:border-gray-300 hover:shadow-md dark:border-gray-700 dark:bg-gray-800 dark:hover:border-gray-600"
                    >
                        <!-- Clickable Chat Session Content -->
                        <Link
                            :href="route('chat-sessions.show', session.id)"
                            class="block p-6 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-inset"
                        >
                            <div class="flex items-start justify-between">
                                <div class="min-w-0 flex-1">
                                    <div class="mb-2 flex items-center gap-2">
                                        <h3
                                            class="truncate text-lg font-semibold text-gray-900 transition-colors group-hover:text-blue-600 dark:text-white dark:group-hover:text-blue-400"
                                        >
                                            {{ session.title || `Chat Session #${session.id}` }}
                                        </h3>
                                        <span
                                            class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:bg-blue-900 dark:text-blue-300"
                                        >
                                            {{ availableAiConfigs[session.ai_configuration_key] || session.ai_configuration_key }}
                                        </span>
                                    </div>

                                    <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                                        <Clock class="h-4 w-4" />
                                        <span>{{ formatRelativeDate(session.created_at) }}</span>
                                    </div>
                                </div>
                            </div>
                        </Link>

                        <!-- Action Buttons - Positioned absolutely to avoid interfering with main click -->
                        <div class="absolute top-4 right-4 flex items-center gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                            <button
                                @click.stop="deleteSession(session.id)"
                                class="inline-flex items-center rounded-lg bg-red-100 p-2.5 text-red-600 transition-colors hover:bg-red-200 hover:text-red-900 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:outline-none dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30 dark:hover:text-red-300 dark:focus:ring-offset-gray-800"
                                title="Delete Chat"
                            >
                                <Trash2 class="h-4 w-4" />
                            </button>
                        </div>

                        <!-- Subtle gradient overlay on hover -->
                        <div
                            class="pointer-events-none absolute inset-0 bg-gradient-to-r from-blue-500/0 to-purple-500/0 opacity-0 transition-opacity duration-300 group-hover:opacity-5"
                        ></div>
                    </div>
                </div>

                <!-- Empty State -->
                <div v-else class="py-12 text-center">
                    <div class="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
                        <MessageSquarePlus class="h-12 w-12 text-gray-400 dark:text-gray-500" />
                    </div>
                    <h3 class="mt-6 text-lg font-semibold text-gray-900 dark:text-white">No chat sessions yet</h3>
                    <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Get started by creating your first AI conversation</p>
                    <div class="mt-6">
                        <button
                            @click="createNewSession"
                            class="inline-flex items-center rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-2.5 text-sm font-semibold text-white shadow-lg transition-all duration-200 hover:from-blue-700 hover:to-blue-800 hover:shadow-xl focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none dark:focus:ring-offset-gray-800"
                        >
                            <MessageSquarePlus class="mr-2 h-5 w-5" />
                            Start Your First Chat
                        </button>
                    </div>
                </div>

                <!-- Add Pagination Links if needed -->
                <!-- <Pagination :links="sessions.links" class="mt-8" /> -->
            </div>
        </div>
    </AppLayout>
</template>
