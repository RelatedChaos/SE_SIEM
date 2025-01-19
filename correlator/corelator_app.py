from socket import *
import requests
import time

class corelator:
    def __init__(self):
        
        self.get_configurations()
        self.query = []
        self.get_queries()
        self.get_port() 
        self.run()

    def get_configurations(self):
        headers = {'Content-Type': 'application/json'}
        self.configs = requests.get('http://127.0.0.1:5001/configuration', json={'type': 'correlation'}, headers=headers).json()

    def get_queries(self):
        for item in self.configs:
            if item['config_name'] == 'query':
                self.query.append(item['value'])
    
    def get_port(self):
        for item in self.configs:
            if item['config_name'] == 'correlationServerPort':
                self.port = item['value']

    def query_events(self):
        for query in self.query:
            q_subparts = query.split(';')
            try:
                correlation_key = q_subparts
            except Exception as e:
                correlation_key = ''
            try:
                outcome = q_subparts[2]
            except Exception as e:
                outcome = ''

            print(f'Here we should query {q_subparts[0]} with correlation key {correlation_key} and outcome {outcome}')

    def run(self):
        while True:
            self.query_events()
            time.sleep(1)


cor = corelator()
            

        
