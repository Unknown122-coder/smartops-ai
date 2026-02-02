from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, root_mean_squared_error
import numpy as np
from sklearn.linear_model import LogisticRegression


def train_and_predict(df, model_choice="random_forest"):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    #Auto-detect problem type
    if y.nunique() <= 10:
        if model_choice == "logistic":
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            accuracy = accuracy_score(y_test, preds)

            result = {
                "type": "Classification",
                "model": "Logistic Regression",
                "accuracy": round(accuracy, 3),
                "feature_importance": {col: 0 for col in X.columns}
            }

        else:
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            accuracy = accuracy_score(y_test, preds)

            result = {
                "type": "Classification",
                "model": "Random Forest",
                "accuracy": round(accuracy, 3),
                "feature_importance": dict(zip(X.columns, model.feature_importances_))
            }

    # ---------------- REGRESSION ----------------
    else:
        if model_choice == "linear":
            model = LinearRegression()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            rmse = mean_squared_error(y_test, preds, squared=False)

            result = {
                "type": "Regression",
                "model": "Linear Regression",
                "rmse": round(rmse, 3),
                "feature_importance": {col: 0 for col in X.columns}
            }

        else:
            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            rmse = mean_squared_error(y_test, preds, squared=False)

            result = {
                "type": "Regression",
                "model": "Random Forest",
                "rmse": round(rmse, 3),
                "feature_importance": dict(zip(X.columns, model.feature_importances_))
            }

    # 🔹 Add AI business insight
    result["insight"] = generate_insights(result)

    return result
        
def generate_insights(result):
    if result["type"] == "classification":
        acc = result["accuracy"]
        if acc >= 0.85:
            return "The model performance is strong and suitable for automated decision-making."
        elif acc >= 0.70:
            return "The model performance is acceptable but could improve with more data."
        else:
            return "Model performance is weak. Feature engineering or a different model is recommended."

    elif result["type"] == "regression":
        rmse = result["rmse"]
        if rmse <= 5:
            return "Predictions are highly reliable for forecasting and planning."
        elif rmse <= 15:
            return "Predictions are moderately reliable and should be validated before decisions."
        else:
            return "Prediction error is high. Results should be used cautiously."

