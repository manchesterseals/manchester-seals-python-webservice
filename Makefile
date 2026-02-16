.PHONY: help install run run-extended test docker-build docker-up docker-down docker-logs clean setup check-ports

help:
	@echo "Manchester Seals Python Webservice - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              - Complete setup (venv + install + config)"
	@echo "  make install            - Install dependencies"
	@echo "  make venv               - Create virtual environment"
	@echo ""
	@echo "Running the Application:"
	@echo "  make run                - Run basic version (app.py)"
	@echo "  make run-extended       - Run extended version (app_extended.py)"
	@echo ""
	@echo "Testing:"
	@echo "  make test               - Run unit tests"
	@echo "  make lint               - Run pylint"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build       - Build Docker image"
	@echo "  make docker-up          - Start Docker Compose stack (port 5100)"
	@echo "  make docker-down        - Stop Docker Compose stack"
	@echo "  make docker-logs        - View Docker logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean              - Clean cache and temp files"
	@echo "  make check-ports        - Check if ports are available"
	@echo "  make health             - Check API health"
	@echo "  make sample-data        - Insert sample data into MongoDB"

# Setup
setup: venv install config
	@echo "✅ Setup complete! Run 'make run' to start the application."

venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "✅ Virtual environment created"

install: venv
	@echo "Installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Dependencies installed"

config:
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		cp .env.example .env; \
		echo "✅ .env file created (update with your MongoDB URI)"; \
	else \
		echo "ℹ️  .env file already exists"; \
	fi

# Running
run:
	@echo "Starting Manchester Seals API (Basic Version)..."
	. venv/bin/activate && python app.py

run-extended:
	@echo "Starting Manchester Seals API (Extended Version)..."
	. venv/bin/activate && python app_extended.py

# Testing
test:
	@echo "Running unit tests..."
	. venv/bin/activate && python -m pytest test_app.py -v

lint:
	@echo "Running pylint..."
	. venv/bin/activate && pylint app.py app_extended.py config.py

# Docker
docker-build:
	@echo "Building Docker image..."
	docker build -t manchester-seals-api:latest .
	@echo "✅ Docker image built"

docker-up:
	@echo "Starting Docker Compose stack..."
	docker-compose up -d
	@echo "✅ Docker Compose stack started"
	@echo "API: http://localhost:5000"
	@echo "MongoDB: mongodb://localhost:27017"

docker-down:
	@echo "Stopping Docker Compose stack..."
	docker-compose down
	@echo "✅ Docker Compose stack stopped"

docker-logs:
	@echo "Viewing Docker logs..."
	docker-compose logs -f api

# Utilities
clean:
	@echo "Cleaning cache and temp files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

health:
	@echo "Checking API health..."
	curl -s http://localhost:5000/api/health | python -m json.tool

roster:
	@echo "Fetching roster data..."
	curl -s http://localhost:5000/api/roster | python -m json.tool

sample-data:
	@echo "Inserting sample data..."
	. venv/bin/activate && python -c "\
		from pymongo import MongoClient; \
		import os; \
		from dotenv import load_dotenv; \
		load_dotenv(); \
		client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/')); \
		db = client[os.getenv('DB_NAME', 'manchester_seals')]; \
		roster = db['roster']; \
		data = [ \
			{'name': 'John Doe', 'position': 'Manager', 'department': 'Operations', 'email': 'john.doe@example.com'}, \
			{'name': 'Jane Smith', 'position': 'Developer', 'department': 'Engineering', 'email': 'jane.smith@example.com'}, \
			{'name': 'Bob Johnson', 'position': 'Analyst', 'department': 'Analytics', 'email': 'bob.johnson@example.com'} \
		]; \
		result = roster.insert_many(data); \
		print(f'✅ Inserted {len(result.inserted_ids)} records')"

# Development
requirements:
	@echo "Updating requirements.txt..."
	. venv/bin/activate && pip freeze > requirements.txt
	@echo "✅ Requirements updated"

freeze:
	@echo "Current installed packages:"
	. venv/bin/activate && pip freeze

reqs-install:
	@echo "Reinstalling all requirements..."
	. venv/bin/activate && pip install --upgrade -r requirements.txt
	@echo "✅ Requirements reinstalled"

# Info
info:
	@echo "Project Information:"
	@echo "  Service: Manchester Seals API"
	@echo "  Framework: Flask"
	@echo "  Database: MongoDB"
	@echo "  Python: 3.7+"
	@echo ""
	@echo "Documentation:"
	@echo "  README.md         - Full documentation"
	@echo "  QUICKSTART.md     - Quick reference"
	@echo "  SETUP.md          - Setup guide"
	@echo "  TESTING.md        - Testing examples"
	@echo "  PROJECT_SUMMARY.md - Project overview"
	@echo ""
	@echo "Run 'make help' for all available commands"

check-ports:
	@echo "Checking port availability..."
	@bash check_ports.sh

.DEFAULT_GOAL := help

