#!/usr/bin/python2.5

import time
from amqp_common import amqp, conf, setup_amqp

class Main:
    def main(self):
        print "py-amqplib consumer"
        self.ch = setup_amqp('r')
        self.ch.queue_bind(conf.queue, conf.exchange, conf.queue)

        #self.poll_forever()
        self.consume_forever()

        self.ch.close()
        conn.close()

    def callback(self, msg):
        #print msg.body,
        msg.channel.basic_ack(msg.delivery_tag)

        self.n += 1
        now = int(time.time())
        if now != self.last:
            self.last = now
            print self.n
            self.n = 0

    def consume_forever(self):
        print "using basic.consume"

        self.last = int(time.time())
        self.n = 0

        self.ch.basic_consume(conf.queue, callback=self.callback)
        while self.ch.callbacks:
            self.ch.wait()

    def poll_forever(self):
        print "using basic.get"
        n = total = 0
        last = int(time.time())
        while 1:
            msg = self.ch.basic_get(conf.queue)
            if msg is None:
                print "no messages, sleeping a bit..."
                time.sleep(1)
            else:
                self.ch.basic_ack(msg.delivery_tag)
                n += 1
                now = int(time.time())
                if now != last:
                    total += n
                    print n, total
                    n = 0
                    last = now

if __name__ == '__main__':
    Main().main()
