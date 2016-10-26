import random
import ids
from entities import GameEntity, GameEntityState, StateMachine
from messages import MessageType
from printcolours import green


class MinersWife(GameEntity):
    def __init__(self, messages, id):
        super(MinersWife, self).__init__(messages, id)

        self._is_cooking = False
        self._state_machine = StateMachine(self, MinersWifeGlobalState(), DoHouseworkState())

    def update(self):
        self._state_machine.execute()

    def change_state(self, state):
        self._state_machine.change_state(state)

    def revert_to_previous_state(self):
        self._state_machine.revert_to_previous_state()

    @property
    def is_cooking(self):
        return self._is_cooking

    @property
    def in_bathroom(self):
        return self._state_machine.current_state_is_a(VisitBathroomState)

    def handle_message(self, message):
        self._state_machine.handle_message(message)

    def start_stew(self):
        self._is_cooking = True
        self._messages.dispatch(sender=self, receiver_id=self.id, message_type=MessageType.STEW_READY, delay=3)

    def stew_finished(self):
        self._is_cooking = False
        self._messages.dispatch(sender=self, receiver_id=ids.MINER, message_type=MessageType.STEW_READY)

    def sing_out(self, message):
        print(green("Elsa {0}: {1}".format(self.id, message)))


class VisitBathroomState(GameEntityState):
    def enter(self, wife):
        wife.sing_out("Walkin' to the can. Need to powda mah pretty li'lle nose")

    def execute(self, wife):
        wife.sing_out("Ahhhhhh! Sweet relief!")
        wife.revert_to_previous_state()


class DoHouseworkState(GameEntityState):
    def enter(self, wife):
        wife.sing_out("Time to do some more housework!")

    def exit(self, wife):
        wife.sing_out("Leavin' the Jon")

    def execute(self, wife):
        tasks = (
            "Moppin' the floor",
            "Washin' the dishes",
            "Makin' the bed"
        )
        wife.sing_out(random.choice(tasks))


class CookStewState(GameEntityState):
    def enter(self, wife):
        if not wife.is_cooking:
            wife.sing_out("Putting the stew in the oven")
            wife.start_stew()

    def execute(self, wife):
        wife.sing_out("Fussin' over food")

    def exit(self, wife):
        wife.sing_out("Puttin' the stew on the table")

    def handle_message(self, wife, message):
        if message.message_type == MessageType.STEW_READY:
            wife.sing_out("StewReady! Lets eat")
            wife.stew_finished()
            wife.change_state(DoHouseworkState())
            return True
        return False


class MinersWifeGlobalState(GameEntityState):
    def execute(self, wife):
        if not wife.in_bathroom and random.randrange(10) == 0:
            wife.change_state(VisitBathroomState())

    def handle_message(self, wife, message):
        if message.message_type == MessageType.HONEY_IM_HOME:
            wife.sing_out("Hi honey. Let me make you some of mah fine country stew")
            wife.change_state(CookStewState())
            return True
        return False
