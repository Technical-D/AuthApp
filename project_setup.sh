#!/bin/bash

# Prompt user for project name
read -p "Enter project name (default: project): " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-project}

# Create project directory
mkdir -p "$PROJECT_NAME"/{app/{controllers,middleware,models,routes,schemas,services,utils},db,resource,venv}

# Create necessary Python files
touch "$PROJECT_NAME/app/__init__.py"
touch "$PROJECT_NAME/app/extensions.py"
touch "$PROJECT_NAME/app/constants.py"
touch "$PROJECT_NAME/app/error_handlers.py"
touch "$PROJECT_NAME/app/models/__init__.py"
touch "$PROJECT_NAME/app/routes/__init__.py"
touch "$PROJECT_NAME/requirements.txt"
touch "$PROJECT_NAME/README.md"
touch "$PROJECT_NAME/.gitignore"
touch "$PROJECT_NAME/config.py"
touch "$PROJECT_NAME/run.py"

# Add a basic .gitignore file
cat <<EOL > "$PROJECT_NAME/.gitignore"
venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
.env
EOL

# Adding Docker configuration 
cat <<EOL > "$PROJECT_NAME/Dockerfile"
# Python image
FROM python:3.9-slim

WORKDIR /app # Setting working dir

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Environment variables 
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Running on gunicorn server
CMD ["gunicorn", "-w", "4", "run:app", "--bind", "0.0.0.0:5000"]

EOL

# Initialize virtual environment
python -m venv "$PROJECT_NAME/venv"

cat <<EOL > "$PROJECT_NAME/requirements.txt"
flask
flask-sqlalchemy
Flask-Migrate
gunicorn
PyMySQL
python-dotenv
EOL

echo "Virtual environment created in $PROJECT_NAME/venv"
echo "Project structure created successfully!"
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. source venv/bin/activate  (Linux/macOS) OR venv\Scripts\activate  (Windows)"
echo "3. Install dependencies: pip install -r requirements.txt
