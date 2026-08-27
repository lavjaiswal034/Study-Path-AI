# Student Performance Prediction ML

Machine-learning component for predicting a student's final examination
performance percentage from engineered academic features.

## Production Model

* Model version: E46\_V1
* Feature-set version: FS\_E46\_V1
* Algorithm: Gradient Boosting Regressor
* Missing-value strategy: Domain-aware imputation with missing indicators
* Removed feature: F010\_PREVIOUS\_SGPA
* Production features: 11
* Target: FINAL\_EXAM\_PERFORMANCE\_PCT
* Prediction output range: 0-100

## Production Features

* F001\_ATTENDANCE\_PCT
* F002\_ASSESSMENT\_AVG\_PCT
* F003\_ASSIGNMENT\_AVG\_PCT
* F004\_ASSIGNMENT\_COMPLETION\_RATE
* F005\_QUIZ\_AVG\_PCT
* F006\_QUIZ\_COMPLETION\_RATE
* F007\_LAB\_AVG\_PCT
* F008\_INTERNAL\_ASSESSMENT\_PCT
* F009\_PREVIOUS\_SEM\_PCT
* F011\_BACKLOG\_COUNT
* F017\_ASSESSMENT\_PARTICIPATION\_RATE

F010\_PREVIOUS\_SGPA is not used by the production E46\_V1 model.

## API

Start the API from the project root:

&#x20;   python -m uvicorn api.main:app --host 0.0.0.0 --port 8001


Health endpoint:

&#x20;   GET /health


Prediction endpoint:

&#x20;   POST /api/v1/predictions/run


Interactive API documentation:

&#x20;   http://127.0.0.1:8001/docs


## Model Artifact

Production model:

&#x20;   models/student\_performance\_e46.joblib


Metadata:

&#x20;   models/student\_performance\_e46\_metadata.json


The production model is loaded by PredictionService. The backend should
communicate with the ML component through the API rather than loading the
model artifact directly.

## Installation

Create a Python virtual environment and install the pinned dependencies:

&#x20;   python -m venv .venv
    .venv\\Scripts\\activate
    python -m pip install -r requirements.txt


## Testing

Run the complete test suite:

&#x20;   python -m pytest -q


The validated project currently passes:

&#x20;   26 passed


A pandas FutureWarning may be displayed during the missing-value API test.
It is currently non-blocking.

## Architecture

&#x20;   Backend
        |
        | POST /api/v1/predictions/run
        v
    ML Prediction API
        |
        v
    PredictionService
        |
        v
    E46\_V1 Production Model


The ML component is responsible for numerical academic performance prediction.
Authentication, authorization, database access, frontend logic, and
natural-language/LLM functionality remain outside the ML model.

## Prediction Output

The prediction response includes:

* predicted\_percentage
* predicted\_marks
* final\_exam\_max\_marks
* model\_version
* feature\_set\_version
* prediction\_timestamp
* data\_status
* verified\_data\_used

Grade category, risk level, and confidence/uncertainty are not currently
implemented as model outputs.

## Handoff Notes

Do not include the local Python virtual environment (.venv),
**pycache** directories, or .pytest\_cache in the handoff package.

