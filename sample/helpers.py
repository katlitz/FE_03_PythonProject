from pathlib import Path
import boto3
import csv
import os
import configparser

def get_answer():
    """Get an answer."""
    return "42"

def get_path_to_data():
    """Return path to data."""
    return Path('data')

def get_base_dir():
    """Return path to base directory."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return Path(config["DEFAULT"]["base_dir"])

def start_dynamo_session():
    """Starts a dynamoDB session and returns the session resource"""

    config = configparser.ConfigParser()
    config.read("config.ini")
    
    session = boto3.Session(
        aws_access_key_id = config["DEFAULT"]["aws_access_key_id"],
        aws_secret_access_key = config["DEFAULT"]["aws_secret_access_key"]
    )
    
    dynamo_resource = session.resource(
        'dynamodb',
        region_name='eu-west-1'
    )
    return(dynamo_resource)

def save_data(dynameResource, filename):
    """Saves raw data from DynamoTable into .csv"""

    # Scan die gesamte Tabelle
    response = dynameResource.scan()
    file = os.path.join(get_base_dir(),get_path_to_data(), filename)
    # Die Artikel in der Tabelle
    items = response['Items']

    # Wenn die Tabelle paginiert ist, durchlaufen Sie die Seiten
    while 'LastEvaluatedKey' in response:
        response = dynameResource.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    # Schreiben Sie die Daten in eine CSV-Datei
    with open(file, mode='w', newline='') as csv_file:
        if items:
            # Holen Sie sich die Header aus dem ersten Artikel
            headers = items[0].keys()
            
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(items)

    print(f'Daten wurden erfolgreich exportiert.')
    
def save_query_data(input, filename):
    """Saves queried data from DynamoTable into .csv in json format"""

    file = os.path.join(get_base_dir(),get_path_to_data(), filename)
    with open(file, 'w') as f:  
        for key, value in input.items():  
            f.write('%s:%s\n' % (key, value))