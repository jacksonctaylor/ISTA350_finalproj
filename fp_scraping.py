import requests
import pandas as pd
import re
import json



url = "https://figshare.com/articles/dataset/Sample_details_and_ELISA_results_for_590_samples_/13362718?file=25751692"

id = re.search(r'/(\d+)\?file=',url).group(1)


api = "https://api.figshare.com/v2/articles/" + str(id)

r = requests.get(api)
data = r.json()

download_url = data['files'][0]['download_url']

df = pd.read_excel(download_url)

#print(df.head())




