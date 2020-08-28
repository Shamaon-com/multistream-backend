from ItsAGramLive import ItsAGramLive
import os
import subprocess
import psutil

instagramUsername = "testpablo1"
instagramPassword = "9NuLvSpqku4tZU"
fileId = "ids.txt"


def check_current(live):
    ids = open(fileId, 'r')
    strId = str(ids.readline().strip('\n').split('?')[0])
    if not strId == "":
        var = live.send_request("live/{}/info/".format(strId))
        print(var)
        return var
    return False

def new_stream(live):
    """
        Create new stream key
    """
    live.create_broadcast()
    live.start_broadcast()

    print("ID: {broadcast_id},\nServer: {server}, \nKey: {key}".format(broadcast_id=live.broadcast_id, server=live.stream_server, key=live.stream_key))

    ids = open(fileId, 'w')
    ids.write(str(live.stream_key))

def realy_stream():

    p = psutil.Process(int(open(fileId, 'r').readline().split(' ')[1]))
    if not p.status() == "running":
        #process = "/usr/local/bin/ffmpeg -i rtmp://localhost/live/test -vcodec copy -acodec copy -f flv rtmp://localhost/test/test"
        process = "ffmpeg -i rtmp://54.154.159.81/live/test -vcodec copy -acodec copy -f flv rtmp://54.154.159.81/test/test"
        pro = subprocess.Popen(process, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        ids = open(fileId, 'r').readline().strip('\n')
        open(fileId, 'w').write(ids + ' ' + str(pro.pid))



if __name__ == "__main__":
    
    live = ItsAGramLive(
        username=instagramUsername,
        password=instagramPassword
    )
    
    live.login()
    
    if not check_current(live):
        new_stream(live)
    
    realy_stream()
