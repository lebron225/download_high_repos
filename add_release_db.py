import os
import traceback
import uuid

from redis import Redis

from DownloadTools import MysqlOperation
from DownloadTools import FormatConvert
from config import config

DOWNLOAD_LIST_PATH = './download_list.txt'

REPO_PATH = config.DEFAULT_PATH
DB_CONFIG = config.REPOSITORY_DB
REDIS = config.REDIS
TABLE = DB_CONFIG['table']['C/C++_releases']

PREFIX_LEN = len('https://github.com')
SEP = '|++*X_-_X*++|'

r = Redis(host=REDIS['host'], db=REDIS['db'], password=REDIS['password'])
uuid_list = []
commit_id_list = []
name_list = []
author_list = []
commit_time_list = []
local_addr_list = []

with open(DOWNLOAD_LIST_PATH) as f:

    for line in f.readlines():

        flag = 0

        if os.path.exists(REPO_PATH + line[PREFIX_LEN:-1]):

            if not os.path.exists(REPO_PATH + line[PREFIX_LEN:-1] + '/releases_added'):
                flag = 1

            # if release_updated(): 后续更新
            #    flag = 2

            if flag > 0:
                os.chdir(REPO_PATH + line[PREFIX_LEN:-1])
                tag_name_list = os.popen('git tag -l').readlines()

                for tag_name in tag_name_list:

                    try:
                        tag_msg_output = os.popen('git show %s ' % tag_name[:-1] + '-q --pretty=format:"%H' + SEP + '%an' + SEP + '%ad"')

                        split = tag_msg_output.readlines()[-1].split(SEP)

                        uuid_list.append(uuid.uuid1().__str__())
                        commit_id_list.append(split[0])
                        name_list.append(tag_name)
                        author_list.append(split[1])
                        commit_time = FormatConvert.local_to_utc(split[2])
                        commit_time_list.append(commit_time)
                        local_addr_list.append(line[PREFIX_LEN:-1])
                    except Exception as e:
                        traceback.print_exc()
                        r.rpush('releases_added_failed_list', line[:-1] + '::' + tag_name)
                        flag = -1


                if flag == 1:
                    with open(REPO_PATH + line[PREFIX_LEN:-1] + '/releases_added', 'w'):
                        pass
                    # os.mknod('./releases_added')

                elif flag == 2:
                    os.system('rm -f ./releases_updated')

            if flag > 0:

                MysqlOperation.insert_into_mysql(
                    db_config = DB_CONFIG,
                    tablename = TABLE,
                    params = {
                        'uuid': uuid_list,
                        'commit_id': commit_id_list,
                        'name': name_list,
                        'author': author_list,
                        'commit_time': commit_time_list,
                        'local_addr': local_addr_list
                    },
                    mode = 'multiple'
                )
                print('')

        uuid_list.clear()
        commit_id_list.clear()
        name_list.clear()
        author_list.clear()
        commit_time_list.clear()
        local_addr_list.clear()