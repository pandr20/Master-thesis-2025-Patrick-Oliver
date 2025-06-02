# Customer Support Phoenix

A modern AI-powered customer support chat application built with Phoenix LiveView and Elixir. This system demonstrates real-time communication, AI integration, user feedback collection, and analytics in a customer support context.

## 🎯 Project Overview

This application serves as a research project demonstrating the integration of AI technology in customer support systems. It features real-time chat capabilities, AI-powered responses using Google's Gemini API, user feedback mechanisms, and comprehensive analytics dashboard.

### Key Features

- **Real-time Chat Interface**: Phoenix LiveView enables instant message updates without page refreshes
- **AI-Powered Responses**: Integration with Google Gemini API for intelligent customer support
- **Feedback System**: Users can rate AI responses as positive or negative
- **Analytics Dashboard**: Real-time statistics and feedback analysis
- **Session Management**: Persistent chat sessions with automatic title generation
- **Modern UI**: Responsive design with Tailwind CSS and DaisyUI components
- **Theme Support**: Light and dark mode switching

## 🛠 Technology Stack

- **Backend**: Elixir 1.15+ with Phoenix Framework 1.8
- **Frontend**: Phoenix LiveView, Tailwind CSS, DaisyUI
- **Database**: MySQL with Ecto ORM
- **AI Integration**: Google Gemini API
- **Real-time**: Phoenix PubSub and LiveView
- **HTTP Client**: Req library for API calls

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Elixir** 1.15 or later
- **Erlang/OTP** 24 or later
- **Node.js** 18+ (for asset compilation)
- **MySQL** 8.0 or later
- **Git**

### Installation Links

