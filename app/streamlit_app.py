import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# Load Model & Scaler
# -----------------------
APP_ROOT = os.path.dirname(__file__)
model_path = os.path.join(APP_ROOT, "best_rf_model.pkl")
scaler_path = os.path.join(APP_ROOT, "scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# -----------------------
# Streamlit Page Config
# -----------------------
st.set_page_config(
    page_title="PCOS Prediction App",
    page_icon="🩺",
    layout="centered"
)

# -----------------------
# Sidebar Instructions
# -----------------------
st.sidebar.header("📌 Instructions")
st.sidebar.markdown(
    """
    - Enter the patient's hormone levels.  
    - Click **Predict** to see the result.  
    - Use realistic medical values for meaningful predictions.  
    """
)

# -----------------------
# App Title
# -----------------------
st.markdown(
    """
    <h1 style="text-align:center;">🩺 PCOS Prediction App</h1>
    <p style="text-align:center; font-size:18px;">
    Predict the probability of PCOS based on hormone levels.
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------
# User Input Form
# -----------------------
st.subheader("Enter Patient Details")

col1, col2, col3 = st.columns(3)

with col1:
    beta_HCG_I = st.number_input("Beta HCG I (mIU/mL)", value=1.0, min_value=0.0)
with col2:
    beta_HCG_II = st.number_input("Beta HCG II (mIU/mL)", value=1.0, min_value=0.0)
with col3:
    AMH = st.number_input("AMH (ng/mL)", value=1.0, min_value=0.0)

# -----------------------
# Prediction Button
# -----------------------
if st.button("🔍 Predict"):
    # Prepare input
    X_new = pd.DataFrame({
        "beta_HCG_I": [beta_HCG_I],
        "beta_HCG_II": [beta_HCG_II],
        "AMH": [AMH],
        "beta_HCG_ratio": [beta_HCG_II / (beta_HCG_I + 1)]
    })

    # Scale input
    X_new_scaled = scaler.transform(X_new)

    # Predict
    prediction = model.predict(X_new_scaled)[0]
    prob = model.predict_proba(X_new_scaled)[0][1]

    # Display Result
    st.subheader("Prediction Result")
    if prediction == 1:
        st.success(f"✅ PCOS Positive — Probability: {prob:.2f}")
    else:
        st.info(f"❌ PCOS Negative — Probability: {prob:.2f}")

    # -----------------------
    # Feature Importances
    # -----------------------
    st.subheader("Top 6 Feature Importances")

    feature_names = ["beta_HCG_I", "beta_HCG_II", "AMH", "beta_HCG_ratio"]
    feature_importances = pd.Series(
        model.feature_importances_, index=feature_names
    ).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=feature_importances.values, y=feature_importances.index, palette="viridis", ax=ax)
    ax.set_title("Feature Importance", fontsize=14)
    ax.set_xlabel("Importance Score")
    ax.set_ylabel("Feature")
    st.pyplot(fig)

# -----------------------
# Footer
# -----------------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:14px;">
    🚀 Built with <b>Streamlit</b> | Machine Learning model trained on medical dataset for PCOS prediction.
    </p>
    """,
    unsafe_allow_html=True
)
