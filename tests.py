import unittest
import random
from elevatoraction.entities import ElevatorUnit, ElevatorCommandCenter
from elevatoraction.exceptions import TooManyElevatorsError, DuplicatedElevatorError

class ElevatorUnitTest(unittest.TestCase):
    def test_create_elevator(self):
        e = ElevatorUnit()
        self.assertEqual(e.max_passengers, 8)
        self.assertEqual(e.current_floor, 0)
        self.assertIsNone(e.target_floor)

class ElevatorCommandCenterTest(unittest.TestCase):
    def test_add_elevator(self):
        cc = ElevatorCommandCenter()
        e = ElevatorUnit()
        cc.add_elevator(e)
        self.assertEqual(cc.elevator_amount(), 1)

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
        cc = ElevatorCommandCenter()
        e = ElevatorUnit()
        cc.add_elevator(e)
        with self.assertRaises(DuplicatedElevatorError):
            cc.add_elevator(e)

if __name__ == '__main__':
    unittest.main()
