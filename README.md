# QuizBot - AI-Powered Quiz Generator

An intelligent quiz bot that generates comprehensive quizzes on any topic using LangChain and Google's Generative AI. The system provides structured output with multiple-choice questions, real-time scoring, and a beautiful web interface.

## Features

- 🧠 **AI-Powered Quiz Generation**: Uses Google's Generative AI to create comprehensive quizzes
- 📝 **Structured Output**: LangChain ensures consistent, well-formatted quiz questions
- 🎯 **Multiple Difficulty Levels**: Easy, Medium, and Hard questions
- 📊 **Real-time Scoring**: Dynamic score tracking with immediate feedback
- 🌐 **Modern Web Interface**: Beautiful, responsive frontend with Tailwind CSS
- 🔄 **Session Management**: Persistent quiz sessions with progress tracking
- 📈 **Performance Analytics**: Detailed results and accuracy metrics

## Technology Stack

### Backend

- **FastAPI**: High-performance web framework for APIs
- **LangChain**: Framework for structured AI output
- **Google Generative AI**: Advanced language model for quiz generation
- **Pydantic**: Data validation and serialization
- **Python 3.8+**: Core backend language

### Frontend

- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive frontend functionality
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library

## Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Generative AI
- Modern web browser

### Setup

#### Option 1: Quick Setup (Recommended)

**Windows:**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Run setup script
setup.bat
```

**Linux/Mac:**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Run setup script
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/basic_query_quizbot.git
   cd basic_query_quizbot
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate

   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

5. **Get Google API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

### Starting the Backend Server

```bash
python run_server.py
```

The API will be available at `http://localhost:8000`

### Accessing the Frontend

Open `frontend/index.html` in your web browser or serve it using a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Then visit `http://localhost:3000`

### API Documentation

Interactive API documentation is available at `http://localhost:8000/docs`

## API Endpoints

### Quiz Generation

- `POST /quiz/generate` - Generate a new quiz
- `GET /quiz/topics` - Get suggested topics

### Quiz Interaction

- `POST /quiz/answer` - Submit an answer
- `GET /quiz/score/{session_id}` - Get current score
- `GET /quiz/session/{session_id}` - Get session details

### Utilities

- `GET /health` - Health check
- `POST /quiz/reset/{session_id}` - Reset quiz session
- `GET /quiz/leaderboard` - Get leaderboard

## Testing

Run the API tests:

```bash
python test_api.py
```

## Project Structure

```
basic_query_quizbot/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── quiz_generator.py    # LangChain integration
│   └── score_manager.py     # Score tracking
├── frontend/
│   ├── index.html           # Main HTML file
│   └── js/
│       └── app.js           # Frontend JavaScript
├── requirements.txt         # Python dependencies
├── run_server.py           # Server startup script
├── test_api.py             # API testing script
├── .env.example            # Environment variables template
└── README.md               # This file
```

## How It Works

1. **Quiz Generation**: User enters a topic, and the system uses LangChain with Google's Generative AI to create structured quiz questions
2. **Session Management**: Each quiz creates a unique session to track progress and scores
3. **Answer Processing**: User selections are validated and scored in real-time
4. **Feedback System**: Immediate feedback with explanations for correct answers
5. **Results Display**: Comprehensive results with accuracy metrics and performance breakdown

## Scoring System

- **Easy Questions**: +1 point for correct, -1 for incorrect
- **Medium Questions**: +2 points for correct, -2 for incorrect
- **Hard Questions**: +3 points for correct, -3 for incorrect

## Configuration

### Environment Variables

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Quiz Settings

You can customize quiz parameters:

- Number of questions (1-20)
- Difficulty level (easy, medium, hard)
- Topic complexity (basic concepts to advanced topics)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Google API Key not working**

   - Ensure your API key is correct in the `.env` file
   - Check that the Generative AI API is enabled in Google Cloud Console

2. **CORS errors**

   - Make sure you're serving the frontend from a web server, not opening the HTML file directly

3. **Quiz generation fails**
   - Check your internet connection
   - Verify the API key has sufficient quota
   - Try with a simpler topic

### Support

For issues and questions, please open an issue on GitHub or contact the maintainers.

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Quiz history and analytics
- [ ] Custom quiz creation
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Advanced question types (true/false, fill-in-the-blank)
- [ ] Timed quizzes
- [ ] Multiplayer quiz competitions

---

Built with ❤️ using AI and modern web technologies.
