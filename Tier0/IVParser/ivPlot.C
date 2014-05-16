ivPlot(const char * inFilename, const char * outFilename , float v1, float v2)
{
 TCanvas c("IV","IV",800,600);
 TFile f(outFilename,"RECREATE");
 TNtuple iv("IV","IV","V:I");
 iv.ReadFile(inFilename);
 iv.Draw("abs(I):abs(V)");
 TGraph gr(iv.GetSelectedRows(),iv.GetV2(), iv.GetV1());
 std::cout << "Results: " <<  gr.Eval(v1) <<  " " <<  gr.Eval(v2) << " " <<  (gr.Eval(v1)/gr.Eval(v2)) << " ";
if(gr.Eval(v1)/gr.Eval(v2) > 2 ||   fabs(gr.Eval(v1)) >  0.000010)
 { std::cout << "C"; }
else {
   if(fabs(gr.Eval(v1)) >  0.000002)  std::cout << "B" ;
   else  std::cout << "A";
}
std::cout << " " << std::endl;

//std::cout << "100: " <<  gr.Eval(100) << std::endl;
//std::cout << "ratio150/100: " <<  gr.Eval(150)/gr.Eval(100) << std::endl;
 gr.Write();
 c.SaveAs("plot.png");
 iv.Write();
 f.Write();
 exit(0);
}
