import joblib

class Model:
    def __init__(self, path):
        self.path = path
        self.loaded_model = joblib.load(path)

    def feature_names(self):
        return self.loaded_model.feature_names_in_

    def predict(self, features):
        return self.loaded_model.predict([features])

if __name__ == "__main__":
    model_final = Model(path="../my_random_forest_final.joblib")
    # print(model.feature_names())
    # print(Model.feature_names(model))
    print(model_final.path)