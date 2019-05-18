
from pythonosc import osc_message_builder
from pythonosc import udp_client

client = udp_client.SimpleUDPClient('localhost', 8998)

#between 20 and 1000
cent_freq = 500 # just adding one amplitude
#between 0.1 and 2
Q = 0.5 # just adding one phase

msg = osc_message_builder.OscMessageBuilder(address = '/parameters')
msg.add_arg(cent_freq, arg_type='f')
msg.add_arg(Q, arg_type='f')
msg = msg.build()
client.send(msg)