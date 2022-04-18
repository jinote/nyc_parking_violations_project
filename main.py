from sodapy import Socrata
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys
import os
import json

parser = argparse.ArgumentParser(description='Process data from NYC parking violation.')
parser.add_argument('--page_size', type=int, help='how many rows to get per page', required=True)
parser.add_argument('--num_pages', type=int, help='how many pages to get in total')
args = parser.parse_args(sys.argv[1:])
print(args)

# DATASET_ID="nc67-uf89"
# APP_TOKEN="6WDdLavsOLAHrWpvJUmprgQZg"
# ES_HOST="https://search-cis9760-project1-fpllkqg44daud3mv5kw33jn77m.us-east-1.es.amazonaws.com"
# ES_USERNAME="hojinlee"
# ES_PASSWORD="Hojinlee12**"
# INDEX_NAME ="parking1"

DATASET_ID = os.environ["DATASET_ID"]
APP_TOKEN = os.environ["APP_TOKEN"]
ES_HOST = os.environ["ES_HOST"]
ES_USERNAME = os.environ["ES_USERNAME"]
ES_PASSWORD = os.environ["ES_PASSWORD"]
INDEX_NAME = os.environ["INDEX_NAME"]

if __name__ == '__main__':

    try:
        resp = requests.put(f"{ES_HOST}/{INDEX_NAME}", auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
                            json={
                                "settings": {
                                    "number_of_shards": 1,
                                    "number_of_replicas": 1
                                },
                                "mappings": {
                                    "properties": {
                                        "plate": {"type": "keyword"},
                                        "state": {"type": "keyword"},
                                        "license_type": {"type": "keyword"},
                                        "summons_number": {"type": "keyword"},
                                        "issue_date": {"type": "date", "format": "mm/dd/yyyy"},
                                        "violation_time": {"type": "keyword"},
                                        "violation": {"type": "keyword"},
                                        "fine_amount": {"type": "float"},
                                        "penalty_amount": {"type": "float"},
                                        "interest_amount": {"type": "float"},
                                        "reduction_amount": {"type": "float"},
                                        "payment_amount": {"type": "float"},
                                        "amount_due": {"type": "float"},
                                        "precinct": {"type": "keyword"},
                                        "county": {"type": "keyword"},
                                        "issuing_agency": {"type": "keyword"}                                        
                                    }
                                },
                            }
                            )

        resp.raise_for_status()
        print(resp.json())
    except Exception as e:
        print("Index already exists! Skipping")
    

    for page in range(0, args.num_pages):
        es_rows=[]
        rows = Socrata("data.cityofnewyork.us", APP_TOKEN).get(DATASET_ID, order = "summons_number", limit=args.page_size, offset= page* (args.page_size))


        for row in rows:
            try:
                # Convert
                es_row = {}
                es_row["plate"] = row["plate"]
                es_row["state"] = row["state"]
                es_row["license_type"] = row["license_type"]
                es_row["summons_number"] = row["summons_number"]
                es_row["issue_date"] = row["issue_date"]
                es_row["violation_time"] = row["violation_time"]
                es_row["violation"] = row["violation"]
                es_row["fine_amount"] = float(row["fine_amount"])
                es_row["penalty_amount"] = float(row["penalty_amount"])
                es_row["interest_amount"] = float(row["interest_amount"])
                es_row["reduction_amount"] = float(row["reduction_amount"])
                es_row["payment_amount"] = float(row["payment_amount"])
                es_row["amount_due"] = float(row["amount_due"])
                es_row["precinct"] = row["precinct"]
                es_row["county"] = row["county"]
                es_row["issuing_agency"] = row["issuing_agency"]

            except Exception as e:
                #print(f"Error!: {e}, skipping row: {row}")
                continue

            es_rows.append(es_row)


# bulk api in first loop
        bulk_upload_data = ""
        for line in es_rows:
            print(f'Handling row {line["summons_number"]}')
            action = '{"index": {"_index": "' + INDEX_NAME + '", "_type": "_doc", "_id": "' + line[
                "summons_number"] + '"}}'
            data = json.dumps(line)
            bulk_upload_data += f"{action}\n"
            bulk_upload_data += f"{data}\n"

        try:
            resp = requests.post(f"{ES_HOST}/_bulk",
                                 data=bulk_upload_data, auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
                                 headers={"Content-Type": "application/x-ndjson"})
            resp.raise_for_status()
            print('Done')

        except Exception as e:
            print(f"Failed to insert in ES: {e}, skipping row: {row}")



