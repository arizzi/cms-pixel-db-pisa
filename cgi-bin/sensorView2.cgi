#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from math import *
import re
import cgi
form = cgi.FieldStorage() # instantiate only once!


print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      
print '<link rel="stylesheet" type="text/css" href="/frames.css" />'
print '''
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.2/css/jquery.dataTables.css">

<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.2/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="http://jquery-datatables-column-filter.googlecode.com/svn/trunk/media/js/jquery.dataTables.columnFilter.js"></script>
<script>
	        var selected = [];
	       function update()
                        {
                                        var name = "iv.cgi?";
					var h=0
                                        for (var i = 0; i < selected.length; i++) {
                                                name+="test="+selected[i]+"&";
						h=400
                                        }
                                        if(document.getElementById('correct').checked) {
                                               name+="correct=1&";
					 } 
                                        if(! document.getElementById('log').checked) {
                                               name+="log=0&"; 
                                               document.getElementById('zoom').disabled=false;}
                                        else { document.getElementById('zoom').disabled=true;}
                                        if(document.getElementById('zoom').checked) name+="fixrange=1&"
                                        document.getElementById("theimg").src=name;
                                        document.getElementById("theimg").height=h;
                                        if(selected.length==0) document.getElementById("theimg").src="";
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
//		  id=rows[i].childNodes[14].innerHTML;
//				  console.log(id)
//				  console.log($(rows[i]).attr('id'))
                                  var index = $.inArray(id, selected);
				  if ( index === -1 ) {
                                        selected.push( id );
                                  }

				}
				update();
			}

              function draw()
                {
                        selString="";
                 console.log($.param(    $("#example").DataTable().ajax.params()))

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
                          
                          $("#plotPH").text("");
                          var rows = $("#example").dataTable().fnGetNodes();
                          if( selected.length != rows.length &&  selected.length  != 0) {
                          $("#plotPH").append("<img id='theImg' src='/cgi-bin/draw.cgi?"+selString+options+"'/>");
                         }else{
                          $("#plotPH").append("<img id='theImg' src='/cgi-bin/draw.cgi?coltoDraw="+j+"&"+options+"&"+$.param(    $("#example").DataTable().ajax.params())+"'/>");
                        }
                        
                }



$(document).ready(function() {
                                $('#example tbody').on( 'click', 'tr', function () {
                                        var id = $(this).attr('id');
//                                        var id = this.childNodes[14].innerHTML;
//					console.log(id);
//					console.log($(this).attr('id'));

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

                var table =          $('#example').DataTable( {
                        "bStateSave": true,
                         "aLengthMenu": [   [25, 50, 100, 200, -1],
                                        [25, 50, 100, 200, "All"]],
                        "order": [[ 3, "desc" ]],
			"iDisplayLength" : 25,
                        "bProcessing": true,
                        "bServerSide": true,
                        "sAjaxSource": "/cgi-bin/rawPredefinedView-backend.cgi",
			"rowCallback": function( row, data ) {
           			 if ( $.inArray(data.DT_RowId.toString(), selected) !== -1 ) {
				console.log("found")
		                $(row).addClass('selected');
            		}},
                        "fnStateLoaded": function (oSettings, oData) {
                                var jqInputs = $('thead input');
                                for ( var i=0 ; i<oSettings.aoPreSearchCols.length ; i++ )
                                {
                                console.log(oSettings.aoPreSearchCols[i].sSearch);
                                if(oSettings.aoPreSearchCols[i].sSearch!='')
                                        {
                                                jqInputs[i].value = oSettings.aoPreSearchCols[i].sSearch;
                                        }
                                }
                          },
                        "fnServerParams": function ( aoData ) {
                        aoData.push( { "name" : "viewNumber", "value" : "0" } );
                        }
                        } );
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

                        </script>
<body><main>
'''
sys.path.append("../PixelDB")

from storm import *
from PixelDB import *

from pixelwebui import *



from  rawPredefinedViews import *
toprint = columns[0]



print "<h2> Sensors view </h2>"

print "<p>"

if True :
        print "<button onclick='draw()'>Draw histogram</button>&nbsp;<select id=sel>"
        i=0
        for (c,s,e) in toprint :
                if e!= "NOPRINT":
                        print "<option value=%d>%s</option>"% (i,c)
                i+=1
        print "</select>"
        print "Xmin: <input type=text id=xmin name=xmin> Xmax: <input type=text id=xmax name=xmax> Nbins: <input type=text id=nbins name=nbins> LogY: <input type=checkbox id=logy> "

print "<div id=plotPH></div>"
print "<hr>"
if True :
 print "<button onclick='selectAll()'>Select all</button>"
 print "<button onclick='selectNone()'>Unselect all</button>"


# print " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <button>Plot all IVs for selected sensors</button> <button>Plot selected IVs</button>"
print "<hr>"
print "<table id=example class='display compact' >"
print " <thead> <tr>"
for (c,e,ev) in toprint :
# print "<th>", c,"<br><input type=\"text\" size=10></th>"
 print "<th>", c,"</th>"
print "</thead></tr><tbody>"

print "</tbody><tfoot></tfoot></table>"
print '<img id=theimg src="" width=900 h=0><p><b>Plot options:</b><p>'
print '<input id=log type="checkbox" checked onclick=update()> Log Scale<p>'
print '<input id=zoom type="checkbox" disabled onclick=update()> Zoom<p>'
print '<input id=correct type="checkbox" checked onclick=update()> Correct to T=20'
printFooter()
