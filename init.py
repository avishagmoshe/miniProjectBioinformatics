
def findCog(currLine, cogList):
    check_cog_list = cogList.copy()
    for i in range(len(currLine)):
        for cog in cogList:
            if cog in currLine[i] and cog != 'X':
                if cog in check_cog_list:
                    check_cog_list.remove(cog)
    if len(check_cog_list) == 0:
        return 1
    return 0


def smallerThenWindow(currLine, currList, flag, NewList, LastGenomeLen):
    currList = currLine
    if flag == 1:  # the first line in new genom
        NewList.append(currList)

    else:  # im in the middle of specipic genom and we need to check if the window already exciset

        pointer = NewList[LastGenomeLen:]
        existP = 0
        for i in range(len(pointer)):
            for j in range(min(len(currLine), len(pointer))):
                if len(currLine) != len(pointer[j]):
                    existP = existP + 1
                    break
                if currLine[j] != pointer[i][j]:
                    existP = existP + 1
                    break
        if existP == len(pointer):
            NewList.append(currList)


def biggerThenWindow(currLine, currList, flag, NewList, LastGenomeLen, window, cogList):
    for i in range(len(currLine)):
        if i + window <= len(currLine):
            foundFlag = 0
            if(findCog(currLine[i:i + window],cogList)):
                foundFlag = 1
            if foundFlag == 1:
                currList = currLine[i:i + window]
                if flag == 1:
                    NewList.append(currList)
                else:  # we need to check if the list is already exist

                    pointer = NewList[LastGenomeLen:]
                    existP = 0
                    for i in range(len(pointer)):
                        for j in range(min(len(currLine), len(pointer))):
                            if len(currLine) != len(pointer[j]):
                                existP = existP + 1
                                break
                            if currLine[j] != pointer[i][j]:
                                existP = existP + 1
                    if existP == len(pointer):
                        NewList.append(currList)


def main(filename,window,cogList,query):

    file = open(filename, "r")
    dataLines = file.readlines()
    NewList = list()

    genom = 0
    counter = 0
    flag = 0
    LastGenomeLen = 0

    for line in dataLines:

        currLine = line.split('\t')
        currLine[-1] = currLine[-1].strip()
        if currLine[-1] == '':
            currLine.pop()
        firstWord = currLine[0].split('#')  # update the flag if its new genom or not
        if line != '\n':
            if firstWord[4] != genom:
                genom = firstWord[4]  # in which genome we are
                counter = counter + 1  # how many genom are there
                flag = 1
                LastGenomeLen = len(NewList)
            else:
                flag = 0

        currLine = currLine[1:len(currLine)]  # cutting the start and leave only the genes

        if len(currLine) > query - 1:  # cut lines without inaf genes
            if findCog(currLine, cogList):  # taking only relevant lines
                currList = list()
                if len(currLine) <= window:
                    smallerThenWindow(currLine, currList, flag, NewList, LastGenomeLen)
                else:
                    biggerThenWindow(currLine, currList, flag, NewList, LastGenomeLen, window,cogList)


    for i in range(len(NewList)):
        for j in range(len(NewList[i])):
            if NewList[i][j] == "X":
                NewList[i][j] = '9999'
            NewList[i][j] = int(NewList[i][j])
    return NewList


if __name__ == "__main__":
    main()

