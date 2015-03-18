#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from math import *
import re
import cgi
from  rawPredefinedViews import *
import Cookie
setcookies = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    setcookies.load(cookie_string)
setcookies["lastview"]= os.environ['REQUEST_URI']


print "Content-Type: text/html"
print setcookies
print
form = cgi.FieldStorage() # instantiate only once!
toprint=[]


objName = "empty"
viewNumber=9

checked = form.getfirst('exact', "")
if checked == "1" :
	checked="checked"
	
searchar=[]
if objName == 'empty' :
	if viewNumber >= len(columns) :
		exit(0)
	else:
		toprint = columns[viewNumber]
		topush='"name" : "viewNumber", "value" : "%s"' % viewNumber
else:
	viewNumber=-1
	objName = parseObjName(cgi.escape(objName))
	id,toprint,query,count = fromObjectName(objName)
	topush='"name" : "objName", "value" : "%s"' % objName


for p in toprint :
	ur = form.getfirst((p[0]).upper(), None)
	if ur is not None :
	   searchar.append(ur)	
	else:
	   searchar.append("")

searcharray='%s'%searchar
		

#topush+=",%s"%(form.getfirst('topush', ''))

print "<html>\n        <head>\n         "      
print '<link rel="stylesheet" type="text/css" href="/frames.css" />'
print '''
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.2/css/jquery.dataTables.css">
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/tabletools/2.2.0/css/dataTables.tableTools.css">

<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.2/js/jquery.dataTables.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/tabletools/2.2.0/js/dataTables.tableTools.js"></script>
<script type="text/javascript" src="http://jquery-datatables-column-filter.googlecode.com/svn/trunk/media/js/jquery.dataTables.columnFilter.js"></script>
<script>
                var selected = [];

$(document).ready(function() {
		$('#example tbody').on( 'click', 'tr', function () {
                                        var id = $(this).attr('id');
                                        var index = $.inArray(id, selected);
                                        if ( index === -1 ) {
                                        selected.push( id );
                                        } else {
                                        selected.splice( index, 1 );
                                        }
                                        $(this).toggleClass('selected');
                                        update();
		} );
		$('#example thead th').each( function () {
			var title = $('#example thead th').eq( $(this).index() ).text();
			$(this).html(title+'<br><input size=10 type="text" onclick="event.stopPropagation();"/>' );
			} );

		var urlSearch = %s;
		var table =          $('#example').DataTable( {
			dom: 'T<"clear">lfrtip',
			"bStateSave": true,
			 "aLengthMenu": [   [25, 50, 100, 200, -1],
				        [25, 50, 100, 200, "All"]],
			"iDisplayLength" : 25,
			"bProcessing": true,
                         "order": [[ 1,"desc" ]],

			"bServerSide": true,
			 "tableTools": {
			            "sSwfPath": "//cdn.datatables.net/tabletools/2.2.0/swf/copy_csv_xls_pdf.swf"
			   },
			"sAjaxSource": "/cgi-bin/rawPredefinedView-backend.cgi",
			"fnStateLoaded": function (oSettings, oData) {
				var jqInputs = $('thead input');
				for ( var i=0 ; i<oSettings.aoPreSearchCols.length ; i++ )
				{
				if(urlSearch.length > i && urlSearch[i]!='')
					{
						oSettings.aoPreSearchCols[i].sSearch = urlSearch[i];
					}
				console.log(oSettings.aoPreSearchCols[i].sSearch);
				if(oSettings.aoPreSearchCols[i].sSearch!='')
					{
						jqInputs[i].value = oSettings.aoPreSearchCols[i].sSearch;
					}
				console.log(urlSearch.length);
				
				}
			  },
			"fnServerParams": function ( aoData ) {
			if( $('#exact').is(':checked')) {
			aoData.push( { "name": "exact", "value":  "1"});
			} else {
			aoData.push( { "name": "exact", "value":  "0"});
			}
			aoData.push( { %s } );
			}
			} );
	         var jqInputs = $('thead input');
                 for ( var i=0 ; i<jqInputs.length ; i++ )
                                {
                                if(urlSearch.length > i && urlSearch[i]!='')
                                        {
                                            jqInputs[i].value = urlSearch[i];
					    table.column(i).search( urlSearch[i] ).draw();

                                        }
		}
		//	
		// Apply the search
		table.columns().eq( 0 ).each( function ( colIdx ) {
			$( 'input', table.column( colIdx ).header() ).on( 'keyup change', function () {
				table
				.column( colIdx )
                .search( this.value )
                .draw();
        } );
    } );

//.columnFilter({ sPlaceHolder: "filterPH"});
				});

	      function update()
		{
		//	console.log(	$("#example").DataTable().ajax.json())
		}
              function draw(all)
		{
			selString="";
		 console.log($.param(    $("#example").DataTable().ajax.params()))

/*			for (var i = 0; i < selected.length; i++) {
                                selString+="dtid="+selected[i]+"&";
                        }*/
			  var el=document.getElementById("sel");
			  var xmin=document.getElementById("xmin").value;
			  var xmax=document.getElementById("xmax").value;
			  var nbins=document.getElementById("nbins").value;
			  var log=0;
			  if( $('#logy').is(':checked')) {
				log=1
			  }
			  var options="xmin="+xmin+"&xmax="+xmax+"&nbins="+nbins+"&log="+log;
			  var j = el.selectedIndex;
	                  var rows = $("#example").dataTable().fnGetNodes();
                          for(var i=0;i<rows.length;i++) {
				  id=$(rows[i]).attr('id');
                                  var index = $.inArray(id, selected);
				  if(index!= -1) {
					selString+="dtid="+rows[i].childNodes[j].innerText+"&";
				  }

			
			  }
			  
			  $("#plotPH").text("")
			  var rows = $("#example").dataTable().fnGetNodes();
	  		  if(all != 1 && selected.length != rows.length &&  selected.length  != 0) {
	                  $("#plotPH").append("<img id='theImg'  src='/cgi-bin/draw.cgi?viewNumber=%d&objName=%s&"+selString+options+"'/>");
			 }else{
			  $("#plotPH").append("<img id='theImg'  src='/cgi-bin/draw.cgi?all="+all+"&coltoDraw="+j+"&"+options+"&"+$.param(    $("#example").DataTable().ajax.params())+"'/>");
			}
			  $("#plotPH").append("<img id='spinner' src='/spinner.gif'/>");
			$('#theImg').load(function() {
			  $('#spinner').fadeOut();
			});
//			$.get( "test.php", function( data ) {
//			  alert( "Data Loaded: " + data );
//			});
			
		}

              function selectNone()
                        {
                                var rows = $("#example").dataTable().fnGetNodes();
                                for(var i=0;i<rows.length;i++)
                                {
                                  $(rows[i]).removeClass('selected');
                                }
                                selected = [];
                                update();
                        }

              function selectAll()
                        {
                                var rows = $("#example").dataTable().fnGetNodes();
                                for(var i=0;i<rows.length;i++)
                                {
                                  $(rows[i]).addClass('selected');
                                  id=$(rows[i]).attr('id');
                                  var index = $.inArray(id, selected);
                                  if ( index === -1 ) {
                                        selected.push( id );
                                  }

                                }
                                update();
                        }
	                </script>
<body>
<main>
''' %(searcharray,topush,viewNumber,objName)
sys.path.append("../PixelDB")

