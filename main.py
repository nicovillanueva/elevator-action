#!/usr/bin/env python3.5

from elevatoraction import entities as ent

if __name__ == '__main__':
    cc = ent.ElevatorCommandCenter()
    cc.add_elevator(ent.ElevatorUnit())
    a = []
    for _ in range(17):
        a.append(ent.ElevatorUnit())
    cc.add_elevators(a)
    cc.status_report()
