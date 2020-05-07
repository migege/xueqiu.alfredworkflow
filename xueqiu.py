#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import os
import requests
from alfred.feedback import Feedback

reload(sys)
sys.setdefaultencoding('utf8')


def run(q, xq_a_token):
    q = str(q).strip()
    if not q:
        return

    try:
        headers = {
            'Host': 'xueqiu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        }

        url = 'https://xueqiu.com/v4/stock/quote.json?code=%s' % q
        cookies = {
            'xq_a_token': xq_a_token,
        }
        r = requests.get(url, headers=headers, cookies=cookies)
        res = r.json()
        data = res[q]
        title = '当前价:{current} 涨:{change} 涨幅:{percentage}%'.format(**data)
        link = 'https://xueqiu.com/S/%s' % q
        subtitle = '{name} 昨收:{last_close} 今开:{open} 最高:{high} 最低:{low}'.format(**data)

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
    xq_a_token = os.getenv('XQ_A_TOKEN') or None
    run(q, xq_a_token)
