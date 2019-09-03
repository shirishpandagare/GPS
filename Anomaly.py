#################################################################
##  Script Info:
##  Author: Shirish Pandagare
##  Date : 05/28/2019
#################################################################



import pandas
from nltk import word_tokenize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
import colorlover as cl

class Anomaly():

    def __init__(self, path, defected_list):
        self.path = path
        self.defected = defected_list
        self.data = None
        self.transformed_data = None

    @property
    def read_file(self):
        """This function creates a pandas data frame of the consolidated csv file."""
        self.data  = pandas.read_csv(self.path)
        return self.data

    def preprocessing(self):
        """This function creates a health status column with 2 classes.
        Good: - If the product is not bad. (Product not tested during quality check)
        Bad: - Product which were found defected in the quality check.

        Args:
            None

        Returns:
            DataFrame: Updated dataframe with an extra column of health status.
        """
        self.data["Health_Status"] = ['Good']*self.data.shape[0]
        defected = word_tokenize(self.defected)
        for gateway in defected:
            self.data.loc[self.data['File'] == gateway, "Health_Status"] = "Bad"
        return self.data

    def imputation(self, method):
        """
        Args:
            method(str): Method of imputation ('Mean', 'Mode', 'Median')
        Returns:
            DataFrame: Updated dataframe with imputed values.
        """

        if method == 'mean':
            values = self.data.mean()
            self.data = self.data.fillna( value=values )
        elif method == 'mode':
            values = self.data.mode(numeric_only=True).iloc[0]
            self.data = self.data.fillna( value=values )
        elif method == 'median':
            values = self.data.median()
            self.data = self.data.fillna( value=values )
        else:
            print("""Please enter the correct method: "Mean" , 'Mode' or "Median". """)

        return self.data

    def principal_component(self , n):
        """
        Args:
            n (int): Total number of significant principal components
        Returns:
            DataFrame: transformed values of the original data.
        """

        X = self.data._get_numeric_data()
        pca = PCA( n_components= n)
        pca.fit(X)
        self.transformed_data = pandas.DataFrame( pca.transform( X ) )
        self.transformed_data.columns = ["PC"+ str(num) for num in range(1,n+1)]
        self.transformed_data = pandas.concat( [self.transformed_data, self.data[["Health_Status"]]], axis=1 )
        return self.transformed_data

    def Kmean(self, cluster):
        """
        Args:
            cluster(int): Total number of clusters.
        Returns:
            DataFrame: transformed values of the original data.
        """
        X = self.transformed_data._get_numeric_data()
        kmeans = KMeans( n_clusters= cluster, random_state=0 ).fit( X )
        self.data["Cluster"] = kmeans.labels_
        self.transformed_data["Cluster"] = kmeans.labels_
        return self.data , self.transformed_data

    def convert(self, x):
        """
        Function used in the plot function
        :param x: Integer either 0, 1 or 2.
        :return: String associated with each number.
        """
        if x == 0:
            return "Cluster_1"
        elif x == 1:
            return "Cluster_2"
        elif x == 2:
            return "Defective"

    def plot(self):
        """
        Function plots the scatter plot.
        :return: save the plot as "Scatter_plot.png"
        """

        df = self.transformed_data

        # Cluster Columns Update
        df.loc[df['Health_Status'] == 'Bad', "Cluster"] = [2] * df.Health_Status.value_counts()['Bad']
        df["Cluster"] = df[["Cluster"]].applymap( lambda x: self.convert(x) )

        # Size Column
        df["Size"] = [10]*df.shape[0]
        # Symbol Column
        df["Symbol"] = ['Circle'] * df.shape[0]
        df.loc[df["Cluster"] == "Defective", "Symbol"] = ["Square"] * df.Cluster.value_counts()["Defective"]

        fig = px.scatter( df, x='PC1', y='PC2', color="Cluster", symbol="Symbol", size="Size",
                          color_discrete_map={"Cluster_1": 'darkturquoise',
                                              "Cluster_2": "sandybrown",
                                              "Defective": "forestgreen", },
                          title="Principal Component Clusters" )
        size = [20, 20]
        return fig.show()



if __name__ == "__main__":
    l = """GN6U-8EF-FZ9 GPZ2-4A8-M7D GSYM-W78-JX8 G8FF-3AH-VYX GRV2-47G-N3B GBZT-SPM-42E GK2U-998-B72 GRVJ-YHK-92D
    G8Y3-TJ8-SA8 GG42-C6K-82K G2G9-WKX-4AD GVSH-4VS-KRM GHVT-NK3-JFZ GJR7-UNB-RAB GEFH-Z25-ZWX"""
    ano = Anomaly("final_data.csv", defected_list= l)
    df = ano.read_file
    df = ano.preprocessing()
    df = ano.imputation(method= "mean")
    df = ano.principal_component(n = 5)
    df, df_trans = ano.Kmean(2)
    ano.plot()
