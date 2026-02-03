import streamlit as st
from src.predict import predict
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Placement Predictor",
    page_icon="⚡",
    layout="wide"
)

# ---------------- CYBERPUNK NEON CSS ----------------
st.markdown("""
<style>
.main {
    background: radial-gradient(circle at top, #0f0c29, #302b63, #24243e);
}

.block-container {
    padding-top: 2rem;
}

.neon-card {
    background: rgba(20, 20, 40, 0.85);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(0, 255, 255, 0.35);
    box-shadow: 0 0 20px rgba(0,255,255,0.25);
}

.title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #00ffff;
    text-shadow: 0 0 12px #00ffff;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #c7d2fe;
    margin-bottom: 35px;
}

.neon-success {
    background: linear-gradient(135deg, #00ffcc, #00c6ff);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    color: black;
    box-shadow: 0 0 25px rgba(0,255,255,0.7);
}

.neon-fail {
    background: linear-gradient(135deg, #ff0844, #ff416c);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    color: white;
    box-shadow: 0 0 25px rgba(255,0,80,0.7);
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
st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
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

# ---------------- PREDICT BUTTON ----------------
predict_btn = st.button("⚡ RUN AI PREDICTION", use_container_width=True)

# ---------------- RESULTS ----------------
if predict_btn:
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

    # ---------- RESULT CARD ----------
    if prediction == 1:
        st.markdown(
            f"<div class='neon-success'>✅ PLACED<br>Confidence: {confidence:.1f}%</div>",
            unsafe_allow_html=True
        )
        st.balloons()
    else:
        st.markdown(
            f"<div class='neon-fail'>❌ NOT PLACED<br>Confidence: {confidence:.1f}%</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- CONFIDENCE METER ----------------
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
        number={"suffix": "%"},
        title={"text": "Placement Confidence"}
    ))

    gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"}
    )

    st.plotly_chart(gauge, use_container_width=True)

    # ---------------- PROBABILITY BAR CHART ----------------
    st.subheader("📈 Placement Probability Comparison")

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
    "<p style='text-align:center; color:#9ca3af; margin-top:40px;'>⚡ Cyberpunk ML Dashboard • Built with Streamlit</p>",
    unsafe_allow_html=True
)
