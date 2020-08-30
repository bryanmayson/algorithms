def readFile(name):
    """
        reads a string which should be the name of a txt file,reads it content
        and imports its contents into a list
        
        Bryan Mayson
        9.8.2018
        
        :param: name: the name of the .txt file
        :return: temp: alist containing of all the items from the .txt file
        :precondition: .txt file should exist in the same folder location of the python file
        :postcondition: temp will contain all the contents of the .txt file
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(MN) in which N represents the size of the list and k representing the alphabets
    """
    f = open(name ,"r+")
    temp=[]
    for lines in f:
        temp.append(lines.strip("\n"))
    return temp

def countSort(alist,index=0,blist = None):
    """
        sorts alist based on one char
        
        Bryan Mayson
        9.8.2018
        
        :param: alist: can be alist or a string which would undergo countSort
        :return: temp_a: a list containing a sorted alist
        :precondition: not an int value
        :postcondition: temp_a would contain the sorted version of alist
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(MN) in which N represents the size of the list and k representing the alphabets
    """
    count_a = [0] * 27
    temp_a = []

    for i in range(len(count_a)):
        count_a[i] = []
        
    # for radix_sort
    if blist is not None:
        count_b = [0] * 27
        temp_b =[]
        for i in range(len(count_b)):
            count_b[i] = []
     
    # appending at proper index
    for i in range(len(alist)):
        position = ord(alist[i][index])-96
        if position < 0:
            position = 0
        count_a[position].append(alist[i])
        # for radix_only
        if blist is not None:
            count_b[position].append(blist[i])
    
    for i in range(len(count_a)):
        temp_a += count_a[i]
        
    if blist is not None:
        for i in range(len(count_b)):
            temp_b += count_b[i]
    
    if blist is not None:
        return temp_a,temp_b
    return temp_a

def maxLength(alist):
    """
        obtains the length of the longest string within alist
        
        Bryan Mayson
        9.8.2018
        
        :param: alist: a list which would undergo the search
        :return: maximum: the longest string length within alist
        :precondition: None
        :postcondition: maximum would hold the length of the longest string in the list
        :worse case:
            time complexity = O(N) in which N represents the size of the list
        space complexity = O(1)
    """
    maximum = 0
    for i in range(len(alist)):
        if len(alist[i])> maximum:
            maximum = len(alist[i])
    return maximum

def radixSort(anagramList,wordList= None):
    """
        sorts alist base on all the character values within its item
    
        Bryan Mayson
        9.8.2018
        
        :param: anagramList : the list which the sort will be based from
                wordList: the list which would follow the actions carried out on anagramList        
        :return: anagramList: sorted version of the list
                wordList: sorted version of the list
        :precondition: None
        :postcondition: anagramList/ Both list would be sorted
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(MN) in which N represents the size of the list and M representing the alphabets
    """
    # gets the max length char
    maximum = maxLength(anagramList)
    # for each index of the list of words
    while maximum > 0:
        if wordList is not None:
            anagramList , wordList = countSort(anagramList,maximum-1,wordList)
        else:
            anagramList = countSort(anagramList,maximum-1)
        maximum -=1
    if wordList is None:
        return anagramList
    else:
        return anagramList,wordList

def anagramList(alist):
    """
        each string within the list will be modified into an angaram
    
        Bryan Mayson
        9.8.2018
        
        :param: alist: the list which its items would be modified
        :return: temp: a list containing the modified items
        :precondition: None
        :postcondition: temp would contain the new list
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(MN) in which N represents the size of the list and k representing the alphabets
    """
    temp=[]
    for i in range(len(alist)):
        temp.append(countSort(alist[i]))
    return temp

def padding(anagram):
    """
        adds a speacial character to an item until it reaches its desired length
        
        Bryan Mayson
        9.8.2018
        
        :param: anagram: the item which would undergo padding
        :return: anagram: a padded verision of the list
        :precondition: None
        :postcondition: anagram would be padded now
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(1)
    """
    maxLen = maxLength(anagram)
    for i in range(len(anagram)):
        while len(anagram[i]) < maxLen:
            anagram[i] += "*"

def mostFreq(charList):
    """
        finds the most frequent item within the list
        
        Bryan Mayson
        9.8.2018
        
        :param: charlist: the list which would be searched through to obtain its most frequent item
        :return: freq_value: the frequent item
        :precondition: None
        :postcondition: freqValue will contain the most frequent item, counter will contain the ammount of occurance, freq_greatest will hold the greatest occurence
        :worse case:
            time complexity = O(N) in which N represents the size of the list
            space complexity = O(1)
    """
    freq_value = charList[0]
    counter = 0
    freq_greatest = 0
    for i in range(1,len(charList)):
        # if prev value dif curr value reset counter
        if charList[i-1] != charList[i]:
            counter = 0
        if counter >freq_greatest:
            freq_greatest = counter
            freq_value = charList[i]
        counter+=1
    return freq_value
            
def obtainWords(charList,wordList,target):
    """
        obtains the group of words of the target anagram
        
        Bryan Mayson
        9.8.2018
        
        :param: charlist: the list of anagrams which would be used to obtain its actual words
                wordList: the actual word itself
                target: the anagram desired
        :return: statement: all the words of the largest group of anagrams
        :precondition: None
        :postcondition: statemnet would contain all the possible words built up from the anagram
        :worse case:
            time complexity = O(log N + W) in which N represents the size of the list ;in which W represent the number of outputs
            space complexity = O(MN) in which N represents the size of the list and M representing the alphabets
    """
    statement =" "
    index = binarySearch(charList,target)
    #Obtain Starting Index
    start = loopToFront(index,charList) 
    #Obtain last Index
    end = loopToEnd(index,charList)
            
    for i in range(start,end+1):
        statement += " " + wordList[i]
    return statement
   
