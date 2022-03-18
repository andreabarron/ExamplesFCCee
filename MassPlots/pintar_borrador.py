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


#Hacemos lo mismo pero con las masas normalizadas al área

# Carga el archivo con los histogramas

#f2=ROOT.TFile("histos_norm.root","READONLY")

"""histoHZnorm = histoHZ.Clone("")
histoWWnorm = histoWW.Clone("")
histoZZnorm = histoZZ.Clone("")

histoHZnorm.Scale(1. / histoHZnorm.Integral(), "width")   #f2.Get("hZmassHZnorm")	
histoWWnorm.Scale(1. / histoWWnorm.Integral(), "width")   #f2.Get("hZmassWW_norm")   
histoZZnorm.Scale(1. / histoZZnorm.Integral(), "width")   #f2.Get("hZmassZZnorm")            

print (histoHZnorm.Integral())
print (histoWWnorm.Integral())
print (histoZZnorm.Integral())

c2 = ROOT.TCanvas("c2","HZ, WW y ZZ analysis canvas", 1024, 768)

histoHZnorm.Draw("")
histoWWnorm.Draw("sames")
histoZZnorm.Draw("sames")

histoHZnorm.SetLineColor(kRed)
histoWWnorm.SetLineColor(kBlue)
histoZZnorm.SetLineColor(kGreen)

legend = ROOT.TLegend(0.2,0.7,0.48,0.9)
entry=legend.AddEntry(histoHZnorm,"HZ","p")
entry=legend.AddEntry(histoWWnorm,"WW","p")
entry=legend.AddEntry(histoZZnorm,"ZZ","p")
legend.Draw()

output2_png = "masaZ_norm.png"           #"Masa del Z para los canales HZ, WW y ZZ"

c2.SaveAs(output2_png)"""


