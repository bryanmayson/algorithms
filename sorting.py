"""
  Compilation of sorting algorithms
  
  Bryan Mayson
"""
def insertion_sort(alist):
    for i in range(1,len(alist)):
        while i>0 and alist[i-1] > alist[i]:
            alist[i-1],alist[i] = alist[i],alist[i-1]
            i-=1

def selection_sort(alist):
    minim = 0
    for i in range(len(alist)):
        for j in range(i+1,len(alist)):
            if alist[j] < alist[i] and alist[j] < alist[minim]:
                minim = j
        alist[minim],alist[i] = alist[i],alist[minim]
        
def partition(my_list,startIndex,lastIndex):
    pivot = alist[startIndex]
    lp = startIndex + 1
    rp = lastIndex
    while lp <= rp:
        while lp <= rp and my_list[lp] < pivot:
            lp = lp + 1
        while lp <= rp and my_list[rp] > pivot:
            rp = rp -1
        if lp <= rp:
            my_list[lp],my_list[rp] = my_list[rp],my_list[lp]
    my_list[startIndex],my_list[rp]= my_list[rp],my_list[startIndex]
    return rp

def quickSort(alist,first,last):
    if (last-first)>1:
        pivot_pos = partition(alist,first,last)
        quickSort(alist,firs,pivot_pos)
        quickSort(alist,pivot,pos+1,last)

def quickSelect (alist):
    k = len(alist)//2
    #partition
    # if k == index(pivot)
        return index