from storm import *
from PixelDB import *
from pixelwebui import *
if form.getfirst('t0', '0') == "1" :  
  sys.path.append("/home/robot/cms-pixel-db-pisa/Tier0")
  from  PixelTier0 import *
  pdb = PixelTier0()
  pdb.connectToDB()
else :
  pdb = PixelDBInterface(operator="webfrontend",center="cern")
  pdb.connectToDB()

if objName == 'empty' :

		print header[viewNumber]

if True :
	print "<button onclick='draw(0)'>Draw histogram</button><button onclick='draw(1)'>Draw for all</button>&nbsp;<select id=sel>"
	i=0
	for (c,s,e) in toprint :
		if e!= "NOPRINT":
			print "<option value=%d>%s</option>"% (i,c)
		i+=1
	print "</select>"
        print "Xmin: <input type=text id=xmin name=xmin> Xmax: <input type=text id=xmax name=xmax> Nbins: <input type=text id=nbins name=nbins> LogY: <input type=checkbox id=logy> "
		

print "<div id=plotPH></div><hr>"

if True :
 print "<button onclick='selectAll()'>Select all</button>"
 print "<button onclick='selectNone()'>Unselect all</button>"


print "<br><input type=checkbox id=exact %s  onclick=\"var table = $('#example').DataTable(); table.ajax.reload();\"> Exact per column search (you can still add the %% yourself)"%(checked) 
print "<p id=filterPH></p>"
print "<table id=example class=\"display cell-border compact\"  width=100%>"
print " <thead> <tr>"
for (c,s,e) in toprint :
 if e!= "NOPRINT":
	 print "<th>", c,"</th>"
print "</thead></tr>"
print " <tfoot> <tr>"
for (c,s,e) in toprint :
 if e!= "NOPRINT":
	 print "<th>", c,"</th>"
print "</tfoot></tr><tbody></tbody></table>"

printFooter()


