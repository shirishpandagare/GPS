#################################################################
##  Script Info:
##  Author: Shirish Pandagare
##  Date : 05/28/2019
#################################################################

""""""

import pandas 

def read_file(path):
    df = pandas.read_csv(path)
    return df



if __name__ == "__main__":
    df = read_file('final_data.csv')
    print(df.head(10))
    print(df[["TTFF"]].describe())
    print(df.isnull().sum())
