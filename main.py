import time
from sys import stdin

from miner import Miner
from minerswife import MinersWife

entities = (Miner(1), MinersWife(2))
while True:
    for i in range(20):
        [e.update() for e in entities]
        time.sleep(1)
    print("Enter to continue")
    stdin.readline()
