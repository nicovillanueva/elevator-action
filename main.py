#!/usr/bin/env python3.5

from elevatoraction import entities as ent

if __name__ == '__main__':
    cc = ent.ElevatorCommandCenter()
    a = ent.ElevatorUnit()
    cc.add_elevator(a)
    cc.add_elevator(a)
    cc.status_report()
