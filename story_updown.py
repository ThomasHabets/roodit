#!/usr/bin/python

import json
import httplib
import numpy
import sys

def GET(path): 
    conn = httplib.HTTPConnection("www.reddit.com")
    conn.request("GET", path)
    r1 = conn.getresponse()
    if r1.status != 200:
        raise "barn"
    ret = r1.read()
    conn.close()
    return ret

def dump(sub, count, after):
    if sub == "":
        s = ""
    else:
        s = "/r/" + sub
    c = ""
    a = ""
    if count:
        c = "?count=" + str(count)
    if after:
        a = "&after=" + after
    path = '%s/.json%s%s' % (s, c, a)
    print path
    a = json.read(GET(path))
    ra = []
    for e in a['data']['children']:
        data = e['data']
        ra.append(
            (data['subreddit'],
             100 * (data['ups'] / (float(data['ups']) +data['downs']))))
    return a['data']['after'], ra

def usage():
    print "%s <subreddit, such as programming>" % (sys.argv[0])
    sys.exit(0)
    
def main():
    if len(sys.argv) != 2:
        usage()
    sub = sys.argv[1]
    after = None
    arr = []
    for n in range(10):
        after, t = dump(sub, n * 25, after)
        arr.extend(t)
    v = [x[1] for x in arr]
    print "%.2f %.2f" % (numpy.average(v), numpy.std(v))

if __name__ == '__main__':
    main()
