# app.py
import streamlit as st
from agents.coordinator import Coordinator
import config

st.set_page_config(layout="wide")

st.title("🤖 Auto-Running Frontend Agent")
st.write("This agent builds a new React application and automatically runs the dev server for you to preview.")

coordinator = Coordinator(st)

with st.form("request_form"):
    user_request = st.text_area(
        "UI Description",
        "Create a simple portfolio landing page for a developer named 'Alex Doe'. It should have a retro, 8-bit theme. Include a header with navigation, a hero section with a typing animation, a project gallery using cards, and a simple footer.",
        height=150
    )

    base_repo_url = st.text_input(
        "Base Vite+React+ShadCN (pnpm) Git Repository URL",
        "https://github.com/dan5py/react-vite-shadcn-ui"
    )

    submitted = st.form_submit_button("🚀 Build & Run Frontend")

if submitted:
    if not config.OPENROUTER_API_KEY or "your-openrouter-api-key" in config.OPENROUTER_API_KEY:
        st.error("Please configure your .env file with your OpenRouter API key.")
    elif not base_repo_url or "github.com" not in base_repo_url:
        st.error("Please provide a valid GitHub URL for the base repository.")
    else:
        st.info("Agents are starting the build process...")
        coordinator.run_frontend_build(user_request, base_repo_url)
