import json
import boto3
import os
from flask import Flask
from flask import request, redirect
import socket

app = Flask(__name__)
client = boto3.client("dynamodb", region_name="eu-west-1")
tableName = "dynamo7539873d-dev"


def getAdress(service):
    adresses = {
        'youtube': 'rtmp://a.rtmp.youtube.com/live2/',
        'facebook': 'rtmp://127.0.0.1:1936/rtmp/'
    }
    
    ip = socket.gethostbyname_ex(adresses[service].split('/')[2])[2][0]
    appName = adresses[service].split('/')[3]
    print(ip, appName)
    return 'rtmp://' + ip + '/' + appName + '/'


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

@app.route("/mutltistream", methods=['POST'])
def mutltistream():
    app.logger.debug(request.values.get('name'), request.values.get('app'))
    streamkey = request.values.get('name')
    appName = request.values.get('app')

    if not streamkey or not appName:
        return "invalid request", 403

    response = client.query(
        TableName=tableName,
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={
            ":pk": {"S": streamkey}
        }
    )

    for item in response["Items"]:
        if item["service"]['S'].lower() == appName and item["active"]['BOOL']:
            app.logger.debug(getAdress(item["service"]['S'].lower()) + item['sk']['S'])
            return redirect(getAdress(item["service"]['S'].lower()) + item['sk']['S'], code=302)


    return "Denied", 403