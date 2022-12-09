lis = ["10", "a", "b", "c", "d", "e", "f", "g", "h"]

def split(lis, count, goal):
    if count == 0:
        lis = [lis]
    if count < goal-1:
        nlis = []
        for x in lis:
            mid = int(len(x)/2)
            print("before", x)
            x = split([x[:mid], x[mid:]], count+1, goal)
            print("after", x)
            nlis.append(x)
        lis = nlis
    print(lis)
    if count == 0:
        return lis[0]
    return lis

print(split(lis[1:], 0, 3))
