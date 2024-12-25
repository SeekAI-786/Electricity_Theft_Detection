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

    # Initialize session state for prediction result
    if "prediction_result" not in st.session_state:
        st.session_state["prediction_result"] = ""

    # Function to clear the prediction result
    def clear_prediction():
        st.session_state["prediction_result"] = ""

    with st.form("theft_prediction_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        inputs = []

        with col1:
            usage = st.number_input(
                "Usage (kWh)", min_value=0.0, step=0.1, value=0.0, on_change=clear_prediction
            )
            fluctuation = st.number_input(
                "Voltage Fluctuations", min_value=0.0, step=0.1, value=0.0, on_change=clear_prediction
            )
            residents = st.number_input(
                "Number of Residents", min_value=0, step=1, value=1, on_change=clear_prediction
            )
            appliances = st.number_input(
                "Appliance Count", min_value=0, step=1, value=1, on_change=clear_prediction
            )

        with col2:
            time_of_day = st.selectbox(
                "Time of Day", ["Morning", "Afternoon", "Evening", "Night"], on_change=clear_prediction
            )
            industrial_area = st.selectbox(
                "Industrial Area Nearby", ["No", "Yes"], on_change=clear_prediction
            )
            theft_history = st.selectbox(
                "Previous Theft History", ["No", "Yes"], on_change=clear_prediction
            )

        with col3:
            daily_usage = st.number_input(
                "Average Daily Usage", min_value=0.0, step=0.1, value=0.0, on_change=clear_prediction
            )
            payment_delay = st.number_input(
                "Bill Payment Delay (days)", min_value=0, step=1, value=0, on_change=clear_prediction
            )
            usage_spike = st.selectbox(
                "Unusual Usage Spike", ["No", "Yes"], on_change=clear_prediction
            )

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
            st.session_state["prediction_result"] = "Theft" if prediction == 1 else "No Theft"

    # Display the prediction result
    if st.session_state["prediction_result"] == "Theft":
        st.markdown("""
            <div style="background-color: #f8d7da; padding: 20px; border-radius: 5px; text-align: center;">
            <h2 style="color: #721c24;">Prediction: Theft</h2>
            </div>
        """, unsafe_allow_html=True)
    elif st.session_state["prediction_result"] == "No Theft":
        st.markdown("""
            <div style="background-color: #d4edda; padding: 20px; border-radius: 5px; text-align: center;">
            <h2 style="color: #155724;">Prediction: No Theft</h2>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
