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

    # Initialize session state for prediction and reset flags
    if "prediction_result" not in st.session_state:
        st.session_state["prediction_result"] = ""
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    # Function to clear the prediction result when inputs change
    def clear_prediction():
        st.session_state["prediction_result"] = ""
        st.session_state["submitted"] = False

    with st.form("theft_prediction_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            usage = st.number_input("Usage (kWh)", min_value=0.0, step=0.1, value=0.0, key="usage", on_change=clear_prediction)
            fluctuation = st.number_input("Voltage Fluctuations", min_value=0.0, step=0.1, value=0.0, key="fluctuation", on_change=clear_prediction)
            residents = st.number_input("Number of Residents", min_value=0, step=1, value=1, key="residents", on_change=clear_prediction)
            appliances = st.number_input("Appliance Count", min_value=0, step=1, value=1, key="appliances", on_change=clear_prediction)

        with col2:
            time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"], key="time_of_day", on_change=clear_prediction)
            industrial_area = st.selectbox("Industrial Area Nearby", ["No", "Yes"], key="industrial_area", on_change=clear_prediction)
            theft_history = st.selectbox("Previous Theft History", ["No", "Yes"], key="theft_history", on_change=clear_prediction)

        with col3:
            daily_usage = st.number_input("Average Daily Usage", min_value=0.0, step=0.1, value=0.0, key="daily_usage", on_change=clear_prediction)
            payment_delay = st.number_input("Bill Payment Delay (days)", min_value=0, step=1, value=0, key="payment_delay", on_change=clear_prediction)
            usage_spike = st.selectbox("Unusual Usage Spike", ["No", "Yes"], key="usage_spike", on_change=clear_prediction)

        # Submit button
        submitted = st.form_submit_button("Predict")

        if submitted:
            # Process the form inputs for prediction
            inputs = [
                st.session_state["usage"],
                ["Morning", "Afternoon", "Evening", "Night"].index(st.session_state["time_of_day"]),
                st.session_state["fluctuation"],
                st.session_state["residents"],
                st.session_state["appliances"],
                ["No", "Yes"].index(st.session_state["industrial_area"]),
                ["No", "Yes"].index(st.session_state["theft_history"]),
                st.session_state["daily_usage"],
                st.session_state["payment_delay"],
                ["No", "Yes"].index(st.session_state["usage_spike"]),
            ]
            inputs_array = np.array([inputs])  # Reshape for a single input
            prediction = model.predict(inputs_array)[0]
            st.session_state["prediction_result"] = "Theft" if prediction == 1 else "No Theft"
            st.session_state["submitted"] = True

    # Display the prediction result
    if st.session_state["submitted"] and st.session_state["prediction_result"]:
        if st.session_state["prediction_result"] == "Theft":
            st.markdown("""
                <div style="background-color: #f8d7da; padding: 20px; border-radius: 5px; text-align: center;">
                <h2 style="color: #721c24;">Prediction: Theft</h2>
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