- [Elixir Installation Guide](https://elixir-lang.org/install.html)
- [MySQL Installation](https://dev.mysql.com/downloads/mysql/)
- [Node.js Download](https://nodejs.org/)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd customer_support_phoenix
```

### 2. Install Dependencies

```bash
mix deps.get
```

### 3. Database Setup

#### Create MySQL Database

```bash
# Connect to MySQL as root
mysql -u root -p

# Create database
CREATE DATABASE customer_support_phoenix_dev;
CREATE DATABASE customer_support_phoenix_test;

# Create user (optional, or use existing MySQL user)
CREATE USER 'phoenix_user'@'localhost' IDENTIFIED BY 'phoenix_password';
GRANT ALL PRIVILEGES ON customer_support_phoenix_dev.* TO 'phoenix_user'@'localhost';
GRANT ALL PRIVILEGES ON customer_support_phoenix_test.* TO 'phoenix_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Configure Database Connection

Update `config/dev.exs` if needed:

```elixir
config :customer_support_phoenix, CustomerSupportPhoenix.Repo,
  username: "root",  # or your MySQL username
  password: "",      # your MySQL password
  hostname: "localhost",
  database: "customer_support_phoenix_dev"
```

#### Run Migrations

```bash
mix ecto.setup
```

### 4. AI Configuration (Optional)

To enable AI responses, you need a Google Gemini API key:

1. Get an API key from [Google AI Studio](https://aistudio.google.com/)
2. Set the environment variable:

```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# Windows
set GEMINI_API_KEY=your-api-key-here
```

Or add it to your `config/dev.exs`:

```elixir
config :customer_support_phoenix, :gemini_api_key, "your-api-key-here"
```

**Note**: The application will work without an API key, showing placeholder responses.

### 5. Install and Build Assets

```bash
mix assets.setup
mix assets.build
```

### 6. Start the Application

```bash
mix phx.server
```

Or start with interactive shell:

```bash
iex -S mix phx.server
```

The application will be available at: [http://localhost:4000](http://localhost:4000)

## 📱 Usage Guide

### For Examinators

1. **Homepage**: Visit [http://localhost:4000](http://localhost:4000) to see the main landing page

2. **Dashboard**: Navigate to [http://localhost:4000/dashboard](http://localhost:4000/dashboard) to view:

   - Total chat sessions
   - Feedback statistics
   - Positive/negative rating ratios
   - Recent feedback entries

3. **Chat Interface**: Go to [http://localhost:4000/chat](http://localhost:4000/chat) to:

   - View existing chat sessions
   - Create new chat sessions
   - Test the real-time chat functionality

4. **Chat Session**: Click on any chat to:
   - Send messages and receive AI responses
   - Rate AI responses (positive/negative)
   - Edit chat session titles
   - Observe real-time updates

### Testing the AI Integration

1. Start a new chat session
2. Send a message (e.g., "I need help with my account")
3. Observe the AI response (or placeholder if no API key)
4. Rate the response using thumbs up/down buttons
5. Check the dashboard for updated statistics

## 🏗 Project Structure

```
lib/
├── customer_support_phoenix/           # Business logic
│   ├── chat/                          # Chat domain
│   │   ├── chat_session.ex           # Session schema
│   │   ├── chat_message.ex           # Message schema
│   │   └── chat_message_feedback.ex  # Feedback schema
│   ├── chat.ex                       # Chat context
│   ├── ai_client.ex                  # AI API integration
│   └── repo.ex                       # Database repository
├── customer_support_phoenix_web/      # Web interface
│   ├── live/                         # LiveView modules
│   │   ├── dashboard_live.ex         # Analytics dashboard
│   │   └── chat_live_live/           # Chat interface
│   ├── components/                   # Reusable components
│   └── router.ex                     # URL routing
priv/
├── repo/migrations/                  # Database migrations
└── static/                          # Static assets
```

## 🧪 Running Tests

```bash
# Run all tests
mix test

# Run tests with coverage
mix test --cover

# Run specific test files
mix test test/customer_support_phoenix_web/live/dashboard_live_test.exs
```

## 🔧 Development Commands

```bash
# Reset database
mix ecto.reset

# Generate new migration
mix ecto.gen.migration add_new_field

# Check code formatting
mix format --check-formatted

# Interactive console with app loaded
iex -S mix

# Live reload for development
mix phx.server
```

## 📊 Research Applications

This project can be used to study:

- **AI Integration Patterns**: How AI is integrated into real-time web applications
- **User Feedback Systems**: Mechanisms for collecting and analyzing user feedback
- **Real-time Communication**: Phoenix LiveView implementation for chat systems
- **Customer Support Analytics**: Data collection and visualization for support metrics
- **User Experience**: Modern web interfaces for customer support

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Ensure MySQL is running
   - Check database credentials in `config/dev.exs`
   - Verify database exists

2. **Asset Compilation Issues**

   - Run `mix assets.setup` again
   - Check Node.js version (18+ required)

3. **AI Responses Not Working**

   - Verify `GEMINI_API_KEY` environment variable
   - Check API key validity
   - Review logs for API errors

4. **Port Already in Use**
   - Change port in `config/dev.exs`: `http: [ip: {127, 0, 0, 1}, port: 4001]`

### Logs and Debugging

- Application logs appear in the terminal
- Database queries are logged in development
- AI API calls are logged with request/response details

## 📝 Configuration

Key configuration files:

- `config/dev.exs` - Development settings
- `config/prod.exs` - Production settings
- `mix.exs` - Dependencies and project settings

## 🤝 For Academic Review

This project demonstrates:

- Modern Elixir/Phoenix development practices
- Real-time web application architecture
- AI service integration patterns
- User feedback collection and analysis
- Responsive web design principles

The codebase is structured for clarity and maintainability, with clear separation between business logic, web interface, and data persistence layers.

## 📚 Learn More

- [Phoenix Framework](https://www.phoenixframework.org/)
- [Phoenix LiveView](https://hexdocs.pm/phoenix_live_view)
- [Elixir](https://elixir-lang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Google Gemini API](https://ai.google.dev/)
