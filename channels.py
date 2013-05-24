# start every time in case that new channels added in to FM
#encoding: utf-8
import httplib, urllib2
import json
from base64 import urlsafe_b64encode as en
from base64 import urlsafe_b64decode as de
#f = open('channels.txt','w')
class Channel:
    def __init__(self):
        self.channels = []
        self.search_list = {}

    def get_channels(self):
        httpConnection = httplib.HTTPConnection('www.douban.com')
        httpConnection.request('GET', '/j/app/radio/channels')
        channels = json.loads(httpConnection.getresponse().read())['channels']
        for channel in channels:
            for key in channel:
                if key == 'name':
                    string = channel[key]
                    channel_name = channel[key]
                if key == 'channel_id':
                    string = str(channel[key])
                    self.search_list[channel[key]] = channel_name

    def display_channels(self):
        self.get_channels()
        i = 0
        for key in self.search_list:
            i = i+1
            print str(key)+':'+self.search_list[key] + '  ',
            if i%2 == 0:
                print '\n'

    def search_channels(self, string):
        for key in search_list:
            if key == string:
                print "id of channel",key, "is", search_list[key]

class Lyric:
    def __init__(self):
        self.address = 'http://geci.me/api/lyric/'
    def get_lyric(self, song, artist):
        song_en = en(song)
        art_en = en(artist)
        response = urllib2.urlopen(self.address+song+'/'+artist)
        result = json.loads(respons.read())['result']
        if result == []:
            print 'No lyric found for this song'
        else:
            lyric = result[0]['lrc']
            req = urllib2.Request(lyric)
            fd = urllib2.urlopen(req)
            data = fd.read()
            print data

