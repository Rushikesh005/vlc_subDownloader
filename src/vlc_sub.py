import subprocess
import time
import os
import hashlib
import sys
try:
	import urllib.request, urllib.parse
	pyVer = 3
except ImportError:
	import urllib2
	pyVer = 2
def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def sub_downloader(path):
    k = path
    print(path)
    time.sleep(10)

    hash = get_hash(path)
    replace = [".avi",".mp4",".mkv",".mpg",".mpeg"]
    for content in replace:
        path = path.replace(content,"")
    if not os.path.exists(path+".srt"):

        headers = { 'User-Agent' : 'github' }
        url = "http://api.thesubdb.com/?action=download&hash="+hash+"&language=en"
        try:
            if pyVer == 3:
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req).read()
            else:
                req = urllib2.Request(url, '', headers)
                response = urllib2.urlopen(req).read()
            with open (path+".srt","wb") as subtitle:
                subtitle.write(response)
#            print path
#            subprocess.Popen('vlc.exe %s'%k)
            return True
        except:
            return False


path = sys.argv[1]
sub_downloader(path)
