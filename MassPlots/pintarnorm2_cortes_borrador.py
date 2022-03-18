import ROOT
import tdrstyle

from ROOT import *

# CMS Style (estilo para los plots)
tdrstyle.setTDRStyle()

# Carga el archivo con los histogramas

f=ROOT.TFile("histos_higgs_cortes.root","READONLY")

historecoilmassHZ = f.Get("hrecoilmassHZ")
historecoilmassWW = f.Get("hrecoilmassWW")
historecoilmassZZ = f.Get("hrecoilmassZZ")

#weightHZ = f.Get("weightHZ")
#weightWW = f.Get("weightWW")
#weightZZ = f.Get("weightZZ")


historecoilmassHZnorm = historecoilmassHZ.Clone("")
historecoilmassWWnorm = historecoilmassWW.Clone("")
historecoilmassZZnorm = historecoilmassZZ.Clone("")

luminosidad = 5e6
norig = 1e6

csHZ = 0.201868
weightHZ = (csHZ*luminosidad)/norig

csWW = 16.4385
weightWW = (csWW*luminosidad)/norig

csZZ = 1.35899
weightZZ = (csZZ*luminosidad)/norig

historecoilmassHZnorm.Scale(weightHZ)           #(1. /weightHZ, "width")
historecoilmassWWnorm.Scale(weightWW)           #(1. /weightWW, "width")
historecoilmassZZnorm.Scale(weightZZ)           #(1. /weightZZ, "width")

print (historecoilmassHZ.Integral())
print (historecoilmassWW.Integral())
print (historecoilmassZZ.Integral())

#historecoilmassHZ.Scale(weightHZ)


#Pintamos histogramas normalizados a la sección eficaz y a la luminosidad

c2 = ROOT.TCanvas("c2","HZ, WW y ZZ analysis canvas", 1024, 768)

historecoilmassHZnorm.Draw("hist,l")
historecoilmassWWnorm.Draw("sames,hist")
historecoilmassZZnorm.Draw("sames,hist")

#historecoilmassHZnorm.Draw("hist")
#historecoilmassWWnorm.Draw("sames,stack")
#historecoilmassZZnorm.Draw("sames,stack")

##historecoilmassHZnorm.SetFillColor(kRed)
##historecoilmassWWnorm.SetFillColor(kBlue)
##historecoilmassZZnorm.SetFillColor(kGreen)

##historecoilmassHZnorm.SetMarkerColor(kRed)
##historecoilmassWWnorm.SetMarkerColor(kBlue)
##historecoilmassZZnorm.SetMarkerColor(kGreen)

##historecoilmassHZnorm.SetMarkerColor(20)
##historecoilmassWWnorm.SetMarkerColor(21)
##historecoilmassZZnorm.SetMarkerColor(22)


historecoil = ROOT.THStack("historecoil","THStack")
historecoil.Add(historecoilmassWWnorm)
historecoil.Add(historecoilmassZZnorm)
historecoil.Add(historecoilmassHZnorm)
historecoil.Draw("hist")

historecoilmassWWnorm.SetFillColor(kBlue)
historecoilmassZZnorm.SetFillColor(kGreen)
historecoilmassHZnorm.SetLineColor(kRed)

historecoil.GetXaxis().SetTitle("m_{recoil} (GeV)")
historecoil.GetYaxis().SetTitle("N_{Events}")

legend = ROOT.TLegend(0.5,0.5,0.9,0.9)
entry=legend.AddEntry(historecoilmassWWnorm,"WW","f")
entry=legend.AddEntry(historecoilmassZZnorm,"ZZ","f")
entry=legend.AddEntry(historecoilmassHZnorm,"HZ","lp")
legend.Draw()

t = ROOT.TLatex()
t.DrawLatexNDC(0.17,0.96, "e{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X #sqrt{s} = 240 GeV, L = 5 ab^{-1}")

output_png = "recoil_massnorm_cortes.png"           #"Masa del Z para los canales HZ, WW y ZZ"

c2.SaveAs(output_png)



