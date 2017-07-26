#!/usr/bin/env python3.5

from typing import Union

class ElevatorCommandCenter(object):
    def __init__(self):
        self.elevators = {}

    # TODO: Serialize response?
    def add_elevator(self, elevator: Elevator) -> Union[bool, str]:
        pass


class ElevatorCoordinator(object):
    pass


class ElevatorUnit(object):
    def __init__(self):
