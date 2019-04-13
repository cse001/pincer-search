def readDatabase():
    f = open("database.txt","r")
    items=f.readline()
    items=items.strip().split(',')
    T = []
    for line in f.readlines():
        T.append(line.strip())
    tdb=[]
    temp = []
    for data in T:
        tempData = data.strip().split(',')
        for i in range(len(items)):
            if tempData[i] == '1':
                temp.append(items[i])
        tdb.append(temp.copy())
        temp.clear()
    return items.copy(),tdb.copy()
def getSupport(items,database):
    support = []
    if not items:
        return support.copy()
    for item in items:
        support.append(0)
    for data in database:
        tempData = data.copy()
        for i in range(len(items)):
            flag = 0
            for item in items[i]:
                if item not in tempData:
                    flag =1
            if flag == 0:
                support[i] = support[i]+1
    # for i in range(len(items)):
    #     if len(items[i])==0:
    #         support[i]=0
    return support.copy()
