import qpid, time

conn = qpid.client.Client('localhost', 5672, qpid.spec.load('qpid/specs/amqp.0-8.xml'), vhost='/')
print conn.start({"LOGIN": "login", "PASSWORD": "password"})
ch = conn.channel(1)
print ch.channel_open()
r = ch.access_request('/data', active=True, read=True, write=True)
ticket = 0
ch.exchange_declare(ticket, "tempexch", "direct", durable=False, auto_delete=False)
ch.queue_declare(queue="tempqueue", durable=False, exclusive=False, auto_delete=False)
ch.queue_bind(queue="tempqueue", exchange="tempexch", routing_key="tempqueue")

while 1:
    msg = ch.basic_get(queue="tempqueue")
    c = msg.content
    if c is not None:
        # handle message now
        print c.body
        ch.basic_ack(msg.delivery_tag)
    else:
        time.sleep(1)
