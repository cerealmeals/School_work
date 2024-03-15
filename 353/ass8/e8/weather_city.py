import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler




def main():
    data = pd.read_csv(sys.argv[1])
    #print('Unique city\'s', data['city'].nunique())
    oops_data = pd.read_csv(sys.argv[2])
    y = data['city'].values
    data = data.drop(['city'], axis=1).values
    oops_data = oops_data.drop(['city'], axis=1).values


    X_train, X_valid, y_train, y_valid = train_test_split(data, y, random_state=42)
    

    model = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=500, max_depth=20, min_samples_leaf=8)
    )
    model.fit(X_train, y_train)

    print("Score of Random Forrest Classifier on training data:", model.score(X_train, y_train))
    print("Score of Random Forrest Classifier on validation data:", model.score(X_valid, y_valid))


    predictions = model.predict(oops_data)
    print(predictions)

    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)

if __name__ == '__main__':
    main()