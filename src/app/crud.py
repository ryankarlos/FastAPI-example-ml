from pycaret.classification import *
import pandas as pd
from sqlalchemy.orm import Session
from src.app import models
import uuid
import datetime


def get_training_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_model(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def serialise_model(model):
    random_id = uuid.uuid1()
    run_id = str(str(datetime.datetime.now())) + "-" + str(random_id)
    save_model(model, "credits")


def train(data):
    data_copy = data.copy()
    exp_clf101 = setup(data=data_copy, target="default", session_id=123)
    best = compare_models()
    performance = predict_model(best)
    auc = performance["AUC"]
    accuracy = performance["accuracy"]
    final_best = finalize_model(best)

    return {
        "best_model_params": final_best,
        "performance": {"accuracy": accuracy, "auc": auc},
    }


def predict(**payload):
    data = pd.DataFrame([[carat_weight, cut, color, clarity, polish, symmetry, report]])
    data.columns = [
        "Carat Weight",
        "Cut",
        "Color",
        "Clarity",
        "Polish",
        "Symmetry",
        "Report",
    ]
    model = get_model()
    predictions = predict_model(model, data=data)
    return {"prediction": int(predictions["Label"][0])}
