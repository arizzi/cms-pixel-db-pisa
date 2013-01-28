<?php


$dir=$argv[1];

$monthN = array("01","02","03","04","05","06","07","08","09","10","11","12");
$monthS = array("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

$testNr = 'n/a';
$finalGrade = 'n/a';
$moduleTemp = '';
$module = '';
$pi=0; $ma=0; $bu=0; $tr=0; $ad=0;
$no=0; $th=0; $ga=0; $pe=0; $pa=0;
$rocs=0; $root=0;
$date=''; $datr=''; $daca='';
$c=''; $t=''; $n='';
$temp=0; $sollTemp=0;$cycl=''; $cy=''; $ecycl='';
$etemp=0;
$i=0; $ivVar=0; $ivDP=0; $slope=0;
$tbm1=1; $tbm2=1;
$iv150 = ''; $iv150_2 = '';
$grade = '';
$mount = '';
$finalGrade = '';
$fullGrade = '';
$shortGrade = '';
$reGrade = '';
$com=' ';
$mis=' ';
$tempWarning=' ';
$noiB=0; $noiC=0; $trmB=0; $trmC=0;
$gainB=0; $gainC=0; $pedB=0; $pedC=0;
$highCur = 0;
$perfDef = 0;
$half = 0;
$regraded = 0;
$star = 0;

$handle = fopen($dir."/summaryTest.txt", "r");
$li = 0;
while ($userinfo = fscanf($handle, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"))  {
  
  $li = $li +1;
  
  // if($li==1)  { ------------------------------------------------------------------
  if( !strcmp($userinfo[0],"Directory") )  {
    
    $moduleTemp = 'M'.$userinfo[1]{1}.$userinfo[1]{2}.$userinfo[1]{3}.$userinfo[1]{4};
    $moduleNr   = $userinfo[1]{2}.$userinfo[1]{3}.$userinfo[1]{4};
    
    $day   = $userinfo[1]{10}.$userinfo[1]{11};
    $month = $userinfo[1]{8}.$userinfo[1]{9};
    $year = $userinfo[1]{6}.$userinfo[1]{7};
    
    for ( $i=0; $i<12;$i++ ) {
      if (!strcmp($month, $monthN[$i]) ) {
	
	$date = $monthS[$i].' '.$day.' 20'.$year;
      }
    }
  }
  
  // if($li==2)  { ------------------------------------------------------------------
  if( !strcmp($userinfo[0],"ModuleNr") ) {
    
    $testNr  = $userinfo[3]; 
    $testDir = $userinfo[2].'/'. $userinfo[3];
    $link    = $userinfo[2].$userinfo[3];
  }
  
  $alvl = "";

  //if($li==3)  { //------------------------------------------------------------------
  if( !strcmp($userinfo[0],"Defects") ) {
    
    $pi=$userinfo[1];
    $ma=$userinfo[2];
    if ( $ma > 0 ) { 
      $star = 1;
      $ma=''.$ma.''; 
    }
    $bu=$userinfo[3];
    $tr=$userinfo[4];
    $ad=$userinfo[5];
  }

          //if($li==3)  { //------------------------------------------------------------------
	  if( !strcmp($userinfo[0],"PerfDefects") ) {
	    
            $no=$userinfo[1];
            $th=$userinfo[2];
            $ga=$userinfo[3];
            $pe=$userinfo[4];
            $pa=$userinfo[5];
	    $perfDef=1;
          }
	  
	  // if($li==4) {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"ROCS") ) {
	    
	    $rocs = $userinfo[5];
	    $defB = $userinfo[6];
	    $defC = $userinfo[7];

	    if ( $defC > 0 ) { 
	      $rocs   = $rocs.' ('.$defC.'C)>'; 
	    }
	    
	  }
	  
	  // if($li==6)  {  ------------------------------------------------------------------
//           if( !strcmp($userinfo[0],"Tested") && $moduleNr < 50 ) {

//             $date=$userinfo[4].' '.$userinfo[5];
// 	  }
	  
	  // if($li==7)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Trimming") ) {

           $t=$userinfo[1];
	  }
	  
	  // if($li==8)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"phCalibration") ) {

           $c=$userinfo[1];
#	   echo "ooooooooooooooooo ".$c;
	  }

	  // if($li==9){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Temp") ) {

	    if ( $userinfo[2] != -100 ) {
	      $temp=sprintf("%01.2f", $userinfo[1]);
	      $etemp=sprintf("%01.2f",$userinfo[2]);
	      $sollTemp=$userinfo[4];
	    }
	    else {
	      $temp=$userinfo[4];
	      $sollTemp=$userinfo[4];
	    }
	    if ( abs($temp - $sollTemp) > 1 ) {
#	      $temp = '<FONT COLOR=#cc0000><B>'.$temp.'</B></FONT>';
	      $tempWarning='T not '.$sollTemp.'!';
	    }
	  }

	  // if($li==10){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Thermal") ) {

	    if (!strcmp($userinfo[2],"yes"))  {
	      $cy= $userinfo[2];
	      if( $userinfo[4] != -100 ) {
		$cycl=sprintf("%01.1f", $userinfo[3]);
		$ecycl=sprintf("%01.1f", $userinfo[4]);
	      }
	    }
	    else {
	      $cy = $userinfo[2];
	    }
	  }

	  // if($li==17)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"TBM1") ) {
	    
            $tbm1=$userinfo[1];
            if ( $tbm1 != 0 )   {
	      
	      $com=' '.$com.' TBM1: <a
href="http://cmspixel.phys.ethz.ch/moduleTests/moduleDB/tbmDefects.html"> Err '.$tbm1.'</a>.';
	    }
	  }
	  
	  // if($li==18)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"TBM2") ) {
	    
            $tbm2=$userinfo[1];
            if ( $tbm2 != 0 )   {
	      
	      $com=' '.$com.' TBM2: <a
href="http://cmspixel.phys.ethz.ch/moduleTests/moduleDB/tbmDefects.html"> Err '.$tbm2.'</a>.';
	      
	    }
	  }

	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"I") ) {

	    $i=$userinfo[2];
	    
	    if($i==0 || $i=='') { $iv150=''; }
	    else {
	      
	      $iv150=sprintf("%01.2f",$i);
	      
	      if ( $sollTemp < 0 ) { 
		
		$i10   = sprintf("%01.2f", $i/12.10188635);
		$iv150_2 = $i10;
		
	      }
	      
	      if ( $sollTemp > 0 ) { 
		
		$iv150_2 = '';

		if ( $i > 10 ) { 
		  $iv150   = $iv150;
		}

	      }
	    }
	  }


	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"SwitchOn") ) {

	    $i=$userinfo[1];
	    
	    if($i==0 || $i=='') { $switchOn ='-'; }
	    else {
	      
	      $switchOn=sprintf("%01.2f",$i);
	    }
	  
	  }
	  
	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Current") ) {

	    $i=$userinfo[1];
	    
	    if($i==0 || $i=='') { $current='-'; }
	    else {
	      
	      $current=sprintf("%01.2f",$i);

	      if ( $sollTemp < 0 ) { 
		
		$i17   = sprintf("%01.2f", $i*12.10188635);
		$current_2 = $i17;
		
		if ( $i17 > 15 ) { 
		  $highCur   = 1;
		}


	      }
	      
	      if ( $sollTemp > 0 ) { 
		
		$current_2 = '';

		if ( $i > 10 ) { 
		  $highCur   = 1;
		}

	      }
	    }
	  }

	  // if($li==20){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"I150/I100") ) {
	    
	    $ivVar=$userinfo[1];
	    if ( $ivVar > 0 ) { 
	      $slope=sprintf("%01.2f",$ivVar);
	    }
	    else {
	      $slope = '';
	    }

	  }

	  // if($li==21){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"iv") ) {

	    $ivDP=$userinfo[2];
	    if ( $ivDP < 10 &&  $ivDP != 0 ) {$com=$com.' incompl. iv-data: '.$iDP.' meas.';}
	  }

	  // if($li==22){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Grade") ) {

	    $grade=$userinfo[1];
	  }


	  // if($li==22){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"position") ) {

	    $mount=$userinfo[1];
	  }

	  // if($li==28){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Noise") ) {

	    $noiB=$userinfo[1];
	    $noiC=$userinfo[2];

	    if ( $noiB == 0 && $noiC == 0 ) {

		$n = 'ok';
	    }
	    else if ( $noiB > 0 && $noiC == 0 ) {
	      $n = $noiB.'B';
	    }
	    else if ( $noiB > 0 && $noiC > 0) {
	      $n = $noiB.'B/'.$noiC.'C';
	    }
	    else if ( $noiC > 0 && $noiB == 0 ) {
	      $n = ''.$noiC.'C';
	    } else {
	      $n = '-';
	    }
	  }

	  // if($li==29){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"VcalThrWidth") ) {

	    $trmB=$userinfo[1];
	    $trmC=$userinfo[2];

	    if ( $trmB == 0 && $trmC == 0 ) {
	      if ( strcmp($t, "no") ) {
		$t = 'ok';
	      }
	    }
	    else if ( $trmB > 0 && $trmC == 0 ) {
	      $t = $trmB.'B';
	    }
	    else if ( $trmB > 0 && $trmC > 0 ) {
	      $t = $trmB.'B/'.$trmC.'C';
	    }
	    else if ( $trmC > 0 && $trmB == 0 ) {
	      $t = ''.$trmC.'C';
	    }
	  }

	  // if($li==30){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"RelGainWidth") ) {

	    $gainB=$userinfo[1];
	    $gainC=$userinfo[2];
	    
	    if (  $gainB == 0 && $gainC == 0 ) {
	      
	      if ( !strcmp($c, "yes") ) {
		$c = '';
	      }
	    }
	    else if ( $gainB > 0 && $gainC == 0 ) {
	      $c = $gainB.'B Gain';
	    }
	    else if ( $gainB > 0 && $gainC > 0 ) {
	      $c = $gainB.'B/'.$gainC.'C Gain';
	    }
	    else if ( $gainC > 0 && $gainB == 0 ) {
	      $c = ''.$gainC.'C Gain';
	    }
	  }

	  // if($li==31){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"PedSpread") ) {

	    $pedB=$userinfo[1];
	    $pedC=$userinfo[2];

	    if (  $gainB == 0 && $gainC == 0 &&
		  $pedB  == 0 && $pedC  == 0 ) {
	      
	      if ( strcmp($c, "yes") ) {
		$c = '';
	      }
	    }
	    else if ( $pedB > 0 && $pedC == 0 ) {
	      $c = $c.'  '.$pedB.'B Ped';
	    }
	    else if ( $pedB > 0 && $pedC > 0 ) {
	      $c = $c.'  '.$pedB.'B/'.$pedC.'C  Ped';
	    }
	    else if ( $pedC > 0 && $pedB == 0 ) {
	      $c = $c.'  '.$pedC.'C Ped';
	    }
	  }


	  // if($li==31){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"MeanParameter1") ) {

	    $par1B=$userinfo[1];
	    $par1C=$userinfo[2];

	    if (  $gainB == 0 && $gainC == 0 &&
		  $pedB  == 0 && $pedC  == 0 &&
		  $par1B  == 0 && $par1C  == 0 ) {
	      
	      if ( strcmp($c, "no") ) {
		$c = 'ok';
	      }
	    }
	    else if ( $par1B > 0 && $par1C == 0 ) {
	      $c = $c.'  '.$par1B.'B Par1';
	    }
	    else if ( $par1B > 0 && $par1C > 0 ) {
	      $c = $c.'  '.$par1B.'B/'.$par1C.'C  Par1';
	    }
	    else if ( $par1C > 0 && $par1B == 0 ) {
	      $c = $c.'  >'.$par1C.'C Ped';
	    }
	  }

	  // if($li==34){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"RATIO") ) {

	    if ( $userinfo[1] > 5 ) { 
	      $com=$com.' I_recalc > 5 x I_meas'; 
	    }
	  }



	  // if($li==36){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"FINAL") ) {

	    $finalGrade = $userinfo[2];

	  }

	  // if($li==35){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"shortTest") ) {

	    $shortGrade =  $userinfo[2];

	  }

	  // if($li==36){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"fullTest")  ) {

	    if ( $star ) { $fullGrade =  $userinfo[2].'*'; } 
	    else         { $fullGrade =  $userinfo[2]; }

	      $module     =  $moduleTemp; 
	  }
	  
	  if (!strcmp($module, "") ) { $module = $moduleTemp; }
	  
	  // commments:
	  // if($li==15 || $li==16 || $li==17 ||$li==18 || $li==37 ) {
	  if (!strcmp($userinfo[2],"Vcal") ||
 	      !strcmp($userinfo[2],"SCurve") ||
 	      !strcmp($userinfo[2],"Gain") ||
 	      !strcmp($userinfo[2],"Ped") ) {
	    
	    $com=$com.' ';
	    $ar = count($userinfo);
	    if($ar>1) {
	      
	      for($en=0; $en<$ar; $en++) {
		
		$com=$com.' '.$userinfo[$en];
	      }
	    }
	  }


	  if( !strcmp($userinfo[0],"Regrading:") ) {
	    
	    $regraded=1;
	    $ar = count($userinfo);
	    
	    
	    for($en=1; $en<$ar; $en++) {
	      
	      $reGrade=$reGrade.' '.$userinfo[$en];
	    }

	    $reGrade=$reGrade.'';
	  }


	  if( !strcmp($userinfo[0],"Missing:") ) {
	    
	    $tmp_mis = ''; $files_mis=0;

	    $mis=$mis.' MISSING: ';
	    $ar = count($userinfo);
	    
	    for($en=1; $en<$ar; $en++) {

	      if ( $files_mis == 1 ) { $mis= $mis.''.$tmp_mis; $files_mis = 0; }

	      if( !strcmp($userinfo[$en],"Files:") ) {

		$tmp_mis = " FILES:";
		$files_mis = 1;
		continue;
	      }
	      
	      $mis=$mis.' '.$userinfo[$en];
	    }

	    $mis=$mis.'';
	  }

	  if( !strcmp($userinfo[0],"Comment:") ) {
 	     	    	      
	    $com=$com.' ';
	    $ar = count($userinfo);
	    
	    for($en=1; $en<$ar; $en++) {
	      
	      $com=$com.' '.$userinfo[$en];
	    }
	  }

	  if( !strcmp($userinfo[0],"Half-Module") ) {
	    $half = 1;
	  }
	}
	
	if ( $highCur ){
	  $com =  $com.' switch-on: '.$switchOn.'';
	}

	$pdef   = '';
	if ( $perfDef ) {
		  $pdef   = $no.'/'.$th.'/'.$ga.'/'.$pe.'/'.$pa; 
	}

	if ( $regraded ) {
	  $com = $reGrade.'<br>'.$com;
	  $finalGrade = $finalGrade.'*';
	}

	if ( $half ) {
	  $module='H-'.$module;
	}
	fclose($handle);
	
