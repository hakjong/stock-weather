import requests
import pymysql
import hashlib
import re
from datetime import datetime

import analyzer


def main():
    conn = pymysql.connect(
        host='127.0.0.1', 
        user='root', 
        passwd='dbmaster', 
        db='stock_weather', 
        charset='utf8')

    with conn.cursor() as cur:
        sql = '''SELECT * FROM stock'''
        cur.execute(sql)
        stocks = cur.fetchall()

    for s in stocks:
        key = s[0]
        s_keywords = s[2].split(',')
        news_items = []

        for k in s_keywords:
            news_items += fetch_news(k)

        store_news(conn, key, news_items)


def fetch_news(keyword):
    uri = 'https://openapi.naver.com/v1/search/news.json?query=%s&display=100&sort=sim' % keyword
    headers = {
        'X-Naver-Client-Id': 'Zn7oHjggUHSTBI_eVky1',
        'X-Naver-Client-Secret': 'sELNSGTMrp'
    }

    try:
        r = requests.get(uri, headers=headers, timeout=1)
    except requests.exceptions.Timeout:
        r = requests.get(uri, headers=headers, timeout=1)

    r = r.json()
    r = r['items']

    return r


def store_news(conn, key, items):
    with conn.cursor() as cur:
        sql = '''INSERT INTO news VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)'''
        for news in items:
            title = pick_hangul(news['title'])
            title_ori = news['title']
            link = news['link']
            description = pick_hangul(news['description'])
            pubdate = datetime.strptime(news['pubDate'], '%a, %d %b %Y %H:%M:%S %z')

            h = hashlib.md5()
            h.update(link.encode('utf-8'))
            link_hash = h.hexdigest()

            sentiment = analyzer.analyze(title, description)

            try:
                cur.execute(sql, (
                    title,
                    title_ori,
                    link,
                    description,
                    pubdate.strftime('%Y-%m-%d %H:%M:%S'),
                    link_hash,
                    sentiment,
                    str(key)))
            except pymysql.err.IntegrityError as e:
                # 중복 뉴스는 저장하지 않는다. 나머지 에러는 raise
                if e.args[0] != 1062:
                    raise e

    conn.commit()


def pick_hangul(origin):
    s = re.sub('[^가-힣]', ' ', origin)
    s = re.sub('\s+', ' ', s)
    return re.sub('^\s+', '', s)


if __name__ == '__main__':
    main()
