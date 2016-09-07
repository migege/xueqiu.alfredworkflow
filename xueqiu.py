#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import os
import requests
from alfred.feedback import Feedback

reload(sys)
sys.setdefaultencoding('utf8')


def run(q):
    q = q.strip()
    if not q:
        return

    try:
        url = 'https://xueqiu.com/v4/stock/quotec.json?code=%s' % q
        headers = {
            'Host': 'xueqiu.com',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        }
        r = requests.get(url, headers=headers)
        res = r.json()
        data = res[q]
        price = data[0]
        delta = data[1]
        rate = data[2]
        time = data[3]
        title = '当前价:{} 涨:{} 涨幅:{}%'.format(price, delta, rate)
        link = 'https://xueqiu.com/S/%s' % q

        url = 'https://xueqiu.com/v4/stock/quote.json?code=%s' % q
        cookies = {'xq_a_token': 'd55b097b6b0cdc269719842662c5f76a4f5a3e72',}
        r = requests.get(url, headers=headers, cookies=cookies)
        res = r.json()
        data = res[q]
        subtitle = '{name} 昨收:{last_close} 今开:{open} 最高:{high} 最低:{low}'.format(
            **data)

        kwargs = {'title': title, 'subtitle': subtitle, 'arg': link}

        fb = Feedback()
        fb.addItem(**kwargs)
        fb.output()
    except Exception, e:
        print 'EXCEPT:', e
        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    q = sys.argv[1]
    run(q)
