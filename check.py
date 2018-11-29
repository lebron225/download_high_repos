from redis import Redis

from config import config

REDIS_CONFIG = config.REDIS
r = Redis(host=REDIS_CONFIG['host'], db=REDIS_CONFIG['db'], password=REDIS_CONFIG['password'])

if not r.exists('download_state'):
    state = None
else:
    state = r['download_state']

if state is None:
    print('download percent: 0%')
    print('download failed: 0')
else:
    split = state.decode().split('/')
    percent = 100.0 * int(split[0]) / int(split[1])
    print('download percent: %.2f' % percent + '%')
    print('download failed: %s' % r.llen('failure_list'))