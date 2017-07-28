from elevatoraction.exceptions import TooManyElevatorsError, DuplicatedElevatorError
from typing import Union
import uuid

class ElevatorUnit(object):
    def __init__(self, max_passengers=8, elevator_id=str(uuid.uuid4())):
        self.eid = elevator_id
        self.max_passengers = max_passengers
        self.current_floor = 0
        self.target_floor = None

    def __str__(self):
        return str({
            'eid': self.eid,
            'current': self.current_floor,
            'target': self.target_floor
        })


class ElevatorCommandCenter(object):
    def __init__(self, max_elevators=16):
        self.elevators = []
        self.max_elevators = max_elevators

    def add_elevator(self, elevator: ElevatorUnit) -> int:
        assert type(elevator) is ElevatorUnit
        if elevator.eid in self.elevator_ids():
            raise DuplicatedElevatorError('elevator {} already controlled')
        if len(self.elevators) + 1 > self.max_elevators:
            raise TooManyElevatorsError('max elevators of {} '
            'reached'.format(self.max_elevators))
        else:
            self.elevators.append(elevator)
            return 1

    def add_elevators(self, elevators: list) -> int:
        acc = 0
        for e in elevators:
            try:
                # FIXME: 'acc' is out of scope!
                acc += self.add_elevator(e)
            except DuplicatedElevatorError:
                pass
        return acc

    def elevator_ids(self) -> list:
        return [e.eid for e in self.elevators]

    def elevator_amount(self):
        return len(self.elevators)

    def status_report(self):
        [print(e) for e in self.elevators]
