import unittest
import random
from elevatoraction.entities import ElevatorUnit, ElevatorCommandCenter
from elevatoraction.exceptions import TooManyElevatorsError, DuplicatedElevatorError, ElevatorNotFoundError


class ElevatorUnitTest(unittest.TestCase):
    def setUp(self):
        self.e1 = ElevatorUnit(elevator_id='1')
        self.e2 = ElevatorUnit(elevator_id='2')

    def test_create_elevator(self):
        self.assertEqual(self.e1.max_passengers, 8)
        self.assertEqual(self.e1.current_floor, 0)
        self.assertEqual(self.e1.direction, 0)
        self.assertIsNone(self.e1.next_floor)
        self.assertListEqual(self.e1.floor_queue, [])

    def test_enqueue_floors(self):
        self.e1.enqueue_floor(10)
        self.e1.enqueue_floor(2)
        self.e1.enqueue_floor(200)
        self.e1.enqueue_floor(31)
        self.assertListEqual(self.e1.floor_queue, [2, 10, 31, 200])


class ElevatorCommandCenterTest(unittest.TestCase):

    def setUp(self):
        self.cc = ElevatorCommandCenter()
        self.e1 = ElevatorUnit(elevator_id='1')
        self.e2 = ElevatorUnit(elevator_id='2')

    @staticmethod
    def new_elevator_state(eid: str = '1'):
        return {
            'eid': eid,
            'current': 0,
            'next': None,
            'pending': [],
            'direction': 0
        }

    def test_add_elevator(self):
        self.cc.add_elevator(self.e1)
        self.assertEqual(self.cc.elevator_amount(), 1)

    def test_add_elevators(self):
        max_ = random.randint(1, 50)
        target_amount = random.randint(1, max_)
        cc = ElevatorCommandCenter(max_elevators=max_)
        elevators = []
        for e in range(target_amount):
            elevators.append(ElevatorUnit())
        cc.add_elevators(elevators)
        self.assertEqual(cc.elevator_amount(), target_amount)

    def test_cc_full(self):
        cc = ElevatorCommandCenter()
        elevators = []
        for e in range(16):
            elevators.append(ElevatorUnit())
        self.assertEqual(cc.add_elevators(elevators), 16)
        self.assertEqual(cc.elevator_amount(), 16)
        e = ElevatorUnit()
        with self.assertRaises(TooManyElevatorsError):
            cc.add_elevator(e)

    def test_duped_elevator(self):
        self.cc.add_elevator(self.e1)
        with self.assertRaises(DuplicatedElevatorError):
            self.cc.add_elevator(self.e1)

    def test_add_ordered_elevators(self):
        e3 = ElevatorUnit(elevator_id='3')
        e4 = ElevatorUnit(elevator_id='4')
        self.e1.current_floor = 30
        self.e2.current_floor = 10
        e3.current_floor = 40
        e4.current_floor = 20
        self.cc.add_elevators([self.e1, self.e2, e3, e4])
        self.assertListEqual(self.cc.list_elevators(), ['2', '4', '1', '3'])

    def test_status_report(self):
        self.cc.add_elevators([self.e1, self.e2])
        self.assertEqual(self.cc.status_report(), [self.new_elevator_state('1'), self.new_elevator_state('2')])

    def test_status_elevator(self):
        self.cc.add_elevator(self.e1)
        self.assertEqual(self.cc.status_elevator(self.e1.eid), self.new_elevator_state())

    def test_elevator_not_found(self):
        with self.assertRaises(ElevatorNotFoundError):
            self.cc.status_elevator('1')

    def test_find_nearest(self):
        self.e1.current_floor = 2
        self.e2.current_floor = 200
        self.cc.add_elevators([self.e1, self.e2])
        self.assertEqual(self.cc._find_nearest_to(10).get_status(), self.e1.get_status())
        self.assertEqual(self.cc._find_nearest_to(190).get_status(), self.e2.get_status())

    def test_request_elevator(self):
        self.e1.current_floor = 2
        self.e2.current_floor = 200
        self.cc.add_elevators([self.e1, self.e2])
        self.cc.request_elevator(180)
        self.cc.time_step()
        self.assertEqual(self.e2.next_floor, 180)

    def test_elevators_dropoff(self):
        self.cc.add_elevators([self.e1, self.e2])
        self.cc.request_elevator(4)
        self.cc.request_elevator(2)
        self.cc.time_step()
        self.cc.request_elevator(5)
        self.cc.time_step()
        self.cc.time_step()
        self.cc.time_step()
        self.cc.time_step()
        self.cc.time_step()
        self.cc.time_step()
        self.cc.time_step()
        self.cc.request_elevator(2)
        self.cc.time_step()
        self.cc.time_step()
        self.assertListEqual(self.cc.status_report(), [
            {'eid': '1', 'current': 2, 'next': None, 'pending': [], 'direction': 0},
            {'eid': '2', 'current': 5, 'next': None, 'pending': [], 'direction': 0}])

if __name__ == '__main__':
    unittest.main()
