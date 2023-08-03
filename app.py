# 1. Library imports
import uvicorn
import pymysql
from TableStructure import bddinputs
#from typing import List
from urllib.parse import urlparse
import os
from fastapi import FastAPI
from model import IrisModel, IrisSpecies

# 2. Create app and model objects
app = FastAPI()
model = IrisModel()


def connect():
    # Récupérer l'URL de la base de données à partir des variables d'environnement
    database_url = os.getenv("DATABASE_URL")

    # Extraire les composants de l'URL de la base de données
    url_components = urlparse(database_url)
    db_host = url_components.hostname
    db_user = url_components.username
    db_password = url_components.password
    db_name = url_components.path.strip('/')

    # Configurer la connexion à la base de données MySQL
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn


# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
@app.post('/predict')
def predict_species(iris: IrisSpecies):
    data = iris.dict()
    prediction, probability = model.predict_species(
        data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }


 #----------------------------------------------API BDD POST-----------------------------------------------------
@app.post("/add")
async def create_item(item: bddinputs):
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        query = "INSERT INTO streamlit (input, prediction, probabilité) " \
                 "VALUES (%s, %s, %s)"
        values = (item.input, item.prediction, item.probabilité)
        cursor.execute(query, values)
        conn.commit()

    return {"message": "Item created successfully"}


@app.post("/del")
async def delete_item():
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        query = "DELETE * FROM streamlit"
        cursor.execute(query)
        conn.commit()

    return {"message": "Items deleted successfully"}


# 4. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    # test
    uvicorn.run(app, host='127.0.0.1', port=8000)
