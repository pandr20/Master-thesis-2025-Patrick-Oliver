# AI-Powered Customer Support Chat System

A Laravel-based customer support chat application with AI integration, featuring multiple AI model configurations, session management, and user feedback collection.

## 🎯 Project Overview

This application demonstrates a customer support chat system built with modern web technologies. It uses traditional HTTP-based architecture to deliver a robust, dependable chat experience while accepting the trade-off of not having real-time interaction capabilities.

### Key Characteristics

- **HTTP-Based Architecture**: Uses traditional request-response cycles rather than WebSockets
- **AI Integration**: Multiple AI providers and models supported through the Prism PHP library
- **Session Management**: Persistent chat sessions with full message history
- **User Authentication**: Complete user registration and authentication system
- **Feedback System**: Thumbs up/down feedback collection for AI responses
- **Admin Dashboard**: Feedback analytics and session management

## 🚀 Technology Stack

### Backend

- **Laravel 12.x** - PHP framework
- **Prism PHP** - AI model integration library
- **SQLite/MySQL** - Database (SQLite by default)
- **Inertia.js** - Full-stack framework bridge

### Frontend

- **Vue.js 3** - JavaScript framework
- **Tailwind CSS 4.x** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and development server

### AI Providers Supported

- Google Gemini (default)
- OpenAI GPT
- Anthropic Claude
- Mistral AI
- Groq
- xAI
- DeepSeek
- Ollama (local models)
- VoyageAI

## ✨ Features

### Core Functionality

- **Multi-Session Chat**: Users can create and manage multiple chat sessions
- **AI Model Selection**: Choose from different AI configurations per session
- **Message History**: Complete conversation history with session persistence
- **Session Titles**: Auto-generated or manually editable session titles
- **User Authentication**: Registration, login, and session management

### AI Integration

- **Multiple Providers**: Support for various AI service providers
- **Configurable Models**: Different model configurations for different use cases
- **System Prompts**: Customizable system prompts via Blade templates
- **Error Handling**: Graceful fallbacks and error reporting

### User Experience

- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode Support**: Automatic theme detection and manual toggle
- **Feedback Collection**: Rate AI responses with thumbs up/down
- **Loading States**: Clear indicators during AI response generation

### Admin Features

- **Feedback Dashboard**: Analytics on user feedback and satisfaction
- **Session Management**: Overview of all chat sessions
- **Performance Monitoring**: Built-in logging and monitoring

## 🏗️ Architecture

### HTTP-Based Communication

This implementation uses traditional HTTP requests for all interactions:

- **POST /api/chat**: Send user messages and receive AI responses
- **GET /api/chat/history**: Retrieve chat session history
- **POST /api/chat/feedback**: Submit feedback for AI responses

### Database Schema

- **Users**: User authentication and profiles
- **Chat Sessions**: Individual chat conversations
- **Chat Messages**: Messages within sessions
- **Chat Feedback**: User feedback on AI responses

### AI Configuration System

The application supports multiple AI configurations defined in `config/ai_configurations.php`:

- Provider selection (Gemini, OpenAI, etc.)
- Model selection (GPT-4, Claude, etc.)
- Custom system prompts
- Per-session configuration persistence

## 📋 Prerequisites

- **PHP 8.2+** with required extensions
- **Composer** for PHP dependencies
- **Node.js 18+** and **npm** for frontend dependencies
- **SQLite** (default) or **MySQL/PostgreSQL** for database
- **AI Provider API Key** (e.g., Google Gemini API key)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd customer-support-laravel
```

### 2. Install PHP Dependencies

```bash
composer install
```

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Environment Configuration

```bash
# Copy the environment file
cp .env.example .env

# Generate application key
php artisan key:generate
```

### 5. Configure Environment Variables

Edit the `.env` file with the following essential configurations:

```env
# Application
APP_NAME="Customer Support Chat"
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000

# Database (SQLite - default, no additional config needed)
DB_CONNECTION=sqlite
DB_DATABASE=database/database.sqlite

# AI Configuration (Required - Get from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Additional AI Providers
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Session Configuration
SESSION_DRIVER=database
SESSION_LIFETIME=120

# Mail Configuration (for user registration)
MAIL_MAILER=log
MAIL_FROM_ADDRESS=noreply@example.com
MAIL_FROM_NAME="${APP_NAME}"
```

### 6. Database Setup

```bash
# Create SQLite database file
touch database/database.sqlite

# Run migrations
php artisan migrate

# Optional: Seed with sample data
php artisan db:seed
```

### 7. Build Frontend Assets

```bash
# Development build
npm run dev

# Or production build
npm run build
```

## 🚀 Running the Application

### Development Mode (Recommended for Evaluation)

This command runs all necessary services concurrently:

```bash
composer run dev
```

This will start:

- Laravel development server (http://localhost:8000)
- Queue worker for background jobs
- Log monitoring (Pail)
- Vite development server for hot reloading

### Manual Setup (Alternative)

If you prefer to run services separately:

```bash
# Terminal 1: Start Laravel server
php artisan serve

