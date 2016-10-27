import time
from sys import stdin

import ids
from entities import EntityManager
from messages import MessageDispatcher
from miner import Miner
from minerswife import MinersWife

entities = EntityManager()
messages = MessageDispatcher(entities)

entities.register(Miner(messages, ids.MINER))
entities.register(MinersWife(messages, ids.ELSA))

while True:
    for i in range(10):
        [e.update() for e in entities]
        time.sleep(1)
        messages.dispatch_delayed_messages()
    print("Enter to continue")
    stdin.readline()
