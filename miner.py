from enum import Enum

from entities import GameEntity, GameEntityState, StateMachine


class Miner(GameEntity):
    CARRIED_GOLD_HEAVY_THRESHOLD = 3
    THIRSTY_THRESHOLD = 5
    WEALTHY_THRESHOLD = 7
    RESTED_FATIGUE_THRESHOLD = 0

    def __init__(self, id):
        super(Miner, self).__init__(id)

        self._location = Location.SHACK
        self._gold_carried = 0
        self._gold_in_bank = 0
        self._thirst = 0
        self._fatigue = 0
        self._state_machine = StateMachine(self, MinerGlobalState(), GoHomeAndSleepTilRestedState())

    def update(self):
        self._thirst += 1
        self._state_machine.execute()

    def collect_gold(self):
        self._gold_carried += 1

    def increase_fatigue(self):
        self._fatigue += 1

    def change_location(self, new_location):
        if new_location == self._location:
            return False
        self._location = new_location
        return True

    @property
    def is_thirsty(self):
        return self._thirst >= Miner.THIRSTY_THRESHOLD

    @property
    def has_enough_in_bank(self):
        return self.gold_in_bank >= Miner.WEALTHY_THRESHOLD

    @property
    def is_carried_gold_getting_heavy(self):
        return self._gold_carried >= Miner.CARRIED_GOLD_HEAVY_THRESHOLD

    @property
    def is_rested(self):
        return self._fatigue <= Miner.RESTED_FATIGUE_THRESHOLD

    @property
    def thirst(self):
        return self._thirst

    @property
    def gold_in_bank(self):
        return self._gold_in_bank

    @property
    def gold_carried(self):
        return self._gold_carried

    def buy_and_consume_drink(self):
        self._thirst = 0
        self._gold_in_bank -= 1

    def put_gold_in_bank(self):
        self._gold_in_bank += self._gold_carried
        self._gold_carried = 0

    def sleep(self):
        if self._fatigue > 0:
            self._fatigue -= 1

    def change_state(self, state):
        self._state_machine.change_state(state)

    def sing_out(self, message):
        print("Miner {0}: {1}".format(self.id, message))


class EnterMineAndDigForNuggetState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.GOLD_MINE):
            miner.sing_out("Walkin' to the gold mine")

    def execute(self, miner):
        miner.collect_gold()
        miner.increase_fatigue()
        miner.sing_out("Pickin' up a nugget, carrying {0} now".format(miner.gold_carried))

        if miner.is_carried_gold_getting_heavy:
            miner.change_state(VisitBankAndDepositGoldState())

        if miner.is_thirsty:
            miner.change_state(QuenchThirstState())

    def exit(self, miner):
        miner.sing_out("Ah'm leavin' the gold mine with mah pockets ful o' sweet gold")


class VisitBankAndDepositGoldState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.BANK):
            miner.sing_out("Walkin' to the bank")

    def execute(self, miner):
        miner.put_gold_in_bank()
        miner.sing_out("Puttin' my money in the bank, now I have {0}".format(miner.gold_in_bank))

        if miner.has_enough_in_bank:
            miner.sing_out("WooHoo! Rich enough for now. Back home to mah li'lle lady")
            miner.change_state(GoHomeAndSleepTilRestedState())
        else:
            miner.change_state(EnterMineAndDigForNuggetState())


class GoHomeAndSleepTilRestedState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.SHACK):
            miner.sing_out("Walkin' to the shack")

    def execute(self, miner):
        if miner.is_rested:
            miner.sing_out("What a God darn fantastic nap! Time to find more gold")
            miner.change_state(EnterMineAndDigForNuggetState())
            return

        miner.sleep()
        miner.sing_out("zzzz...")


class QuenchThirstState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.SALOON):
            miner.sing_out("Runnin' to the saloon, yeeeehaw!")

    def execute(self, miner):
        miner.buy_and_consume_drink()
        miner.sing_out("Drinkin' mah whiskey, no more thirst")
        miner.change_state(EnterMineAndDigForNuggetState())


class MinerGlobalState(GameEntityState):
    def execute(self, miner):
        if miner.is_thirsty:
            miner.change_state(QuenchThirstState())


class Location(Enum):
    SHACK = 1
    GOLD_MINE = 2
    BANK = 3
    SALOON = 4