# Terminal 2: Start frontend build process
npm run dev

# Terminal 3: (Optional) Start queue worker
php artisan queue:work
```

### 8. Access the Application

- **Frontend**: http://localhost:8000
- **Register/Login**: Create a new account or use existing credentials
- **Chat Interface**: Navigate to chat sessions to start conversations

## 🔧 AI Provider Setup

### Google Gemini (Default)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`

### OpenAI (Optional)

1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

### Other Providers

Check `config/prism.php` for all supported providers and their required environment variables.

## 📱 Usage Guide

### For Evaluators

1. **Registration**: Create a new account at the login page
2. **Dashboard**: View feedback analytics and system overview
3. **Chat Sessions**:
    - Click "New Chat" to start a conversation
    - Select different AI models from the dropdown
    - Send messages and observe response times
    - Provide feedback using thumbs up/down buttons
4. **Session Management**:
    - View all previous chat sessions
    - Click on sessions to continue conversations
    - Edit session titles by clicking the pencil icon

### Testing Different AI Models

The application comes pre-configured with multiple AI setups:

- **Standard (Gemini Flash)**: Fast responses, good for general queries
- **Advanced (Gemini Pro)**: More sophisticated responses
- **Experimental Prompt**: Different system prompt configuration

## 🔍 Key Implementation Details

### Architecture Decisions

- **HTTP over WebSockets**: Chosen for simplicity and reliability over real-time features
- **Inertia.js**: Provides SPA-like experience without API complexity
- **SQLite**: Default database for easy setup and evaluation
- **Prism PHP**: Unified interface for multiple AI providers

### Limitations & Trade-offs

- **No Real-time Updates**: Messages require page refresh or manual reload
- **No Typing Indicators**: Not feasible with HTTP-only architecture
- **No Live Presence**: Cannot show who's currently online
- **Response Delays**: Each message involves a complete HTTP request cycle

### Security Considerations

- **Authentication Required**: All chat endpoints require user authentication
- **Session Ownership**: Users can only access their own chat sessions
- **Input Validation**: All user inputs are validated and sanitized
- **API Key Protection**: AI provider keys are server-side only

## 🧪 Testing

### Run the Test Suite

```bash
# Run all tests
composer run test

# Run with coverage
php artisan test --coverage
```

### Manual Testing Scenarios

1. **User Registration/Login Flow**
2. **Chat Session Creation and Management**
3. **Message Sending and AI Response**
4. **Feedback Submission**
5. **Session History Retrieval**
6. **Different AI Model Configurations**

## 📊 Performance Considerations

### Response Times

- **User Message Processing**: ~100-200ms (database operations)
- **AI Response Generation**: 1-5 seconds (depends on provider/model)
- **History Loading**: ~50-100ms (cached after first load)

### Scalability Notes

- Database queries are optimized with proper indexing
- AI responses could be cached for repeated questions
- Queue system handles background processing
- Session-based authentication reduces database calls

## 🔧 Configuration

### AI Model Configurations

Edit `config/ai_configurations.php` to add new AI setups:

```php
'custom-config' => [
    'name' => 'Custom AI Setup',
    'provider' => 'openai',
    'model' => 'gpt-4',
    'system_prompt_view' => 'prompts.custom-prompt',
],
```

### System Prompts

Create custom system prompts in `resources/views/prompts/`:

```php
// resources/views/prompts/custom-prompt.blade.php
You are a helpful customer support assistant...
```

## 📝 API Documentation

### Main Endpoints

- `POST /api/chat` - Send message and get AI response
- `GET /api/chat/history` - Get chat session history
- `POST /api/chat/feedback` - Submit feedback for AI message
- `POST /chat-sessions` - Create new chat session
- `GET /chat-sessions/{id}` - View specific chat session

### Response Formats

All API responses follow consistent JSON structure with proper HTTP status codes.

## 🐛 Troubleshooting

### Common Issues

**AI Not Responding**

- Check if API key is set correctly in `.env`
- Verify API key has sufficient credits/quota
- Check Laravel logs: `tail -f storage/logs/laravel.log`

**Database Errors**

- Ensure SQLite file exists: `touch database/database.sqlite`
- Run migrations: `php artisan migrate`
- Check file permissions on database directory

**Frontend Not Loading**

- Ensure Node.js dependencies are installed: `npm install`
- Run development server: `npm run dev`
- Check for TypeScript errors in console

### Debug Mode

Enable debug mode in `.env` for detailed error messages:

```env
APP_DEBUG=true
LOG_LEVEL=debug
```

## 📄 License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

## 👥 Contributing

This is an educational project. For evaluation purposes, focus on:

- Testing the chat functionality
- Trying different AI models
- Reviewing the feedback system
- Examining the code architecture
- Understanding the HTTP-based approach vs real-time alternatives

---

**Note for Evaluators**: This application demonstrates a practical approach to AI-powered customer support using familiar web technologies. While it lacks real-time features, it provides a solid foundation that could be extended with WebSockets or Server-Sent Events for live updates if needed.
