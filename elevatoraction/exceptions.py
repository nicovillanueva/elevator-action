class TooManyElevatorsError(Exception):
    """Command center overload!"""
    pass

class DuplicatedElevatorError(Exception):
    """This elevator is already under the CC control"""
    pass
