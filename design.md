- ElevatorCommandCenter:request_elevator
    revisar que ascensor está más cerca (binary search)
    considerar si el ascensor está subiendo o bajando?
    submit de "request" al ElevatorUnit

- ElevatorUnit
    considerar capacidad de gente
    queue de pisos a ir

---

Features:

- status_all -> status_report() : DONE
- status_elv : DONE
- list_elevators : DONE
- request_elevator : DONE
- time_step()

- target floors queue
    current: 4
    queue: 2 3 ! 6 7 9
    hacer inserts ordenados
    settear un sentido (up/down) on first insert
    switchear de sentido on top/bottom

TODO:
- proper logging