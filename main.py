import time
from sys import stdin

from entities import EntityManager
from messages import MessageDispatcher
from miner import Miner
from minerswife import MinersWife

entities = EntityManager()
messages = MessageDispatcher(entities)

entities.register(Miner(messages, 1))
entities.register(MinersWife(messages, 2))

while True:
    for i in range(20):
        [e.update() for e in entities]
        time.sleep(1)
        messages.dispatch_delayed_messages()
    print("Enter to continue")
    stdin.readline()
