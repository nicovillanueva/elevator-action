# Elevator Action

*[This repository is the solution for a coding challenge. Uploading it for preservation reasons.]*

The solution provided is mainly comprised of two entities that work together: The ElevatorControlCenter and the ElevatorUnit. Both can be found in the aptly named 'entities' module.

The idea is that a ControlCenter coordinates a bunch of Elevators. The latter are 'dumb' units that get orders from the CC on which floor to go to.

## Components

### Elevator Unit

The actions that a Elevator can do by itself are: report it's status (current floor, it's floor queue, next floor to go to, direction, id), enqueue a new floor, and time step (meaning, move and drop off passengers).

The floor queueing leverages the bisect module to make all insertions ordered, so that the elevator is able to stop mid-trip, to drop off a passenger. This improves on the simplest "first-come, first-serve" approach, that otherwise would increase the travel time dramatically.

The bisect is used and abused in several parts of the implementation. For example, to also decide if to go up or down, when enqueueing several floors.  
For example, if the elevator were to be on the 4th floor, and the following floors were requested: 2 3 6 7 9. In this implementation, it would give priority to going up to the 6th, 7th and 9th floors, and then go down to the 3rd and 2nd.  
If at any point of the trip, the 8th floor were to be queued too, given that insertions are ordered, it would stop on it while going up or down.

Movement itself is dictated by the `direction` field. It's represented in -1 (going down), 0 (stationary), 1 (going up). As it's just an integer, it's added to the `current_floor` value to be moved around. When the elevator reaches the bottom or top floors, and it still has work to do, it switches it's direction and gets back to work.

### Control Center

The Control Center has a more impressive name than what it does, really.

It can control, by default, 16 different elevators. They are 'linked' by calling the add_elevator or add_elevators methods. The latter simply receives a list of elevators and goes over it adding them. If any of them is already under it's control, it skips it.

It's other two most useful methods are to list the status of all elevators, and the request_elevator.

The CC can receive a elevator request, and then it will find out which elevator is the nearest to this requested floor. This is done by, again, exploiting the fact that the elevators are ordered by it's floor (TODO: Check if this is still true after a few time_steps), so a binary search is done on the elevator list to find the nearest.

### Others

Two other modules were coded too: custom exceptions, and some log functions. And the "TOP_FLOOR" variable is defined at module level (\_\_init\_\_.py)

## Building/Running

The solution is built using all stdlib modules, so no pip requirements file is included, and no virtualenv should be needed.

It's only requirement is Python 3.x (developed using Python 3.6, but should work in any 3.x)

To run the tests:

    python3 -m unittest tests.py

It's basically the same as the tests, but there's an example workflow on the main.py. To run it, obviously:

    python3 main.py

### Dockerized

In order to pinpoint the specific Python version, a Dockerfile is also provided. Portability is king.

    docker build -t elevator-action .
    docker run --rm elevator-action:latest

## Pendings

Some features that I thought of, but didn't have time to implement

- Passenger entity: A passenger representation, which would count towards the "max_passengers" field on the ElevatorUnits. According to classical physics laws, the Elevators shouldn't be infinite. Unless they are a Tardis of sorts.
- Proper logging: Timestamped, write to file
- Implement the Control Center as a REST API
- Save statistics of, for example, travel time
- Look for most-requested floors and determine the most efficient floor to be when idle (Tensorflow would be a fun overengineering)
- Unnecesarily restrict so that the Elevator can only receive new floor queues from the Control Center (using the inspect module and inspecting the stack, though apparently is awfully inefficient and implementation-dependant)

## Disclaimer

It's definitely not a perfect implementation, and may fail on some corner cases.

Also, I may have worked on it a bit more than 4 hours. More in the 5h30 mark, I suppose.
