from channels.routing import route
from TEMPO.consumers import ws_connect
from TEMPO.consumers import ws_message
from TEMPO.consumers import ws_disconnect
# from TEMPO.consumers import ws_disconnect

from TEMPO.consumers import ws_live_connect
from TEMPO.consumers import ws_live_message
from TEMPO.consumers import ws_live_disconnect
from TEMPO.consumers import ws_practice_connect
from TEMPO.consumers import ws_practice_message
from TEMPO.consumers import ws_practice_disconnect

from channels import include

chat_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]

live_routing = [
    route("websocket.connect", ws_live_connect),
    route("websocket.receive", ws_live_message),
    route("websocket.disconnect", ws_live_disconnect),
]

practice_routing = [
    route("websocket.connect", ws_practice_connect),
    route("websocket.receive", ws_practice_message),
    route("websocket.disconnect", ws_practice_disconnect),
]

channel_routing = [
    include(chat_routing, path=r"^/chat"),
    include(live_routing, path=r"^/live"),
    include(practice_routing, path=r"/practice")
]