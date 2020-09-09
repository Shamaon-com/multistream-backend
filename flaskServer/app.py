import json
import boto3
import os
from flask import Flask
from flask import request

app = Flask(__name__)
client = boto3.client("dynamodb", region_name="eu-west-1")
tableName = "dynamo7539873d-dev"

@app.route("/")
def home():
    return 'shamaon streaming server', 200

@app.route("/authenticate", methods=['POST'])
def authenticate():
    
    app.logger.debug(request.values.get('name'))
    streamkey = request.values.get('name')
        
    if not streamkey:
        return "No stream key", 403

    response = client.query(
        TableName=tableName,
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={
            ":pk": {"S": streamkey}
        }
    )

    for item in response["Items"]:
        if item["service"]['S'] == "primary" and item["active"]['BOOL']:
            return "Allowed", 200
    return "Denied", 403