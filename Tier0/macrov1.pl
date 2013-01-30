#!/usr/bin/perl -w       


$dirMacros = shift;


print "<MMMMMMMMMM", $dirMacros;


open(ROOT, "|root -l -b ") || die "Cannot open ROOT\n";

print ROOT ".L PHCalibration.C\n";
print ROOT "FitAllCurves(\"$dirMacros\", 0)\n";
print ROOT ".L SCurve.C\n";
print ROOT "FitSCurves(\"$dirMacros\")\n"; 


#print ROOT ".L chipSummaryPage.C\n";
#print ROOT "chipSummaries(\"$dirMacros\",\"m\")\n"; 

print ROOT ".L moduleSummaryPage.C\n";
print ROOT "moduleSummary(\"$dirMacros\", \"m\")\n";
print ROOT ".q\n";
close(ROOT);
