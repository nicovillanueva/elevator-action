import bisect
import random
import uuid
from typing import List

from elevatoraction import TOP_FLOOR
from elevatoraction.exceptions import TooManyElevatorsError, DuplicatedElevatorError, ElevatorNotFoundError
from elevatoraction.utils import *


class Passenger(object):
    def __init__(self, intent: int = None):
        self.intent = intent if intent is not None else random.randint(1, TOP_FLOOR)


class ElevatorUnit(object):
    def __init__(self, max_passengers: int = 8, elevator_id: str = None):
        self.eid = elevator_id if elevator_id is not None else str(
            uuid.uuid4())
        self.max_passengers = max_passengers
        self.current_floor = 0
        self.next_floor = None
        self.floor_queue = []
        self.direction = 0

    def get_status(self) -> dict:
        return {
            'eid': self.eid,
            'current': self.current_floor,
            'next': self.next_floor,
            'pending': self.floor_queue,
            'direction': self.direction
        }

    def enqueue_floor(self, floor: int) -> None:
        """Keep the floors ordered by using bisect

        :param floor: Floor to be enqueued
        :return: Nothing
        """
        # TODO: Do not insert duplicates
        bisect.insort(self.floor_queue, floor)

    def time_step(self) -> None:
        """If stationary and have work to do, start moving (or as we say, agarrá la pala)
        Move > dequeue > recalc direction

        :return: Nothing
        """
        # FIXME: Cleanup this mess of a method
        if self.direction == 0 and len(self.floor_queue) != 0:
            if self.current_floor == 0:
                self.direction = 1
                self.next_floor = self.floor_queue[0]
            elif self.current_floor == TOP_FLOOR:
                self.direction = -1
                self.next_floor = self.floor_queue[-1]
            else:
                below = self.floor_queue[:bisect.bisect_left(self.floor_queue, self.current_floor)]
                above = self.floor_queue[bisect.bisect_left(self.floor_queue, self.current_floor):]
                if len(below) >= len(above):
                    self.direction = -1
                    self.next_floor = below[-1]
                else:
                    self.direction = 1
                    self.next_floor = above[0]

        self.current_floor += self.direction
        info('Elevator {} moving: {} (now at {})'.format(self.eid, self.direction, self.current_floor))
        if self.current_floor == self.next_floor:
            if len(self.floor_queue) == 1:
                info('Elevator {} arrived at final target: {}. Dropping dude off...'.format(self.eid,
                                                                                            self.current_floor))
                self.floor_queue.pop()
                self.next_floor = None
                self.direction = 0
                return
            i = self.floor_queue.index(self.current_floor)
            self.next_floor = self.floor_queue[i + self.direction]
            info('Elevator {} arrived at floor: {}. Dropping dudes off...'
                 'Next up: {}'.format(self.eid, self.current_floor, self.next_floor))
            self.floor_queue.remove(self.current_floor)

        if self.current_floor == 0 and len(self.floor_queue) != 0:
            info('Down at the bottom. Switching...')
            self.direction = 1
        elif self.current_floor == TOP_FLOOR and len(self.floor_queue) != 0:
            info('Up above. Switching...')
            self.direction = -1

    def __str__(self) -> str:
        return str(self.get_status())


class ElevatorCommandCenter(object):
    def __init__(self, max_elevators: int = 16, controller_id: str = None):
        self.cid = controller_id if controller_id is not None else str(
            uuid.uuid4())
        self.elevators = []
        self.max_elevators = max_elevators
        self.cid = controller_id

    def add_elevator(self, elevator: ElevatorUnit) -> int:
        """Adds an elevator to this Control Center's claws.
        May raise exceptions upon receiving an already-controlled elevator, or if it's reached it's
        maximum amount of elevators

        :param elevator: Elevator to be controlled
        :return: Amount of elevators added (usually, 1; more if called by add_elevators)
        """
        assert type(elevator) is ElevatorUnit
        if elevator.eid in self.list_elevators():
            raise DuplicatedElevatorError(
                'elevator {} already controlled by {}'.format(elevator.eid, self.cid))
        elif len(self.elevators) + 1 > self.max_elevators:
            raise TooManyElevatorsError('max elevators of {} '
                                        'reached'.format(self.max_elevators))
        else:
            # Insert ordered by current_floor (leveraging bisect/binary search)
            self.elevators.insert(bisect.bisect_right(list(map(lambda x: x.current_floor, self.elevators)),
                                                      elevator.current_floor), elevator)
            return 1

    def add_elevators(self, elevators: List[ElevatorUnit]) -> int:
        """Adds a list of elevators

        :param elevators: List of ElevatorUnit to be added
        :return: Amount of elevators added to our control
        """
        acc = 0
        # FIXME: Some nicer way to add/count
        for e in elevators:
            try:
                acc += self.add_elevator(e)
            except DuplicatedElevatorError:
                info('Elevator already controlled. Skipping.')
        return acc

    def list_elevators(self) -> List[str]:
        """List the IDs of the elevators under our control

        :return: List of elevators' IDs
        """
        return [e.eid for e in self.elevators]

    def elevator_amount(self) -> int:
        """How many elevators do we have?
        :return: Self explanatory
        """
        return len(self.elevators)

    def status_report(self) -> List[dict]:
        """Report the status of all of our elevators
        :return: List of each elevator's status
        """
        return [e.get_status() for e in self.elevators]

    def status_elevator(self, eid: str) -> dict:
        """Report the status of a given elevator.
        :return: The status of the elevator, in it's dict form
        """
        if eid not in self.list_elevators():
            raise ElevatorNotFoundError(
                'Elevator not under this CC\'s control')
        return list(filter(lambda x: x.eid == eid, self.elevators))[0].get_status()

    def _find_nearest_to(self, target: int) -> ElevatorUnit:
        """Find the elevator nearest to the target
        The self.elevators list is already ordered, so, just bisect it by the current_floor of each elevator
        :return: Reference of the nearest Elevator to the target floor
        """
        index = bisect.bisect_left(list(map(lambda x: x.current_floor, self.elevators)), target)
        # If the index is higher than the amount of elevators, means the requested floor is above all of our elevators
        # (the bisect's insertion point would be after all our elevators)
        # Proof: bisect.bisect_left([0, 2, 2], 4) -> 3
        # Being [0, 2, 2] the elevators' current floors, 4 the target, and 3 the resulting index
        if index >= len(self.elevators):
            return self.elevators[-1]
        if self.elevators[index].current_floor - target < target - self.elevators[index-1].current_floor:
            return self.elevators[index]
        return self.elevators[index-1]

    def request_elevator(self, target_floor: int) -> None:
        """Find the nearest elevator, and enqueue it a floor
        :return: Nothing
        """
        e = self._find_nearest_to(target_floor)
        e.enqueue_floor(target_floor)
        info('Elevator {} will be going to floor {}'.format(e.eid, target_floor))

    def time_step(self) -> None:
        """Time stepping is actually done by each elevator.
        So just call each elevator's time_step method
        :return: Nothing
        """
        [e.time_step() for e in self.elevators]
