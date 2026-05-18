# Importing necessary libraries
import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, FunctionTransformer, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVR
from sklearn.model_selection import RandomizedSearchCV, train_test_split, KFold, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeRegressor
import joblib

class AiSalaryPredictor:

    def __init__(self, data):
        self.df = pd.read_csv(data)
        with open('config.yml', 'r') as f:
            self.config = yaml.safe_load(f)
        self.results = {}
        self.trained_models = {}
        self.X = self.df.drop(["salary_usd"], axis=1)
        self.y = self.df["salary_usd"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=self.config["data"]["test_size"], random_state=self.config["data"]["random_state"])
        self.kf = KFold(n_splits=self.config["Kfold"]["folds"], shuffle=self.config["Kfold"]["shuffle"], random_state=self.config["Kfold"]["random_state"])

    def load_data(self):
        print(self.df.head())

    def model_evaluation(self, y_pred, y_test, model_name):

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        # Store results
        self.results[model_name] = {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        }

        print(f"\n{model_name}")
        print(f"MAE: {mae:.2f}")
        print(f"MSE: {mse:.2f}")
        print(f"RMSE: {rmse:.2f}")
        print(f"R2 Score: {r2:.4f}")

    def fit_model(self, pipe, X_train, y_train, X_test):
        pipe.fit(X_train, y_train)
        return pipe.predict(X_test), pipe

    def tune_model(self, grid, X_train, y_train, X_test):
        grid.fit(X_train, y_train)
        print("\nBest Parameters:", grid.best_params_)
        print("Best CV Score:", grid.best_score_)
        return grid.best_estimator_.predict(X_test), grid.best_estimator_
    
    def compare_models(self):

        print("\nFinal Model Comparison\n")

        for model, metrics in self.results.items():
            print(f"\n{model}")
            print(f"  R2: {metrics['R2']:.4f}")
            print(f"  MAE: {metrics['MAE']:.2f}")
            print(f"  RMSE: {metrics['RMSE']:.2f}")

        # Best model
        best_model = max(self.results, key=lambda x: self.results[x]['R2'])
        print(f'\nBest Model: {best_model}\n')
        return best_model

    def save_model(self):

        best_model_name = self.compare_models()
        print(f'Saving Model: {best_model_name}')

        best_model = self.trained_models[best_model_name]

        joblib.dump(best_model, 'model.pkl')
        print("Model Saved as model.pkl")

    def create_preprocessor(self, model_type="linear"):

        cat_cols = ['country', 'job_role', 'ai_specialization', 'industry', 'work_mode', 'education_required']

        nominal = Pipeline([
            ("onehot", OneHotEncoder(handle_unknown='ignore', sparse_output=True))
        ])

        ordinal1 = Pipeline([
            ("ordinal", OrdinalEncoder(categories=[['Entry', 'Mid', 'Senior', 'Lead']]))
        ])

        ordinal2 = Pipeline([
            ("ordinal", OrdinalEncoder(categories=[['Startup', 'Small', 'Medium', 'Large', 'Enterprise']]))
        ])

        transform = Pipeline([
            ("log", FunctionTransformer(np.log1p))
        ])

        num_cols = [
            'weekly_hours', 'hiring_difficulty_score', 'ai_adoption_score', 'economic_index',
            'offer_acceptance_rate', 'tax_rate_percent', 'skill_demand_score', 'automation_risk',
            'job_security_score', 'career_growth_score', 'work_life_balance_score',
            'promotion_speed', 'salary_percentile', 'employee_satisfaction'
        ]

        transformers = [
            ("onehot", nominal, cat_cols),
            ("ordinal1", ordinal1, ['experience_level']),
            ("ordinal2", ordinal2, ['company_size']),
            ("log", transform, ['bonus_usd'])
        ]

        if model_type == "linear":
            transformers.append(("scaler", StandardScaler(), num_cols))
        else:
            transformers.append(("num", "passthrough", num_cols))

        return ColumnTransformer(transformers)

    def linear_regression(self):

        print("\nLinear Regression")

        preprocessor = self.create_preprocessor("linear")

        pipe = Pipeline([
            ("preprocessing", preprocessor),
            ("model", LinearRegression())
        ])

        y_pred, pipe = self.fit_model(pipe, self.X_train, self.y_train, self.X_test)
        self.trained_models["Linear Regression"] = pipe

        self.model_evaluation(y_pred, self.y_test, "Linear Regression")

    def svm(self):

        print("\nSupport Vector Machine")

        preprocessor = self.create_preprocessor("linear")

        pipe = Pipeline([
            ("preprocessing", preprocessor),
            ("model", LinearSVR())
        ])

        grid = GridSearchCV(pipe, 
            param_grid=self.config["Model"]["svm"], 
            cv=self.kf, 
            scoring=self.config["Grid"]["scoring"], 
            n_jobs=self.config["Grid"]["n_jobs"]
        )

        # Before tuning
        y_pred, pipe = self.fit_model(pipe, self.X_train, self.y_train, self.X_test)
        self.trained_models["SVM (Before Tuning)"] = pipe
        self.model_evaluation(y_pred, self.y_test, "SVM (Before Tuning)")

        # After tuning
        y_pred, tuned_model = self.tune_model(grid, self.X_train, self.y_train, self.X_test)
        self.trained_models["SVM (After Tuning)"] = tuned_model
        self.model_evaluation(y_pred, self.y_test, "SVM (After Tuning)")

    def decision_tree(self):

        print("\nDecision Tree")
        
        preprocessor = self.create_preprocessor("tree")

        pipe = Pipeline([
            ("preprocessing", preprocessor),
            ("model", DecisionTreeRegressor(random_state=42))
        ])

        grid = GridSearchCV(
            pipe, 
            param_grid=self.config["Model"]["decision_tree"], 
            cv=self.kf, 
            scoring=self.config["Grid"]["scoring"], 
            n_jobs=self.config["Grid"]["n_jobs"]
        )

        # Before tuning
        y_pred, pipe = self.fit_model(pipe, self.X_train, self.y_train, self.X_test)
        self.trained_models["Decision Tree (Before Tuning)"] = pipe
        self.model_evaluation(y_pred, self.y_test, "Decision Tree (Before Tuning)")

        # After tuning
        y_pred, tuned_model = self.tune_model(grid, self.X_train, self.y_train, self.X_test)
        self.trained_models["Decision Tree (After Tuning)"] = tuned_model
        self.model_evaluation(y_pred, self.y_test, "Decision Tree (After Tuning)")

    def random_forest(self):

        print("\nRandom Forest")

        preprocessor = self.create_preprocessor("tree")

        pipe = Pipeline([
            ("preprocessing", preprocessor),
            ("model", RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1))
        ])

        grid = RandomizedSearchCV(
            pipe,
            param_distributions=self.config["Model"]["random_forest"],
            cv=self.kf,
            scoring=self.config["Grid"]["scoring"],
            n_jobs=self.config["Grid"]["n_jobs"],
            random_state=self.config["Grid"]["random_state"]
        )

        # Before tuning
        y_pred, pipe = self.fit_model(pipe, self.X_train, self.y_train, self.X_test)
        self.trained_models["Random Forest (Before Tuning)"] = pipe
        self.model_evaluation(y_pred, self.y_test, "Random Forest (Before Tuning)")

        # After tuning
        y_pred, tuned_model = self.tune_model(grid, self.X_train, self.y_train, self.X_test)
        self.trained_models["Random Forest (After Tuning)"] = tuned_model
        self.model_evaluation(y_pred, self.y_test, "Random Forest (After Tuning)")

if __name__ == "__main__":

    predictor = AiSalaryPredictor('Dataset/global_ai_jobs.csv')
    predictor.load_data()

    predictor.linear_regression()
    predictor.svm()
    predictor.decision_tree()
    predictor.random_forest()

    predictor.save_model()