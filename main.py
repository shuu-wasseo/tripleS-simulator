from random import randint, choice
import math
import time

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
            "upper bunk" : "",
            "lower bunk" : ""
        },
        "purple" : {
            "upper bunk" : "",
            "lower bunk" : "",
            "single" : ""
        }
    },
    "HAUS 2" : {
        "orange" : {
            "upper bunk" : "",
            "lower bunk" : ""
        },
        "pink" : {
            "upper bunk" : "",
            "lower bunk" : ""
        },
        "yellow" : {
            "upper bunk" : "",
            "lower bunk" : "",
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
    return text

def move(house, membs, hs, move_event=""):
    length = len(membs)
    if len(membs) > 1:
        p("\nmass moving event!")
    
    beds = []
    for h in house:
        if h in hs and h != "seoul":
            for room in house[h]:
                for bed in house[h][room]:
                    if move_event != "":
                        beds.append(b(h, room, bed))
                    elif house[h][room][bed] == "":
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
            if (move_event != "" and bed.haus == move_event) or move_event == "":
                if move_event != "":
                    for h in house:
                        for room in house[h]:
                            for be in house[h][room]:
                                if house[h][room][be] == m:
                                    house[h][room][be] = ""
                haus = edhaus(house, m, bed)
                beds.remove(bed)
                p(f"{pm(m)} has moved into {bed.haus}, {bed.room} room, {bed.bed} bed.")
            else:
                haus = house
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

def phaus(haus, seoul=False):
    if seoul:
        p(f"\nHAUS update: (seoul)")
    else:
        p(f"\nHAUS update:")
    for h in haus:
        if (h=="seoul") == seoul:
            for room in haus[h]:
                str = f"{h}, {room} room: "
                for bed in haus[h][room]:
                    if seoul:
                        str += pm(bed) + ", "
                    else:
                        try:
                            str += pm(haus[h][room][bed]) + ", "
                        except:
                            pass
                if str[-2:] == ", ":
                    str = str[:-2]
                p(str)


def event(ohaus, haus, omembers, number, hs):
    match number:
        case 5:
            haus = move(haus, [omembers[-1]], hs)
            p("HAUS 1 is full.")
            phaus(haus)
        case 6:
            haus = move(ohaus, omembers, ["HAUS 1", "HAUS 2"], "HAUS 2")
            phaus(haus)
        case 8:
            haus = move(haus, [omembers[-1]], hs)
            phaus(haus)
            omembers = gravity(omembers, ["aaa", "kre"])
            haus = smove(haus, omembers)
            phaus(haus, True)
        case 12:
            haus = move(haus, [omembers[-1]], hs)
            p("HAUS 1 and 2 are full.")
            phaus(haus)
        case _:
            haus = move(haus, [omembers[-1]], hs)

    return haus

for x in range(len(members)):
    length = len(members)

    # add member to database
    nmemb = choice(members)
    new = memb(x+1, nmemb)
    omembers.append(new)
    members.remove(nmemb)

    # reveal new member
    def genhex():
        n = hex(randint(0,255))[2:]
        if len(n) == 1:
            return "0" + n
        return n
    hexc = "#" + genhex() + genhex() + genhex()
    p(f"{prefix}{x+1} is revealed to be {omembers[-1].name}, with color {hexc}.")

    # moving
    if x+1 <= 5:
        hs = ["HAUS 1"]
    elif x+1 <= 12:
        hs = ["HAUS 1", "HAUS 2"]

    uhaus = event(ohaus, uhaus, omembers, x+1, hs)

    p("")

    if x+1 == length and x+1 not in [5, 6, 8, 12]:
        phaus(uhaus)

p("to be continued...")
