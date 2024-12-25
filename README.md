# Electricity Theft Detection System

## Purpose

Electricity theft is a major issue in regions like Karachi, where unauthorized consumption of electricity leads to significant losses for utility companies. This project provides a solution for detecting electricity theft using machine learning models. By analyzing various factors such as electricity usage, voltage fluctuations, and historical data, the system predicts the likelihood of theft.

## Model Overview

The machine learning model used in this project is a **Random Forest Classifier**. This model was chosen due to its ability to handle complex data with multiple features and its robustness in classification tasks.

### Key Techniques Used:
1. **SMOTE (Synthetic Minority Over-sampling Technique)**: Used to handle class imbalance in the dataset. It generates synthetic samples for the underrepresented class (theft) to improve model performance.
   
2. **Grid Search for Hyperparameter Tuning**: The model was fine-tuned using `GridSearchCV`, which optimizes the hyperparameters of the Random Forest classifier to find the best-performing configuration. Key hyperparameters tuned include:
   - `n_estimators`: The number of trees in the forest (100, 200, 300).
   - `max_depth`: The maximum depth of the trees (None, 10, 20).
   - `min_samples_split`: The minimum number of samples required to split an internal node (2, 5, 10).

### Model Pipeline:
The model is part of a pipeline that includes:
- **Standard Scaling**: Scales input features to standardize the dataset.
- **Random Forest Classifier**: A robust classification model to predict the likelihood of electricity theft.

## How to Run the Streamlit App

1. **Install Dependencies**:
   Before running the Streamlit app, make sure to install all necessary dependencies. You can do this by running the following command:
   ```bash
   pip install -r requirements.txt

2. **Run the Streamlit App**:
Once the dependencies are installed, you can run the Streamlit app using the following command:
```bash
streamlit run app.py
```

This will launch the app in your web browser, typically at http://localhost:8501.
