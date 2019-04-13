#!/usr/bin/python3
from readDatabase import *
from prettytable import PrettyTable
def uniqueList(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list.copy()
def mfcs_gen(mfcs,sk):
    print ("MFCS GENERATOR PROGRAM")
    print (mfcs, "MFCS")
    print (sk, "SK")
    for s in sk:
        for m in mfcs:
            flag = 0
            for ss in s:
                if ss not in m:
                    flag = 1
            if flag != 1:
                #This is where I will remove one by one sk and compare.
                for ss in s:
                    temp_mfcs = m.copy()
                    temp_mfcs.remove(ss)
                    mfcs.append(temp_mfcs.copy())
                    temp_mfcs.clear()
                mfcs.remove(m.copy())
                temp_mfcs = mfcs.copy()
                for x in temp_mfcs:
                    for y in temp_mfcs:
                        if set(x).issubset(set(y)) and x != y:
                            mfcs.remove(x)
                            break
    mfcs = uniqueList(mfcs.copy())
    print (mfcs,"Updated MFCS")
    return mfcs.copy()
def recovery(ck , mfs,k):
    print ("The recovery")
    ck1 = []
    for c in ck:
        for m in mfs:
            tempC = c[:k-1]
            tempM = m[:k-1]
            if tempC == tempM:
                tempCk = tempC.copy()
                for i in range(k,len(m)):
                    ck1.append(m[i])
    return ck1.copy()
def mfs_prune(ck,mfs):
    removedList = []
    print("The MFS Pruning")
    for x in ck:
        for y in mfs:
            if set(x).issubset(set(y)):
                ck.remove(x)
                removedList.append(x.copy())
                break
    return ck.copy(),mfs.copy(),removedList.copy()
def mfcs_prune(ck1,mfcs):
    print ("MFCS Prune")
    for x in ck1:
        for y in mfcs:
            if not set(x).issubset(set(y)):
                ck1.remove(x)
                print (x, "Removed in MFCS Prune")
                break
    return ck1.copy()
def generate_c_k_plus_one(ck):
    ck1 = []
    if not ck:
        return ck1.copy()
    lenCk = len(ck)
    lent = len(ck[0])
    ckcopy = ck.copy()
    for i in range(lenCk):
        for j in range(i+1,lenCk):
            l1 = ckcopy[i][0:lent-1]
            l2 = ckcopy[j][0:lent-1]
            l1.sort()
            l2.sort()
            if l1 == l2 and ckcopy[i][-1] != ckcopy[j][-1]:
                temp = ckcopy[i].copy()
                temp.append(ckcopy[j][-1])
                ck1.append(temp.copy())
                temp.clear()
    ck1 = uniqueList(ck1.copy())
    for c in ck1:
        if not c:
            ck1.remove(c.copy())
    print ("c k+1 Generated")
    return ck1
def print_values(L,S,C,MFCS,MFS):
    print (L,"L")
    print (S, "S")
    print (C, "C")
    print (MFCS, "MFCS")
    print (MFS, "MFS")
    return
def init_pincer(itemset):
    #Initialising the Algorithm
    # Terminology
    # L contains l0, l1, l2
    # S contains s0, s1, s2
    # C contains c0, c1, c2
    L = []
    l = []
    S = []
    s = []
    C = []
    c = []
    MFCS =[]
    MFS = []
    #C1 is the List of All Items, C0 is empty
    D = []
    t=[]
    C.append(c.copy())
    for item in itemset:
        c.append(item)
        t.append(item)
        D.append(c.copy())
        c.clear()
    C.append(D.copy())
    #L0 is empty
    L.append(l.copy())
    #s0 is empty
    S.append(s.copy())
    MFCS.append(t.copy())
    return L.copy(),S.copy(),C.copy(),MFCS.copy(),MFS.copy()
def pincer_search(items,database):
    item_count = len(items)
    support_count = 3
    L,S,C,MFCS,MFS = init_pincer(items.copy())
    k = 1
    print_values(L.copy(),S.copy(),C.copy(),MFCS.copy(),MFS.copy())
    while (len(C[k])!=0 ):
        print ("-------------------Pass-------------------------" + str(k))
        print (C[k],"The Ck")
        support_ck = getSupport(C[k].copy(),database.copy())
        print (support_ck,"Support cK")
        print (MFCS, "The MFCS")
        support_mfcs = getSupport(MFCS.copy(),database.copy())
        print (support_mfcs, "Support MFCS")
        # Evaluate MFS = MFS + (Most Frequent in MFCS)
        for i in range(len(MFCS)):
            if support_mfcs[i] >=support_count:
                MFS.append(MFCS[i].copy())
        tempSk = []
        # Generate The SK
        for i in range(len(C[k])):
            if support_ck[i] <support_count:
                tempSk.append(C[k][i])
        S.append(tempSk.copy())
        # Call MFCS Gen if sK is not Null
        if len(S[k])!=0:
            print ("MFCS Gen")
            MFCS = mfcs_gen(MFCS.copy(),S[k].copy())
        # Call the MFS Pruning Procedure
        removedList = []
        if len(MFS)!=0:
            C[k],MFS, removedList=mfs_prune(C[k].copy(),MFS.copy())
        #Generate Candidates from cK to cK+1
        for s in S[k]:
            C[k].remove(s)
        c = generate_c_k_plus_one(C[k].copy())
        c = uniqueList(c.copy())
        print(c,"cK+1 generated")
        # If any Frequent itemset in cK was removed during MFS pruning, call recovery on cK+1
        ck = c.copy()
        tempCk = []
        if removedList:
            tempCk = recovery(C[k].copy(),MFS.copy(),k)
        if tempCk:
            ck.append(tempCk.copy())
        #Call MFCS Prune
        ck = mfcs_prune(ck.copy(),MFCS.copy())
        C.append(ck.copy())
        print (support_ck, "Support CK")
        print (support_mfcs, "Support MFCS")
        print (S[k], "SK")
        # print (C[k+1], "Generated c K+1")
        k = k+1
    if MFCS:
        support_mfcs = getSupport(MFCS.copy(),database.copy())
        for i in range(len(MFCS)):
            if support_mfcs[i] >=support_count:
                MFS.append(MFCS[i].copy())
    return MFS
def main():
    items,database = readDatabase()
    support = getSupport([['A1'],['A4'],['A3']], database.copy())
    mfs = pincer_search(items.copy(),database.copy())
    mfs = uniqueList(mfs.copy())
    print (mfs,"The Most Frequent Set")
    supp = getSupport(mfs.copy(),database.copy())
    print (supp)
    x = PrettyTable()
    x.field_names = ["Set","Frequency"]
    for i in range(len(supp)):
        x.add_row([mfs[i],supp[i]])
    print (x)

if __name__ == '__main__':
    main()
