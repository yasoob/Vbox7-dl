import urllib
import re
import sys
import subprocess

def give_info(url):
    url = "http://vbox7.com/play:03fbd68d4e"
    _VALID_URL = r'(?:http://)?(?:www\.)?vbox7\.com/play:([^/]+)'
    mobj = re.match(_VALID_URL, url)
    if mobj is None:
        print "[vbox7]  Error: The url is incorrect."
        sys.exit()
    video_id = mobj.group(1)
    print "[vbox7]  Opening the main webpage."
    webpage = urllib.urlopen(url) 
    title = re.search(r'<title>(.*)</title>',webpage.read())
    if title:
        title = (title.group(1)).split('/')[0]
    else:
        print "[vbox7]  Unable to extract title."
    info_url = "http://vbox7.com/play/magare.do"
    data = urllib.urlencode({'as3':'1','vid':video_id})
    print "[vbox7]  Extracting the absolute url of the video."
    try:
        request = urllib.urlopen(info_url,data)
    except:
        print "[vbox7]  Error: Check your internet connection."
        sys.exit()
    final_url = ((request.read()).split('&')[0]).split('=')[1]
    ext = "flv"
    print [{
            'id':       video_id,
            'url':      final_url,
            'ext':      ext,
            'title':    title,
    }]
    cmd = 'wget -O "%s.flv" "%s"' % (title,final_url) 
    process = subprocess.Popen(cmd, shell=True)
    try:
        process.wait() #Wait for wget to finish
    except KeyboardInterrupt: #If we are interrupted by the user
        print "\n[vbox7]  Download cancelled by the user."

if __name__ == '__main__':
    url = sys.argv[-1]#raw_input("What is the url of the video ?  ")
    give_info(url)