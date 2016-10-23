import time

from miner import Miner

miner = Miner(1)
while True:
    miner.update()
    time.sleep(1)
