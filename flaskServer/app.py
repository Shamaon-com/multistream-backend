import json
import boto3
import os
from flask import Flask
from flask import request, redirect
import socket
from ItsAGramLive import ItsAGramLive

app = Flask(__name__)
client = boto3.client("dynamodb", region_name="eu-west-1")
tableName = "dynamo7539873d-dev"

"""
    Instagram generation functions
"""

class Instagram:
    def __init__(self, item):
        app.logger.debug(item)
        self.item = item
        self.live = ItsAGramLive(
            username=item['username']['S'],
            password=item['password']['S']
        )
        try:
            self.instagramKey = item['instagramKey']['S']
        except KeyError:
            self.instagramKey = None
        self.live.login()

    def checkCurrent(self):
        """
            Checks if IG streamkey exists and is active aka is stream is active in Instagram
        """

        if self.instagramKey and self.live.send_request("live/{}/info/".format(self.instagramKey.split('?')[0])):
            return True
        return False
      
    def newStream(self):
        if not self.checkCurrent():
            self.live.create_broadcast()
            self.live.start_broadcast()
            app.logger.debug("ID: {broadcast_id}, \nKey: {key}".format(broadcast_id=self.live.broadcast_id, key=self.live.stream_key))
            self.item['instagramKey'] = {'S': self.live.stream_key}
            app.logger.debug(self.live.stream_server)
            app.logger.debug(self.item)
            client.put_item(
                TableName=tableName,
                Item= self.item
            )
            return self.live.stream_key
        return self.item['instagramKey']['S']



"""
    other functions
"""
def getAdress(service):
    adresses = {
        'youtube': 'rtmp://a.rtmp.youtube.com/live2/',
        'facebook': 'rtmp://127.0.0.1:1936/rtmp/',
        'instagram': 'rtmp://127.0.0.1:1937/rtmp/'
    }
    
    if service == 'facebook' or service == 'instagram':
       return adresses[service]
    ip = socket.gethostbyname_ex(adresses[service].split('/')[2])[2][0]
    appName = adresses[service].split('/')[3]
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

    pk = streamkey.split('_')[0]
    response = client.query(
        TableName=tableName,
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={
            ":pk": {"S": pk}
        }
    )

    for item in response["Items"]:
        if item["sk"]['S'] == streamkey:
            return "Allowed", 200
    return "Denied", 403


@app.route("/multistream", methods=['POST'])
def multistream():
    app.logger.debug(request.values.get('name'))
    app.logger.debug(request.values.get('app'))
    streamkey = request.values.get('name')
    appName = request.values.get('app')

    if not streamkey or not appName:
        return "invalid request", 403

    pk = streamkey.split('_')[0]

    response = client.query(
        TableName=tableName,
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={
            ":pk": {"S": pk}
        }
    )

    for item in response["Items"]:
        if item["service"]['S'].lower() == appName and item["active"]['BOOL']:
            if appName == "instagram":
                ig = Instagram(item)
                app.logger.debug(getAdress(item["service"]['S'].lower()) + ig.newStream())
                return redirect(getAdress(item["service"]['S'].lower()) + ig.newStream(), code=302)

            app.logger.debug(getAdress(item["service"]['S'].lower()) + item['sk']['S'])
            return redirect(getAdress(item["service"]['S'].lower()) + item['sk']['S'], code=302)


    return "Denied", 403