# A Place For Me

A faith-based web application for sharing stories, inspiration, and building community.

## Quick Start

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode (connects to dev database)
python server.py

# Or use the development helper
python dev.py run-dev
```

### Production Mode
```bash
# Run in production mode (connects to production database)
python run.py
```

## Development Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Admin User
```bash
# Method 1: Using Flask CLI
flask create-admin

# Method 2: Using development helper
python dev.py create-admin

# Method 3: Manual via Flask shell
flask shell
>>> from src.models.main import User
>>> admin = User(username='admin', email='admin@example.com', role='admin')
>>> admin.set_password('your-password')
>>> db.session.add(admin)
>>> db.session.commit()
```

### 3. Database Operations
```bash
# Reset development database
python dev.py reset-db

# Initialize database manually
flask init-db
```

### 4. Development Tools
```bash
# Show all routes
python dev.py routes

# Run development server
python dev.py run-dev
```

## Project Structure

```
aplaceforme/
├── server.py              # Main server file (development mode)
├── run.py                 # Production runner
├── dev.py                 # Development helper
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py       # Flask app factory
│   ├── models/
│   │   └── main.py       # Database models
│   ├── controllers/
│   │   ├── main.py       # Main routes
│   │   ├── auth.py       # Authentication
│   │   └── admin.py      # Admin panel
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, images
├── docs/                 # Project documentation
└── uploads/              # File uploads (auto-created)
```

## Environment Modes

### Development Mode
- **Trigger**: Run `python server.py` directly
- **Database**: `aplaceforme_dev.db`
- **Debug**: Enabled
- **Features**: Hot reload, detailed error pages

### Production Mode
- **Trigger**: Run `python run.py`
- **Database**: `aplaceforme.db`
- **Debug**: Disabled
- **Features**: Optimized for deployment

## Key Features

### User Management
- Role-based access control (Admin, User, Author)
- User registration and authentication
- Admin-managed author accounts

### Content Management
- Blog posts with draft/publish workflow
- God stories with multimedia support
- Song uploads and streaming
- Testimonials with approval system
- Radio sessions/podcasts

### Community Features
- Newsletter subscription
- Email campaigns
- Community engagement

## API Endpoints

### Public Routes
- `/` - Landing page
- `/blog` - Blog posts
- `/stories` - God stories
- `/songs` - Songs
- `/testimonials` - Testimonials
- `/radio` - Radio sessions

### Authentication
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/logout` - User logout
- `/auth/profile` - User profile

### Admin Panel
- `/admin/dashboard` - Admin overview
- `/admin/users` - User management
- `/admin/blog` - Blog management
- `/admin/stories` - Stories management
- `/admin/newsletters` - Newsletter management

## Configuration

### Environment Variables
```bash
# Optional - defaults provided
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///aplaceforme.db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Configuration
The application uses SQLite by default:
- Development: `aplaceforme_dev.db`
- Production: `aplaceforme.db`

## Development Workflow

1. **Start Development Server**
   ```bash
   python server.py
   ```

2. **Create Admin User**
   ```bash
   python dev.py create-admin
   ```

3. **Access Application**
   - Main site: http://localhost:5000
   - Admin panel: http://localhost:5000/admin/dashboard

4. **Development Commands**
   ```bash
   python dev.py routes      # Show all routes
   python dev.py reset-db    # Reset database
   python dev.py create-admin # Create admin user
   ```

## Production Deployment

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   ```

3. **Run Production Server**
   ```bash
   python run.py
   ```

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Flask-Bcrypt, Flask-Login
- **Email**: Flask-Mail

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
