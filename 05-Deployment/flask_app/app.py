from flask import Flask, request, jsonify, render_template
import pickle
import sqlite3
import os

app = Flask(__name__)

# Paths to the model files
base_dir = os.getcwd()
print(base_dir)

dv_path = os.path.join(base_dir, '05-Deployment/streamlit_app/dv.bin')
model_path = os.path.join(base_dir, '05-Deployment/streamlit_app/model1.bin')
print(model_path)

# Load model and vectorizer
if not os.path.isfile(dv_path) or not os.path.isfile(model_path):
    raise FileNotFoundError("Model files 'dv.bin' or 'model1.bin' not found in the directory. Check file paths.")
else:
    with open(dv_path, 'rb') as f:
        dv = pickle.load(f)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

# Initialize database
def init_db():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thumbs_up BOOLEAN,
            comment TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize database on app start
init_db()

# Home route with form input
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    client_data = {
        "job": data.get("job"),
        "duration": int(data.get("duration")),
        "poutcome": data.get("poutcome")
    }

    # Transform input and predict
    X = dv.transform([client_data])
    y_pred = model.predict_proba(X)[0, 1]
    will_subscribe = y_pred >= 0.5

    # Generate prediction message
    if will_subscribe:
        message = f"The client is likely to subscribe with a probability of {y_pred * 100:.2f}%."
    else:
        message = f"The client is unlikely to subscribe, with a probability of {(1 - y_pred) * 100:.2f}%."

    # Return the result as JSON
    result = {
        "message": message,
        "subscription_probability": f"{y_pred * 100:.2f}%",
        "subscribe": bool(will_subscribe)
    }
    return jsonify(result)

# Feedback route
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    thumbs_up = data.get('thumbs_up')
    comment = data.get('comment')

    # Insert feedback into the database
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (thumbs_up, comment) VALUES (?, ?)", (thumbs_up, comment))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Thank you for your feedback!"})

# Fetch feedback
@app.route('/get_feedback', methods=['GET'])
def get_feedback():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedback_data = cursor.fetchall()
    conn.close()

    # Return feedback data as JSON
    return jsonify({"feedback": feedback_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
