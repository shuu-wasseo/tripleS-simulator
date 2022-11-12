from random import randint, choice
import math

members = []
omembers = []

members = open('input.txt', "r").read().splitlines()
prefix = members[0]
members = members[1:]
open('output.txt', 'w')
story = open('output.txt', 'a')

# HAUS classes + methods
ohaus = {
    "HAUS 1" : {
        "mint" : {
            "upper" : "",
            "lower" : ""
        },
        "purple" : {
            "upper" : "",
            "lower" : "",
            "single" : ""
        }
    },
    "HAUS 2" : {
        "orange" : {
            "upper" : "",
            "lower" : ""
        },
        "pink" : {
            "upper" : "",
            "lower" : ""
        },
        "yellow" : {
            "upper" : "",
            "lower" : "",
            "single" : ""
        }
    },
    "seoul" : {
        "2-1" : [],
        "2-2" : [],
        "4" : []
    }
}

uhaus = ohaus.copy()
    
class b:
    def __init__(self, haus, room, bed):
        self.haus = haus
        self.room = room
        self.bed = bed

def edhaus(haus, memb, bed):
    dic = haus
    dic[bed.haus][bed.room][bed.bed] = memb
    return dic 

# member classes + methods
class memb:
    def __init__(self, serial, name):
        self.serial = serial
        self.name = name

def pm(memb):
    return f"{prefix}{memb.serial} {memb.name}"
       
def p(text):
    story.write(text + "\n")
    print(text)

def move(house, membs, hs, move_event=""):
    length = len(membs)
    if len(membs) > 1:
        p("\nmass moving event!")
    
    beds = []
    for h in house:
        if h in hs and h != "seoul":
            for room in house[h]:
                for bed in house[h][room]:
                    if house[h][room][bed] == "":
                        beds.append(b(h, room, bed))

    for m in membs:
        try:
            if move_event != "" and m.serial == length:
                bed = choice([bed for bed in beds if bed.haus == move_event])
            else:
                bed = choice(beds)
        except:
            p("oh dear! it appears we have run out of beds. time to wait for HAUS 3!")
            exit()
        else:
            haus = edhaus(house, m, bed)
            beds.remove(bed)
            p(f"{pm(m)} has moved into {bed.haus}, {bed.room} room, {bed.bed} bed.")
    
    return haus
    
def gravity(membs, units):
    ms = membs.copy()
    p("\ngrand gravity time!")
    for x in range(math.floor(len(membs)/len(units))):
        pair = []
        for y in range(len(units)):
            try:
                picked = choice(membs)
            except:
                pass
            else:
                pair.append(pm(picked))
                membs.remove(picked)
        p(f"{pair[0]} in {units[0]}, {pair[1]} in {units[1]}")
    return ms

def smove(haus, membs):
    haus = haus.copy()
    p("\nmoving into seoul HAUS!")
    for m in membs:
        while 1:
            new = choice(list(haus["seoul"].keys()))
            if len(haus["seoul"][new]) < int(new.split("-")[0]):
                haus["seoul"][new].append(m)
                p(f"{pm(m)} has moved into room {new} in the seoul HAUS.")
                break
    return haus

def event(ohaus, haus, omembers, number, hs):
    match number:
        case 5:
            haus = move(haus, [omembers[-1]], hs)
            p("HAUS 1 is full.")
        case 6:
            ohaus = {
                "HAUS 1" : {
                    "mint" : {
                        "upper" : "",
                        "lower" : ""
                    },
                    "purple" : {
                        "upper" : "",
                        "lower" : "",
                        "single" : ""
                    }
                },
                "HAUS 2" : {
                    "orange" : {
                        "upper" : "",
                        "lower" : ""
                    },
                    "pink" : {
                        "upper" : "",
                        "lower" : ""
                    },
                    "yellow" : {
                        "upper" : "",
                        "lower" : "",
                        "single" : ""
                    }
                },
                "seoul" : {
                    "2-1" : [],
                    "2-2" : [],
                    "4" : []
                }
            }
            haus = move(ohaus, omembers, ["HAUS 1", "HAUS 2"])
        case 8:
            haus = move(haus, [omembers[-1]], hs)
            omembers = gravity(omembers, ["aaa", "kre"])
            haus = smove(haus, omembers)
        case 12:
            haus = move(haus, [omembers[-1]], hs)
            p("HAUS 1 and 2 are full.")
        case _:
            haus = move(haus, [omembers[-1]], hs)

    return haus

for x in range(len(members)):
    # add member to database
    nmemb = choice(members)
    new = memb(x+1, nmemb)
    omembers.append(new)
    members.remove(nmemb)

    # reveal new member
    hexc = "#" + hex(randint(0,255))[2:] + hex(randint(0,255))[2:] + hex(randint(0,255))[2:]
    p(f"{prefix}{x+1} is revealed to be {omembers[-1].name}, with color {hexc}.")

    # moving
    if x+1 <= 5:
        hs = ["HAUS 1"]
    elif x+1 <= 12:
        hs = ["HAUS 1", "HAUS 2"]

    uhaus = event(ohaus, uhaus, omembers, x+1, hs)

    p("")

p("to be continued...")
