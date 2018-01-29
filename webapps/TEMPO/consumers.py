from channels import Group, Channel
from channels.asgi import get_channel_layer
from urllib.parse import parse_qs
from TEMPO.models import *
import json

# Connected to websocket
channel_event = {}
broadcast_event = {}
def ws_connect(message):
    # parse the query string
    params = parse_qs(message.content["query_string"])
    username = ""
    create_user = ""
    room_number = 0
    create = False

    if b"roomNumber" in params:
        # Set the room_number
        room_number = params[b"roomNumber"][0].decode("utf8")

    if b"username" in params:
        # Set the username
        username = params[b"username"][0].decode("utf8")

    if b"create" in params:
        # Set the create
        create_user = params[b"create"][0].decode("utf8")

    if create_user == "Broadcaster":
        create = True

    msg = {}
    channel_event[message.reply_channel.name] = room_number
    if create:
        broadcast_event[username] = room_number
        msg['state'] = 'create'
        msg['username'] = username
        Group("room-%s" % room_number).add(message.reply_channel)
        message.reply_channel.send({
            "accept" : True,
            "text" : json.dumps(msg)
        })
    else:
        msg['state'] = 'join'
        msg['username'] = username
        Group("room-%s" % room_number).add(message.reply_channel)
        Group("room-%s" % room_number).send({
            "accept" : True,
            "text" : json.dumps(msg)
        })

# recieve the message
def ws_message(message):
    data = json.loads(message['text'])
    msg = {}
    username = data['username']
    room_number = data['roomNumber']
    user_message = data['message']
    msg['state'] = 'chatting'
    msg['username'] = username
    msg['message'] = user_message
    Group("room-%s" % room_number).send({
        "text" : json.dumps(msg)
    })

# Disconnected to websocket
def ws_disconnect(message):
    event_number = channel_event.get(message.reply_channel.name)
    Group("room-%s" % event_number).discard(message.reply_channel)
    del channel_event[event_number]


broadcast_room = {}
broadcast_username = {}
# connect the band_user in live session
def ws_live_connect(message):
    # parse the query string
    params = parse_qs(message.content["query_string"])
    band_name = ""
    username = ""
    start = False
    msg = {}

    if b"bandName" in params:
        band_name = params[b"bandName"][0].decode("utf8")

    if b"start" in params:
        start = True

    if b"username" in params:
        username = params[b"username"][0].decode("utf8")

    Group("live-"+band_name).add(message.reply_channel)
    message.reply_channel.send({
        "accept": True
    })

    broadcast_room[message.reply_channel.name] = band_name
    if start:
        broadcast_username[message.reply_channel.name] = username
        msg['state'] = "start"
        Group("live-"+band_name).send({
            # "accept": True,
            "text": json.dumps(msg)
        })

# recieve the band_user message in live session
def ws_live_message(message):
    data = json.loads(message['text'])
    msg = {}
    state = data['message']
    band_name = data['bandName']

    msg['state'] = state

    # channel_layer = get_channel_layer()
    # ch_group_list = channel_layer.group_channels("live-"+band_name)
    # for channel in ch_group_list:
    #     print(channel)

    Group("live-"+band_name).send({
        # "accept" : True,
        "text" : json.dumps(msg)
    })

def ws_live_disconnect(message):
    msg = {}
    band_name = broadcast_room.get(message.reply_channel.name)
    Group("live-"+band_name).discard(message.reply_channel)
    del broadcast_room[message.reply_channel.name]

    if message.reply_channel.name in broadcast_username:
        username = broadcast_username.get(message.reply_channel.name)
        del broadcast_username[message.reply_channel.name]

        event_id = broadcast_event.get(username)
        del broadcast_event[username]

        event = BandEvent.objects.get(id=event_id)
        event.is_live = False
        event.is_end = True
        event.save()

        msg['state'] = "end"
        Group("live-"+band_name).send({
            # "accept": True,
            "text": json.dumps(msg)
        })





practice_band_name = {}
start_band_user = {}
# connect the band_user in practice session
def ws_practice_connect(message):
    params = parse_qs(message.content["query_string"])
    band_name = ""
    start = False
    practice_id = ""
    msg = {}
    if b"bandName" in params:
        band_name = params[b"bandName"][0].decode("utf8")

    if b"start" in params:
        start = True

    if b"practiceID" in params:
        practice_id = params[b"practiceID"][0].decode("utf8")

    Group("practice-"+band_name).add(message.reply_channel)
    message.reply_channel.send({
        "accept": True
    })

    practice_band_name[message.reply_channel.name] = band_name
    if start:
        start_band_user[message.reply_channel.name] = practice_id
        msg['state'] = "start"
        Group("practice-"+band_name).send({
            "text": json.dumps(msg)
        })

# recieve the band_user message in practice session
def ws_practice_message(message):
    data = json.loads(message['text'])
    msg = {}
    state = data['message']
    band_name = data['bandName']

    msg['state'] = state

    channel_layer = get_channel_layer()
    ch_group_list = channel_layer.group_channels("practice-"+band_name)
    for channel in ch_group_list:
        print(channel)

    Group("practice-"+band_name).send({
        "text": json.dumps(msg)
    })



# disconnect the band_user in practice session
def ws_practice_disconnect(message):
    msg = {}
    band_name = practice_band_name[message.reply_channel.name]
    # Group("practice-"+band_name).discard(message.reply_channel)
    del practice_band_name[message.reply_channel.name]
    if message.reply_channel.name in start_band_user:
        practice_id = start_band_user[message.reply_channel.name]
        pid = int(practice_id)
        practice = PracticeSession.objects.get(id=pid)
        practice.is_live = False
        practice.is_end = True
        practice.save()

        msg['state'] = "end"
        Group("practice-"+band_name).send({
            "text": json.dumps(msg)
        })

    Group("practice-" + band_name).discard(message.reply_channel)
