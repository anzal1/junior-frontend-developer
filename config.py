# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
YOUR_SITE_URL = os.getenv("YOUR_SITE_URL", "")
YOUR_SITE_NAME = os.getenv("YOUR_SITE_NAME", "")

# Model Selection for OpenRouter
MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"

# This is the path where the agent will create and manage the React project.
WORKSPACE_DIR = "generated_frontend_project"
