from ItsAGramLive import ItsAGramLive
import os
import subprocess


instagramUsername = "testpablo1"
instagramPassword = "9NuLvSpqku4tZU"
fileId = "ids.txt"


def check_current(live):
    ids = open(fileId, 'r')
    strId = str(ids.readline().strip('\n'))
    if not strId == "":
        return live.send_request("live/{}/info/".format(strId))
    return False

def new_stream(live):
    """
        Create new stream key
    """
    live.create_broadcast()
    live.start_broadcast()

    print("ID: {broadcast_id},\nServer: {server}, \nKey: {key}".format(broadcast_id=live.broadcast_id, server=live.stream_server, key=live.stream_key))

    ids = open(fileId, 'w')
    ids.write(str(live.broadcast_id))


if __name__ == "__main__":
    

    live = ItsAGramLive(
        username=instagramUsername,
        password=instagramPassword
    )
    
    live.login()
    
    if not check_current(live):
        new_stream(live)

