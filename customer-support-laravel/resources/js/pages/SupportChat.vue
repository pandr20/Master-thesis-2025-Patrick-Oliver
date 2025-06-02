<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue'; // Assuming you have a layout
import { useForm } from '@inertiajs/vue3'; // Import useForm
import axios from 'axios';
import { Pencil, ThumbsDown, ThumbsUp } from 'lucide-vue-next'; // Import icons
import { defineProps, nextTick, onMounted, ref } from 'vue';

// Define props passed from controller (show method)
const props = defineProps<{
    chatSessionId: number;
    chatSessionTitle: string; // Add title prop
}>();

// Make title reactive for renaming later
const currentChatTitle = ref(props.chatSessionTitle);
const isEditingTitle = ref(false);

// Form helper for title update
const titleForm = useForm({
    title: props.chatSessionTitle,
});

interface Message {
    id: number;
    db_id?: number;
    text: string;
    sender: 'user' | 'ai';
    aiMessageId?: number; // Store the DB ID for AI messages
    feedbackGiven?: 'positive' | 'negative' | null; // Track feedback state
}

const messages = ref<Message[]>([]);
const newMessage = ref('');
const isLoading = ref(false);
const isLoadingHistory = ref(false);
let messageIdCounter = 0;
const chatContainer = ref<HTMLDivElement | null>(null);

const scrollToBottom = async () => {
    await nextTick();
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
};

onMounted(async () => {
    if (!props.chatSessionId) return;
    isLoadingHistory.value = true;
    try {
        const response = await axios.get<{ messages: any[] }>(route('api.chat.history', { session_id: props.chatSessionId }));
        messages.value = response.data.messages.map((msg) => ({
            id: messageIdCounter++,
            db_id: msg.db_id,
            text: msg.text,
            sender: msg.sender,
            feedbackGiven: msg.feedbackGiven,
            aiMessageId: msg.sender === 'ai' ? msg.db_id : undefined,
        }));
        scrollToBottom();
    } catch (error) {
        console.error('Error fetching chat history:', error);
    } finally {
        isLoadingHistory.value = false;
    }
});

const sendMessage = async () => {
    if (!props.chatSessionId) return;
    const userMessageText = newMessage.value.trim();
    if (!userMessageText) return;

    const userFrontendId = messageIdCounter++;
    messages.value.push({
        id: userFrontendId,
        text: userMessageText,
        sender: 'user',
    });
    scrollToBottom();

    newMessage.value = '';
    isLoading.value = true;

    try {
        const response = await axios.post<{ reply: string; ai_message_id: number; session_title?: string }>('/api/chat', {
            message: userMessageText,
            session_id: props.chatSessionId,
        });

        messages.value.push({
            id: messageIdCounter++,
            db_id: response.data.ai_message_id,
            text: response.data.reply,
            sender: 'ai',
            aiMessageId: response.data.ai_message_id,
            feedbackGiven: null,
        });

        if (response.data.session_title) {
            currentChatTitle.value = response.data.session_title;
            titleForm.title = response.data.session_title;
        }

        scrollToBottom();
    } catch (error) {
        console.error('Error sending message:', error);
        messages.value.push({
            id: messageIdCounter++,
            text: 'Sorry, there was an error getting a response.',
            sender: 'ai',
        });
        scrollToBottom();
    } finally {
        isLoading.value = false;
    }
};

const submitFeedback = async (message: Message, rating: 'positive' | 'negative') => {
    const messageIdForFeedback = message.db_id;
    if (!messageIdForFeedback || message.feedbackGiven) return;

    message.feedbackGiven = rating;

    try {
        await axios.post('/api/chat/feedback', {
            message_id: messageIdForFeedback,
            rating: rating,
        });
    } catch (error) {
        console.error('Error submitting feedback:', error);
        message.feedbackGiven = null;
    }
};

const startEditingTitle = () => {
    titleForm.title = currentChatTitle.value; // Sync form with current title
    isEditingTitle.value = true;
    // Focus input field maybe?
};

const cancelEditingTitle = () => {
    isEditingTitle.value = false;
    titleForm.reset(); // Reset any changes
};

const saveTitle = () => {
    titleForm.patch(route('chat-sessions.update', props.chatSessionId), {
        preserveScroll: true,
        onSuccess: () => {
            currentChatTitle.value = titleForm.title; // Update local title on success
            isEditingTitle.value = false;
        },
        onError: () => {
            // Handle validation errors (shown automatically by useForm)
            // Maybe keep editing state active?
        },
    });
};
</script>

