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
				  id=rows[i].childNodes[14].innerHTML;
                                  var index = $.inArray(id, selected);
				  if ( index === -1 ) {
                                        selected.push( id );
                                  }

				}
				update();
			}

$(document).ready(function() {
                                $('#example tbody').on( 'click', 'tr', function () {
                                        var id = this.childNodes[14].innerHTML;
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
                        "iDisplayLength" : 10,
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
