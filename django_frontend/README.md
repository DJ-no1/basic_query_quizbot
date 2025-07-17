# Django Quiz Bot Frontend

This is a Django-based frontend for the Quiz Bot application that consumes the FastAPI backend via HTTP requests.

## Features

- **Modern Django Web Interface**: Clean, responsive design using Tailwind CSS
- **FastAPI Integration**: Communicates with the existing FastAPI backend
- **Session Management**: Uses Django sessions to manage quiz state
- **Real-time Scoring**: Live score updates during quiz taking
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Graceful error handling and user feedback

## Project Structure

```
django_frontend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── run_django.py            # Python server runner
├── start_django.bat         # Windows batch file to start server
├── quizbot_web/             # Django project settings
│   ├── settings.py          # Main Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── quiz/                    # Main Django app
│   ├── views.py             # View functions and API client
│   ├── urls.py              # App URL patterns
│   ├── models.py            # Django models (if needed)
│   └── templates/quiz/      # HTML templates
│       ├── base.html        # Base template
│       ├── index.html       # Home page with topic selection
│       └── quiz.html        # Quiz interface
└── static/                  # Static files (CSS, JS, images)
```

## Installation & Setup

### Prerequisites

1. **FastAPI Backend**: Make sure your FastAPI backend is running on `http://localhost:8000`
2. **Python Environment**: Use the same virtual environment as your backend

### Quick Start

1. **Navigate to Django frontend directory**:

   ```bash
   cd django_frontend
   ```

2. **Install Django dependencies** (if not already installed):

   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Start the Django development server**:

   ```bash
   python manage.py runserver 8001
   ```

   Or use the provided scripts:

   - **Windows**: Double-click `start_django.bat`
   - **Python**: `python run_django.py`

5. **Access the application**:
   - Django Frontend: http://localhost:8001
   - FastAPI Backend: http://localhost:8000 (must be running)

## Configuration

### Django Settings

Key settings in `quizbot_web/settings.py`:

```python
# API Configuration
BACKEND_API_URL = "http://localhost:8000"

# Static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "quiz",  # Our main app
]
```

### Backend API Integration

The Django frontend communicates with the FastAPI backend through the `APIClient` class in `quiz/views.py`:

```python
class APIClient:
    def __init__(self):
        self.base_url = settings.BACKEND_API_URL

    def generate_quiz(self, topic, num_questions=10, difficulty="medium"):
        # Makes HTTP requests to FastAPI backend

    def submit_answer(self, session_id, question_index, selected_option):
        # Submits answers to FastAPI backend

    # ... other methods
```

## API Endpoints

The Django frontend provides these internal API endpoints:

- `GET /` - Home page with topic selection
- `GET /quiz/` - Quiz interface page
- `POST /api/generate/` - Generate new quiz (proxies to FastAPI)
- `POST /api/answer/` - Submit quiz answer (proxies to FastAPI)
- `GET /api/score/` - Get current score (proxies to FastAPI)
- `GET /api/topics/` - Get suggested topics (proxies to FastAPI)
- `POST /api/reset/` - Reset quiz session (proxies to FastAPI)

## Features

### Home Page (`/`)

- Topic selection with suggested topics
- Quiz configuration (number of questions, difficulty)
- Responsive form with real-time validation

### Quiz Interface (`/quiz/`)

- Question display with multiple choice options
- Real-time score tracking
- Navigation between questions
- Progress indicator
- Results summary with statistics

### Session Management

- Django sessions store quiz state
- Seamless integration with FastAPI backend sessions
- Automatic cleanup of expired sessions

## Templates

### Base Template (`base.html`)

- Common layout and styling
- Navigation header with score display
- Footer with branding
- Responsive design with Tailwind CSS

### Index Template (`index.html`)

- Topic selection form
- Suggested topics grid
- Loading and error modals
- Form validation and submission

### Quiz Template (`quiz.html`)

- Question display interface
- Answer option buttons
- Navigation controls
- Results summary screen
- Real-time score updates

## Styling

The frontend uses:

- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icons and visual elements
- **Custom CSS**: Additional animations and effects
- **Responsive Design**: Mobile-first approach

## Error Handling

The frontend includes comprehensive error handling:

- API connection errors
- Invalid quiz data
- Session timeouts
- Network failures
- User-friendly error messages

## Development

### Running in Development Mode

```bash
# Start FastAPI backend (in another terminal)
cd backend
python run_server.py

# Start Django frontend
cd django_frontend
python manage.py runserver 8001
```

### Adding New Features

1. **New Views**: Add to `quiz/views.py`
2. **New Templates**: Create in `quiz/templates/quiz/`
3. **New URLs**: Update `quiz/urls.py`
4. **Static Files**: Add to `static/` directory

### Database

Django uses SQLite by default for sessions and user management. No custom models are required for basic quiz functionality as all quiz data is managed by the FastAPI backend.

## Deployment

For production deployment:

1. **Configure Settings**:

   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use production database
   - Set secure `SECRET_KEY`

2. **Static Files**:

   ```bash
   python manage.py collectstatic
   ```

3. **Web Server**: Use Gunicorn, uWSGI, or similar WSGI server

4. **Environment Variables**:
   - `BACKEND_API_URL`: FastAPI backend URL
   - `SECRET_KEY`: Django secret key
   - Database configuration

## Troubleshooting

### Common Issues

1. **"Connection refused" errors**:

   - Ensure FastAPI backend is running on port 8000
   - Check `BACKEND_API_URL` setting

2. **Static files not loading**:

   - Run `python manage.py collectstatic`
   - Check `STATICFILES_DIRS` setting

3. **Session issues**:

   - Clear browser cookies
   - Restart Django server

4. **Template not found**:
   - Ensure templates are in correct directory structure
   - Check `INSTALLED_APPS` includes 'quiz'

### Logs

Django logs are available in the terminal where you run the server. For production, configure proper logging in `settings.py`.

## Comparison with Original Frontend

| Feature          | Original HTML/JS     | Django Frontend    |
| ---------------- | -------------------- | ------------------ |
| Framework        | Vanilla JS           | Django Templates   |
| Styling          | Tailwind CSS         | Tailwind CSS       |
| State Management | JavaScript variables | Django sessions    |
| API Calls        | Fetch API            | Python requests    |
| Routing          | Single page          | Django URL routing |
| Template Engine  | None                 | Django templates   |
| Server           | Static files         | Django dev server  |

The Django frontend provides the same functionality as the original but with better server-side state management, more robust error handling, and easier maintenance.

## Next Steps

Potential enhancements:

- User authentication and profiles
- Quiz history and analytics
- Admin interface for quiz management
- Advanced scoring algorithms
- Social features (sharing, leaderboards)
- Progressive Web App (PWA) features
