import os
import requests
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from pages.project_issues_chat import project_issues_chat
from pages.issue_summary import issue_summary

from components.sidebar import sidebar

st.set_page_config(layout='wide', initial_sidebar_state='expanded')


def launch_app():
    st.title('Github PM Assistant')

    status()

    sidebar()


def status():
    with st.spinner("Checking if API reachable..."):
        api_url = os.environ["API_URL"]
        response = requests.get(f"{api_url}/healthz")
        if response.status_code == 200:
            st.success("Healthy")
        else:
            st.error("API Unreachable")


if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    launch_app()
