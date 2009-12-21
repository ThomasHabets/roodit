#!/usr/bin/python

import json
import httplib
import numpy
import sys
import re

def GET(path): 
    conn = httplib.HTTPConnection("www.reddit.com")
    conn.request("GET", path)
    r1 = conn.getresponse()
    if r1.status != 200:
        print r1.status
        raise "barn"
    ret = r1.read()
    conn.close()
    return ret

def dump(user, count, after):
    s = "/user/%s/comments" % (user)
    a = ""
    if after:
        a = "?after=" + after
    path = '%s/.json%s' % (s, a)
    a = json.read(GET(path))
    print path
    return a['data']['after'], [x['data'] for x in a['data']['children']]

def printComment(c):
    def noPrefix(s):
        return re.sub('(.*_)?(.*)','\\2',s)
    if not c.has_key('body'):
        return
    print '-------------'
    print ("http://www.reddit.com/comments/%s/dummy/%s"
           % (noPrefix(c['link_id']), noPrefix(c['name'])))
    print 'Article: %s' % (c['link_title'][:40])
    print 'Id:      %s' % (c['id'])
    print 'Karma:   %d (%d up / %d down)' % (c['ups'] - c['downs'],
                                             c['ups'],
                                             c['downs'])
    print c['body']

def printData(data):
    data.sort(lambda x,y: (y['ups'] - y['downs']) - (x['ups'] - x['downs']))
    for c in data[:10]:
        printComment(c)

def getData(user):
    after = None
    arr = []
    n = 0
    while True:
        n = n+1
        after, t = dump(user, n * 25, after)
        arr.extend(t)
        if after is None:
            break
    for e in arr:
        for k in e.keys():
            if isinstance(e[k], unicode):
                e[k] = e[k].encode('utf-8')
    return arr

def usage():
    print "%s <reddit username>" % (sys.argv[0])
    sys.exit(0)

def main():
    if len(sys.argv) != 2:
        usage()
    try:
        data = json.read(open("comments-%s.json" % (sys.argv[1])).read())
    except:
        data = getData(sys.argv[1])
        open("comments-%s.json" % (sys.argv[1]), "w").write(json.write(data))
    printData(data)

if __name__ == '__main__':
    main()
