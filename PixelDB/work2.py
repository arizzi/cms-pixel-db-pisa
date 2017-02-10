

#
# search for Bare_module_ROC[00-15]_setup.csv
#
   for num in range(0,16):
       #
       # I need a two digit number like 00
       #
       pattern = str(num).zfill(2)
       searchname = "Bare_module_ROC"+pattern+"_setup.csv"
       
       ppp = subprocess.Popen("ls -1 "+dir.rstrip()+searchname, shell=True, stdout=subprocess.PIPE, stderr=None)
       retval = ppp.wait()
        
       if (retval != 0):
           print "no files", searchname,"  in ",str(dir)
#            return None
        lines = ppp.stdout.readlines()
        if ( len (lines) > 1):
            print "too many Bare_module_QA_*.csv in ",str(dir)
            return None

        filename= lines[0]
        filename = filename.rstrip(os.linesep)
        print "FILENAME = "+filename

       
