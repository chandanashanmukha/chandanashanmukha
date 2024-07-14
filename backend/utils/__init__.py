# backend/__init__.py
# Initialize the Flask app
from flask import Flask
app = Flask(__name__)

# Import the routes to ensure they are registered with the app
from backend import routes
