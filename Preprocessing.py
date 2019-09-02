#################################################################
##  Script Info:
##  Author: Shirish Pandagare
##  Date : 05/27/2019
#################################################################


import os
import pandas
import numpy
from nltk.tokenize import word_tokenize

class DataWrangling:
    def __init__(self, folder_name= None):
        self.folder = folder_name
        self.filename_list = []
        self.column_list = ['TTFF', 'SNR1', 'SNR2', 'SNR3', 'SNR4', 'SNR5', 'SNR6', 'SNR7', 'SNR8']

    ## Create a list of all the files in the folder.
    def file_name(self, folder):
        """This function creates the list of file names present in a target folder.
        Args:
            folder(str): Name of the target folder.

        Returns:
            List(str): List with all the names.
        """
        path = os.getcwd() + "/" + folder
        for root, dirs, files in os.walk(path):
            for filename in files:
                self.filename_list.append(filename)
        self.filename_list.remove('.DS_Store')
        return self.filename_list

    def read_file(self, file):
        """Functions read the file as text and return the tokens
        Args:
            file(str): File name
        Returns:
            List: List of all the word tokens in the file
        """
        try:
            text = open(file)
            tokens = word_tokenize(text.read())
            return tokens
        except:
            return []


    def search_value(self, token, key):
        try:
            index = token.index(key)
        except:
            index = None

        if index == None:
            value = numpy.nan
        else:
            value = token[index+2]
        return float(value)


    def features(self, token):
        """Function for Date and time feature"""
        if token == []:
            pass
        else:
            dict_tokens = {}

            dict_tokens['Date'] = token[0]
            dict_tokens['Time'] = token[1]
            dict_tokens['File'] = token[5]

            for key in self.column_list:
                dict_tokens[key] = self.search_value(token, key)

            return pandas.DataFrame(dict_tokens, index= [0])

    def data_frame(self):
        name_list = self.file_name(folder="GPSTestData")
        dataframe = pandas.DataFrame({'Date':[],
                                      'Time':[],
                                      'File':[],
                                      'TTFF':[],
                                      'SNR1':[],
                                      'SNR2':[],
                                      'SNR3':[],
                                      'SNR4':[],
                                      'SNR5':[],
                                      'SNR6':[],
                                      'SNR7':[],
                                      'SNR8':[]})
        # column = ['Date', 'Time', 'File', 'TTFF','SNR1', 'SNR2', 'SNR3', 'SNR4', 'SNR5', 'SNR6', 'SNR7', 'SNR8' ]
        # dataframe.columns = column
        for files in name_list:
            text = self.read_file("data/" + files)
            dic = self.features(text)
            dataframe = dataframe.append(pandas.DataFrame(dic))

        return dataframe.to_csv("final_data.csv", index= False)



def main():
    DW = DataWrangling()
    DW.data_frame()


if __name__ == "__main__":
    main()