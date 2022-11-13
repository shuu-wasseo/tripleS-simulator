from random import randint, choice
import math
import json
import toml

members = []
omembers = []

open('output.txt', 'w')
story = open('output.txt', 'a')

# members + events
config = toml.load(open("config.toml"))
prefix = config["prefix"]
members = config["members"]

# HAUS classes + methods
ohaus = json.load(open("haus.json"))

valid = True
if "seoul" not in ohaus.keys():
    valid = False
else:
    for room in ohaus["seoul"]:
        if type(ohaus["seoul"][room]) != list:
            valid = False
            break
    for haus in ohaus:
        if haus != "seoul":
            for room in ohaus[haus]:
                if type(ohaus[haus][room]) != dict:
                    valid = False
                    break

if not valid:
    print("your haus is invalid. please ensure that you have structured each room correctly.")
    exit()

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
                    print(house)
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
    for x in range(math.ceil(len(membs)/len(units))):
        pair = []
        for y in range(len(units)):
            try:
                picked = choice(membs)
            except:
                pass
            else:
                pair.append(pm(picked))
                membs.remove(picked)
        str = ""
        for x in range(len(units)):
            try:
                str += f"{pair[x]} in {units[x]}, "
            except:
                pass
        str = str[:-2]
        p(str)
    return ms

def csbeds(haus, c):
    count = 0
    for room in haus["seoul"]:
        count += len(haus["seoul"][room])
    if count >= c:
        return True
    else:
        return False

def smove(haus, members):
    haus = haus.copy()
    membs = members.copy()
    p("\nmoving into seoul HAUS!")
    for m in membs:
        if csbeds(haus, sum([int(room[0]) for room in list(haus["seoul"].keys())])):
            p("oh dear! the seoul HAUS does not have enough beds. time to wait for a renovation!")
            exit() 
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

def full(uhaus, hs):
    full = True
    for haus in uhaus:
        if haus in hs:
            for room in uhaus[haus]:
                for bed in uhaus[haus][room]:
                    if uhaus[haus][room][bed] == "":
                        full = False

    return full

def cbeds(uhaus, hs):
    count = 0
    for haus in uhaus:
        if haus in hs:
            for room in uhaus[haus]:
                for bed in uhaus[haus][room]:
                    count += 1
    
    return count

def event(haus, omembers, number, hs, events):
    if number == cbeds(uhaus, hs) + 1:
        events.append(["mmove"])

    if len(events) == 0:
        haus = move(haus, [omembers[-1]], hs)
    
    for e in events: 
        match e[0]:
            case "mmove":
                haus = move(haus, [omembers[-1]], hs, hs[-1])
                phaus(haus)
            case "gravity":
                haus = move(haus, [omembers[-1]], hs)
                phaus(haus)
                omembers = gravity(omembers, e[1])
                haus = smove(haus, omembers)
                phaus(haus, True)
                
    p("")

    if number == cbeds(uhaus, hs):
        p(f"{hs} is/are full.")

    if csbeds(uhaus, sum([int(room[0]) for room in list(haus["seoul"].keys())])):
        p(f"the seoul HAUS is full.")

    return haus

length = len(members)

for x in range(len(members)):
    events = []

    # add member to database
    if config["random"]:
        nmemb = choice(members)
    else:
        nmemb = members[0]
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
    hauses = list(dict.keys(ohaus))
    hauses.remove("seoul")
    for y in range(len(hauses)):
        if x+1 <= cbeds(uhaus, hauses[:y+1]):
            hs = hauses[:y+1]
            break

    for grav in config["gravity"]:
        if x+1 == int(grav[0]):
            events.append(["gravity", grav[1:]])
    
    om = omembers.copy()

    uhaus = event(uhaus, om, x+1, hs, events)
    
    p("")

p("to be continued...")
