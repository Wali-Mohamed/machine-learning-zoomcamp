import streamlit as st
import pickle
#import sklearn  # Import scikit-learn to support deserializing objects

import os
# Define paths to the model files relative to the app directory
base_dir = os.getcwd()  # Gets the directory of the current script
print(base_dir)
dv_path = os.path.join(base_dir, '05-Deployment/streamlit_app/dv.bin')
model_path = os.path.join(base_dir, '05-Deployment/streamlit_app/model1.bin')
print(dv_path, model_path)
# Check if files exist and load models
if not os.path.isfile(dv_path) or not os.path.isfile(model_path):
    st.error("Model files 'dv.bin' or 'model1.bin' not found in the directory. Check file paths.")
else:
    # Load your pre-trained model and transformer 
    with open(dv_path, 'rb') as f_in:
        dv = pickle.load(f_in)
    with open(model_path, 'rb') as f_in:
        model = pickle.load(f_in)



# CSS for business theme background
st.markdown("""
    <style>
    /* Set background color and styling */
    .stApp {
        background-color: #f2f2f2;  /* Light gray background */
        color: #333333;              /* Dark text for contrast */
    }

    /* Customize headers */
    h1, h2, h3, h4, h5, h6 {
        color: #003366; /* Dark blue for headings */
    }

    /* Customize sidebar */
    .css-1d391kg {
        background-color: #e6e6e6;  /* Slightly darker gray sidebar */
    }

    /* Style prediction result */
    .prediction-result {
        font-weight: bold;
        font-size: 1.2em;
        color: #003366;
    }
    </style>
    """, unsafe_allow_html=True)
# App Title and Description
st.title("Bank Term Deposit Prediction")
st.write("""
    This app predicts whether a bank client will subscribe to a term deposit based on their profile and past campaign outcomes.
    The model considers three key features: `job`, `duration`, and `poutcome`. For more detailed information on all available features, see the sidebar.
""")

# Explain the three main features used in this simplified model
st.write("### Features Used in This Model:")
st.write("""
- **Job**: The type of job the client has, such as management, technician, entrepreneur, or blue-collar. Job type often reflects income stability and financial behavior.
- **Duration**: The duration of the last contact with the client in seconds. Generally, longer durations indicate higher engagement and interest from the client.
- **Poutcome**: The outcome of the previous marketing campaign, if any. Possible values include:
    - **Success**: The client subscribed in a previous campaign.
    - **Failure**: The client was contacted but did not subscribe.
    - **Unknown**: There was no information from a previous campaign.
""")

# Note on Model Simplification
st.write("**Note:** In real-life applications, models often include many more features to improve prediction accuracy. This example has been simplified for testing purposes.")

# Sidebar with Feature Information
st.sidebar.header("Client Information")

# Add option to read more about all features
show_features = st.sidebar.checkbox("Show Full Feature Descriptions")

# If checked, show descriptions of all features except 'default' and 'loan'
if show_features:
    st.sidebar.write("### All Feature Descriptions (Except `loan` and `default`):")
    st.sidebar.write("""
    - **age**: The age of the client.
    - **job**: The type of job the client has (e.g., management, technician, blue-collar, entrepreneur).
    - **marital**: Marital status of the client (e.g., married, single, divorced).
    - **education**: Level of education (e.g., primary, secondary, tertiary, or unknown).
    - **balance**: Average yearly balance in euros in the client’s bank account.
    - **housing**: Whether the client has a housing loan (`yes` or `no`).
    - **contact**: Type of communication used to contact the client (e.g., cellular, telephone, unknown).
    - **day**: Day of the month when the client was last contacted.
    - **month**: Month of last contact (e.g., jan, feb, mar).
    - **duration**: Duration of the last contact in seconds. Longer durations generally indicate higher engagement.
    - **campaign**: Number of contacts performed during this campaign for this client.
    - **pdays**: Number of days since the client was last contacted in a previous campaign. `-1` indicates no prior contact.
    - **previous**: Number of contacts performed before this campaign for this client.
    - **poutcome**: Outcome of the previous marketing campaign (e.g., success, failure, nonexistent).
    """)

# Job options
job_options = ["management", "technician", "entrepreneur", "blue-collar", "unknown"]
job = st.sidebar.selectbox("Select Job", job_options)

# Duration input
duration = st.sidebar.slider("Duration of Last Contact (seconds)", min_value=0, max_value=1000, value=400, step=10)

# Poutcome options
poutcome_options = ["success", "failure", "unknown"]
poutcome = st.sidebar.selectbox("Outcome of Previous Campaign", poutcome_options)

# Input data formatting
client_data = {
    "job": job,
    "duration": duration,
    "poutcome": poutcome
}
print(dv)
# Predict button
if st.sidebar.button("Predict"):
    st.write("### Prediction Result")
    
    # transform
    X = dv.transform(client_data)
    # predict
    y_pred = model.predict_proba(X)[0, 1]
    print(y_pred, type(y_pred))
    will_subscribe = y_pred >= 0.5
    
    # Create stakeholder-friendly message
    if will_subscribe:
        message = f"The model predicts that the client is likely to subscribe to a term deposit with a probability of {y_pred * 100:.2f}%."
    else:
        message = f"The model predicts that the client is unlikely to subscribe to a term deposit, with a probability of {(1 - y_pred) * 100:.2f}%."

    # Display the result
    result = {
        "message": message,
        "subscription_probability": f"{y_pred * 100:.2f}%",
        "subscribe": bool(will_subscribe)
    }
    
    st.write(result["message"])
    st.json(result)  # Display detailed JSON format for technical review