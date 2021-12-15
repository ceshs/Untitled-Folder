from google_play_scraper import Sort, reviews
import pandas as pd
import pyodbc
from pprint import pprint
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_profiling import ProfileReport
from utilities import Review, criatudo

#Conexão com o google cloud
key_path = "GBQ.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes = ["https://www.googleapis.com/auth/cloud-platform"])

client = bigquery.Client('projeto-1-335101',credentials)

#Criando a query.
QUERY = ('SELECT thumbsUpCount,reviewDate,content FROM `projeto-1-335101.review.reviews`')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

#Função web-scraper
result, continuation_token = reviews(  
    'com.amazon.dee.app',
    lang='pt', 
    country='br', 
    sort=Sort.NEWEST, 
    count=200,
    filter_score_with= None
    )

#Função principal
def main():
    qlist = []
    for p in rows:
        qlist.append(Review(p.get('content'),-1,-1,-1,p.get('reviewDate'),-1,-1)) #Cria uma lista a partir do banco de datos para comparação

    review_list = []
    for x in result:
        
        for row in qlist:
            exists = False   
            if  str(x.get('at'))+'+00:00'== str(row.at) and x.get('content') == row.content:    #Compara o que foi puxado na api com o banco de dados
                exists = True
                break 
                
        if exists == False:
            
            review_list.append(Review(x.get('content'),x.get('score'),x.get('thumbsUpCount'),x.get('reviewCreatedVersion'),x.get('at'),x.get('repliedContent'),x.get('repliedAt'))) #Cria a lista com os novos reviews
    
    mt = []
    for object in review_list:
        list=[]
        for variable in vars(object).values():
            list.append(variable)
        mt.append(list)

    df = pd.DataFrame(mt, #cria dataframe
                    columns =['content', 'score','thumbsUpCount','reviewCreatedVersion','reviewDate','repliedContent','repliedAt'])
    df.head()

    #separa tudo que foi puxado pelo score
    df_high = df.loc[(df['score']) > 3]
    df_medium = df.loc[(df['score']) == 3]
    df_low = df.loc[(df['score']) < 3]

    #envia para o banco de dados, cria a planilha e o review
    criatudo(df_high, 'aval_positiva','avaliação positiva', credentials)
    criatudo(df_medium, 'aval_neutra','avaliação neutra', credentials)
    criatudo(df_low, 'aval_negativa','avaliação negativa', credentials)


main()