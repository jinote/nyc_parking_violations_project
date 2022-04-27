# New York City Parking Violations
### Project Description
In this project, I applied what I have learned about EC2, Terminal, Docker, Elasticsearch and Kibana to a real-world dataset powered by NYC Open Data. This dataset has 14.4 million rows and 16 columns. Each row is an open parking and camera violations issued in New York city. The columns include the summons number, violation time, violation type, penalty amount, and other violation details.

I wrote a python script that runs in docker to consume data from the Socrata Open Data API and then pushes that information into an Elasticsearch cluster provisioned via AWS. After loading all the data into an Elasticsearch instance, I visualized and analyzed the data with Kibana.



### Technology/Framework used
- Docker
- Service: Elasticsearch, Kibana
- sodapy, sys, argparse, json, requests, os

### Usage
**Step1**: Create an Elasticsearch Domain in AWS

**Step2**: Create an APP Token for the NYC Open Data API
Data link: https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89


**Step3**: Python Scripting<br>
Some key arguments that I used:
- APP_TOKEN: This is how a user can pass along an APP_TOKEN for the API in a safe manner.
- bigdataproject1:1.0 This is the name of my docker image. 
- ES_HOST: This is the domain endpoint of my Elasticsearch cluster.
- page_size: It asks for how many records to request from the API per call. 
- num_pages: It continues querying for data num_pages times. 

**Step4**: Visualizing and Analysis on Kibana (OpenSearch Dashboard)

![Alt text](https://github.com/jinote/my-projects/blob/main/BigDataTech/Kibana%20Dashboard.jpg)


**Observation:**
- Parking violations have occured the most in photo school zone speed violation points, for the past 10 years (2012-2021)
- Parking violations mostly occured in the morning. 11:30AM was the time when it occured most.  




