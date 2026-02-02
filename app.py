import streamlit as st
from src.predict import predict

st.set_page_config(
    page_title="Student Placement Predictor",
    page_icon="",
    layout="centered"
)

st.title(" Student Placement Predictor")
st.write("Predict student placement using academic, technical, and readiness scores.")

st.divider()

#  INPUT SECTION 
st.subheader("Enter Student Details")

maths = st.number_input("Maths Score", min_value=0, max_value=100, step=1)
python_score = st.number_input("Python Score", min_value=0, max_value=100, step=1)
sql = st.number_input("SQL Score", min_value=0, max_value=100, step=1)
attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, step=1)
mini_projects = st.number_input("Number of Mini Projects", min_value=0, step=1)
communication = st.number_input("Communication Score (1–10)", min_value=1, max_value=10, step=1)
readiness = st.number_input("Placement Readiness Score", min_value=0, max_value=100, step=1)

# PREDICTION 
if st.button("Predict Placement"):
    input_data = {
        "Maths": maths,
        "Python": python_score,
        "SQL": sql,
        "Attendance": attendance,
        "Mini_Projects": mini_projects,
        "Communication_Score": communication,
        "Placement_Readiness_Score": readiness
    }

    prediction, probability = predict(input_data)

    st.divider()

    if prediction == 1:
        st.success(f" Student is likely to be placed (Probability: {probability:.2f})")
    else:
        st.error(f"Student is unlikely to be placed (Probability: {probability:.2f})")