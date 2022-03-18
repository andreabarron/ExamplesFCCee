import ROOT
import tdrstyle

from ROOT import *

# CMS Style (estilo para los plots)
tdrstyle.setTDRStyle()

# Carga el archivo con los histogramas

f=ROOT.TFile("histos_cortes.root","READONLY")

histoHZ = f.Get("hZmassHZ")
histoWW = f.Get("hZmassWW")
histoZZ = f.Get("hZmassZZ")

histoHZnorm2 = histoHZ.Clone("")
histoWWnorm2 = histoWW.Clone("")
histoZZnorm2 = histoZZ.Clone("")

luminosidad = 5e6
norig = 1e6

csHZ = 0.201868
weightHZ = (csHZ*luminosidad)/norig

csWW = 16.4385
weightWW = (csWW*luminosidad)/norig

csZZ = 1.35899
weightZZ = (csZZ*luminosidad)/norig

histoHZnorm2.Scale(weightHZ)
histoWWnorm2.Scale(weightWW)
histoZZnorm2.Scale(weightZZ)


#Hacemos la integral de los histogramas

print (histoHZnorm2.Integral())
print (histoWWnorm2.Integral())
print (histoZZnorm2.Integral())


#Pintamos histogramas normalizados a la sección eficaz y a la luminosidad

c3 = ROOT.TCanvas("c3","HZ, WW y ZZ analysis canvas", 1024, 768)

histoZZnorm2.Draw("hist,l")
histoWWnorm2.Draw("sames,hist")
histoHZnorm2.Draw("sames,hist")

histo = ROOT.THStack("histo","THStack")
histo.Add(histoWWnorm2)
histo.Add(histoZZnorm2)
histo.Add(histoHZnorm2)
histo.Draw("hist")

histoWWnorm2.SetFillColor(kBlue)
histoZZnorm2.SetFillColor(kGreen)
histoHZnorm2.SetLineColor(kRed)

histo.GetXaxis().SetTitle("m_{Z} (GeV)")
histo.GetYaxis().SetTitle("N_{Events}")

legend = ROOT.TLegend(0.2,0.7,0.48,0.9)
entry=legend.AddEntry(histoWWnorm2,"WW","f")
entry=legend.AddEntry(histoZZnorm2,"ZZ","f")
entry=legend.AddEntry(histoHZnorm2,"HZ","lp")
legend.Draw()

t = ROOT.TLatex()
t.DrawLatexNDC(0.23,0.96, "e{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X #sqrt{s} = 240 GeV, L = 5 ab^{-1}")

output_png = "masaZ_norm2_cortes.png"           #"Masa del Z para los canales HZ, WW y ZZ"

c3.SaveAs(output_png)

