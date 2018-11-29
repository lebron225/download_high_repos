import requests
from redis import Redis
from config import config

HEADER = {'Authorization':'token ' + config.GITHUB['token']}

language = 'C'
query = 'stars:>=1000+language:%s' % language
order = 'asc'
sort_by = 'stars'
page = 1

REDIS_HOST = config.REDIS['host']
REDIS_DB = config.REDIS['db']
REDIS_PASSWORD = config.REDIS['password']

r = Redis(host=REDIS_HOST, db=REDIS_DB, password=REDIS_PASSWORD)

while True:

    with open('./download_list', 'a') as f:

        url = 'https://api.github.com/search/repositories?q=%s&sort=%s&order=%s&page=%s&per_page=100' \
              % (query, sort_by, order, page)
        try:
            rep = requests.get(url, headers=HEADER, timeout=30)
            if rep.status_code != 200:
                r.rpush('get_failed_list', url)
                raise Exception

        except Exception as e:
            r.rpush('get_failed_list', url)

        else:
            rep_json = rep.json()
            for item in rep_json['items']:
                f.write(item['html_url'] + '\n')

            if len(rep_json['items']) == 1:
                break

            stars = rep_json['items'][-1]['stargazers_count']

            query = 'stars:>=%s+language:%s' % (stars, language)
