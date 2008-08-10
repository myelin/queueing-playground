import time, sys, os.path
HERE = os.path.split(sys.argv[0])[0]
sys.path.insert(0, os.path.join(HERE, '..', 'shared'))
import config
conf = config.Config()
import qpid

print "qpid consumer"
conn = qpid.client.Client(conf.host, conf.port, qpid.spec.load(os.path.join(HERE, 'amqp.0-8.xml')), vhost='/')
conn.start({"LOGIN": conf.user, "PASSWORD": conf.password})
ch = conn.channel(1)
ch.channel_open()
r = ch.access_request('/data', active=True, read=True, write=True)
ticket = 0
ch.exchange_declare(ticket, conf.exchange, "direct", durable=False, auto_delete=False)
ch.queue_declare(queue=conf.queue, durable=False, exclusive=False, auto_delete=False)
ch.queue_bind(queue=conf.queue, exchange=conf.exchange, routing_key=conf.queue)

print "using basic.get"
last = int(time.time())
n = 0
while 1:
    msg = ch.basic_get(queue=conf.queue)
    c = msg.content
    now = int(time.time())
    if now != last:
        last = now
        print n
        n = 0
    if c is not None:
        # handle message now
        #print c.body
        n += 1
        ch.basic_ack(msg.delivery_tag)
    else:
        time.sleep(1)
