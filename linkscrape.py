import pandas as pd
import os
import sys
from dotenv import load_dotenv
import json
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConfigurationError, OperationFailure


load_dotenv(".\.env")

serps = pd.read_csv("google_scraper\serps.csv") # read from the google search scraper
links = serps["link"].to_list() # get links
scraperapi = os.getenv('SCRAPERAPI_KEY') # so you don't get IP banned lol
userpass = os.getenv('MONGO_ATLAS_PWD') # get user pass for Atlas connection URI
uri = os.getenv('MONGO_URI').replace("<MONGO_ATLAS_PWD>", userpass) # grab URI and put credentials in placeholder

try:
    client = MongoClient(uri)
except ConfigurationError:
    print("Invalid URI host error, ensure your Atlas host name is correct in your connection string.")
    sys.exit(1)

db = client["dow_jones"] # since our info is about the Dow Jones

for link in links: # can take a while with many links, would like to improve efficiency in the future (parallelizing?)
    try:
        employee_data = pd.read_html(f'http://api.scraperapi.com?api_key={scraperapi}&url={link}') # grab table data from link source and throw into dataframe
        counter = 0
        for table in employee_data:
            collection_name = serps.loc[serps["link"] == link]["title"].iloc[0].lower().replace(" ", "_") # format link title into collection name
            if not os.path.isfile(f"./{collection_name}_{counter}.json"): # check if json file exists or not to save some rw time
                collection = db[collection_name]
                table.to_json(f"./{collection_name}_{counter}.json", orient='index', indent=2) # instead of saving as file locally can just store json as string in memory and then feed to MongoDB but makes it annoying for inserting multiple records
            file = open(f"./{collection_name}_{counter}.json")
            docs = [i for i in json.load(file).values()] # for inserting multiple records, has to be in list of dict format
            try:
                insert = collection.insert_many(docs)
            except OperationFailure:
                print("Authentication error, ensure this user has the appropriate permissions.")
                sys.exit(1)
            else:
                inserted_count = len(insert.inserted_ids) # to ensure that records are actually being inserted
                print(f"{inserted_count} documents inserted\n")
    except:
        pass # this is because some of the dfs are too big to be turned into a json format with table.to_json() and will produce an error, not really a solution but works well enough for our purposes
