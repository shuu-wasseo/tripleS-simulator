from random import randint, choice
import math
import json
import toml
from prettytable import PrettyTable
from colors import color
from plotext import tw

members = []
omembers = []

open('output.txt', 'w')
story = open('output.txt', 'a')

# members + events
config = toml.load(open("config.toml"))
prefix = config["prefix"]
members = config["members"]
colors = config["colors"]
sgrav = config["sgravity"]

def split(lis, count, goal):
    if count == 0:
        lis = [lis]
    if count < goal-1:
        nlis = []
        for x in lis:
            mid = int(len(x)/2)
            x = split([x[:mid], x[mid:]], count+1, goal)
            nlis.append(x)
        lis = nlis
    if count == 0:
        return lis[0]
    return lis

# HAUS classes + methods
ohaus = json.load(open("haus.json"))["haus"]

uhaus = ohaus.copy()
    
class b:
    def __init__(self, haus, room, bed, seoul):
        self.haus = haus
        self.room = room
        self.bed = bed
        self.seoul = seoul
        
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
    if bed == "":
        return ""
    else:
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
        p("\nmoving time!")
    
    beds = []
    for h in house:
        if h in hs:
            for room in house[h]:
                for bed in house[h][room]:
                    if move_event != "":
                        beds.append(b(h, room, bed, hs=="seoul"))
                    elif house[h][room][bed] == "":
                        beds.append(b(h, room, bed, hs=="seoul"))
                    
    for m in membs:
        found = False
        if hs == "seoul":
            for room in house["seoul"]:
                for bed in house["seoul"][room]:
                    if house["seoul"][room][bed] == m:
                        found = True
        if found:
            continue
        try:
            if move_event != "" and m.serial == length:
                bed = choice([bed for bed in beds if bed.haus == move_event])
            else:
                bed = choice(beds)
        except:
            p("oh dear! it appears we have run out of beds. time to wait for HAUS 3!")
            return house 
        else:
            if (move_event != "" and bed.haus == move_event) or move_event == "":
                if move_event != "":
                    for h in house:
                        if house != "seoul":
                            for room in house[h]:
                                for be in house[h][room]:
                                    if house[h][room][be] == m:
                                        house[h][room][be] = ""
                haus = edhaus(house, m, bed)
                beds.remove(bed)
                if len(membs) > 1:
                    tab.add_row([pm(m), pb(bed)])
                if hs == "seoul":
                    m.seoul = bed
                else:
                    m.beds.append(bed)
            else:
                haus = house
                if hs == "seoul":
                    m.seoul = bed
                else:
                    m.beds.append(m.beds[-1])

    if len(membs) > 1:
        p(tab)
    return haus


def perms(ls): # credits to geeksforgeeks i could not bother to do this on my own
    if len(ls) == 0:
        return []
 
    if len(ls) == 1:
        return [ls]
 
    l = []
 
    for i in range(len(ls)):
       m = ls[i]
 
       remLst = ls[:i] + ls[i+1:]
 
       # Generating all permutations where m is first
       # element
       for p in perms(remLst):
           l.append([m] + p)
    return l

def ugravity(membs, units):
    p("\ngrand unit gravity time!")
    tab = PrettyTable(["unit", "description"])
    for x in units:
        found = False
        for y in config["units"]:
            if y[0] == x:
                tab.add_row(y)
                found = True
                break
        if not found:
            tab.add_row([x, "null"])
    p(tab)
    tab = PrettyTable(units)
    ms = membs.copy()
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
        if not config["random_ugravity"]:
            subt = PrettyTable(["number"] + units)
            for n in range(len(perms(pair))):
                subt.add_row([n] + [pm(m) for m in perms(pair)[n]])
            print(f"\nround {x+1}:")
            print(subt)
            while 1:
                pick = input("pick the number of your desired permutation: ")
                try:
                    pair = perms(pair)[int(pick)]
                except:
                    pass
                else:
                    break
        tab.add_row([pm(m) for m in pair])
        for y in range(len(units)):
            try:
                pair[y].gravity.append(units[y])
            except:
                pass
    p(tab)
    return ms        

def tree(lis):
    dic = {"final": {"rem": []}}
    rounds = []

    def todic(lis, pround, depth):
        try:
            rounds[depth]
        except:
            rounds.append(0)
        pround["rem"] = lis
        for x in pround["rem"].copy():
            if type(x) == list:
                pround[f"round {rounds[depth]+1}"] = {"rem": x}
                rounds[depth] += 1
                pround["rem"].remove(x)
        for sround in pround.copy():
            if sround != "rem":
                pround[sround] = todic(pround[sround]["rem"], pround[sround], depth+1)
                if len(pround[sround].keys()) == 1:
                    pround[sround] = pround[sround]["rem"]
        
        return pround

    return todic(lis, dic["final"], 0)

def depth(d): # i stole this code from someone on stackoverflow
    if isinstance(d, dict):
        return 1 + (max(map(depth, d.values())) if d else 0)
    return 0

