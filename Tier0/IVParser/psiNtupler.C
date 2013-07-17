psiNtupler(const char * inFilename, const char * outFilename , float v1, float v2)
{
 TCanvas c("IV","IV",800,600);
 TFile f(outFilename,"RECREATE");
 TNtuple iv("IV","IV","time:V:I");
 iv.ReadFile(inFilename);
 iv.Draw("-I:-V");
 TGraph gr(iv.GetSelectedRows(),iv.GetV2(), iv.GetV1());
 std::cout << "Results: " <<  gr.Eval(v1) <<  " " <<  gr.Eval(v2) << " " <<  (gr.Eval(v1)/gr.Eval(v2)) << " " << std::endl;
//std::cout << "100: " <<  gr.Eval(100) << std::endl;
//std::cout << "ratio150/100: " <<  gr.Eval(150)/gr.Eval(100) << std::endl;
 gr.Write();
 c.SaveAs("debug.png");
 iv.Write();
 f.Write();
 exit(0);
}