#
# substitute with fields
#
echo "testN ".$testNr."\n";
echo "finalGrade ".$finalGrade."\n";
echo "module ".$module."\n";
echo "date ".$date."\n";
echo "fullGrade ".$fullGrade."\n";
echo "shortGrade ".$shortGrade."\n";  
echo "grade ".$grade."\n";  
echo "currentn2 ".$current_2."\n";  
echo "current ".$current."\n";  
echo "iv150n2 ".$iv150_2."\n";  
echo "iv150 ".$iv150."\n";  
echo "slope ".$slope."\n";
echo "temp ".$temp."\n";
echo "etemp ".$etemp."\n";
echo "mount ".$mount."\n";
echo "tempWarning ".$tempWarning."\n";
echo "com ".$com."\n";
echo "mis ".$mis."\n";
echo "deadpi ".$pi."\n";
echo "mask ".$ma."\n";
echo "bump ".$bu."\n";
echo "trim ".$tr."\n";
echo "add ".$ad."\n";
#echo "pdef ".$pdef."\n";
echo "noisy ".$no."\n";
echo "thres ".$th."\n";
echo "gain ".$ga."\n";
echo "pedestal ".$pe."\n";
echo "parameter1 ".$pa."\n";
echo "rocs ".$rocs."\n";
echo "noise ".$n."\n";
echo "trimming ".$t."\n";
echo "phcal ".$c."\n";
echo "tcy ".$cy."\n";
echo "tcycl ".$cycl."\n";
echo "etcycl ".$ecycl."\n";

?>
