import pandas as pd
import streamlit as st
import joblib

# Load the trained model
house_price_model = joblib.load('xgb_model.jb')

# Streamlit app title and instructions
st.title("🏡 House Price Prediction")
st.write("Enter the details below to predict the house price.")

# Dictionary mapping technical feature names to user-friendly names
feature_labels = {
    'OverallQual': 'Overall Quality (1-10)',
    'GrLivArea': 'Above Ground Living Area (sq ft)',
    'GarageArea': 'Garage Area (sq ft)',
    '1stFlrSF': 'First Floor Area (sq ft)',
    'FullBath': 'Number of Full Bathrooms',
    'YearBuilt': 'Year Built',
    'YearRemodAdd': 'Year of Last Remodel',
    'MasVnrArea': 'Masonry Veneer Area (sq ft)',
    'Fireplaces': 'Number of Fireplaces',
    'BsmtFinSF1': 'Finished Basement Area (sq ft)',
    'LotFrontage': 'Lot Frontage (feet)',
    'WoodDeckSF': 'Wood Deck Area (sq ft)',
    'OpenPorchSF': 'Open Porch Area (sq ft)',
    'LotArea': 'Lot Area (sq ft)',
    'CentralAir': 'Has Central Air Conditioning'
}

# Dictionary to store user inputs
user_inputs = {}

# Collect user inputs
for feature, label in feature_labels.items():
    if feature == 'CentralAir':
        user_inputs[feature] = st.selectbox(f"{label}", options=['Yes', 'No'], index=0)
    else:
        user_inputs[feature] = st.number_input(
            f"{label}:", value=0.0, 
            step=1.0 if feature in ['OverallQual', 'FullBath', 'Fireplaces'] else 0.1
        )

# Button to trigger prediction
if st.button("🔍 Predict Price"):
    user_inputs['CentralAir'] = 1 if user_inputs['CentralAir'] == "Yes" else 0

    # Convert inputs to DataFrame and make a prediction
    prediction = house_price_model.predict(pd.DataFrame([user_inputs], columns=feature_labels.keys()))

    # Display predicted house price
    st.success(f"🏠 Estimated House Price: **${prediction[0]:,.2f}**")
