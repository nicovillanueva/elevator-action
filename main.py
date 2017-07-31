#!/usr/bin/env python3.5

from elevatoraction import entities as ent

if __name__ == '__main__':
    cc = ent.ElevatorCommandCenter()
    e1 = ent.ElevatorUnit(elevator_id='1')
    e2 = ent.ElevatorUnit(elevator_id='2')
    cc.add_elevators([e1, e2])
    print(cc.status_report())
    cc.request_elevator(4)
    cc.request_elevator(2)
    cc.time_step()
    cc.request_elevator(5)
    cc.time_step()
    cc.time_step()
    cc.time_step()
    cc.time_step()
    cc.time_step()
    cc.time_step()
    cc.time_step()
    cc.request_elevator(2)
    cc.time_step()
    cc.time_step()
    print(cc.status_report())
