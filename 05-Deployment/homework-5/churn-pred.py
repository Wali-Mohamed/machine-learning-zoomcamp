from flask import Flask, request, jsonify
import pickle
import numpy

app = Flask('churn-prediction') # give an identity to your web service

with open('dv.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary 
    dv = pickle.load(f_in)
with open('model1.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary 
    model = pickle.load(f_in)
## Note: never open a binary file you do not trust the source!
print(dv)
print(model)


@app.route('/pred', methods=['POST']) # use decorator to add Flask's functionality to our function
def predict():
    
    client=request.get_json()
    

    X = dv.transform(client)
    y_pred = model.predict_proba(X)[:, 1]
    churn=y_pred>=0.5
    result={
        'churn_probability':float(y_pred),
        'churn':bool(churn)

    }
    return jsonify(result)
    

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=9696) # run the code in local machine with the debugging mode true and port 9696