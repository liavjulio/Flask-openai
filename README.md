# Flask OpenAI PostgreSQL Project

## Overv# 🤖 GPT Clone - Flask OpenAI Chat Application

## 🌟 Overview

A fully-featured **GPT Clone** web application built with Flask that provides a ChatGPT-like interface for conversing with AI. This modern chat application features conversation management, real-time messaging, and a responsive design that works seamlessly across desktop and mobile devices.

## ✨ Features

### 🎯 Core Features
- **Modern Chat Interface**: Clean, dark-themed UI similar to ChatGPT
- **Multiple Conversations**: Create, manage, and switch between different chat sessions
- **Context-Aware AI**: Each conversation maintains full chat history for contextual responses
- **Real-time Typing Indicators**: Visual feedback during AI response generation
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

### 🔧 Technical Features
- **Flask Web Server**: RESTful API with modern endpoints
- **OpenAI Integration**: Uses GPT-3.5-turbo for intelligent responses
- **SQLite Database**: Stores conversations and messages with relationships
- **Database Migrations**: Alembic for schema management
- **Mock Mode**: Fallback mode for API quota/billing issues
- **Docker Support**: Containerized deployment ready
- **CORS Enabled**: Cross-origin resource sharing support

### 🎨 UI/UX Features
- **Sidebar Navigation**: Easy conversation switching and management
- **Example Prompts**: Quick-start suggestions for new users
- **Code Block Support**: Properly formatted code in responses
- **Message History**: Persistent conversation storage
- **Mobile-Optimized**: Touch-friendly interface for mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)
- OpenAI API Key

### 🛠️ Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/liavjulio/Flask-openai.git
   cd Flask-openai
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file with:
   ```env
   # OpenAI API Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Database Configuration
   DATABASE_URL=sqlite:///gpt_clone.db
   
   # Flask Configuration
   FLASK_HOST=127.0.0.1
   FLASK_PORT=5001
   FLASK_DEBUG=True
   
   # Mock Mode (set to 'true' if you have quota issues)
   MOCK_MODE=false
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

6. **Open your browser:**
   Visit `http://127.0.0.1:5001` to start chatting!

## 🐳 Docker Setup

### Using Docker Compose

1. **Build and run:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Visit `http://localhost:8080`

### Manual Docker Build

```bash
docker build -t gpt-clone .
docker run -p 5001:5001 --env-file .env gpt-clone
```

## 📡 API Endpoints

### Conversations
- `GET /api/conversations` - List all conversations
- `POST /api/conversations` - Create new conversation
- `DELETE /api/conversations/{id}` - Delete conversation

### Messages
- `GET /api/conversations/{id}/messages` - Get conversation messages
- `POST /api/conversations/{id}/chat` - Send message and get AI response

### Legacy
- `POST /ask` - Legacy single Q&A endpoint (backward compatibility)

## 🎮 Usage Examples

### Web Interface
1. **Start New Chat**: Click "New Chat" button
2. **Ask Questions**: Type your message and press Enter
3. **View History**: Previous conversations appear in the sidebar
4. **Delete Chats**: Use the trash icon to remove conversations

### API Usage
```bash
# Create a new conversation
curl -X POST http://localhost:5001/api/conversations

# Send a message
curl -X POST http://localhost:5001/api/conversations/1/chat 
  -H "Content-Type: application/json" 
  -d '{"message": "Hello, how are you?"}'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///gpt_clone.db` |
| `FLASK_HOST` | Server host | `127.0.0.1` |
| `FLASK_PORT` | Server port | `5001` |
| `FLASK_DEBUG` | Debug mode | `True` |
| `MOCK_MODE` | Use mock responses | `false` |

### Mock Mode
If you encounter OpenAI quota issues, set `MOCK_MODE=true` to use simulated responses for testing.

## 🧪 Testing

Run the test suite:
```bash
# Unit tests
pytest

# Test specific file
pytest tests/test_app.py

# With coverage
pytest --cov=app tests/
```

## 📁 Project Structure

```
Flask-openai/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # API endpoints
│   ├── models.py            # Database models
│   ├── config.py            # Configuration
│   ├── templates/
│   │   └── index.html       # Main chat interface
│   └── static/
│       ├── style.css        # Styling
│       └── script.js        # Frontend logic
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker services
├── Dockerfile              # Container definition
└── README.md               # This file
```

## 🔄 Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🎯 Example Prompts

Try these example prompts to get started:
- "Explain quantum computing in simple terms"
- "Write a creative story about time travel"
- "Help me plan a healthy meal for today"
- "Debug this Python code"

## 🚨 Troubleshooting

### Common Issues

1. **OpenAI API Quota Exceeded**
   - Set `MOCK_MODE=true` in `.env`
   - Add billing to your OpenAI account
   - Use a different API key

2. **Port Already in Use**
   - Change `FLASK_PORT` in `.env`
   - Kill existing processes: `lsof -ti:5001 | xargs kill`

3. **Database Issues**
   - Delete `gpt_clone.db` to reset
   - Run `alembic upgrade head`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new features
5. Run tests: `pytest`
6. Commit changes: `git commit -am 'Add feature'`
7. Push to branch: `git push origin feature-name`
8. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Flask community for the excellent web framework
- Contributors and testers

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/liavjulio/Flask-openai/issues)
3. Create a new issue with detailed information

---

**Built with ❤️ using Flask and OpenAI**ew

This project is a simple Flask server application that integrates with the OpenAI API to answer questions. The application also stores questions and answers in a PostgreSQL database. Both the server and the database are dockerized and managed with Docker Compose.

## Features

- Flask server with an endpoint to ask questions
- Integration with the OpenAI API for generating answers
- PostgreSQL database for storing questions and answers
- Dockerized application with Docker Compose
- Database migrations using Alembic
- Basic testing with pytest

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
   git clone https://github.com/yourusername/flask-openai-postgres.git
   cd flask-openai-postgres
   
2. Create a .env.api-key file in the root of the project directory and update it with your OpenAI API key and PostgreSQL database credentials. Use the provided template below:
   #### OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here

3. Build and run the containers:
   #### docker-compose up --build
4. Apply Database Migrations:
   #### docker-compose run web alembic upgrade head

### Test
To run the tests, use the following command:
#### docker-compose run web pytest

### Run
To run the app , use the following command:
#### curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" -d '{"question": "Enter your question here?"}

