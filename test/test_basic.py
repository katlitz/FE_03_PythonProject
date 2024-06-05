# -*- coding: utf-8 -*-
# content of test_sample.py
import boto3
from sample.helpers import get_dynamo_resource

# need to install as package before this works pytest tests/

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def test_table_exists():
    session = boto3.Session(
        _access_key_id = config["DEFAULT"]["aws_access_key_id"],
        aws_secret_access_key = config["DEFAULT"]["aws_secret_access_key"]
    )
    tables = get_dynamo_resource(session)
    table_names = [table.name for table in tables]
    assert "doc-example-table-movies" in table_names