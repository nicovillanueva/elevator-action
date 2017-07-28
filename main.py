#!/usr/bin/env python3.5

from elevatoraction import entities as ent

import uuid

if __name__ == '__main__':
    cc = ent.ElevatorCommandCenter()
    e1 = ent.ElevatorUnit()
    e2 = ent.ElevatorUnit()
    print(e1.eid)
    print(e2.eid)
    print(cc.cid)
    cc.add_elevators([e1, e2])
    # a = []
    # for _ in range(17):
        # a.append(ent.ElevatorUnit())
    # cc.add_elevators(a)
    cc.status_report()
