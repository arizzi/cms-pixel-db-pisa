import string
def parseTestFullModuleDir(dir):
            #
            # tries to open a standard dir, as in the previous above
            # searches for summaryTest.txt inside + tars the dir in add_data
            #
            fileName = dir+'/summaryTest.txt'
            f = open(fileName,'r')
            fileContent = []
            for line in f:
                  fileContent.append( line )
            f.close()
            #
            # parse it
            #
            for line in fileContent:
                fields = (line.strip()).split(" ")
                #
                # real parsing
                #
                if (fields[0] == 'ModuleNr'):
                    ModuleNumber = fields[2]
                    TestNumber = fields[3]
                if (fields[0] == 'Defects'):
                    Defects=string.join(fields[1:]," ")
                if (fields[0] == 'PerfDefects'):
                    PerfDefects=string.join(fields[1:]," ")
                if (fields[0] == 'FINAL'):
                    FinalGrade = fields[2]
                if (fields[0] == 'fullTest'):
                    FulltestGrade = fields[2]
                if (fields[0] == 'Grade'):
                    Grade = fields[1]
                if (fields[0] == 'shortTest'):
                    ShorttestGrade = fields[2]
                if (fields[0] == 'ROCS'):
                    RocDefects = string.join(fields[5:]," ")
                if (fields[0] == 'Tested'):
                    isTested = fields[1]
                    Date = string.join(fields[3:]," ")
                if (fields[0] == 'Trimming'):
                    isTrimming = fields[1]
                if (fields[0] == 'phCalibration'):
                    isphCal = fields[1]
                if (fields[0] == 'NOISE'):
                    NOISE ='ok'
                if (fields[0] == 'Current' ):
                    Current = fields[1]
                if (fields[0] == 'I' and fields[1] == '150'):
                    I150 = fields[2]
                if (fields[0] == 'I150/I100'):
                    I150I100 = fields[1]
                if (fields[0] == 'I150/I100'):
                    I150I100 = fields[1]
                if (fields[0] == 'Temp'):
                    Temp = fields[1]
                    eTemp = fields[2]
                if (fields[0]=='Thermal'):
                    isThermalCyclying=fields[2]
                    vThermalCycling = fields[3]
                    eThermalCycling = fields[4]
                if (fields[0] == 'position'):
                    position=fields[1]
            #
            #
            # print
            #
            #
            print 'ModulNr',ModuleNumber,TestNumber
            print 'Defects',(Defects+','+PerfDefects)
            print 'Grades', FulltestGrade, ShorttestGrade, FinalGrade, Grade
            print 'Tested', isTested,Date
            print 'ROCS',RocDefects
            print 'Trimming, PhCal',isTrimming,isphCal
            print 'Thermal cycling', (isThermalCyclying+' ('+vThermalCycling+'+-'+vThermalCycling+')')
            print 'Current',Current
            print 'I150',I150
            print 'I150I100',I150I100
            print 'Temp', (Temp+'+-'+eTemp)
            print 'Mount',position
            print 'Noise',NOISE
                    
dir = 'testDir'
parseTestFullModuleDir(dir)


            
