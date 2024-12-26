import streamlit as st
import pickle
import numpy as np

# Load the saved pipeline
with open('theft_prediction_pipeline.pkl', 'rb') as file:
    model = pickle.load(file)

# Define input features for the model
input_features = [
    "Usage (kWh)", "TimeOfDay", "VoltageFluctuations", "NumberOfResidents",
    "ApplianceCount", "IndustrialAreaNearby", "PreviousTheftHistory",
    "AverageDailyUsage", "BillPaymentDelay (days)", "UnusualUsageSpike"
]

# Streamlit app
def main():
    st.set_page_config(page_title="Electricity Theft Prediction System", layout="wide")

    st.title("🚨 Electricity Theft Prediction System")
    st.markdown("""<style> 
        .main {background-color: #f9f9f9;} 
        div[data-testid="stMarkdownContainer"] h1 {color: #ff4b4b; text-align: center;} 
    </style>""", unsafe_allow_html=True)
    st.markdown("This app predicts whether electricity is being theft or not based on various input features. Please enter all the required inputs below:")

    with st.form("theft_prediction_form"):
        col1, col2, col3 = st.columns(3)
        inputs = []

        with col1:
            usage = st.number_input("Usage (kWh)", min_value=0.0, step=0.1, value=0.0)
            fluctuation = st.number_input("Voltage Fluctuations", min_value=0.0, step=0.1, value=0.0)
            residents = st.number_input("Number of Residents", min_value=0, step=1, value=1)
            appliances = st.number_input("Appliance Count", min_value=0, step=1, value=1)

        with col2:
            time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
            industrial_area = st.selectbox("Industrial Area Nearby", ["No", "Yes"])
            theft_history = st.selectbox("Previous Theft History", ["No", "Yes"])

        with col3:
            daily_usage = st.number_input("Average Daily Usage", min_value=0.0, step=0.1, value=0.0)
            payment_delay = st.number_input("Bill Payment Delay (days)", min_value=0, step=1, value=0)
            usage_spike = st.selectbox("Unusual Usage Spike", ["No", "Yes"])

        # Convert inputs to required format
        time_of_day = ["Morning", "Afternoon", "Evening", "Night"].index(time_of_day)
        industrial_area = ["No", "Yes"].index(industrial_area)
        theft_history = ["No", "Yes"].index(theft_history)
        usage_spike = ["No", "Yes"].index(usage_spike)

        inputs = [
            usage, time_of_day, fluctuation, residents, appliances,
            industrial_area, theft_history, daily_usage, payment_delay, usage_spike
        ]

        # Submit button
        submitted = st.form_submit_button("Predict")

        if submitted:
            inputs_array = np.array([inputs])  # Reshape for a single input
            prediction = model.predict(inputs_array)[0]
            result = "Theft" if prediction == 1 else "No Theft"

            if result == "Theft":
                    st.markdown("""
                    <div style="background-color: #f8d7da; padding: 20px; border-radius: 5px; text-align: center;">
                    <h2 style="color: #721c24;">Prediction: Theft</h2>
                    <p style="color: #721c24; font-size: 16px;">Please contact K Electric at <b>118</b> or <b>99000</b> to report the issue immediately.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                    st.markdown("""
                    <div style="background-color: #d4edda; padding: 20px; border-radius: 5px; text-align: center;">
                    <h2 style="color: #155724;">Prediction: No Theft</h2>
                    </div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
