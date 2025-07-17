# Django AI Quiz Bot - Complete Implementation

A complete Django-based quiz application powered by Google Generative AI that creates personalized quizzes on any topic.

## Features

- 🤖 **AI-Powered Quiz Generation**: Uses Google's Gemini model to generate unique quizzes
- 🎯 **Customizable Difficulty**: Choose from Easy, Medium, or Hard difficulty levels
- 📊 **Real-time Scoring**: Instant feedback and detailed explanations
- 💾 **Database Storage**: All quizzes and results stored in Django database
- 📱 **Responsive Design**: Beautiful UI built with Tailwind CSS
- 🔧 **Admin Interface**: Django admin for managing quizzes and results

## Quick Start

### 1. Install Dependencies

```bash
cd django_complete
pip install -r requirements.txt
```

### 2. Set Up API Key

Edit the `.env` file and add your Google Generative AI API key:

```
GOOGLE_GENERATIVE_AI_API_KEY=your-actual-api-key-here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run Database Migrations

```bash
python manage.py migrate
```

### 4. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```

Visit http://localhost:8000 to start using the quiz bot!

## Project Structure

```
django_complete/
├── quizbot/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI config
├── quiz/                   # Quiz application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # App URLs
│   ├── admin.py            # Admin configuration
│   └── ai_service.py       # AI integration
├── templates/              # HTML templates
│   └── quiz/
│       ├── base.html       # Base template
│       ├── index.html      # Home page
│       ├── quiz_detail.html # Quiz interface
│       └── results.html    # Results page
├── static/                 # Static files (CSS, JS, images)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## Database Models

### Quiz

- Stores quiz metadata (topic, difficulty, questions count)
- Unique session ID for each quiz

### QuizQuestion

- Individual questions with 4 multiple choice options
- Correct answer index and explanations
- Linked to parent quiz

### QuizSession

- Tracks user progress through quiz
- Current score and question index
- Completion status

### QuizAnswer

- User's answers to questions
- Correctness and score tracking

### QuizStatistics

- Aggregated statistics for each quiz session
- Percentage scores and answer counts

## AI Integration

The app uses Google's Gemini 1.5 Flash model through LangChain for:

- Dynamic quiz generation based on user topics
- Structured output parsing with Pydantic
- Context-aware question difficulty scaling
- Detailed answer explanations

## API Endpoints

- `GET /` - Home page
- `POST /generate/` - Generate new quiz
- `GET /quiz/<session_id>/` - Quiz interface
- `POST /quiz/<session_id>/submit/` - Submit answer
- `GET /quiz/<session_id>/results/` - View results
- `GET /quiz/<session_id>/restart/` - Restart quiz
- `GET /api/quiz/<session_id>/status/` - Quiz status (JSON)

## Admin Interface

Access the Django admin at http://localhost:8000/admin/ to:

- View all generated quizzes
- Monitor user answers and statistics
- Manage quiz content
- Export quiz data

## Usage Examples

### Generate a Programming Quiz

1. Visit the home page
2. Enter "Python Programming" as topic
3. Select "Medium" difficulty
4. Choose 10 questions
5. Click "Generate Quiz"

### View Quiz Results

After completing a quiz, you'll see:

- Overall percentage score
- Correct/incorrect answer breakdown
- Detailed explanations for each question
- Option to restart or create new quiz

## Environment Variables

- `DEBUG`: Django debug mode (True/False)
- `SECRET_KEY`: Django secret key
- `GOOGLE_GENERATIVE_AI_API_KEY`: Your Google AI API key

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Google Generative AI API key is correctly set in `.env`
2. **Database Error**: Run `python manage.py migrate` to set up database
3. **Static Files Warning**: The static directory exists but may be empty (normal for development)
4. **Template Error**: Ensure templates are in `templates/quiz/` directory

### Error Handling

The app includes robust error handling:

- Graceful fallback if AI generation fails
- Form validation for user inputs
- Database transaction safety
- User-friendly error messages

## Development

### Running Tests

```bash
python manage.py test quiz
```

### Making Model Changes

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

## Technology Stack

- **Backend**: Django 4.2.7
- **AI**: Google Generative AI (Gemini 1.5 Flash)
- **AI Framework**: LangChain
- **Database**: SQLite (default), PostgreSQL/MySQL supported
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Validation**: Pydantic models

## Comparison with FastAPI Version

This Django implementation offers:

- ✅ **Unified Architecture**: Single Django app vs FastAPI + Django frontend
- ✅ **Database Integration**: Native Django ORM vs separate API calls
- ✅ **Admin Interface**: Built-in Django admin vs no admin interface
- ✅ **Session Management**: Django sessions vs manual session handling
- ✅ **Simplified Deployment**: One server vs two servers
- ✅ **Better Error Handling**: Django's robust error system

## License

MIT License - Feel free to use and modify for your projects!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
