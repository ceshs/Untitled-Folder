from pandas.core.base import DataError
from google_play_scraper import Sort, reviews
import pandas as pd
import pyodbc
from pprint import pprint
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_profiling import ProfileReport

class Review(): #objeto que armazena dados de cada review
    def __init__(self,content,score,thumbsUpCount,reviewsCreatedVersion,at,replyContent,repliedAt):
        self.content = content
        self.score = score
        self.thumbsUpCount = thumbsUpCount
        self.reviewsCreatedVersion = reviewsCreatedVersion
        self.at = at
        self.replyContent = replyContent
        self.repliedAt = repliedAt


def criatudo(dataframe, titulo1, titulo2,credentials1):
    dataframe.to_gbq(credentials=credentials1,
                        destination_table='review.'+ titulo1,
                        if_exists='append')
    dataframe.to_csv('C:/Users/cesar/Documents/Untitled Folder/'+ titulo1+'.csv')

    rep = ProfileReport(dataframe, title="Report "+ titulo2)
    rep.to_file('C:/Users/cesar/Documents/Untitled Folder/report_'+titulo1+'.html')





