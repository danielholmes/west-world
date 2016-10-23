import abc
from enum import Enum


class GameEntity(object):
    __metaclass__ = abc.ABCMeta

    next_valid_id = 1

    def __init__(self, id):
        if id < GameEntity.next_valid_id:
            raise ValueError("Invalid id: {0}".format(id))
        self._id = id
        GameEntity.next_valid_id = id + 1

    @property
    def id(self):
        return self._id

    @abc.abstractmethod
    def update(self):
        pass


class GameEntityState(object):
    __metaclass__ = abc.ABCMeta

    def enter(self, entity):
        pass

    def exit(self, entity):
        pass

    @abc.abstractmethod
    def execute(self, entity):
        pass


class Miner(GameEntity):
    POCKET_GOLD_CAPACITY = 3
    THIRSTY_THRESHOLD = 5

    def __init__(self, id):
        super(Miner, self).__init__(id)

        self.location = Location.SHACK
        self._gold_carried = 0
        self._money_in_bank = 0
        self._thirst = 0
        self._fatigue = 0
        self._enter_state(StartState())

    def update(self):
        self._thirst += 1
        self._state.execute(self)

    def collect_gold(self):
        assert(self._gold_carried < Miner.POCKET_GOLD_CAPACITY)
        self._gold_carried += 1

    def increase_fatigue(self):
        self._fatigue += 1

    @property
    def is_thirsty(self):
        return self._thirst >= Miner.THIRSTY_THRESHOLD

    @property
    def are_pockets_full_of_gold(self):
        return self._gold_carried == Miner.POCKET_GOLD_CAPACITY

    def change_state(self, state):
        if state is None:
            raise ValueError("State shouldn't be None")
        self._state.exit(self)
        self._enter_state(state)

    def _enter_state(self, state):
        self._state = state
        self._state.enter(self)

    def sing_out(self, message):
        print("Miner {0}: {1}".format(self.id, message))


class StartState(GameEntityState):
    def execute(self, miner):
        miner.change_state(EnterMineAndDigForNuggetState())


class EnterMineAndDigForNuggetState(GameEntityState):
    def enter(self, miner):
        if miner.location != Location.GOLD_MINE:
            miner.sing_out("Walkin' to the gold mine")
            miner.location = Location.GOLD_MINE

    def execute(self, miner):
        miner.collect_gold()
        miner.increase_fatigue()
        miner.sing_out("Pickin' up a nugget")

        if miner.are_pockets_full_of_gold:
            miner.change_state(VisitBankAndDepositGoldState())

        if miner.is_thirsty:
            miner.change_state(QuenchThirstState())

    def exit(self, miner):
        miner.sing_out("Ah'm leavin' the gold mine with mah pockets ful o' sweet gold")


class VisitBankAndDepositGoldState(GameEntityState):
    def execute(self, miner):
        pass


class GoHomeAndSleepTilRestedState(GameEntityState):
    def execute(self, miner):
        pass


class QuenchThirstState(GameEntityState):
    def execute(self, miner):
        pass


class Location(Enum):
    SHACK = 1
    GOLD_MINE = 2
    BANK = 3
    SALOON = 4
