import streamlit as st
import pandas as pd
import joblib

# Load saved AI model
model = joblib.load("../model/churn_model.pkl")

st.title("🤖 AI Customer Churn Predictor")
st.write("Enter customer details to predict churn risk.")

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30
)

tenure = st.number_input(
    "Tenure (months)",
    min_value=0,
    max_value=120,
    value=12
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0,
    value=2000
)

support_calls = st.number_input(
    "Support Calls",
    min_value=0,
    max_value=50,
    value=2
)

late_payments = st.number_input(
    "Late Payments",
    min_value=0,
    max_value=50,
    value=1
)

contract = st.selectbox(
    "Contract",
    ["Monthly", "Yearly"]
)

if st.button("🔮 Predict Churn"):

    customer = pd.DataFrame({
        "Age": [age],
        "Tenure": [tenure],
        "Monthly_Charges": [monthly_charges],
        "Support_Calls": [support_calls],
        "Late_Payments": [late_payments],
        "Contract": [contract]
    })

    prediction = model.predict(customer)[0]
    probability = model.predict_proba(customer)[0][1]

    # Prediction result
    if prediction == 1:
        st.error("⚠️ Customer is likely to churn")
    else:
        st.success("✅ Customer is likely to stay")

    st.write(f"Churn Probability: **{probability:.1%}**")

    # Risk Dashboard
    st.divider()
    st.header("📊 Customer Risk Dashboard")

    if probability >= 0.70:
        risk_level = "🔴 HIGH RISK"
    elif probability >= 0.40:
        risk_level = "🟠 MEDIUM RISK"
    else:
        risk_level = "🟢 LOW RISK"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Churn Probability",
            f"{probability:.1%}"
        )

    with col2:
        st.metric(
            "Risk Level",
            risk_level
        )

    with col3:
        st.metric(
            "Support Calls",
            int(support_calls)
        )

    # Risk Score
    st.subheader("Customer Risk Score")
    st.progress(float(probability))

    # Customer Details
    st.subheader("👤 Customer Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Age:**", int(age))
        st.write("**Tenure:**", int(tenure), "months")

    with col2:
        st.write("**Monthly Charges:** ₹", int(monthly_charges))
        st.write("**Late Payments:**", int(late_payments))

    with col3:
        st.write("**Support Calls:**", int(support_calls))
        st.write("**Contract:**", contract)

    # Risk Factors
    st.subheader("⚠️ Risk Factors")

    factors = []

    if support_calls >= 4:
        factors.append("High number of support calls")

    if late_payments >= 2:
        factors.append("Multiple late payments")

    if contract == "Monthly":
        factors.append("Monthly contract")

    if monthly_charges >= 3000:
        factors.append("High monthly charges")

    if len(factors) == 0:
        st.success("✅ No major risk factors detected.")
    else:
        for factor in factors:
            st.warning("⚠️ " + factor)

    # Customer Analysis Chart
    st.subheader("📊 Customer Analysis")

    chart_data = pd.DataFrame({
        "Metric": [
            "Age",
            "Tenure",
            "Support Calls",
            "Late Payments"
        ],
        "Value": [
            age,
            tenure,
            support_calls,
            late_payments
        ]
    })

    st.bar_chart(
        chart_data.set_index("Metric")
    )