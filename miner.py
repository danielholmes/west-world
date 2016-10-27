from enum import Enum

import ids
from entities import GameEntity, GameEntityState, StateMachine, DelayedState
from messages import MessageType
from printcolours import blue


class Miner(GameEntity):
    CARRIED_GOLD_HEAVY_THRESHOLD = 3
    THIRSTY_THRESHOLD = 5
    WEALTHY_THRESHOLD = 5
    TIREDNESS_THRESHOLD = 6

    def __init__(self, messages, id):
        super(Miner, self).__init__(messages, id)

        self._location = Location.SHACK
        self._gold_carried = 0
        self._gold_in_bank = 0
        self._thirst = 0
        self._fatigue = 0
        self._state_machine = StateMachine(
            self,
            MinerGlobalState(),
            DelayedState(EnterMineAndDigForNuggetState())
        )

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
    def location(self):
        return self._location

    @property
    def is_thirsty(self):
        return self._thirst >= Miner.THIRSTY_THRESHOLD

    @property
    def is_tired(self):
        return self._fatigue >= Miner.TIREDNESS_THRESHOLD

    @property
    def has_enough_in_bank(self):
        return self.gold_in_bank >= Miner.WEALTHY_THRESHOLD

    @property
    def is_carried_gold_getting_heavy(self):
        return self._gold_carried >= Miner.CARRIED_GOLD_HEAVY_THRESHOLD

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
        self._gold_in_bank -= 2

    def put_gold_in_bank(self):
        self._gold_in_bank += self._gold_carried
        self._gold_carried = 0

    def sleep(self):
        if self._fatigue > 0:
            self._fatigue -= 1

    def change_state(self, state):
        self._state_machine.change_state(state)

    def revert_to_previous_state(self):
        self._state_machine.revert_to_previous_state()

    def handle_message(self, message):
        self._state_machine.handle_message(message)

    def tell_wife_home(self):
        self._messages.dispatch(sender=self, receiver_id=ids.ELSA, message_type=MessageType.HONEY_IM_HOME)

    def swear_at_barfly(self):
        self.sing_out('Hey bar fly, you\'re a pecker head')
        self._messages.dispatch(sender=self, receiver_id=ids.BAR_FLY, message_type=MessageType.COME_AT_ME_BRO)

    def sing_out(self, message):
        print(blue("Miner {0}: {1}".format(self.id, message)))


class EnterMineAndDigForNuggetState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.GOLD_MINE):
            miner.sing_out("Walkin' to the goldmine")

    def execute(self, miner):
        miner.collect_gold()
        miner.increase_fatigue()
        miner.sing_out("Pickin' up a nugget, carrying {0} now".format(miner.gold_carried))

        if miner.is_carried_gold_getting_heavy:
            miner.change_state(VisitBankAndDepositGoldState())

        if miner.is_thirsty:
            miner.change_state(QuenchThirstState())

    def exit(self, miner):
        miner.sing_out("Ah'm leavin' the goldmine with mah pockets full o' sweet gold")


class VisitBankAndDepositGoldState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.BANK):
            miner.sing_out("Goin' to the bank. Yes siree")

    def execute(self, miner):
        miner.put_gold_in_bank()
        miner.sing_out("Depositing gold. Total savings now: {0}".format(miner.gold_in_bank))

        if miner.has_enough_in_bank:
            miner.sing_out("WooHoo! Rich enough for now. Back home to mah li'lle lady")
            miner.change_state(GoHomeAndSleepTilRestedState())
        else:
            miner.change_state(EnterMineAndDigForNuggetState())


class GoHomeAndSleepTilRestedState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.SHACK):
            miner.sing_out("Walkin' home")
            miner.tell_wife_home()

    def execute(self, miner):
        if miner.is_tired:
            miner.sleep()
            miner.sing_out("zzzz...")
        else:
            miner.sing_out("What a God darn fantastic nap! Time to find more gold")
            miner.change_state(EnterMineAndDigForNuggetState())


class QuenchThirstState(GameEntityState):
    def enter(self, miner):
        if miner.change_location(Location.SALOON):
            miner.sing_out("Boy, ah sure is thusty! Walking to the saloon")
            miner.swear_at_barfly()

    def execute(self, miner):
        miner.buy_and_consume_drink()
        miner.sing_out("That's mighty fine sippin liquer")
        miner.change_state(EnterMineAndDigForNuggetState())

    def exit(self, miner):
        miner.sing_out("Drinkin times over")


class MinerGlobalState(GameEntityState):
    def handle_message(self, miner, message):
        if message.message_type == MessageType.STEW_READY and miner.location == Location.SHACK:
            miner.sing_out("I'm coming")
            miner.change_state(EatStewState())
            return True

        if message.message_type == MessageType.PUNCH_COMING_AT_YOU:
            miner.sing_out('What\'s yer problem')
            miner.change_state(BlockPunchesState())
            return True

        return False


class BlockPunchesState(GameEntityState):
    def execute(self, miner):
        miner.sing_out('Missed meh! Try again')

    def handle_message(self, miner, message):
        if message.message_type == MessageType.IM_DONE_WITH_YA:
            miner.sing_out('Ya wimp!')
            miner.revert_to_previous_state()
            return True

        if message.message_type == MessageType.PUNCH_COMING_AT_YOU:
            return True

        return False


class EatStewState(GameEntityState):
    def enter(self, miner):
        miner.sing_out("Smells Reaaal goood Elsa!")

    def execute(self, miner):
        miner.sing_out("Tastes real good too!")
        miner.revert_to_previous_state()

    def exit(self, miner):
        miner.sing_out("Thankya li'lle lady. Ah better get back to whatever ah wuz doin'")


class Location(Enum):
    SHACK = 1
    GOLD_MINE = 2
    BANK = 3
    SALOON = 4
