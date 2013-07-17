import string

import subprocess

def parseTestFullModuleDir(dir):
            #
            # tries to open a standard dir, as in the previous above
            # searches for summaryTest.txt inside + tars the dir in add_data
            #
            fileName = dir
            #
            # run php on it
            #
            p = subprocess.Popen("php prodTable.php "+fileName, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()
            if (retval!=0):
                  return None
            fileContent = []
            for line in p.stdout.readlines():
                  fileContent.append( line )
            #
            # parse it
            #
            for line in fileContent:
                fields = (line.strip()).split(" ")
                #
                # real parsing
                #
                if (fields[0] == 'module'):
                    ModuleNumber = fields[1]
                if (fields[0] == 'deadpi'):
                    DeadPixels=string.join(fields[1:]," ")

                if (fields[0] == 'mask'):
                    MaskPixels=string.join(fields[1:]," ")
                    


                if (fields[0] == 'bump'):
                    BumpPixels=string.join(fields[1:]," ")


                if (fields[0] == 'trim'):
                    TrimPixels=string.join(fields[1:]," ")


                if (fields[0] == 'add'):
                    AddressPixels=string.join(fields[1:]," ")

                if (fields[0] == 'noisy'):
                    NoisyPixels=string.join(fields[1:]," ")

                if (fields[0] == 'thres'):
                    TreshPixels=string.join(fields[1:]," ")

                if (fields[0] == 'gain'):
                    GainPixels=string.join(fields[1:]," ")
                    
                if (fields[0] == 'pedestal'):
                    PedPixels=string.join(fields[1:]," ")

                if (fields[0] == 'parameter1'):
                    ParPixels=string.join(fields[1:]," ")

                if (fields[0] == 'finalGrade'):
                    FinalGrade = fields[1]
                if (fields[0] == 'fullGrade'):
                    FulltestGrade = fields[1]
                if (fields[0] == 'grade'):
                    Grade = fields[1]
                if (fields[0] == 'shortGrade'):
                    ShorttestGrade = fields[1]

                if (fields[0] == 'rocs'):
                    RocDefects = string.join(fields[1:]," ")


                if (fields[0] == 'date'):
                    Date = string.join(fields[1:]," ")
                if (fields[0] == 'trimming'):
                    isTrimming = fields[1]
                if (fields[0] == 'phcal'):
                      isphCal = string.join(fields[1:]," ")

                if (fields[0] == 'noise'):
                    NOISE = fields[1]
                if (fields[0] == 'iv150'):
                      if (len(fields) >1):
                              I150 = fields[1]
                      else:
                            I150=0
                if (fields[0] == 'iv150n2'):
                      if (len(fields) >1):
                        I1502 = fields[1]
                      else:
                         I1502=0   
                if (fields[0] == 'current' ):
                      if (len(fields) >1):
                            Current = fields[1]
                      else:
                            Current=0
                if (fields[0] == 'currentn2' ):
                      if (len(fields) >1):
                            Current2 = fields[1]
                      else:
                            Current2=0
                
                if (fields[0] == 'slope'):
                      if (len(fields) >1):
                            I150I100 = fields[1]
                      else:
                             I150I100 = 0
                if (fields[0] == 'temp'):
                    Temp = fields[1]
                if (fields[0] == 'etemp'):
                    eTemp = fields[1]

                if (fields[0]=='tcy'):
                    isThermalCycling=fields[1]
                if (fields[0]=='tcycl'):
                    TThermalCycling=fields[1]

                if (fields[0]=='etcycl'):
                    eTThermalCycling=fields[1]

                if (fields[0] == 'mount'):
                    position=fields[1]
                if (fields[0] == 'testN'):
                    TestNumber=fields[1]
                    
            #
            #
            # print
            #
            #
            print 'ModulNr',ModuleNumber,TestNumber
            print 'Defects',DeadPixels,MaskPixels,BumpPixels,TrimPixels,AddressPixels,NoisyPixels, TreshPixels, GainPixels, PedPixels, ParPixels
            print 'Grades', FulltestGrade, ShorttestGrade, FinalGrade, Grade
            print 'Tested', Date
            print 'ROCS',RocDefects
            print 'Trimming, PhCal',isTrimming,isphCal
            print 'Thermal cycling', (isThermalCycling+' ('+TThermalCycling+'+-'+eTThermalCycling+')')
            print 'Current',Current
            print 'I150',I150
            print 'I150_2',I1502
            print 'Current_2',Current2

            print 'I150I100',I150I100
            print 'Temp', (Temp+'+-'+eTemp)
            print 'Mount',position
            print 'Noise',NOISE
                    
dir = '/afs/cern.ch/user/s/starodum/public/moduleDB/M1215-080320.09:34/T+17a/'

parseTestFullModuleDir(dir)


            
