import joblib
from helper import fillVariables

class Predictor:
    def __init__(self, file_path, alias, min_size):
        self.model = joblib.load(file_path)
        self.alias = alias
        self.min_size = min_size

    def predict(self, variables):
        filledVars = fillVariables(variables, self.min_size)
        result = self.model.predict([filledVars])
        print("result", result)
        return float(result[0][0])

class PredictionService:
    def __init__(self):
        self.predictors = []
        self.predictors.append(Predictor('diabetes/model.joblib', 'diabetes', 8))
        self.predictors.append(Predictor('heart_attack/model.joblib', 'heart-attack', 13))
        self.predictors.append(Predictor('stroke/model.joblib', 'stroke', 21))

    def predict_diseases(self, variables):
        results = {}
        for predictor in self.predictors:
            results[predictor.alias] = predictor.predict(variables)
        return results