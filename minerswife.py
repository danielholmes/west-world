from random import randrange

from entities import GameEntity, GameEntityState, StateMachine


class MinersWife(GameEntity):
    def __init__(self, id):
        super(MinersWife, self).__init__(id)

        self._state_machine = StateMachine(self, MinersWifeGlobalState(), DoHouseworkState())

    def update(self):
        self._state_machine.execute()

    def change_state(self, state):
        self._state_machine.change_state(state)

    def revert_to_previous_state(self):
        self._state_machine.revert_to_previous_state()

    def sing_out(self, message):
        print("Elsa {0}: {1}".format(self.id, message))


class VisitBathroomState(GameEntityState):
    def execute(self, wife):
        wife.sing_out("Ahhhhh that's better")
        wife.revert_to_previous_state()


class DoHouseworkState(GameEntityState):
    def execute(self, wife):
        wife.sing_out("Houseworkin'")


class MinersWifeGlobalState(GameEntityState):
    def execute(self, wife):
        if randrange(10) == 0:
            wife.sing_out("Gotta pee!!")
            wife.change_state(VisitBathroomState())
