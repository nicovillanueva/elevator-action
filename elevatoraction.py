#!/usr/bin/env python3.5

from typing import Union
import uuid

class ElevatorUnit(object):
    def __init__(self, elevator_id=str(uuid.uuid4())):
        self.eid = elevator_id
        self.current_floor = 0
        self.target_floor = None

    def __str__(self):
        return str({
            'id': self.eid,
            'current': self.current_floor,
            'target': self.target_floor
        })

class ElevatorCommandCenter(object):
    def __init__(self, max_elevators=16):
        self.elevators = []
        self.max_elevators = max_elevators

    # TODO: Serialize response?
    def add_elevator(self, elevator: ElevatorUnit) -> Union[bool, str]:
        if len(self.elevators) + 1 > self.max_elevators:
            return False, 'max elevators reached'
        else:
            self.elevators.append(elevator)
            return True, 'added'

    #def status_report(self):

if __name__ == '__main__':
    a = ElevatorUnit()
    print(a)
