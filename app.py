import streamlit as st
import pandas as pd
import bcrypt
import os
from chatbot_module import run_chatbot

st.set_page_config(page_title="MetaBot - Natural Health Assistant", layout="centered")
st.title("🌿 MetaBot - Natural Metabolic Health Assistant")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSV file paths
USERS_CSV = "users.csv"
PROFILES_CSV = "profiles.csv"

# Ensure CSVs exist
if not os.path.exists(USERS_CSV):
    pd.DataFrame(columns=["name", "username", "password"]).to_csv(USERS_CSV, index=False)
if not os.path.exists(PROFILES_CSV):
    pd.DataFrame(columns=[
        "username", "age", "height", "weight", "conditions",
        "food_habit", "sleep", "exercise", "stress"
    ]).to_csv(PROFILES_CSV, index=False)

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

def load_users():
    return pd.read_csv(USERS_CSV)

def load_profiles():
    return pd.read_csv(PROFILES_CSV)

def save_user(name, username, password):
    df = load_users()
    new_user = pd.DataFrame([[name, username, password]], columns=["name", "username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_CSV, index=False)

def save_profile(profile):
    df = load_profiles()
    df = df[df["username"] != profile["username"]]  # remove existing
    df = pd.concat([df, pd.DataFrame([profile])], ignore_index=True)
    df.to_csv(PROFILES_CSV, index=False)

if choice == "Register":
    st.subheader("Create New Account")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Register"):
        users = load_users()
        if username in users["username"].values:
            st.warning("Username already exists")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            save_user(name, username, hashed_pw)
            st.success("Account created! You can now log in.")

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        users = load_users()
        user_row = users[users["username"] == username]
        if not user_row.empty:
            stored_hash = user_row.iloc[0]["password"]
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Welcome {user_row.iloc[0]['name']}!")

                with st.form("health_form"):
                    st.write("### Fill your Health Details")
                    age = st.number_input("Age", min_value=1, max_value=120)
                    height = st.number_input("Height (cm)")
                    weight = st.number_input("Weight (kg)")
                    conditions = st.text_area("Existing Conditions")
                    food_habit = st.text_area("Food Habits")
                    sleep = st.text_input("Sleep hours (e.g., 6 hours)")
                    exercise = st.text_input("Exercise routine")
                    stress = st.selectbox("Stress level", ["Low", "Moderate", "High"])

                    submitted = st.form_submit_button("Submit")

                    if submitted:
                        profile = {
                            "username": username,
                            "age": age,
                            "height": height,
                            "weight": weight,
                            "conditions": conditions,
                            "food_habit": food_habit,
                            "sleep": sleep,
                            "exercise": exercise,
                            "stress": stress,
                        }
                        save_profile(profile)
                        st.success("Data saved! Redirecting to MetaBot Chat...")
                        st.session_state['profile'] = profile
                        run_chatbot(profile)
            else:
                st.error("Incorrect password")
        else:
            st.error("Username not found")
