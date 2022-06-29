#!/usr/bin/env python
import sys
procDict = {}

def findChildren(idIn):
  return procDict.get(idIn, [])

if __name__ == "__main__":
  if len(sys.argv) == 2:
    outList = sys.argv[1].split(",")
    for i in outList:
      print(i.strip())
    exit(0)
  searchSpace = sys.argv[2].split(",")
  diffSpace = []
  for i in range(0, len(searchSpace)):
    searchSpace[i] = int(searchSpace[i].strip())
    diffSpace.append(searchSpace[i])
  taxFile = open(sys.argv[1])
  for line in taxFile.readlines():
    segments = line.split("\t|\t")
    thisID = int(segments[0].strip())
    thisParent = int(segments[1].strip())
    if thisParent in procDict.keys():
      procDict[thisParent].append(thisID)
    else:
      procDict[thisParent] = [thisID]
  while len(diffSpace) != 0:
    processes = []
    thisRun = []
    for exID in diffSpace:
        res = findChildren(exID)
        for i in res:
          for j in searchSpace:
            if j == i:
              break
          else:
            thisRun.append(i)
            searchSpace.append(i)
    diffSpace = thisRun
  
  for i in searchSpace:
    print(i)

