#encoding: utf-8
import channels,json
import getpass
import httplib,urllib
import gobject, glib
import gst,pygst, select, sys
import thread, gobject, glib
types={'NEW':'n', 'BYE':'b', 'END':'e', 'LAST':'p', 'SKIP':'s', 'RATE':'r',
'UNRATE':'u'}
class FM:

    def __init__(self):
        self.channel_id = 0
        self.has_login = False
        self.song_list = {}
        self.channels = None
        self.lyric = None
        self.loginadd='www.douban.com'
        self.songadd = 'www.douban.com'
        self.loginarg={'app_name':'radio_desktop_win', 'version':100,
                                'email':'', 'password':''}
        self.songarg = {'app_name':'radio_desktop_win', 'version':100}
        self.playing = False
        self.player = gst.element_factory_make('playbin', 'player')
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.playing = False
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.playing = False

    def login(self):
            loginarg['email'] = raw_input("input email adress: ")
            loginarg['passwd'] = getpass.getpass("input passwd: ")
            connection = httplib.HTTPConnection(self.loginadd)
            params = urllib.urlencode(self.loginarg)
            connection.request('POST', '/j/app/radio/login?'+params)
            data = json.loads(connection.getrespons().read())
            if data['err']!='ok':
                return False
            else:
                self.songarg['user_id']= data['usr_id']
                self.songarg['token'] = data['token']
                self.songarg['expire'] = data['expire']
                self.has_login = True
                return True

    def get_play_list(self, request):
        httpConnection = httplib.HTTPConnection(self.songadd)
        self.songarg['type']=types[request]
        self.songarg['channel'] = self.channel_id
        params = urllib.urlencode(self.songarg)
        httpConnection.request('GET','/j/app/radio/people?'+params)
        song_list = json.loads(httpConnection.getresponse().read())['song']
        return song_list


    def song_handle(self, comm, sid):
        httpConnection = httplib.HTTPConnection(self.songadd)
        self.songarg['type']=types[comm]
        self.songarg['sid'] = sid
        params = urllib.urlencode(self.songarg)
        httpConnection.request('GET','/j/app/radio/people?'+params)
        results = json.loads(httpConnection.getresponse().read())['song']
        return results

    def del_song(self,sid):
        song_list = song_handle('BYE',sid)
        self.song_list = song_list

    def next_song(self,sid):
        print 'next song'

    def rate_song(self, sid):
        self.song_handle('RATE', sid)

    def unrate_song(self, sid):
        self.song_handle('UNRATE', sid)

    def channel_choise(self):
        self.channels = channels.Channel()
        self.channels.get_channels()
        self.channels.display_channels()
        self.channel_id = raw_input("input id of channels: ")
        if self.channel_id == 0:
            result = self.login()
            while not result:
                chose = raw_input('''error login, enter r to try again or
                                    g to give up''')
                if chose == 'g':
                    result = 1
                elif chose == 'r':
                    result = self.login()
        self.song_list = self.get_play_list('NEW')
    def wait_input(self, song):
        read, _, _ = select.select([sys.stdin],[],[],1)
        if read:
            command = sys.stdin.readline()
            if command[0] == 'r' and self.has_login:
                self.rate_song(sid)
                return 'rate'
            elif command[0] == 'n':
                return 'next'
            if command[0] == 'd' and self.has_login:
                self.del_song(sid)
                return 'delete'
            if command[0] == 'u' and self.has_login:
                self.unrate_song(sid)
            if command[0] == 'c':
                return 'change'

    def play(self):
        while 1:
            self.channel_choise()
            result = ''
            for song in self.song_list:
                song_url=song['url']
                print u'正在播放 '+song['title']+u' 歌手  '+song['artist']
                self.playing = True
                self.player.set_property('uri',song_url)
                self.player.set_state(gst.STATE_PLAYING)
                self.lyric = channels.Lyric()
                self.lyric.get_lyric(song['title'], song['artist'])
                while self.playing:
                    result = self.wait_input(song)
                    if result == 'delete' or result == 'next':
                        self.player.set_state(gst.STATE_NULL)
                        self.playing = False
                        break
                    elif result == 'rate':
                        print 'rate success'
                    elif result == 'unrate':
                        print 'unrate success'
                    elif result == 'change':
                        break
                loop.quit()
                if result == 'change':
                    break
                loop.quit()
while 1:
    doubanfm = FM()
    thread.start_new_thread(doubanfm.play, ())
    gobject.threads_init()
    loop = glib.MainLoop()
    loop.run()

