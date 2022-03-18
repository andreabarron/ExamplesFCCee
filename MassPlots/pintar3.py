import ROOT
import tdrstyle

from ROOT import *

# CMS Style (estilo para los plots)
tdrstyle.setTDRStyle()

# Carga el archivo con los histogramas

f=ROOT.TFile("histos_higgs.root","READONLY")

historecoilmassHZ = f.Get("hrecoilmassHZ")
historecoilmassWW = f.Get("hrecoilmassWW")
historecoilmassZZ = f.Get("hrecoilmassZZ")



#historecoilmassHZ.Scale(weightHZ)

c1 = ROOT.TCanvas("c1","HZ, WW y ZZ analysis canvas", 1024, 768)



historecoilmassHZ.Draw("")
historecoilmassWW.Draw("sames")
historecoilmassZZ.Draw("sames")

historecoilmassHZ.SetLineColor(kRed)
historecoilmassWW.SetLineColor(kBlue)
historecoilmassZZ.SetLineColor(kGreen)


legend = ROOT.TLegend(0.5,0.5,0.9,0.9)
entry=legend.AddEntry(historecoilmassHZ,"HZ","l")
entry=legend.AddEntry(historecoilmassWW,"WW","l")
entry=legend.AddEntry(historecoilmassZZ,"ZZ","l")
legend.Draw()

output_png = "recoil_mass.png"         

c1.SaveAs(output_png)







