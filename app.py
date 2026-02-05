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

# ---------------- CSS (DESIGN SYSTEM) ----------------
st.markdown("""
<style>
body {
    background-color: #F0F4F8;
}

.block-container {
    padding: 32px;
    max-width: 1400px;
}

/* HEADER */
.header-title {
    font-size: 36px;
    font-weight: 800;
    color: #00D4FF;
    text-align: center;
}

.header-subtitle {
    font-size: 14px;
    color: #8B92A1;
    text-align: center;
    margin-bottom: 30px;
}

/* CARDS */
.card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

/* SECTION HEADERS */
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #2D3436;
    margin-bottom: 16px;
}

/* RESULT BANNER */
.result-success {
    background: linear-gradient(135deg, #00D4FF, #00B8D4);
    color: white;
    padding: 22px;
    border-radius: 14px;
    font-size: 20px;
    font-weight: 800;
    text-align: center;
}

.result-fail {
    background: linear-gradient(135deg, #FF1654, #FF006E);
    color: white;
    padding: 22px;
    border-radius: 14px;
    font-size: 20px;
    font-weight: 800;
    text-align: center;
}

/* BUTTON */
div.stButton > button {
    background: linear-gradient(135deg, #00D4FF, #0099FF);
    color: white;
    font-weight: 700;
    font-size: 16px;
    border-radius: 12px;
    padding: 12px;
    border: none;
    transition: 0.3s ease;
}

div.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(135deg, #00B8D4, #0077FF);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header-title'>⚡ Student Placement Predictor</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='header-subtitle'>Cyberpunk AI • Placement Probability • Real-time Insights</div>",
    unsafe_allow_html=True
)

# ---------------- MAIN GRID ----------------
left, right = st.columns([1.1, 0.9], gap="large")

# ---------------- INPUT CARD ----------------
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🧠 Student Skill Matrix</div>", unsafe_allow_html=True)

    maths = st.slider("📐 Maths Score", 0, 100, 60)
    python_score = st.slider("🐍 Python Score", 0, 100, 60)
    sql = st.slider("🗄 SQL Score", 0, 100, 60)
    attendance = st.slider("📅 Attendance (%)", 0, 100, 75)

    mini_projects = st.number_input("🧩 Mini Projects", min_value=0, step=1)
    communication = st.slider("🗣 Communication Skills", 1, 10, 6)
    readiness = st.slider("🚀 Placement Readiness", 0, 100, 65)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- OUTPUT ----------------
with right:
    if st.button("⚡ RUN AI PREDICTION", use_container_width=True):

        with st.spinner("Analyzing profile..."):
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

        # RESULT BANNER
        if prediction == 1:
            st.markdown(
                f"<div class='result-success'>✓ PLACED<br>Confidence: {confidence:.1f}%</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='result-fail'>✗ NOT PLACED<br>Confidence: {confidence:.1f}%</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- CONFIDENCE METER ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📈 Confidence Meter</div>", unsafe_allow_html=True)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00D4FF"},
                "steps": [
                    {"range": [0, 40], "color": "#FF1654"},
                    {"range": [40, 70], "color": "#FFB703"},
                    {"range": [70, 100], "color": "#2ECC71"},
                ],
            }
        ))

        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#2D3436"}
        )

        st.plotly_chart(gauge, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- BAR CHART ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Probability Comparison</div>", unsafe_allow_html=True)

        bar_fig = go.Figure(go.Bar(
            x=[100 - confidence, confidence],
            y=["Not Placed", "Placed"],
            orientation="h",
            marker_color=["#FF1654", "#00D4FF"],
            text=[f"{100-confidence:.1f}%", f"{confidence:.1f}%"],
            textposition="outside"
        ))

        bar_fig.update_layout(
            xaxis=dict(range=[0, 100]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2D3436")
        )

        st.plotly_chart(bar_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center; color:#8B92A1; margin-top:40px;'>⚡ Modern ML Dashboard • Auto-deployed via CI/CD</p>",
    unsafe_allow_html=True
)
