import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline




def main():
    data = pd.read_csv(sys.argv[1])
    print(data)


if __name__ == '__main__':
    main()