def loopToFront(index,alist):
    """
        loop to the first occurence of the anagram in the cluster
        
        Bryan Mayson
        9.8.2018
        
        :param: index: any point within the cluster
                alist: the list which contains the cluster
        :return: index: first occurence of the the anagram
        :precondition: None
        :postcondition: index will contain the first occurence of the the anagram
        :worse case:
            time complexity = O(W) in which W represent the number of outputs
            space complexity = O(1)
    """
    while index > 0 and alist[index] == alist[index-1]:
        index-=1
    return index

def loopToEnd(index,alist):
    """
        loop to the last occurence of the anagram in the cluster
        
        Bryan Mayson
        9.8.2018
        
        :param: index: any point within the cluster
                alist: the list which contains the cluster
        :return: index: last occurence of the the anagram
        :precondition: None
        :postcondition: index will contain the last occurence of the the anagram
        :worse case:
            time complexity = O(W) in which W represent the number of outputs
            space complexity = O(1)
    """
    while index < len(alist)-1 and alist[index] == alist[index+1]:
        index+=1
    return index

def getScrabbleWords(blist,alist,recieve,maxLen):
    """
        obtains the possible words which could be built up by the anagram of recieve
        
        Bryan Mayson
        9.8.2018
        
        :param: blist: the anagramList
                alist: the wordList
                recieve: the query string
                maxLen: the length of the longest string in the list
        :return: None
        :precondition: None
        :postcondition: index will contain the first occurence of the the anagram
        :worse case:
            time complexity = O(k log N + W) in which k represents length of the query string , N representing the size of the list and W representing the size of the output.
            space complexity = O(k) k represents length of the query string
    """
    #TASK2    
    #arrange word into alphabetical order
    word = countSort(recieve)
         
    # word padding
    for i in range(maxLen):
        if len(word)< maxLen:
            word+="*"
                
    statement=""
    try:
        #Binary Search
        index = binarySearch(blist,word)
        #Obtain Starting Index
        start = loopToFront(index,blist) 
        #Obtain last Index
        end = loopToEnd(index,blist)
            
        for i in range(start,end+1):
            statement += " " + alist[i]
    except:
        statement =""
    print("\nWords without using a wildcard:" + statement)
    
def binarySearch(charList,word):
    """
        binarySearch looks throught the anagramList through binary search for the word being searched
        
        Bryan Mayson
        9.8.2018
        
        :param: charList: the anagramList
                word: the the word being searched for
        :return: lo: the index which the itme was found
        :precondition: None
        :postcondition: lo and hi would eventually be next together
        :worse case:
            time complexity = O(k log N + W) in which k represents length of the query string , N representing the size of the list and W representing the size of the output.
            space complexity = O(k) k represents length of the query string
    """
    lo = 0
    hi = len(charList)
    while lo < hi and (hi-lo)>0:
        mid = (lo+hi)//2
        if word == charList[mid]:
            return mid
        if word > charList[mid]:
            lo = mid + 1
            
        else:
            hi = mid-1
    if len(charList) > 0 and charList[lo] == word:
        return lo
    else:
        raise Exception 
 
def getWildcardWords(blist,alist,recieve,maxLen):
        """
            obtains the possible words which could be built up by the anagram of recieve and any extra character
            
            Bryan Mayson
            9.8.2018
            
            :param: blist: the anagramList
                    alist: the wordList
                    recieve: the query string
                    maxLen: the length of the longest string in the list
            :return: None
            :precondition: None
            :postcondition: index will contain the first occurence of the the anagram
            :worse case:
                time complexity = (k log N + kW in which k represents length of the query string , N representing the size of the list and W representing the size of the output.
                space complexity = O(k + W) k represents length of the query string
        """
        #TASK3
        possible=[]
        for i in range(0,26):
            temp = ""
            temp+= recieve + chr(i + 97)
            # sort into alphabetical order
            temp = countSort(temp)
            #pads the string
            for i in range(maxLen):
                if len(temp)< maxLen:
                    temp+="*"
            try:  
                #Binary Search
                index = binarySearch(blist,temp)
                #Obtain Starting Index
                start = loopToFront(index,blist) 
                #Obtain last Index
                end = loopToEnd(index,blist)
                
                for i in range(start,end+1):
                    possible.append(alist[i])

            except:
                pass;
        
        
        statement = ""
        possible = radixSort(possible)
        for i in range(len(possible)):
            statement += " " + possible[i]
        print("Words using a wildcard:" + statement + "\n")
                   

def largestAnagram(filename):
    """
        obtains most frequent anagram within a text file
        
        Bryan Mayson
        9.8.2018
        
        :param: filename: the text file being read
        :return: blist,alist = anagramList , wordList
        :precondition: textfile must exist
        :postcondition: None
        :worse case:
            time complexity = O(MN) in which N represents the size of the list and M representing the alphabets
            space complexity = O(MN) in which N represents the size of the list and M representing the alphabets
    """
    alist = readFile(filename)                                                  # TC -> O(N)
    #obtain the max possible len of string in a list    
    blist=anagramList(alist)                                                    # TC -> O(N); SC -> O(N)
    padding(blist)                                                              # TC -> O(N*c) but c may be insignificant ; SC -> O(N)
    blist,alist=radixSort(blist,alist)
    
    print("The largest group of anagrams:"+ obtainWords(blist,alist,mostFreq(blist)))
    
    return alist,blist
