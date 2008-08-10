#!/usr/bin/python2.5

import time
from amqp_common import amqp, conf, setup_amqp

def main():
    ch = setup_amqp('w')
    start = time.time()
    try:
        last = int(time.time())
        n = total = 0
        seq = 0
        while 1:
            for n in range(1000):
                msg = amqp.Message("#%d" % seq, content_type='text/plain')
                ch.basic_publish(msg, conf.exchange, conf.queue)
                seq += 1
            print seq, seq/(time.time()-start)
            continue
            n += 1
            seq += 1
            now = int(time.time())
            if now != last:
                print seq, n, seq/(time.time()-start)
                total += n
                n = 0
                last = now
    except KeyboardInterrupt:
        print "total",total + n

    ch.close()
    conn.close()

if __name__ == '__main__':
    main()
