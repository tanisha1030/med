import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from pymongo import MongoClient
from chatbot_module import run_chatbot
import bcrypt

client = MongoClient("mongodb://localhost:27017")
db = client["metabot_db"]
users = db["users"]

st.set_page_config(page_title="MetaBot - Natural Health Assistant", layout="centered")
st.title("🌿 MetaBot - Natural Metabolic Health Assistant")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Register"):
        if users.find_one({"username": username}):
            st.warning("Username already exists")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            users.insert_one({"name": name, "username": username, "password": hashed_pw})
            st.success("Account created! You can now log in.")

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user = users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user['password']):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome {user['name']}!")

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
                    db.user_profiles.update_one(
                        {"username": username},
                        {"$set": profile},
                        upsert=True
                    )
                    st.success("Data saved! Redirecting to MetaBot Chat...")
                    st.session_state['profile'] = profile
                    run_chatbot(profile)
        else:
            st.error("Invalid credentials")
