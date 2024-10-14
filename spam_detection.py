import pandas as pd
import numpy as np
import re
import emoji
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score


def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = emoji.demojize(text, delimiters=(" ", " "))
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Load and preprocess the dataset
data = pd.read_csv("Youtube01.csv")
data = data[["CONTENT", "CLASS"]]
data["CLASS"] = data["CLASS"].map({0: "NOT A SPAM COMMENT", 1: "SPAM COMMENT"})
data["CONTENT"] = data["CONTENT"].apply(preprocess_text)

# Split the dataset into features and labels
x = np.array(data["CONTENT"])
y = np.array(data["CLASS"])

# Vectorize the text data
cv = CountVectorizer()
x = cv.fit_transform(x)

# Split the data into training, validation, and test sets
xtrain, x_temp, ytrain, y_temp = train_test_split(x, y, train_size=0.7, random_state=42)
xval, xtest, yval, ytest = train_test_split(
    x_temp, y_temp, test_size=0.5, random_state=42
)

# Initialize the models
model_nb = BernoulliNB()
model_lr = LogisticRegression(max_iter=1000)
model_svc = SVC(probability=True)

# Create the Voting Classifier
voting_clf = VotingClassifier(
    estimators=[("nb", model_nb), ("lr", model_lr), ("svc", model_svc)], voting="soft"
)

# Fit the model on the training data
voting_clf.fit(xtrain, ytrain)

# Predict the labels for the training data
ytrain_pred = voting_clf.predict(xtrain)
# Predict the labels for the validation data
yval_pred = voting_clf.predict(xval)
# Predict the labels for the test data
ytest_pred = voting_clf.predict(xtest)
# Calculate the training accuracy
training_accuracy = accuracy_score(ytrain, ytrain_pred)
print("Training accuracy:", training_accuracy)
# Calculate the validation accuracy
validation_accuracy = accuracy_score(yval, yval_pred)
print("Validation accuracy:", validation_accuracy)

# Calculate the test accuracy
test_accuracy = accuracy_score(ytest, ytest_pred)
print("Test accuracy:", test_accuracy)


def predict_spam_comments(input_csv, output_csv):
    input_data = pd.read_csv(input_csv)
    comments = input_data["Comment"]

    comments = comments.apply(preprocess_text)

    transformed_comments = cv.transform(comments)

    predictions = voting_clf.predict(transformed_comments)

    spam_comments = input_data[predictions == "SPAM COMMENT"]

    spam_comments_csv = spam_comments.to_csv(output_csv, index=False)

    spam_count = len(spam_comments)
    non_spam_count = len(predictions) - spam_count

    return spam_count, non_spam_count, spam_comments
