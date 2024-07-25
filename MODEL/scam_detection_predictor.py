from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

app = FastAPI()

# Load the models
logistic_regression = joblib.load('logistic_regression_model.pkl')
neural_network_model = load_model('neural_network_model.h5')

# Load the scaler used for scaling data
scaler = MinMaxScaler()  # Change this to the actual scaler used during training

class TransactionData(BaseModel):
    data: dict

@app.post("/predict_logistic")
def predict_logistic(transaction: TransactionData):
    input_data = pd.DataFrame([transaction.data])
    input_data = scaler.transform(input_data)
    prediction = logistic_regression.predict(input_data)
    return {"prediction": int(prediction[0])}

@app.post("/predict_neural_network")
def predict_neural_network(transaction: TransactionData):
    input_data = pd.DataFrame([transaction.data])
    input_data = scaler.transform(input_data)
    prediction = neural_network_model.predict(input_data)
    return {"prediction": float(prediction[0][0])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
