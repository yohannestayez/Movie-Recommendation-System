from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('.env')

# Set environment variables
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
