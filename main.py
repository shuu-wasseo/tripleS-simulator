from random import randint, choice
import math
import json
import toml
from prettytable import PrettyTable
from colors import color

members = []
omembers = []

open('output.txt', 'w')
story = open('output.txt', 'a')

# members + events
config = toml.load(open("config.toml"))
prefix = config["prefix"]
members = config["members"]
colors = config["colors"]

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

def croom(room):
    try:
        rm = color(room, "white", [x[1] for x in colors if x[0] == room][0])
    except:
        return room
    else:
        return rm

def pb(bed):
    return f"{bed.haus}, {croom(bed.room)} room, {bed.bed} bed"

# member classes + methods
class memb:
    def __init__(self, serial, name, gravity, beds, seoul, color):
        self.serial = serial
        self.name = name
        self.beds = beds
        self.gravity = gravity
        self.seoul = seoul
        self.color = color

def pm(memb):
    return f"{prefix}{memb.serial} {memb.name}"
       
def p(text):
    story.write(str(text) + "\n")
    print(text)
    return text

def move(house, membs, hs, move_event=""):
    length = len(membs)
    if len(membs) > 1:
        tab = PrettyTable(["member", "room"])
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
            return  
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
                if len(membs) > 1:
                    tab.add_row([pm(m), pb(bed)])
                m.beds.append(bed)
            else:
                haus = house
                m.beds.append(m.beds[-1])

    if len(membs) > 1:
        p(tab)
    return haus
    
def gravity(membs, units):
    tab = PrettyTable(units)
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
                pair.append(picked)
                membs.remove(picked)
        tab.add_row([pm(m) for m in pair])
        for y in range(len(units)):
            try:
                pair[y].gravity.append(units[y])
            except:
                pass
    p(tab)
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
    tab = PrettyTable(["member", "room"])
    haus = haus.copy()
    membs = members.copy()
    p("\nmoving into seoul HAUS!")
    for m in membs:
        found = False
        for x in haus["seoul"]:
            if m in haus["seoul"][x]:
                found = True
        if not found:
            if csbeds(haus, sum([int(room[0]) for room in list(haus["seoul"].keys())])):
                p("oh dear! the seoul HAUS does not have enough beds. time to wait for a renovation!")
                break
            while 1:
                new = choice(list(haus["seoul"].keys()))
                if len(haus["seoul"][new]) < int(new.split("-")[0]):
                    haus["seoul"][new].append(m)
                    m.seoul.append(new)
                    tab.add_row([pm(m), new])
                    break

    p(tab)
    return haus

def phaus(haus, seoul=False, final=False):
    if seoul:
        str = f"\nHAUS update: (seoul)"
    else:
        str = f"\nHAUS update:"
    if final:
        p(str.replace("HAUS update", "final HAUS"))
    else:
        p(str)
    tab = PrettyTable(["room", "members"])
    for h in haus:
        if (h=="seoul") == seoul:
            for room in haus[h]:
                row = [f"{h}, {croom(room)} room", ""]
                for bed in haus[h][room]:
                    if seoul:
                        row[-1] += pm(bed) + ", "
                    else:
                        try:
                            row[-1] += pm(haus[h][room][bed]) + ", "
                        except:
                            pass
                row[-1] = row[-1][:-2]
                tab.add_row(row)
    p(tab)

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

def event(haus, omembers, number, hs, events, gravities, mmoves, tab):
    if number == cbeds(uhaus, hs[:-1]) + 1 and len(hs) > 1:
        events.append(["mmove"])

    if len(events) == 0:
        haus = move(haus, [omembers[-1]], hs)
        tab.add_row([pm(omembers[-1]), color(omembers[-1].color, "white", omembers[-1].color), pb(omembers[-1].beds[-1])])
    
    moved = False
            
    for e in events: 
        match e[0]:
            case "mmove":
                mmoves += 1
                tab.add_row([pm(omembers[-1]), color(omembers[-1].color, "white", omembers[-1].color), "TBC"])
                p(f"new wave of {prefix}!")
                p(tab)
                tab = PrettyTable(["member", "color", "bed"])
                moved = True
                haus = move(haus, omembers, hs, hs[-1])
                phaus(haus)
            case "gravity":
                gravities += 1
                haus = move(haus, [omembers[-1]], hs)
                if not moved:
                    tab.add_row([pm(omembers[-1]), color(omembers[-1].color, "white", omembers[-1].color), pb(omembers[-1].beds[-1])])
                    p(f"new wave of {prefix}!")
                    p(tab)
                    tab = PrettyTable(["member", "color", "bed"])
                phaus(haus)
                omembers = gravity(omembers, e[1])
                haus = smove(haus, omembers)
                phaus(haus, True)
                
    if csbeds(uhaus, sum([int(room[0]) for room in list(haus["seoul"].keys())])) and len(events) > 0:
        p(f"the seoul HAUS is full.\n")

    return haus, gravities, mmoves, tab

def summary():
    p("")
    maxg = 0
    maxm = 0
    maxs = 0

    for memb in omembers:
        if len(memb.gravity) > maxg:
            maxg = len(memb.gravity)
        if len(memb.beds) > maxm:
            maxm = len(memb.beds)

    for memb in omembers:
        while len(memb.gravity) < maxg:
            memb.gravity = [""] + memb.gravity
        while len(memb.beds) < maxm:
            memb.beds = [""] + memb.beds

    gs = []
    bs = []

    for x in range(maxg):
        gs.append(f"unit {x+1}")
    for x in range(maxm):
        bs += [f"haus {x+1}", f"room {x+1}", f"bed {x+1}"]

    tab = PrettyTable(["name", "serial", "color"] + gs + bs + ["seoul"])
    
    for m in omembers:
        beds = []
        for bed in m.beds:
            if bed != "":
                beds += [bed.haus, croom(bed.room), bed.bed]
            else:
                beds += ["", "", ""]
        if m.seoul == []:
            m.seoul = [""]
        row = [m.name, prefix + str(m.serial), color(m.color, "white", m.color)] + m.gravity + beds + m.seoul
        tab.add_row(row)
        
    p(tab)

length = len(members)

gravities = 0
mmoves = 1
tab = PrettyTable(["member", "color", "bed"])

for x in range(len(members)):
    events = []

    # add member to database
    if config["random"]:
        nmemb = choice(members)
    else:
        nmemb = members[0]
    new = memb(x+1, nmemb, [], [], [], "")
    omembers.append(new)
    members.remove(nmemb)

    # reveal new member
    def genhex():
        n = hex(randint(0,255))[2:]
        if len(n) == 1:
            return "0" + n
        return n
    hexc = "#" + genhex() + genhex() + genhex()
    omembers[-1].color = hexc
            
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

    lis = event(uhaus, om, x+1, hs, events, gravities, mmoves, tab)
    uhaus = lis[0]
    gravities = lis[1]
    mmoves = lis[2]
    tab = lis[3]

    
p("to be continued...")
phaus(uhaus, False, True)
phaus(uhaus, True, True)

# summary table
summary()
