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

histoHZnorm = histoHZ.Clone("")
histoWWnorm = histoWW.Clone("")
histoZZnorm = histoZZ.Clone("")

histoHZnorm.Sumw2()   # con esto me salen los errores (para que se pinten tengo que darle
                      # a las opciones y a "simple")
histoWWnorm.Sumw2()
histoZZnorm.Sumw2()


histoHZnorm.Scale(1. / histoHZnorm.Integral(), "width")          
histoWWnorm.Scale(1. / histoWWnorm.Integral(), "width")      
histoZZnorm.Scale(1. / histoZZnorm.Integral(), "width")               

print (histoHZnorm.Integral())
print (histoWWnorm.Integral())
print (histoZZnorm.Integral())

c2 = ROOT.TCanvas("c2","HZ, WW y ZZ analysis canvas", 1024, 768)

histoHZnorm.Draw("hist,l")       # si al lado de hist pongo ,E2 se me pintan los errores
histoWWnorm.Draw("sames,hist")   # si al lado de hist pongo ,p se me pintan puntos
histoZZnorm.Draw("sames,hist")

histoHZnorm.SetFillColor(kRed)
histoWWnorm.SetFillColor(kBlue)
histoZZnorm.SetFillColor(kGreen)

histoHZnorm.SetMarkerColor(kRed)
histoWWnorm.SetMarkerColor(kBlue)
histoZZnorm.SetMarkerColor(kGreen)

histoHZnorm.SetMarkerStyle(20)
histoWWnorm.SetMarkerStyle(21)
histoZZnorm.SetMarkerStyle(22)  # esto es el tipo de marcador o punto

histoHZnorm.SetLineColor(kRed)
histoWWnorm.SetLineColor(kBlue)
histoZZnorm.SetLineColor(kGreen)


legend = ROOT.TLegend(0.2,0.7,0.48,0.9)
entry=legend.AddEntry(histoHZnorm,"HZ","lp")
entry=legend.AddEntry(histoWWnorm,"WW","lp")
entry=legend.AddEntry(histoZZnorm,"ZZ","lp")
legend.Draw()

output2_png = "masaZ_norm.png"         #"Masa del Z normalizada para los canales HZ, WW y ZZ"

c2.SaveAs(output2_png)

