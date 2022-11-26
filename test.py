import math

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
        for sround in pround.copy():
            if sround == "rem" and pround[sround] == []:
                del pround[sround]

        return pround

    dic = todic(lis, dic["final"], 0)

    return dic

def finddepth(dic, count, goal):
    if count < goal:
        for x in dic:
            if type(dic[x]) == dict:
                return dic, finddepth(dic[x], count+1, goal)
            elif type(dic[x]) == list and count == goal-1:
                return dic, dic[x]
    else:
        return dic, None

lis = [[["a", "b"], ["c", "d"]], [["e", "f"], ["g", "h"]]]
