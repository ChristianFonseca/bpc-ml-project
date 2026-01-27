from fastapi import FastAPI
import uvicorn
import mlflow
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

mlflow.set_tracking_uri("http://ec2-184-73-140-65.compute-1.amazonaws.com:5000")
model = mlflow.pyfunc.load_model('models:/rent_model/Production')


class RentData(BaseModel):
    BHK: int = 2
    Size: int = 1200
    Area_Type: str = 'Super Area'
    City: str = 'Hyderabad'
    Furnishing_Status: str = 'Semi-Furnished'
    Tenant_Preferred: str = 'Bachelors/Family'
    Bathroom: int = 2
    Point_of_Contact: str = 'Contact Owner'

def convert_to_dataframe(data):
    data = dict(data)
    data = pd.DataFrame(data, index=[0])
    data = data.rename(columns={
        'BHK': 'BHK',
        'Size': 'Size',
        'Area_Type': 'Area Type',
        'City': 'City',
        'Furnishing_Status': 'Furnishing Status',
        'Tenant_Preferred': 'Tenant Preferred',
        'Bathroom': 'Bathroom',
        'Point_of_Contact': 'Point of Contact'
    })
    return data

@app.post("/predict")
def predict(data: RentData):
    data = convert_to_dataframe(data)
    prediction = model.predict(data)
    return {"prediction": prediction[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



