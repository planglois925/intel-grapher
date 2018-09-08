# intel_grapher

#Requirements [to be added to a requirements.txt]
Docker [if you want to run neo4j locally and easily]
Requests
py2neo

#Getting started
First install neo4j using docker onto your system


'''docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    neo4j'''
    
Login and it'll force you to change the password. For testing and dev purposes we just choose 'password' since it will at this time only run locally

To test data ingestion, run the tester.py file and it should consume some of the data

#NEXT STEPS

Create the API end-points based on the nodes and relationships
Develop some basic API queries that can be used
Add additional plugins

#Plugin Design
To help facilitate the creation of different plugins, here are the recommended structured and elements for each plugin:
Plugins need to provide a means to collecting data, transforming it and querying it.

