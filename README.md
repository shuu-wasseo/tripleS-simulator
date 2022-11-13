# tripleS-simulator
welcome to tripleS-simulator. instructions are as follows:

## requirements
- python 3.10 and above
- python toml library

## config.toml
before you begin, remember to input the necessary data in config.toml.

- prefix: the prefix for every member's serial number. (e.g. "S" for tripleS)
- members: a list containing all the names of the (potential) members.
- random: a boolean value to decide whether the member reveals go in the order or the given list, or are random.
- gravity: a list of lists. each mini-list should contain the number of members (as a string) at which to start a gravity, followed by all the names of the units to shuffle the members into.

default values that can serve as examples have been provided.

## haus.json
this json file represents the structure of the haus. 

### normal HAUS
other than the seoul HAUS, each haus contains multiple rooms in the form of a dictionary, each containing a "upper bunk", "lower bunk" and optionally, a "single" bed. the default structure of the haus (based on the original tripleS) has been provided.

### seoul HAUS
due to the much less detailed structure of the seoul HAUS, the "seoul" dictionary contains multiple rooms in the form of a list. the names of these rooms are typically based on the number of beds in the room, while rooms with the same number of beds are differentiated by a suffix, separated from the original nunumber of beds with a "-".

for example, the default seoul HAUS contains 3 rooms, "2-1", "2-2" and "4". the "2", "2" and "4" in these names indicates the number of beds there will be while "-1" and "-2" are simply used to differentiate the rooms.

## events
in the tripleS simulator, there are multiple types of events. as of now, we only feature two major events, mass moving and (grand) gravity.

### mass moving
after the occupied HAUS become full, each member will either "choose" to stay in their original HAUS or move to the next HAUS. 

for example, based on the default HAUS:
- when the 6th member arrives, a mass moving event is initiated as HAUS 1 can only house 5 people.
- the 6th member is automatically put into HAUS 2.
- the other 5 members either choose to move to HAUS 2 or stay in HAUS 1.

### gravity
after your group reaches a certain number of members (specified in config.toml), a gravity (or grand gravity) will be initiated. gravity cannot be customised or controlled in any way, and every unit is assigned members at random. however, the number of members in every unit is as equal as possible.
