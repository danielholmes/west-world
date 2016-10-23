from datetime import datetime, timedelta
from enum import Enum
from heapq import heappush, heappop


class Message(object):
    def __init__(self, sender, receiver_id, message_type, dispatch_time, extra=None):
        self._sender = sender
        self._receiver_id = receiver_id
        self._message_type = message_type
        self._dispatch_time = dispatch_time
        if extra is None:
            self._extra = {}
        else:
            self._extra = extra

    @property
    def receiver_id(self):
        return self._receiver_id

    @property
    def message_type(self):
        return self._message_type

    @property
    def dispatch_time(self):
        return self._dispatch_time

    def __lt__(self, other):
        return self.dispatch_time < other.dispatch_time


class MessageType(Enum):
    HONEY_IM_HOME = 1
    STEW_READY = 2


class MessageDispatcher(object):
    def __init__(self, entities):
        self._entities = entities
        self._delayed = []

    def dispatch(self, sender, receiver_id, message_type, delay=0, extra=None):
        dispatch_time = datetime.utcnow() + timedelta(seconds=delay)
        message = Message(sender, receiver_id, message_type, dispatch_time, extra)
        if delay <= 0:
            self._discharge(message)
        else:
            heappush(self._delayed, message)

    def _discharge(self, message):
        receiver = self._entities.get_by_id(message.receiver_id)
        receiver.handle_message(message)

    def dispatch_delayed_messages(self):
        now = datetime.utcnow()
        while len(self._delayed) > 0 and self._delayed[0].dispatch_time <= now:
            self._discharge(heappop(self._delayed))