<template>
    <AppLayout :title="currentChatTitle">
        <div class="flex h-[calc(100vh-10rem)] flex-col rounded-lg bg-gray-100 p-4 shadow-md dark:bg-gray-900">
            <!-- Optional: Add header within chat area to display/edit title -->
            <div class="flex items-center justify-between border-b border-gray-300 p-3 dark:border-gray-700">
                <!-- Show Title or Edit Input -->
                <h2 v-if="!isEditingTitle" class="text-lg font-semibold text-gray-800 dark:text-gray-200">{{ currentChatTitle }}</h2>
                <input
                    v-else
                    v-model="titleForm.title"
                    @keyup.enter="saveTitle"
                    @keyup.esc="cancelEditingTitle"
                    type="text"
                    class="flex-grow rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-lg dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    ref="titleInput"
                />
                <!-- Edit/Save/Cancel Buttons -->
                <div class="ml-3">
                    <button
                        v-if="!isEditingTitle"
                        @click="startEditingTitle"
                        class="p-1 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                    >
                        <Pencil class="h-5 w-5" />
                    </button>
                    <template v-else>
                        <button
                            @click="saveTitle"
                            :disabled="titleForm.processing"
                            class="mr-2 rounded bg-green-500 px-2 py-1 text-xs text-white hover:bg-green-600 disabled:opacity-50"
                        >
                            Save
                        </button>
                        <button @click="cancelEditingTitle" class="rounded bg-gray-500 px-2 py-1 text-xs text-white hover:bg-gray-600">Cancel</button>
                    </template>
                </div>
            </div>

            <!-- Chat Messages -->
            <div ref="chatContainer" class="mb-4 flex-1 space-y-4 overflow-y-auto pr-2">
                <div v-if="isLoadingHistory" class="py-4 text-center text-gray-500">Loading history...</div>
                <div
                    v-else
                    v-for="message in messages"
                    :key="message.id"
                    :class="['flex flex-col', message.sender === 'user' ? 'items-end' : 'items-start']"
                >
                    <div
                        :class="[
                            'max-w-xs rounded-lg px-4 py-2 shadow lg:max-w-md',
                            message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-white text-gray-900 dark:bg-gray-700 dark:text-gray-100',
                        ]"
                    >
                        <p class="whitespace-pre-wrap">{{ message.text }}</p>
                    </div>
                    <div v-if="message.sender === 'ai' && message.db_id" class="mt-1 flex space-x-2">
                        <button
                            @click="submitFeedback(message, 'positive')"
                            :disabled="!!message.feedbackGiven"
                            title="Good response"
                            :class="[
                                'rounded-full p-1 text-gray-400 hover:bg-green-100 hover:text-green-600 disabled:text-gray-400 disabled:opacity-50 disabled:hover:bg-transparent dark:hover:bg-gray-600',
                                message.feedbackGiven === 'positive' ? 'bg-green-100 !text-green-500 dark:bg-gray-600' : '',
                            ]"
                        >
                            <ThumbsUp class="h-4 w-4" />
                        </button>
                        <button
                            @click="submitFeedback(message, 'negative')"
                            :disabled="!!message.feedbackGiven"
                            title="Bad response"
                            :class="[
                                'rounded-full p-1 text-gray-400 hover:bg-red-100 hover:text-red-600 disabled:text-gray-400 disabled:opacity-50 disabled:hover:bg-transparent dark:hover:bg-gray-600',
                                message.feedbackGiven === 'negative' ? 'bg-red-100 !text-red-500 dark:bg-gray-600' : '',
                            ]"
                        >
                            <ThumbsDown class="h-4 w-4" />
                        </button>
                    </div>
                </div>
                <div v-if="isLoading && !isLoadingHistory" class="flex justify-start">
                    <div class="max-w-xs rounded-lg bg-white px-4 py-2 text-gray-900 shadow lg:max-w-md dark:bg-gray-700 dark:text-gray-100">
                        <p class="italic">AI is thinking...</p>
                    </div>
                </div>
            </div>

            <!-- Message Input -->
            <div class="flex border-t border-gray-300 pt-4 dark:border-gray-700">
                <input
                    v-model="newMessage"
                    @keyup.enter="sendMessage"
                    :disabled="isLoading"
                    type="text"
                    placeholder="Spørger CJ Complex Support..."
                    class="flex-1 rounded-l-md border px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100"
                />
                <button
                    @click="sendMessage"
                    :disabled="isLoading || !newMessage.trim()"
                    class="rounded-r-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
                >
                    Send
                </button>
            </div>
        </div>
    </AppLayout>
</template>
