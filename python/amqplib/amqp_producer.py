#!/usr/bin/python2.5

import time
from amqp_common import amqp, conf, setup_amqp

def main():
    ch = setup_amqp('w')
    start = last = now = time.time()
    try:
        n = total = 0
        seq = 0

        while 1:
            # in batches of 1000
            N = 1000
            for n in range(N):
                msg = amqp.Message("#%d" % seq, content_type='text/plain')
                ch.basic_publish(msg, conf.exchange, conf.queue)
                seq += 1
            now = time.time()
            print "%d in %.2f (last is %d) is %.2f/sec.  Overall %.2f/sec." % (
                N, now-last, seq, float(N)/(now-last), seq/(now-start),
                )
            last = now

        last = int(time.time())
        while 0:
            # one at a time
            n += 1
            seq += 1
            msg = amqp.Message("#%d" % seq, content_type='text/plain')
            ch.basic_publish(msg, conf.exchange, conf.queue)
            now = int(time.time())
            if now != last:
                print seq, n, seq/(time.time()-start)
                total += n
                n = 0
                last = now
    except KeyboardInterrupt:
        print "total %d" % (total + n)

    ch.close()

if __name__ == '__main__':
    main()
