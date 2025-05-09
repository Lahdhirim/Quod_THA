from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import xgboost as xgb
from colorama import Fore, Style
from src.utils.training_config_loader import ModelsConfig
import pandas as pd
from typing import Dict
from sklearn.base import RegressorMixin
import numpy as np

class MLModels:
    """
    A class for managing and training multiple machine learning models.

    This class initializes and trains several regression models (KNeighborsRegressor, ElasticNet, 
    RandomForestRegressor, XGBoost) based on the provided configuration. It handles training, 
    prediction, and ensures non-negative outputs for predictions.

    Methods:
        train(X_train, y_train, X_val, y_val): Trains the models on the provided training and validation data.
        predict(X_test, predictions): Makes predictions on the test data and ensures non-negative values.
    """
    def __init__(self, config: ModelsConfig):
        self.models = {}
        for model_name, model_config in config.items():
            if model_config.enabled:
                if model_name == "KNeighborsRegressor":
                    params = {k: v for k, v in model_config.dict().items() if k != "enabled" and v is not None}
                    self.models["KNeighborsRegressor"] = KNeighborsRegressor(**params)
                elif model_name == "ElasticNet":
                    params = {k: v for k, v in model_config.dict().items() if k != "enabled" and v is not None}
                    self.models["ElasticNet"] = ElasticNet(**params)
                elif model_name == "RandomForest":
                    params = {k: v for k, v in model_config.dict().items() if k != "enabled" and v is not None}
                    self.models["RandomForest"] = RandomForestRegressor(**params)
                elif model_name == "XGBoost":
                    params = {k: v for k, v in model_config.dict().items() if k != "enabled" and v is not None}
                    self.models["XGBoost"] = xgb.XGBRegressor(**params)

    def train(self, X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series) -> Dict[str, RegressorMixin]:
        for name, model in self.models.items():
            print(f"{Fore.BLUE}Training {name}{Style.RESET_ALL}")
            if isinstance(model, xgb.XGBRegressor):
                model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=50)
            else:
                model.fit(X_train, y_train)
        return self.models
    
    def predict(self, X_test: pd.DataFrame, predictions: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            y_pred = np.maximum(y_pred, 0) 
            predictions[name] = y_pred
        return predictions