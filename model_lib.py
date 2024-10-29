from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def run_on_rfc_model (value_to_predict, dependent_var, columns_to_drop, random_state=0):
  # Load the data
  movie_data_train_path = Path("movie_data_train.csv")
  movie_data_train_df = pd.read_csv(movie_data_train_path)

  movie_data_test_path = Path("movie_data_test.csv")
  movie_data_test_df = pd.read_csv(movie_data_test_path)


  # Drop columns
  movie_data_train_df = movie_data_train_df.drop(columns=columns_to_drop)
  movie_data_test_df = movie_data_test_df.drop(columns=columns_to_drop)

  # Drop rows with missing values
  movie_data_train_df = movie_data_train_df.dropna()
  movie_data_test_df = movie_data_test_df.dropna()

  # Create the features
  X_train = movie_data_train_df.drop(columns=columns_to_drop + [dependent_var])
  X_test = movie_data_test_df.drop(columns=columns_to_drop + [dependent_var])

  # Create the target
  y_train = movie_data_train_df[dependent_var]
  y_test = movie_data_test_df[dependent_var]

  # Create the model
  model = RandomForestClassifier(random_state=random_state)

  # Fit the model
  model.fit(X_train, y_train)

  # Make predictions
  y_pred = model.predict(X_test)

  # Calculate the balanced accuracy score
  balanced_accuracy = balanced_accuracy_score(y_test, y_pred)

  # Print the balanced accuracy score
  print(f"Balanced accuracy score: {balanced_accuracy}")

  # Print the classification report
  print("Classification report:")
  print(classification_report(y_test, y_pred))

  # Print the confusion matrix
  print("Confusion matrix:")
  print(confusion_matrix(y_test, y_pred))

  # Plot the confusion matrix
  cm = confusion_matrix(y_test, y_pred)
  sns.heatmap(cm, annot=True, fmt="d")
  plt.xlabel("Predicted")
  plt.ylabel("Actual")
  plt.show()

  # Create the value to predict
  value_to_predict = pd.DataFrame(value_to_predict).T

  # Make the prediction
  prediction = model.predict(value_to_predict)

  # Print the prediction
  print(f"Prediction: {prediction}")

  return prediction


if __name__ == '__main__':
  print('Hello from main method of second_script.py')

