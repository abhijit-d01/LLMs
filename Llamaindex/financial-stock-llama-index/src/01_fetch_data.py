import os
import urllib.request as request

data_url = "https://github.com/abhijit-d01/LLMs/blob/fed1ff649b0841c02ae08b3f55efd2da9709dfcd/Llamaindex/financial-stock-llama-index/articles.zip"

def download_file():

    filename, headers = request.urlretrieve(
        url = data_url,
        filename = "articles.zip"
    )
    

download_file()
os.system("unzip articles.zip")
os.system("rm -rf articles.zip")