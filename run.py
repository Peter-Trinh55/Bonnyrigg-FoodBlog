"""
run.py
Entry point for running the Flask development server locally.
"""

from flaskblog import create_app  # Import the app factory so config/extensions are loaded.

# Create the Flask app using the factory pattern (Corey Schafer style).
app = create_app()

if __name__ == "__main__":
    # Run in debug mode for development only (auto-reload + helpful error pages).
    app.run(debug=True)
