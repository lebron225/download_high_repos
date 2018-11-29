import os
from threading import Thread

from redis import Redis

from config import config
from run import download_path

REDIS_CONFIG = config.REDIS
GITHUB_ACCOUNT = config.GITHUB['account']
GITHUB_PASSWORD = config.GITHUB['password']
MAX_THREAD = config.MAX_THREAD

r = Redis(host=REDIS_CONFIG['host'], db=REDIS_CONFIG['db'], password=REDIS_CONFIG['password'])

class DownloadThread(Thread):
    def __init__(self, thread_id, length):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.length = length

    def run(self):
        while True:
            if r.llen('download_list') == 0:
                break

            pop = r.lpop('download_list')
            if pop is None:
                break

            url = pop.decode()
            split = url.split('/')

            if not os.path.exists(download_path + '/' + split[3]):
                os.makedirs(download_path + '/' + split[3])

            repo_path = download_path + '/%s/%s' % (split[3], split[4])

            flag = 0

            if not os.path.exists(repo_path):
                os.chdir(download_path + '/' + split[3])
                ret = os.system('git clone https://%s:%s@' % (GITHUB_ACCOUNT, GITHUB_PASSWORD) + url.replace('https://', ''))

                if ret != 0:
                    r.rpush('failure_list', url)
                    flag = 1

            if flag == 0:
                r['download_state'] = str(self.length - r.llen('download_list')) + '/' + str(self.length)


length = r.llen('download_list')

for i in range(MAX_THREAD):
    t = DownloadThread(i, length)
    t.start()