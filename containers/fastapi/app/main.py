from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import pandas as pd
#import pickle
import joblib

model = joblib.load("/opt/static/model_rf.joblib")

class Input(BaseModel):
    age: int
    no_of_pregnancy: int
    gestation_in_previous_pregnancy: int
    bmi: float
    hdl: float
    family_history: int
    unexplained_prenetal_loss: int
    large_child_or_birth_default: int
    pcos: int
    sys_bp: float
    dia_bp: int
    ogtt: float
    hemoglobin: float
    sedentary_lifestyle: int
    prediabetes: int

app = FastAPI()
 
# for root endpoint
@app.get('/')
def main():
    return 'This endpoint accepts JSON encoded data in the /predict endpoint'

# /predict endpoint
@app.post("/predict")
async def predict(data: Input):
    response = jsonable_encoder(data)
    for key, value in response.items():
        response[key] = [value]
    prediction = model.predict(pd.DataFrame(response,index=[0]))
    if prediction[0] == 0:
        return "No GDM"
    else:
        return "GDM Predicted!"

