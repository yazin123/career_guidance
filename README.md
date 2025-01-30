# Django Project Setup Guide for Windows

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher (64-bit version recommended)
- Git (optional, but recommended for version control)
- Windows 10 or Windows 11

## Step 1: Install Python

1. Download Python from the official website:
   - Visit [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
   - Download the latest Python 3.x version
   - **Important**: Check the box that says "Add Python to PATH" during installation

2. Verify Python installation
   ```
   python --version
   pip --version
   ```

## Step 2: Create a Virtual Environment

1. Open Command Prompt or PowerShell
2. Navigate to your project directory
3. Create a virtual environment
   ```
   python -m venv venv
   ```

4. Activate the virtual environment
   ```
   .\venv\Scripts\activate
   ```

## Step 3: Install Project Dependencies

1. With the virtual environment activated, install project requirements
   ```
   pip install -r requirements.txt
   ```

## Step 4: Database Setup

### Option 1: SQLite (Default)
- No additional setup required. Django uses SQLite by default.

### Option 2: PostgreSQL
1. Install PostgreSQL from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Create a database for the project
3. Update `settings.py` with database configuration

### Option 3: MySQL
1. Install MySQL from [https://dev.mysql.com/downloads/windows/](https://dev.mysql.com/downloads/windows/)
2. Create a database for the project
3. Update `settings.py` with database configuration

## Step 5: Environment Variables

1. Create a `.env` file in the project root
2. Add the following sample configurations:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=your-database-connection-string
   ```

3. Install python-dotenv to load environment variables:
   ```
   pip install python-dotenv
   ```

## Step 6: Database Migrations

1. Run database migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

## Step 7: Create Superuser (Optional)

1. Create an admin account
   ```
   python manage.py createsuperuser
   ```

## Step 8: Run Development Server

1. Start the Django development server
   ```
   python manage.py runserver
   ```

2. Open a web browser and navigate to:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Troubleshooting

### Common Issues
- **ModuleNotFoundError**: Ensure virtual environment is activated
- **Permission Errors**: Run Command Prompt or PowerShell as Administrator
- **Path Issues**: Verify Python and pip are correctly added to PATH

### Dependency Installation Problems
If you encounter issues installing packages:
1. Upgrade pip
   ```
   python -m pip install --upgrade pip
   ```
2. Install individual packages manually
   ```
   pip install django djangorestframework
   ```

## Project Structure
```
project_name/
│
├── venv/                # Virtual environment
├── manage.py            # Django management script
├── project_name/        # Project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                # Django apps
│   ├── app1/
│   └── app2/
│
├── static/              # Static files
├── templates/           # HTML templates
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables
```

## Deactivating Virtual Environment

When you're done working on the project:
```
deactivate
```

## Version Control

1. Create a `.gitignore` file:
   ```
   venv/
   *.pyc
   __pycache__/
   db.sqlite3
   .env
   ```

2. Initialize Git repository
   ```
   git init
   git add .
   git commit -m "Initial project setup"
   ```

## Additional Resources
- Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Python Documentation: [https://docs.python.org/](https://docs.python.org/)

## License
[Add your project license here]

---

**Note**: Always refer to your project's specific documentation for any unique setup requirements.
