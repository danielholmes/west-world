import time

from entities import Miner

miner = Miner(1)
while True:
    miner.update()
    time.sleep(0.5)
