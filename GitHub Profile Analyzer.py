import requests
import streamlit as st

def fetch_user_data(username):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"

    user_data = requests.get(user_url).json()
    repos_data = requests.get(repos_url).json()

    return user_data, repos_data

def display(user, repos):
    st.image(user['avatar_url'], width=100)
    st.write(f"👤 Name: {user.get('name', 'N/A')}")
    st.write(f"📍 Location: {user.get('location', 'N/A')}")
    st.write(f"📦 Public Repos: {user['public_repos']}")
    st.write(f"👥 Followers: {user['followers']}")
    st.write("---")

    lang_count = {}
    for repo in repos:
        lang = repo.get('language')
        if lang:
            lang_count[lang] = lang_count.get(lang, 0) + 1

    st.subheader("📊 Top Languages")
    for lang, count in sorted(lang_count.items(), key=lambda x: -x[1]):
        st.write(f"{lang}: {count} repos")

st.title("🐙 GitHub Profile Analyzer")

username = st.text_input("Enter GitHub Username")

if st.button("Analyze"):
    user, repos = fetch_user_data(username)
    if "message" in user:
        st.error("User not found!")
    else:
        display(user, repos)
