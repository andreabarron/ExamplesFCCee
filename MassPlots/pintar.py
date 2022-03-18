import ROOT
import tdrstyle

from ROOT import *

# CMS Style (estilo para los plots)
tdrstyle.setTDRStyle()

# Carga el archivo con los histogramas

f=ROOT.TFile("histos.root","READONLY")

histoHZ =f.Get("hZmassHZ")	
histoWW =f.Get("hZmassWW")            
histoZZ =f.Get("hZmassZZ")            

print (histoZZ.Integral())

c1 = ROOT.TCanvas("c1","HZ, WW y ZZ analysis canvas", 1024, 768)

histoHZ.Draw("")
histoWW.Draw("sames")
histoZZ.Draw("sames")

histoHZ.SetLineColor(kRed)
histoWW.SetLineColor(kBlue)
histoZZ.SetLineColor(kGreen)

legend = ROOT.TLegend(0.2,0.7,0.48,0.9)
entry=legend.AddEntry(histoHZ,"HZ","l")
entry=legend.AddEntry(histoWW,"WW","l")
entry=legend.AddEntry(histoZZ,"ZZ","l")
legend.Draw()

output_png = "masaZ.png"           #"Masa del Z para los canales HZ, WW y ZZ"

c1.SaveAs(output_png)


