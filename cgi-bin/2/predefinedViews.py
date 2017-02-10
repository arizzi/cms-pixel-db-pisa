columns=[]
tables=[]
objects=[]
joins=[]
columns.append([
#"Sel","'<input type=checkbox name=sel>'"),
          ("Sensor id","'%s<input type=checkbox name=sel_sensor%s>'%(o[0].SENSOR_ID,o[0].SENSOR_ID)"),
#           ("Sensor ID","o[0].SENSOR_ID"),
           ("Status","o[0].STATUS"),
           ("Center","o[2].RECEIVER"),
           ("Test date","o[1].DATE.strftime('%Y-%m-%d %H:%M:%S')"),
           ("Type","o[1].TYPE"),
           ("Grade","o[1].GRADE"),
           ("v1","'%6g'%o[1].V1"),
           ("v2","'%6g'%o[1].V2"),
           ("i1","'%6g'%o[1].I1"),
           ("i2","'%6g'%o[1].I2"),
           ("Slope","o[1].SLOPE"),
           ("Temp","o[1].TEMPERATURE"),
           ("i1@20&deg;","'%6g'%corTemp(o[1].I1,o[1].TEMPERATURE)"),
           ("i2@20&deg;","'%6g'%corTemp(o[1].I2,o[1].TEMPERATURE)"),
#           ("Test id","'%s<input type=checkbox name=sel_sensor%s>'%(o[1].TEST_ID,o[1].TEST_ID)"),
           ("Test id","o[1].TEST_ID"),
           ("Files","'<a href=%s>link</a>'%o[1].data.PFNs"),
          ])
tables.append("(Sensor,Test_IV,Transfer)")
joins.append("Sensor.SENSOR_ID==Test_IV.SENSOR_ID, Sensor.TRANSFER_ID==Transfer.TRANSFER_ID")

