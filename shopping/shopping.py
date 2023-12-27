import csv
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename) -> tuple:
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    data = ([],[])
    
    col_names = pd.read_csv(filename).columns.tolist()
    month_mapping = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
    visitor_type_mapping = {'Returning_Visitor': 1, 'New_Visitor': 0, 'Other':0}
    weekend_mapping = {'TRUE': 1, 'FALSE': 0}

    with open(filename,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            evidence_list = [
                int(row[col_names[0]]),
                float(row[col_names[1]]),
                int(row[col_names[2]]),
                float(row[col_names[3]]),
                int(row[col_names[4]]),
                float(row[col_names[5]]),
                float(row[col_names[6]]),
                float(row[col_names[7]]),
                float(row[col_names[8]]),
                float(row[col_names[9]]),
                month_mapping[row[col_names[10]]],
                int(row[col_names[11]]),
                int(row[col_names[12]]),
                int(row[col_names[13]]),
                int(row[col_names[14]]),
                visitor_type_mapping[row[col_names[15]]],
                weekend_mapping[row[col_names[16]]],
            ]

            labelValue = row[col_names[17]] == "TRUE"

            data[0].append(evidence_list)
            data[1].append(labelValue)

    return data

def train_model(evidence:list, labels:list):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels:list, predictions:list) -> tuple:
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    print(predictions)
    #Label is either 1 or 0 so sum adds up to num_total_positives
    total_true_positives = sum(labels) 
    total_true_negatives = len(labels) - total_true_positives

    num_positives_correctly_identified = 0
    num_negatives_correctly_identified = 0
    for trueLabel, predictedLabel in zip(labels,predictions):
        
        if trueLabel == predictedLabel and predictedLabel == 1:
            num_negatives_correctly_identified += 1
        elif trueLabel == predictedLabel and predictedLabel == 0:
            num_negatives_correctly_identified += 1

    sensitivity = num_positives_correctly_identified/total_true_positives
    specificity = num_negatives_correctly_identified/total_true_negatives

    return (sensitivity,specificity)


if __name__ == "__main__":
    main()
