import os
import requests
import streamlit as st
from streamlit_chat import message

from components.sidebar import sidebar
from services.assistant import make_request
from utils.urls import get_username_repo


def project_issues_chat(title: str = "Project Issues Chat"):
    st.title(title)

    sidebar(title)

    if "repo_added" not in st.session_state:
        repo_link = st.text_input(
            "Enter a github repo link (username/reponame):",
            placeholder="user_name/repo_name",
        )

        def load_repo():
            with st.spinner("Loading issues from repo"):
                username_repo = get_username_repo(repo_link)
                response = make_request(
                    "post", "/fetch-issues", payload={"repo_url": username_repo}
                ) if username_repo else None

            if response and response.status_code == 200:
                st.session_state.repo_added = repo_link
            else:
                st.error("Failed to add repo. Please confirm you entered the correct repo path")
        st.button("Add repo", on_click=load_repo)
    else:
        chat_interface()


def chat_interface():
    messages_key = "project_issue_messages"

    if messages_key not in st.session_state:
        st.session_state[messages_key] = []

    user_prompt = st.chat_input("Enter a message")

    if user_prompt:
        user_message = user_prompt
        st.session_state[messages_key].append(user_message)

        response = chat(query=user_message)
        st.session_state[messages_key].append(response["response"])

    for i, msg in enumerate(st.session_state[messages_key]):
        message(
            msg,
            is_user=i % 2 == 0,
            key=f"message{i}",
            allow_html=True,
        )


def chat(query):
    response = make_request("get", f"/qa/{query}")
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "response": "An error occurred. The system was not able to process your request"
        }


project_issues_chat()
