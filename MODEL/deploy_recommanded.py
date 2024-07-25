from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import tensorflow as tf

app = FastAPI()

# Load the trained models
ml_model = joblib.load('ml_model.pkl')
dl_model = tf.keras.models.load_model('dl_model.h5')

class UserFeatures(BaseModel):
    features: list

def epsilon_greedy_policy(state, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.choice(len(state))
    else:
        return np.argmax(state)

def recommend_items(user_features):
    state = np.array(user_features).reshape(1, -1)
    rl_action = epsilon_greedy_policy(state)
    ml_prediction = ml_model.predict(state)[0]
    dl_prediction = dl_model.predict(state)[0][0]
    combined_recommendations = (rl_action + ml_prediction + dl_prediction) / 3.0
    return combined_recommendations

@app.post("/recommend")
def get_recommendations(user_features: UserFeatures):
    recommendations = recommend_items(user_features.features)
    return {"recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
