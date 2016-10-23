import abc


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


class StateMachine(object):
    def __init__(self, owner, global_state, state):
        self._owner = owner
        self._global_state = global_state
        self._previous_state = None
        self._enter_state(state)

    def change_state(self, state):
        if state is None:
            raise ValueError("State shouldn't be None")
        self._state.exit(self._owner)
        self._previous_state = self._state
        self._enter_state(state)

    def revert_to_previous_state(self):
        if self._previous_state is None:
            raise Exception("No previous state")
        self.change_state(self._previous_state)

    def _enter_state(self, state):
        self._state = state
        self._state.enter(self._owner)

    def execute(self):
        self._global_state.execute(self._owner)
        self._state.execute(self._owner)
