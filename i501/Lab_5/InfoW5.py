# built-in
import requests
import os

from multiprocessing import Pool
from time import sleep

# user-installed
import pandas as pd

from tqdm import tqdm
from numpy.random import uniform
from dotenv import load_dotenv


search_terms = ['The Beatles', 
                    'Missy Elliot', 
                    'Andy Shauf', 
                    'Slowdive', 
                    'Men I Trust']
n = 10
dfs = []
load_dotenv()

# constants
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
NAME_DEMO = __name__


 

def genius(search_term, per_page=15):
    '''
    Collect data from the Genius API by searching for `search_term`.
    
    **Assumes ACCESS_TOKEN is loaded in the environment.**
    '''
    genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                        f"access_token={ACCESS_TOKEN}&per_page={per_page}"
    
    try:
        response = requests.get(genius_search_url)
        #response.raise_for_status()  
        json_data = response.json()
        return json_data['response']['hits']
    except requests.exceptions.RequestException as e:
        print(f"Error for search term '{search_term}': {e}")
        return []

def genius_to_df(search_term, n_results_per_term=10):
    json_data = genius(search_term, per_page=n_results_per_term)
    
    if not json_data:
        return pd.DataFrame()  
    
    hits = [hit['result'] for hit in json_data]
    df = pd.DataFrame(hits)

    # expand dictionary elements
    df_stats = df['stats'].apply(pd.Series)
    df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                    inplace=True)
    
    df_primary = df['primary_artist'].apply(pd.Series)
    df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns},
                      inplace=True)
    
    df = pd.concat((df, df_stats, df_primary), axis=1)
    
    return df

def process_search_term(search_terms):
    
    for search_term in tqdm(search_terms):
        df = genius_to_df(search_term, n_results_per_term=n)
        dfs.append(df)
    df_genius = pd.concat(dfs)
    df_genius.to_csv(f"/Users/ramyaamudapakula/Desktop/Sem1/Intro to Informatics/Projects/I501 labs and pair problems/lab_5/genius_data.csv", index=False)

process_search_term(search_terms)