def rnd(dic, count, goal, r):
    thing = None
    if count < goal and type(dic) == dict or (count == 0 and goal == 0):
        for x in dic.copy():
            if x != "rem":
                if count == goal-1 or (count == 0 and goal == 0):
                    if (count == 0 and goal == 0):
                        ch = dic
                    else:
                        ch = dic[x]
                    table = PrettyTable(["number", "song"])
                    table.add_row([0, ch[0]])
                    table.add_row([1, ch[1]])
                    p(f"gravity depth {goal}, round {r}")
                    p(table)
                    if config["random_sgravity"]:
                        while 1:
                            try:
                                chosen = ch[int(input("pick the number of your desired song: "))]
                            except:
                                pass
                            else:
                                break
                    else:
                        chosen = choice(ch)
                    if count == 0 and goal == 0:
                        p(f"{chosen} has been picked as the title song for your group!")
                    else:
                        p(f"{chosen} has been picked.\n")
                    if not (count == 0 and goal == 0):
                        dic["rem"].append(chosen)
                        del dic[x]
                        thing = dic["rem"]
                        if len(dic.keys()) == 1:
                            dic = dic["rem"]
                    return dic, thing
                else:
                    if type(dic[x]) == dict and list(dic[x].keys()) != ["rem"]:
                        dic[x], thing = rnd(dic[x], count+1, goal, r)
                        if thing:
                            break
                    else:
                        continue

    return dic, thing

def sgravity(songs):
    p("\ngrand song gravity time!")
    if math.log(len(songs), 2) % 1 != 0:
        print("number of songs in sgravity should have a power of 2.")
        exit()
    else:
        tr = tree(split(songs, 0, math.log(len(songs), 2)))
    d = int(math.log(len(songs), 2)) 
    for x in range(d, -1, -1):
        count = 0
        while 1:
            count += 1
            tr, thing = rnd(tr, 0, x, count)
            if not thing:
                break
            
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

def brk():
    str = ""
    for x in range(tw()):
        str += "-"
    return str

def event(haus, omembers, number, hs, events, gravities, mmoves, tab, wave):
    if number == cbeds(uhaus, hs[:-1]) + 1 and len(hs) > 1:
        events = [["mmove"]] + events

    if len(events) == 0:
        haus = move(haus, [omembers[-1]], hs)
        try:
            bed = pb(omembers[-1].beds[-1])
        except:
            bed = ""
        tab.add_row([pm(omembers[-1]), color(omembers[-1].color, "white", omembers[-1].color), bed])
      
    moved = False
            
    for e in events: 
        match e[0]:
            case "mmove":
                mmoves += 1
                tab.add_row([pm(omembers[-1]), color(omembers[-1].color, "white", omembers[-1].color), "TBC"])
                wave += 1
                p(f"new wave of {prefix}!")
                p(f"wave {str(wave)}:")
                p(tab)
                tab = PrettyTable(["member", "color", "bed"])
                moved = True
                haus = move(haus, omembers, hs, hs[-1])
                phaus(haus)
                p(brk())
            case "ugravity" | "sgravity":
                gravities += 1
                haus = move(haus, [omembers[-1]], hs)
                if not moved:
                    tab.add_row([pm(omembers[-1]), color(omembers[-1].color, "white", omembers[-1].color), pb(omembers[-1].beds[-1])])
                    wave += 1
                    p(f"new wave of {prefix}!")
                    p(f"wave {str(wave)}:")
                    p(tab)
                    tab = PrettyTable(["member", "color", "bed"])
                phaus(haus)
                if e[0] == "ugravity":
                    omembers = ugravity(omembers, e[1])
                else:
                    sgravity(e[1])
                haus = move(haus, omembers, "seoul")
                phaus(haus, True)
                p(brk())
    
    if full(ohaus, "seoul") and len(events) > 0:
        p(f"the seoul HAUS is full.\n")

    return haus, gravities, mmoves, tab, wave

def summary():
    p("")
    maxg = 0
    maxm = 0
    
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

    tab = PrettyTable(["name", "serial", "color"] + gs + bs + ["seoul room", "seoul bed"])
    
    for m in omembers:
        beds = []
        for bed in m.beds:
            if bed != "":
                beds += [bed.haus, croom(bed.room), bed.bed]
            else:
                beds += ["", "", ""]
        try:
            seoul = [croom(m.seoul.room), m.seoul.bed]
        except:
            seoul = ["", ""]
        row = [m.name, prefix + str(m.serial), color(m.color, "white", m.color)] + m.gravity + beds + seoul
        tab.add_row(row)
        
    p(tab)

# main code
print()

length = len(members)

gravities = 0
mmoves = 1
wave = 0
tab = PrettyTable(["member", "color", "bed"])

for x in range(len(members)):
    events = []

    # add member to database
    if config["random_members"]:
        nmemb = choice(members)
    else:
        nmemb = members[0]
    new = memb(x+1, nmemb, [], [], "", "")
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

    for grav in config["ugravity"]:
        if x+1 == int(grav[0]):
            events.append(["ugravity", grav[1:]])

    for grav in config["sgravity"]:
        if x+1 == int(grav[0]):
            events.append(["sgravity", grav[1:]])
    
    om = omembers.copy()

    lis = event(uhaus, om, x+1, hs, events, gravities, mmoves, tab, wave)
    uhaus = lis[0]
    gravities = lis[1]
    mmoves = lis[2]
    tab = lis[3]
    wave = lis[4]

    
p("to be continued...")
phaus(uhaus, False, True)
phaus(uhaus, True, True)

# summary table
summary()
