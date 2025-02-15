import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1628348070889-cb656235b4eb?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
      }
      [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);  
      }
      [data-testid="stToolbar"] {
        right: 2rem;
      }
      .st-emotion-cache-czk5ss.e16jpq800 {
        visibility: hidden;
      }
      .st-emotion-cache-mnu3yk.ef3psqc5 {
        visibility: hidden;
      }
      .st-emotion-cache-15ecox0.ezrtsby0 {
        visibility: hidden;
      }
      .st-emotion-cache-fm8pe0.e1nzilvr4 {
        color: black;
      }
      .st-emotion-cache-fm8pe0.e1nzilvr4{
        color: white;
      }
    </style>
    """, unsafe_allow_html=True)

# Load trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

st.title("🏦 Loan Approval Prediction App with Visual Insights")

# User Inputs with Sliders
person_age = st.slider("Age", 18, 100, 30)
person_income = st.slider("Annual Income ($)", 10000, 200000, 50000)
loan_amnt = st.slider("Loan Amount ($)", 1000, 100000, 20000)
credit_score = st.slider("Credit Score", 300, 850, 720)
person_emp_exp = st.slider("Employment Experience (years)", 0, 40, 5)
loan_int_rate = st.slider("Loan Interest Rate (%)", 0.0, 30.0, 7.5)
cb_person_cred_hist_length = st.slider("Credit History Length (years)", 1, 30, 10)

# Derived Feature
loan_percent_income = loan_amnt / (person_income + 1e-5)

# Dropdown for Loan Intent
loan_intent_options = ['EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE']
loan_intent = st.selectbox("Loan Intent", loan_intent_options)

# Placeholder dummy features for demonstration
person_education_label = 1
person_home_ownership_OWN = 0
person_home_ownership_RENT = 1
person_home_ownership_OTHER = 0
previous_loan_defaults_on_file_Yes = 0
person_gender_male = 1

# One-hot encoding for loan intent
loan_intent_EDUCATION = 1 if loan_intent == 'EDUCATION' else 0
loan_intent_HOMEIMPROVEMENT = 1 if loan_intent == 'HOMEIMPROVEMENT' else 0
loan_intent_MEDICAL = 1 if loan_intent == 'MEDICAL' else 0
loan_intent_PERSONAL = 1 if loan_intent == 'PERSONAL' else 0
loan_intent_VENTURE = 1 if loan_intent == 'VENTURE' else 0

# Constructing Input Dataframe
input_data = pd.DataFrame({
    'person_age': [person_age],
    'person_income': [person_income],
    'person_emp_exp': [person_emp_exp],
    'loan_amnt': [loan_amnt],
    'loan_int_rate': [loan_int_rate],
    'loan_percent_income': [loan_percent_income],
    'cb_person_cred_hist_length': [cb_person_cred_hist_length],
    'credit_score': [credit_score],
    'person_education_label': [person_education_label],
    'person_home_ownership_OTHER': [person_home_ownership_OTHER],
    'person_home_ownership_OWN': [person_home_ownership_OWN],
    'person_home_ownership_RENT': [person_home_ownership_RENT],
    'previous_loan_defaults_on_file_Yes': [previous_loan_defaults_on_file_Yes],
    'person_gender_male': [person_gender_male],
    'loan_intent_EDUCATION': [loan_intent_EDUCATION],
    'loan_intent_HOMEIMPROVEMENT': [loan_intent_HOMEIMPROVEMENT],
    'loan_intent_MEDICAL': [loan_intent_MEDICAL],
    'loan_intent_PERSONAL': [loan_intent_PERSONAL],
    'loan_intent_VENTURE': [loan_intent_VENTURE],
})

# Predict
if st.button("Predict Loan Approval"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    result = 'Approved ✅' if prediction == 1 else 'Rejected ❌'
    st.subheader(f"Loan Status: {result}")
    st.write(f"Confidence: {probability * 100:.2f}%")

    # Plot 1: Loan Amount vs Income
    fig, ax = plt.subplots()
    ax.bar(["Loan Amount", "Annual Income"], [loan_amnt, person_income], color=['orange', 'green'])
    ax.set_title("Loan Amount vs Annual Income")
    st.pyplot(fig)

    # Plot 2: Credit Score Distribution
    fig, ax = plt.subplots()
    sns.histplot(np.random.normal(700, 100, 500), kde=True, color='lightblue', ax=ax)
    ax.axvline(credit_score, color='red', linestyle='--', label=f"Your Score: {credit_score}")
    ax.set_title("Your Credit Score Position")
    ax.legend()
    st.pyplot(fig)

    # Plot 3: Loan Percent Income Gauge
    st.write("### Loan Percent Income Ratio")
    st.write(f"Loan Percent Income Ratio: {loan_percent_income:.2f}")
    if loan_percent_income > 0.4:
        st.error("⚠️ High Loan Percent Income Ratio (Risky)")
    else:
        st.success("✅ Healthy Loan Percent Income Ratio")
