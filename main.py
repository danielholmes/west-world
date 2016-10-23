import time

from miner import Miner
from minerswife import MinersWife

entities = (Miner(1), MinersWife(2))
while True:
    [e.update() for e in entities]
    time.sleep(1)
