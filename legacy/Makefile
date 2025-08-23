.PHONY: install build clean serve dev help setup venv-create

# Virtual environment variables
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Default target
all: setup build

# Create virtual environment
venv-create:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "Virtual environment created!"

# Setup: create venv and install dependencies
setup: venv-create
	@echo "Installing Python dependencies in virtual environment..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Setup complete!"

# Install dependencies (alias for setup)
install: setup

# Generate HTML files using improved script
build:
	@echo "Generating HTML files..."
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	$(PYTHON) script_improved.py
	@echo "Build complete!"

# Generate HTML files using original script (fallback)
build-old:
	@echo "Generating HTML files with original script..."
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	$(PYTHON) script.py
	@echo "Build complete!"

# Clean generated HTML files and virtual environment
clean:
	@echo "Cleaning generated files..."
	rm -f articulos.html libros.html videos.html sobremi.html
	@echo "Clean complete!"

# Remove virtual environment
clean-venv:
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "Virtual environment removed!"

# Full clean: files + venv
clean-all: clean clean-venv

# Serve locally for development (requires Python 3)
serve:
	@echo "Starting local server at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	$(PYTHON) -m http.server 8000

# Development workflow: clean, build, serve
dev: clean build serve

# Show help
help:
	@echo "Available targets:"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  install     - Alias for setup"
	@echo "  build       - Generate HTML files from templates (improved script)"
	@echo "  build-old   - Generate HTML files using original script"
	@echo "  clean       - Remove generated HTML files"
	@echo "  clean-venv  - Remove virtual environment"
	@echo "  clean-all   - Remove generated files and virtual environment"
	@echo "  serve       - Start local HTTP server"
	@echo "  dev         - Clean, build and serve (development workflow)"
	@echo "  help        - Show this help message"