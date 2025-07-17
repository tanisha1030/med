import streamlit as st

def run_chatbot(profile):
    st.subheader("🧠 MetaBot Chat Assistant")

    st.write("### Based on your profile, here are some personalized natural suggestions:")

    # Simple rule-based suggestions
    suggestions = []

    if profile["weight"] / ((profile["height"] / 100) ** 2) > 25:
        suggestions.append("✅ Try reducing refined carbs and increase fiber intake (e.g., oats, leafy greens).")

    if profile["stress"].lower() == "high":
        suggestions.append("🧘 Practice 10 mins of meditation or breathing exercises daily.")

    if "vitamin" in profile["conditions"].lower():
        suggestions.append("🍊 Include citrus fruits and sunshine exposure for Vitamin D.")

    if profile["sleep"] and int(profile["sleep"].split()[0]) < 6:
        suggestions.append("😴 Improve your sleep routine. Aim for 7–8 hours each night.")

    if not profile["exercise"] or "none" in profile["exercise"].lower():
        suggestions.append("🚶 Start a 20 min daily walk post-meal to help regulate metabolism.")

    if not suggestions:
        suggestions.append("🎉 You're on the right track! Keep maintaining a balanced lifestyle.")

    for tip in suggestions:
        st.write(tip)
