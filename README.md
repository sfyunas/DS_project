# Gestational Diabetes Mellitus (GDM) predictor

## Introduction

Gestational Diabetes Mellitus (GDM) is a diabetic condition, in which a harmone produced by placenta prevents the body from using insulin effectively. Resultantly, the glucose starts accumulating in the blood stream instead of being absorbed by the cells.

Gestational diabetes is for the first time diagnosed during pregnancy (gestation). If left untreated, it can affect the pregnancy and cause problems in baby's health, such as macrosomia (fat baby), premature birth or even still birth.

Gestational diabetes usually goes away after the baby is born, however, in some cases it may continue even after delivery as type II diabetes.

Proper management/treatment of gestational diabetes can significantly reduce risk factors associated with it. Hence, early diagnosis of the GDM can helpful in this regards. 

This GDM predictor is a web-based application that can help in prediction of gestational diabetes. It asks for several key information that corresponds to the risk factors associated with GDM. The input are passed to a machine learning model, which outputs either 'GDM predicted' or 'No GDM'. It uses Random Forest classifier for prediction. The application is dockerized.

## Use case

The web-based application when deployed on cloud can prove to be very helpful especially in the developing countries where majority of the population lives in rural areas and do not have access to proper hospitals. For instance, the web-based application can be used by public health workers in order to timely predict GDM in high risk pregnant females and hence refer them for proper medical care.


## Data

The dataset used for training the model is available on Kaggle and can be accessed here: https://www.kaggle.com/datasets/sumathisanthosh/gestational-diabetes-mellitus-gdm-data-set/code. The dataset is stored in a postgres relational database.

## Services

The project repository has four components:

- A container running Jupyter notebooks with common machine learning libraries (available @ localhost:8888).  The notebook persists in a mounted volume (./volumes/notebooks)
- A container running Postgres in the event a relational database is useful (available @ localhost:5432).  Any transformations will persist between containers in a mounted volume (./volumes/postgres)
- A container running FastAPI to serve predictions from the ML model (available @ localhost:8080)
- A container running Streamlit to access the predictions from the ML model based on user inputs (available at localhost:8501)

## Usage

turn on the application 
```
docker-compose up 
```

turn off the application
```
docker-compose down
```

rebuild the application
```
docker-compose down
```


## Structure

```
|-- containers - code
|   |-- python      # interactive jupyter notebooks
|   |-- fastapi     # deploy pickled model as a REST API 
|   |-- streamlit   # access REST API in a user interface 
|-- volumes         # persistent data
|   |-- notebooks   # jupyter notebooks persisted here
|   |-- postgres    # database files persisted here, not in version control
|   |-- static      # static files that are loaded into postgres or jupyter
```

## Database connectivity

There are several secrets pertaining to the postgres datbasse stored in the .env file at the root of the repository.

```
PGHOST=postgres
PGUSER=local
PGPASSWORD=password
PGPORT=5432
PGDATABASE=postgres
```

You can connect to PostgreSQL on localhost:5432 with a user 'local' and password 'password' with any SQL client.

Inside the dockerized jupyter notebook, you can connect to PostgreSQL with the following URI

```
from sqlalchemy import create_engine 
engine = create_engine('postgresql://local:password@postgres:5432/postgres)
connection = engine.connect()
```

## Package Manager

This template uses conda environments in each container.  Simply modify the environment.yml to add anything you like.

## REST API Endpoint

The model is available as a REST API endpoint on port 8080.  It accepts JSON data that look like 1 row of the dataframe it as trained on. 
```
curl --request POST http://127.0.0.1:8080/predict \
    -H 'Content-Type: application/json' \
    -d '{"age_group": "Under 15 yrs","reported_race_ethnicity": "White, non-Hispanic", "previous_births": "None","tobacco_use_during_pregnancy": "Yes","adequate_prenatal_care": "Inadequate"}'
```

## Streamlit User Interface

![](./resources/streamlit.png)  

A small web application can take features used to drive your model, then return a prediction from the REST API.   

## Known Vulnerabilities
There is literally zero security.  Keep this on localhost.
- There is no password for the postgres database.
- The rest API calls are not encrypted.
- The jupyter notebook runs as root in a container.
- The user interface is exposed without encryption or a password.
