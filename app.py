import streamlit as st
from src.predict import predict
import plotly.graph_objects as go
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Placement Predictor",
    page_icon="⚡",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f0c29, #302b63, #24243e);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Glass card */
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 0 30px rgba(0,255,255,0.15);
}

/* Title */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #00ffff;
    text-shadow: 0 0 15px #00ffff;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #cbd5f5;
    margin-bottom: 35px;
}

/* Result cards */
.success {
    background: linear-gradient(135deg, #00ffcc, #00c6ff);
    color: #001b1b;
    padding: 25px;
    border-radius: 18px;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0 0 30px rgba(0,255,255,0.7);
}

.fail {
    background: linear-gradient(135deg, #ff0844, #ff416c);
    color: white;
    padding: 25px;
    border-radius: 18px;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0 0 30px rgba(255,0,80,0.7);
}

/* Button */
div.stButton > button {
    background: linear-gradient(135deg, #00ffff, #00c6ff);
    color: black;
    font-weight: 800;
    border-radius: 14px;
    height: 3.2em;
    font-size: 18px;
    border: none;
    box-shadow: 0 0 25px rgba(0,255,255,0.6);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>⚡ Student Placement Predictor</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Cyberpunk AI • Placement Probability • Real-time Insights</div>",
    unsafe_allow_html=True
)

# ---------------- INPUT SECTION ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("🧠 Student Skill Matrix")

col1, col2 = st.columns(2)

with col1:
    maths = st.slider("📐 Maths Score", 0, 100, 60)
    python_score = st.slider("🐍 Python Score", 0, 100, 60)
    sql = st.slider("🗄 SQL Score", 0, 100, 60)
    attendance = st.slider("📅 Attendance (%)", 0, 100, 75)

with col2:
    mini_projects = st.number_input("🧩 Mini Projects", min_value=0, step=1)
    communication = st.slider("🗣 Communication Skills", 1, 10, 6)
    readiness = st.slider("🚀 Placement Readiness", 0, 100, 65)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------- PREDICT ----------------
if st.button("⚡ RUN AI PREDICTION", use_container_width=True):

    with st.spinner("⚡ Analyzing student profile..."):
        time.sleep(1)

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
    confidence = probability * 100

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- RESULT ----------------
    if prediction == 1:
        st.markdown(
            f"<div class='success'>✅ PLACED<br>Confidence: {confidence:.1f}%</div>",
            unsafe_allow_html=True
        )
        st.balloons()
    else:
        st.markdown(
            f"<div class='fail'>❌ NOT PLACED<br>Confidence: {confidence:.1f}%</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- CHARTS ----------------
    colA, colB = st.columns(2)

    with colA:
        st.subheader("📊 Confidence Meter")
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00ffff"},
                "steps": [
                    {"range": [0, 40], "color": "#ff4b5c"},
                    {"range": [40, 70], "color": "#fbbf24"},
                    {"range": [70, 100], "color": "#22c55e"},
                ],
            },
            number={"suffix": "%"}
        ))

        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )

        st.plotly_chart(gauge, use_container_width=True)

    with colB:
        st.subheader("📈 Probability Comparison")
        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=["Not Placed", "Placed"],
                    y=[100 - confidence, confidence],
                    marker_color=["#ff4b5c", "#00ffff"]
                )
            ]
        )

        bar_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Probability (%)",
            font=dict(color="white")
        )

        st.plotly_chart(bar_fig, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center; color:#9ca3af; margin-top:40px;'>⚡ Cyberpunk ML Dashboard • Deployed with CI/CD</p>",
    unsafe_allow_html=True
)
