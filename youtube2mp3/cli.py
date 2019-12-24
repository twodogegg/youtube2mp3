from __future__ import unicode_literals

import youtube_dl
import os
import platform
import tempfile
import sys
import shutil
from mutagen.easyid3 import EasyID3


# from youtube2mp3.options import options


class Youtube2mp3:

    def __init__(self):
        tempdir = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()
        os.chdir(tempdir)

    def run(self):
        ydl_opts = {'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'proxy': 'socks5://127.0.0.1:1086',
                    # 'outtmpl': '%(title)s-%(id)s.%(ext)s',
                    'outtmpl': '%(id)s.%(ext)s',
                    # 'writethumbnail': 'true', // 专辑封面
                    # 'writeinfojson': 'true', 歌曲信息
                    # 'writesubtitles': 'true', // 字幕
                    # 'writedescription': 'true' 详情
                    }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                url = 'https://www.youtube.com/playlist?list=PLECJpeeyOivVJFABa1XNHerLTLrgHCmAn'
                # url = "https://www.youtube.com/watch?v=yarMN6qFaKo"

                results = ydl.extract_info(url=url)
                if 'entries' in results.keys():
                    for res in results['entries']:
                        self._set_id3(res)
                else:
                    self._set_id3(results)

                pass

            except (youtube_dl.utils.DownloadError, youtube_dl.utils.ContentTooShortError,
                    youtube_dl.utils.ExtractorError) as e:
                # print(e.message)
                sys.exit(1)

    @staticmethod
    def _set_id3(res):
        file = EasyID3(res['id'] + '.mp3')

        if res['artist']:
            file['title'] = res['artist']
        else:
            file['artist'] = res['uploader']

        if res['alt_title']:
            title = res['alt_title']
        else:
            title = res['title']

        file['title'] = title

        if res['album']:
            file['album'] = res['album']

        file.save()
        try:
            if os.path.exists(os.path.join('/Users/twodogegg/Music/Music', title + '.mp3')):
                print(title + "已经存在")
            else:
                shutil.move(res['id'] + '.mp3', os.path.join('/Users/twodogegg/Music/Music', title + '.mp3'))
        except Exception:
            print("文件格式异常")


def main():
    y2mp3 = Youtube2mp3()
    y2mp3.run()


if __name__ == '__main__':
    main()
