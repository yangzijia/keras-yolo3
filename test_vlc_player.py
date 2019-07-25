import sys
import http.client
import time
import os
os.environ['PYTHON_VLC_MODULE_PATH'] = "C:/Program Files/VideoLAN/VLC"
from vlc import VideoMarqueeOption, Position, EventType,Instance
from threading import Thread


class RTSP_Client():
    pass


class VLC_Player():

    def __init__(self, url):
        self.url = url

    def start_with_marquee(self,timeout=60):
        """这种方案是可以带字幕的，根据vlc自带测试源码改写
        """

        movie = self.url
        # Need --sub-source=marq in order to use marquee below
        print(sys.argv[:])
        instance = Instance(["--sub-source=marq"] + sys.argv[1:])
        try:
            media = instance.media_new(movie)
        except (AttributeError, NameError) as e:
            sys.exit(1)
        player = instance.media_player_new()
        player.set_media(media)
        player.play()

        # Some marquee examples.  Marquee requires '--sub-source marq' in the
        # Instance() call above, see <http://www.videolan.org/doc/play-howto/en/ch04.html>
        player.video_set_marquee_int(VideoMarqueeOption.Enable, 1)
        player.video_set_marquee_int(VideoMarqueeOption.Size, 24)  # pixels
        player.video_set_marquee_int(VideoMarqueeOption.Position, Position.Bottom)
        player.video_set_marquee_int(VideoMarqueeOption.Timeout, 0)  # millisec, 0==forever
        player.video_set_marquee_int(VideoMarqueeOption.Refresh, 1000)  # millisec (or sec?)
        ##t = '$L / $D or $P at $T'
        t = '%Y-%m-%d  %H:%M:%S 111'
        player.video_set_marquee_string(VideoMarqueeOption.Text, str_to_bytes(t))

        # Some event manager examples.  Note, the callback can be any Python
        # callable and does not need to be decorated.  Optionally, specify
        # any number of positional and/or keyword arguments to be passed
        # to the callback (in addition to the first one, an Event instance).
        event_manager = player.event_manager()
        event_manager.event_attach(EventType.MediaPlayerEndReached, end_callback)
        event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)
        time.sleep(timeout)

    def start(self,timeout=4):
        """这种是最简方案，用来测试播放足够了
        """

        instance = Instance()
        player = instance.media_player_new()
        Media = instance.media_new(self.url)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        #如果是看直播这里直接写while True 即可
        time.sleep(timeout)


def str_to_bytes(s):
    """Translate string or bytes to bytes.
    """
    if isinstance(s, str):
        return bytes(s, encoding="UTF-8")
    else:
        return s

def end_callback(event):
    print('End of media stream (event %s)' % event.type)
    sys.exit(0)

echo_position = False
def pos_callback(event, player):
    if echo_position:
        sys.stdout.write('\r%s to %.2f%% (%.2f%%)' % (event.type,
                            event.u.new_position * 100,
                            player.get_position() * 100))
        sys.stdout.flush()

class MyThread(Thread):

    def __init__(self, path):
        Thread.__init__(self)
        self.path = path
    
    def run(self):
        while True:

            p1 = VLC_Player(self.path)
            p1.start(4)

if __name__ == "__main__":
    #测试url为浙江卫视直播流
    url1 = "rtsp://user:Ccb123123@56.3.179.111:554/h264/ch1/sub/av_stream"
    url2 = "rtsp://user:Ccb123123@56.3.179.111:554/h264/ch2/sub/av_stream"

    t1 = MyThread(url1)
    t1.setDaemon(True)
    t1.start()

    # t2 = MyThread(url2)
    # t2.setDaemon(True)
    # t2.start()

    time.sleep(1000000)