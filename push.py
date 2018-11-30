#coding:utf-8
import os

import re
import traceback

from redis import Redis
import sys
from DownloadTools import MysqlOperation
from config import config



def is_match(string, pattern):
    ret = re.match(pattern, string)
    if ret is None:
        return False
    else:
        return True


REDIS_CONFIG = config.REDIS
DB_CONFIG = config.REPOSITORY_DB
DEFAULT_PATH = config.DEFAULT_PATH
TABLE = DB_CONFIG['table']['repository_java']


print('\n')
print('----- start -----\n')

r = Redis(host=REDIS_CONFIG['host'], db=REDIS_CONFIG['db'], password=REDIS_CONFIG['password'])
r.delete('download_list')
r.delete('download_state')


try:

    mode = sys.argv[1]

    assert mode == 'mode:default' or mode == 'mode:ff'

    download_path = sys.argv[3]
    assert download_path[:14] == 'download-path:'

    if download_path == 'download-path:default':
        download_path = DEFAULT_PATH
    else:
        download_path = download_path[14:]
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    if mode == 'mode:default':

        star = sys.argv[2]
        assert is_match(star, pattern='star:\d{1,}-\d{1,}')

        split = star[5:].split('-')
        star_min = split[0]
        star_max = split[1]
        assert int(star_max) >= int(star_min) and int(star_min) >= 0

    else:

        file_path = sys.argv[2]
        assert file_path[:10] == 'data-path:'

        file_path = file_path[10:]
        os.path.exists(file_path)

except Exception as e:
    print('Error: illegal command')
    traceback.print_exc()
    exit()

else:

    if mode == 'mode:default':
        where = 'convert(stars,signed) >= %s and repository_id != -1 and convert(stars,signed) <= %s' % (star_min, star_max)
        ret = MysqlOperation.get_data_from_mysql(
            db_config = DB_CONFIG,
            tablename = TABLE,
            fields=['git_addr'],
            where=where
        )
        for item in ret:
            r.rpush('download_list', item[0])

    else:
        with open(sys.argv[2][10:], 'r') as f:
            for item in f.readlines():
                r.rpush('download_list', item[:-1])
