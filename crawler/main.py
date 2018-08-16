import requests
import pymysql
import hashlib
import re
from datetime import datetime


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
    # TODO: Timeout 걸어서 한 번 retry 하자.. (자주 멎음)
    uri = 'https://openapi.naver.com/v1/search/news.json?query=%s&display=100&sort=sim' % keyword
    headers = {
        'X-Naver-Client-Id': '***',
        'X-Naver-Client-Secret': '***'
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
        sql = '''INSERT INTO news VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)'''
        for news in items:
            title = remove_tag(news['title'])
            link = news['link']
            description = remove_tag(news['description'])
            pubdate = datetime.strptime(news['pubDate'], '%a, %d %b %Y %H:%M:%S %z')

            h = hashlib.md5()
            h.update(link.encode('utf-8'))
            link_hash = h.hexdigest()

            try:
                cur.execute(sql, (
                    title,
                    link,
                    description,
                    pubdate.strftime('%Y-%m-%d %H:%M:%S'),
                    link_hash,
                    None,
                    str(key)))
            except pymysql.err.IntegrityError as e:
                # 중복 뉴스는 저장하지 않는다. 나머지 에러는 raise
                if e.args[0] != 1062:
                    raise e

    conn.commit()


def remove_tag(origin):
    return re.sub('<\S+>', '', origin)


if __name__ == '__main__':
    main()
