from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

def run_on_rfc_model (value_to_predict, dependent_var, columns_to_drop, random_state=0):

  columns_to_check = ['budget', 'runtime', 'genres_0_name', 'genres_1_name', 'genres_2_name']

  if value_to_predict[0]['budget'] == 0 and value_to_predict[0]['runtime'] == 0 and value_to_predict[0]['genres_0_name'] == '':
    print("Missing data in value_to_predict")
    return

  # Load the data
  movie_data_train_path = Path("../source_data/movie_data_train.csv")
  movie_data_train_df = pd.read_csv(movie_data_train_path)

  movie_data_test_path = Path("../source_data/movie_data_test.csv")
  movie_data_test_df = pd.read_csv(movie_data_test_path)

  # Drop columns
  movie_data_train_df = movie_data_train_df.drop(columns=columns_to_drop)
  movie_data_test_df = movie_data_test_df.drop(columns=columns_to_drop)

  # Drop rows with missing values
  movie_data_train_df = movie_data_train_df.dropna()
  movie_data_test_df = movie_data_test_df.dropna()

  train_bins = pd.qcut(movie_data_train_df[dependent_var], q=3, labels=["Low", "Medium", "High"])
  movie_data_train_df[dependent_var] = train_bins

  test_bins = pd.qcut(movie_data_test_df[dependent_var], q=3, labels=["Low", "Medium", "High"])
  movie_data_test_df[dependent_var] = test_bins

  # Create the features
  X_train = movie_data_train_df.drop(columns=[dependent_var])
  X_test = movie_data_test_df.drop(columns=[dependent_var])

  # Create the target
  y_train = movie_data_train_df[dependent_var]
  y_test = movie_data_test_df[dependent_var]

  genre_columns = X_train.columns[X_train.columns.str.contains("genres")]

  # Create the model
  model = RandomForestClassifier(random_state=random_state)

  #it the model
  model.fit(X_train, y_train)

  # Make predictions
  y_pred = model.predict(X_test)

  # Calculate the balanced accuracy score
  balanced_accuracy = balanced_accuracy_score(y_test, y_pred)

  # Print the balanced accuracy score
  print(f"\r\nBalanced accuracy score: {balanced_accuracy}")

  # Print the classification report
  print("\r\nClassification report:")
  print(classification_report(y_test, y_pred))

  # Plot the confusion matrix
  cm = confusion_matrix(y_test, y_pred)
  sns.heatmap(cm, annot=True, fmt="d")
  plt.xlabel("Predicted")
  plt.ylabel("Actual")
  plt.show()

  feature_importances = model.feature_importances_
  importances_sorted = sorted(zip(feature_importances, X_test), reverse=True)
  print(f'\r\nFeature Importance: \r\n{importances_sorted[:14]}')

  value_to_predict_df = pd.DataFrame(value_to_predict)

  value_to_predict_df = encodeData(value_to_predict_df, ['genres_0_name', 'genres_1_name', 'genres_2_name'])

  prediction_value_genres = value_to_predict_df.columns[value_to_predict_df.columns.str.contains("genres")]

  for genre in genre_columns:
    if genre not in prediction_value_genres:
      value_to_predict_df[genre] = 0

  # Remove columns from value_to_predict_df that start with 'genres' and end with '_name'
  value_to_predict_df = value_to_predict_df.loc[:, ~value_to_predict_df.columns.str.startswith("genres") | ~value_to_predict_df.columns.str.endswith("_name_")]

  # Ensure the column order in value_to_predict_df matches the column order in X_train
  value_to_predict_df = value_to_predict_df[X_train.columns]

  # Make the prediction
  prediction = model.predict(value_to_predict_df)

  # Print the prediction
  print(f"\r\nPrediction: {prediction}")

  return prediction


def encodeData (df, columns_to_encode):
  # Encode the data
  ohe = OneHotEncoder()
  encoded_genres = ohe.fit_transform(df[columns_to_encode]).toarray()
  encoded_genres_df = pd.DataFrame(encoded_genres, columns=ohe.get_feature_names_out(columns_to_encode))

  df_encoded = pd.concat([df.drop(columns=columns_to_encode), encoded_genres_df], axis=1)

  return df_encoded


if __name__ == '__main__':
  dictionary_to_send = [{'budget': 10000000.0, 'runtime': 109, 'genres_0_name': 'Fantasy', 'genres_1_name': '', 'genres_2_name': ''}]

  run_on_rfc_model(dictionary_to_send, 'revenue', ['popularity', 'profit', 'roi', 'vote_average'], 0)
