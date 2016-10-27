import random

import ids
from entities import GameEntity, GameEntityState, StateMachine, NullState
from messages import MessageType
from printcolours import red


class BarFly(GameEntity):
    MAX_ENERGY = 3

    def __init__(self, messages, id):
        super(BarFly, self).__init__(messages, id)

        self._energy = 2
        self._state_machine = StateMachine(self, NullState(), WaitingForMinerState())

    def update(self):
        self._state_machine.execute()

    def handle_message(self, message):
        self._state_machine.handle_message(message)

    def revert_to_previous_state(self):
        self._state_machine.revert_to_previous_state()

    def change_state(self, state):
        self._state_machine.change_state(state)

    def throw_punch_at_miner(self):
        self._energy = max(0, self._energy - 1)
        self._messages.dispatch(sender=self, receiver_id=ids.MINER, message_type=MessageType.PUNCH_COMING_AT_YOU)

    def tell_miner_done_with_him(self):
        self._messages.dispatch(sender=self, receiver_id=ids.MINER, message_type=MessageType.IM_DONE_WITH_YA)

    def bide_time(self):
        self._energy = min(BarFly.MAX_ENERGY, self._energy + 1)

    @property
    def worn_out(self):
        return self._energy == 0

    def sing_out(self, message):
        print(red("Bar Fly {0}: {1}".format(self.id, message)))


class WaitingForMinerState(GameEntityState):
    def execute(self, fly):
        fly.bide_time()

    def handle_message(self, fly, message):
        if message.message_type == MessageType.COME_AT_ME_BRO:
            if not fly.worn_out and random.random() < 0.5:
                fly.sing_out('Wrong day Miner, yer done for!')
                fly.change_state(FightMinerState())
            else:
                fly.sing_out('One of these days miner, grrrrr')
            return True

        return False


class FightMinerState(GameEntityState):
    def execute(self, fly):
        if fly.worn_out:
            fly.sing_out('Ahh yer not worth it. Leave me here to rest')
            fly.tell_miner_done_with_him()
            fly.revert_to_previous_state()
            return

        fly.sing_out(random.choice(('Take that!', 'Booya', 'Here\'s the shake and bake')))
        fly.throw_punch_at_miner()
