import sys, os.path
HERE = os.path.split(sys.argv[0])[0]
sys.path.insert(0, os.path.join(HERE, '..', 'shared'))
import config
conf = config.Config()
import amqplib.client_0_8 as amqp

def setup_amqp(mode='r'):
    conn = amqp.Connection(conf.host, userid=conf.user, password=conf.password, ssl=conf.ssl)

    ch = conn.channel()
    ch.access_request('/data', active=True, read=(mode=='r'), write=(mode=='w'))

    ch.exchange_declare(conf.exchange, 'direct', durable=conf.durable, auto_delete=False)
    qname, n_msgs, n_consumers = ch.queue_declare(conf.queue, durable=conf.durable, exclusive=False, auto_delete=False)
    print "queue %s (%d msgs, %d consumers)" % (qname, n_msgs, n_consumers)

    return ch
