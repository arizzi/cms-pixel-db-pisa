def dictToString(aDict):
        result=""
        for i in aDict.keys:
          aList = aDict[i]
          print i, aList
          for j in aList:
              (x,y) = i
              if result != "":
               result= result + ","
              result = result + i+"_"+x+"_"+y
        return result

def stringToDict(failures):
        myDict = {}
        positions = failures.split(",")
        print positions
        for i in positions:
          print i
          (a,b,c) = i.split("_")
          d = (b,c)
          print "ll", a, b, c, d
          (myDict[a]).append(d)
        return myDict

