#! /usr/bin/env python3
#
# 1) Setup ROOT with: 
#   "source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh"
# 2) Run this script as:
#   "python -i [python_script]"
#

import os, sys, math
import ROOT
import multiprocessing

import tdrstyle

from ROOT import *

# CMS Style (estilo para los plots)
tdrstyle.setTDRStyle()

# Proceso que vamos a estudiar
sampleName="eeHZ"

# Archivo de entrada
#file = "/afs/ciemat.es/user/a/alcaraz/public/FCCee/"+sampleName+"_skimmed_reduced.root"
#file = TFile('/afs/ciemat.es/user/c/cepeda/public/archivoPruebaAndrea.root')

file = TFile('/afs/ciemat.es/user/a/alcaraz/public/FCCee/eeHZ_skimmed_reduced.root')


# Este rootfile tiene un 'tree' llamado events que vamos a
# convertir en un dataframe para analizarlo: 
print("\nProcessing file '%s'..." % (file))
df = ROOT.RDataFrame("events",file)
# Para ver que variables hay en el tree: imprimamos unos cuantos sucesos
#df.Display("").Print()

# Vamos a ver cuantos muones hay en cada suceso:
# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna/rama")
hNMuons = df.Histo1D(("hNMuons", "Muones Por Suceso ;N_{#mu};N_{Events}",10,0,10), "NMuon")

# Podemos filtrar la muestra para seleccionar parte de
# los sucesos (df.Filter( Seleccion, Explicacion) 
# Por ejemplo, vamos a fijarnos solo en los sucesos con dos muones: 
dfMuons = df.Filter("NMuon == 2", "Events with exactly two muons")



# Tambien podemos annadir variables. 
# Dada la geometria del detector es comodo trabajar en cilindricas 
# en vez de cartesianas: vamos a definir el momento del muon en el plano transverso y
# annadirlo al dataframe: 
dfMuons = dfMuons.Define("Muon_pt","sqrt( pow(Muon_px,2)+pow(Muon_py,2) ) ")
dfMuons = dfMuons.Define("Muon_energy","sqrt(pow(Muon_mass,2)+(pow(Muon_px,2)+pow(Muon_py,2)+pow(Muon_pz,2)))")
dfMuons = dfMuons.Define("Muon_px_0","Muon_px[0]")
dfMuons = dfMuons.Define("Muon_pt_0","sqrt( pow(Muon_px[0],2)+pow(Muon_py[0],2) ) ")
dfMuons = dfMuons.Define("Muon_charge_0","Muon_charge[0]")
dfMuons = dfMuons.Define("Muon_energy_0","sqrt(pow(Muon_mass[0],2)+pow(Muon_px[0],2)+pow(Muon_py[0],2)+pow(Muon_pz[0],2))")
dfMuons = dfMuons.Define("Muon_px_1","Muon_px[1]")
dfMuons = dfMuons.Define("Muon_pt_1","sqrt( pow(Muon_px[1],2)+pow(Muon_py[1],2) ) ")
dfMuons = dfMuons.Define("Muon_charge_1","Muon_charge[1]")
dfMuons = dfMuons.Define("Muon_energy_1","sqrt(pow(Muon_mass[1],2)+pow(Muon_px[1],2)+pow(Muon_py[1],2)+pow(Muon_pz[1],2))")
dfMuons = dfMuons.Define("Z_mass", "sqrt( 2*pow(Muon_mass,2) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt(pow(Muon_mass,2) + pow(Muon_px[0],2) + pow(Muon_py[0],2) + pow(Muon_pz[0],2)))*(sqrt(pow(Muon_mass,2) + pow(Muon_px[1],2) + pow(Muon_py[1],2) + pow(Muon_pz[1],2))))")

# Vamos a volver a imprimir sucesos: ahora puedes ver que esta ahi el Pt
#dfMuons.Display({"Muon_px","Muon_py","Muon_pz","Muon_pt","Muon_charge"},10 ).Print()

dfMuons = dfMuons.Filter("Muon_pt[0] > 20 && Muon_pt[1] > 20", "Pt mayores que 20 GeV")


# Cuantos sucesos sobreviven a este corte?
report = dfMuons.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsPx = dfMuons.Histo1D(("hAllMuonsPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsPt = dfMuons.Histo1D(("hAllMuonsPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_pt")
hAllMuonsCharge = dfMuons.Histo1D(("hAllMuonsCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsEnergy = dfMuons.Histo1D(("hAllMuonsEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100), "Muon_energy")
hMuon0Px = dfMuons.Histo1D(("hMuon0Px", "Muon0Px ; p_{x} (#mu_{0}) (GeV) ; N_{Events}", 100,-100,100), "Muon_px_0")
hMuon0Pt = dfMuons.Histo1D(("hMuon0Pt", "Muon0Pt ; p_{T} (#mu_{0}) (GeV) ; N_{Events}", 100,0,100), "Muon_pt_0")
hMuon0Charge = dfMuons.Histo1D(("hMuon0Charge", "Muon0Charge ; Muon or Antimuon? ; N_{Events}", 5,-2,2), "Muon_charge_0")
hMuon0Energy = dfMuons.Histo1D(("hMuon0Energy", "Muon0Energy ; E (#mu_{0}) (GeV) ; N_{Events}", 100,0,100), "Muon_energy_0")
hMuon1Px = dfMuons.Histo1D(("hMuon1Px", "Muon1Px ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px_1")  #hemos quitado en px, pt y energy "_{1}" detrás de "#mu" para que en los ejes de la superposición de los muones nos aparezca solo "mu"
hMuon1Pt = dfMuons.Histo1D(("hMuon1Pt", "Muon1Pt ; p_{T} (#mu) (GeV) ; N_{Events}", 100,0,100), "Muon_pt_1")
hMuon1Charge = dfMuons.Histo1D(("hMuon1Charge", "Muon1Charge ; Muon or Antimuon? ; N_{Events}", 5,-2,2), "Muon_charge_1")
hMuon1Energy = dfMuons.Histo1D(("hMuon1Energy", "Muon1Energy ; E (#mu) (GeV) ; N_{Events}", 100,0,100), "Muon_energy_1")

hZmass = dfMuons.Histo1D(("hZmass", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,60,120), "Z_mass")

out = ROOT.TFile("histosHZ.root","RECREATE") 
out.cd()

hAllMuonsPx.Write()
hAllMuonsPt.Write()
hAllMuonsCharge.Write()
hAllMuonsEnergy.Write()
hMuon0Px.Write()
hMuon0Pt.Write()
hMuon0Charge.Write()
hMuon0Energy.Write()
hMuon1Px.Write()
hMuon1Pt.Write()
hMuon1Charge.Write()
hMuon1Energy.Write()







