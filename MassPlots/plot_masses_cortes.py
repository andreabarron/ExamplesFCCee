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
#sampleName="eeHZ"

# Archivo de entrada
fHZ = TFile('/afs/ciemat.es/user/a/alcaraz/public/FCCee/eeHZ_skimmed_reduced.root')
fWW = TFile('/afs/ciemat.es/user/a/alcaraz/public/FCCee/eeWW_skimmed_reduced.root')
fZZ = TFile('/afs/ciemat.es/user/a/alcaraz/public/FCCee/eeZZ_skimmed_reduced.root')

# Este rootfile tiene un 'tree' llamado events que vamos a
# convertir en un dataframe para analizarlo: 
print("\nProcessing file '%s'..." % (fHZ))
dfHZ = ROOT.RDataFrame("events",fHZ)

print("\nProcessing file '%s'..." % (fWW))
dfWW = ROOT.RDataFrame("events",fWW)

print("\nProcessing file '%s'..." % (fZZ))
dfZZ = ROOT.RDataFrame("events",fZZ)


## PRIMER ARCHIVO HZ ##

# Vamos a ver cuantos muones hay en cada suceso:
# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna/rama")
hNMuonsHZ = dfHZ.Histo1D(("hNMuonsHZ", "Muones Por Suceso ;N_{#mu};N_{Events}",10,0,10), "NMuon")

# Podemos filtrar la muestra para seleccionar parte de
# los sucesos (df.Filter( Seleccion, Explicacion) 
# Por ejemplo, vamos a fijarnos solo en los sucesos con dos muones: 
dfMuonsHZ = dfHZ.Filter("NMuon == 2", "Events with exactly two muons")

# Tambien podemos annadir variables. 
# Dada la geometria del detector es comodo trabajar en cilindricas 
# en vez de cartesianas: vamos a definir el momento del muon en el plano transverso y
# annadirlo al dataframe: 
dfMuonsHZ = dfMuonsHZ.Define("Muon_ptHZ","sqrt((Muon_px)*(Muon_px) + (Muon_py)*(Muon_py))")
dfMuonsHZ = dfMuonsHZ.Define("Muon_energyHZ","sqrt((Muon_mass)*(Muon_mass) + (Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) + (Muon_pz)*(Muon_pz))")
dfMuonsHZ = dfMuonsHZ.Define("Z_massHZ", "sqrt( 2*(Muon_mass)*(Muon_mass) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[0])*(Muon_px[0]) + (Muon_py[0])*(Muon_py[0]) + (Muon_pz[0])*(Muon_pz[0])))*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[1])*(Muon_px[1]) + (Muon_py[1])*(Muon_py[1]) + (Muon_pz[1])*(Muon_pz[1]))))")

dfMuonsHZ = dfMuonsHZ.Filter("Muon_ptHZ[0] > 10 && Muon_ptHZ[1] > 10", "Pt mayores que 10 GeV")
dfMuonsHZ = dfMuonsHZ.Filter("Z_massHZ[0] > 86 && Z_massHZ[0] < 96", "Masa del HZ entre 86 y 96 GeV")


# Cuantos sucesos sobreviven a este corte?
report = dfMuonsHZ.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsHZPx = dfMuonsHZ.Histo1D(("hAllMuonsHZPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsHZPt = dfMuonsHZ.Histo1D(("hAllMuonsHZPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_ptHZ")
hAllMuonsHZCharge = dfMuonsHZ.Histo1D(("hAllMuonsHZCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsHZEnergy = dfMuonsHZ.Histo1D(("hAllMuonsHZEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100), "Muon_energyHZ")

hZmassHZ = dfMuonsHZ.Histo1D(("hZmassHZ", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,70,110), "Z_massHZ")


## SEGUNDO ARCHIVO WW ##

# Vamos a ver cuantos muones hay en cada suceso:
# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna/rama")
hNMuonsWW = dfWW.Histo1D(("hNMuonsWW", "Muones Por Suceso ;N_{#mu};N_{Events}",10,0,10), "NMuon")

# Podemos filtrar la muestra para seleccionar parte de
# los sucesos (df.Filter( Seleccion, Explicacion) 
# Por ejemplo, vamos a fijarnos solo en los sucesos con dos muones: 
dfMuonsWW = dfWW.Filter("NMuon == 2", "Events with exactly two muons")

# Tambien podemos annadir variables. 
# Dada la geometria del detector es comodo trabajar en cilindricas 
# en vez de cartesianas: vamos a definir el momento del muon en el plano transverso y
# annadirlo al dataframe:
dfMuonsWW = dfMuonsWW.Define("Muon_ptWW","sqrt((Muon_px)*(Muon_px) + (Muon_py)*(Muon_py))")
dfMuonsWW = dfMuonsWW.Define("Muon_energyWW","sqrt((Muon_mass)*(Muon_mass) + (Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) + (Muon_pz)*(Muon_pz))")
dfMuonsWW = dfMuonsWW.Define("Z_massWW", "sqrt( 2*(Muon_mass)*(Muon_mass) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[0])*(Muon_px[0]) + (Muon_py[0])*(Muon_py[0]) + (Muon_pz[0])*(Muon_pz[0])))*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[1])*(Muon_px[1]) + (Muon_py[1])*(Muon_py[1]) + (Muon_pz[1])*(Muon_pz[1]))))") 


dfMuonsWW = dfMuonsWW.Filter("Muon_ptWW[0] > 10 && Muon_ptWW[1] > 10", "Pt mayores que 10 GeV")
#dfMuonsWW = dfMuonsWW.Filter("Z_massWW > 86 && Z_massWW < 96", "Masa del WW entre 86 y 96 GeV")

# Cuantos sucesos sobreviven a este corte?
report = dfMuonsWW.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsWWPx = dfMuonsWW.Histo1D(("hAllMuonsWWPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsWWPt = dfMuonsWW.Histo1D(("hAllMuonsWWPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_ptWW")
hAllMuonsWWCharge = dfMuonsWW.Histo1D(("hAllMuonsWWCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsWWEnergy = dfMuonsWW.Histo1D(("hAllMuonsWWEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100), "Muon_energyWW")

hZmassWW = dfMuonsWW.Histo1D(("hZmassWW", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,70,110), "Z_massWW")


## TERCER ARCHIVO ZZ ##

# Vamos a ver cuantos muones hay en cada suceso:
# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) , # "columna/rama")
hNMuonsZZ = dfZZ.Histo1D(("hNMuonsZZ", "Muones Por Suceso ;N_{#mu};N_{Events}",10,0,10), "NMuon")

# Podemos filtrar la muestra para seleccionar parte de
# los sucesos (df.Filter( Seleccion, Explicacion) 
# Por ejemplo, vamos a fijarnos solo en los sucesos con dos muones: 
dfMuonsZZ = dfZZ.Filter("NMuon == 2", "Events with exactly two muons")

# Tambien podemos annadir variables. 
# Dada la geometria del detector es comodo trabajar en cilindricas 
# en vez de cartesianas: vamos a definir el momento del muon en el plano transverso y
# annadirlo al dataframe:
dfMuonsZZ = dfMuonsZZ.Define("Muon_ptZZ","sqrt((Muon_px)*(Muon_px) + (Muon_py)*(Muon_py))")
dfMuonsZZ = dfMuonsZZ.Define("Muon_energyZZ","sqrt((Muon_mass)*(Muon_mass) + (Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) + (Muon_pz)*(Muon_pz))")
dfMuonsZZ = dfMuonsZZ.Define("Z_massZZ", "sqrt( 2*(Muon_mass)*(Muon_mass) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[0])*(Muon_px[0]) + (Muon_py[0])*(Muon_py[0]) + (Muon_pz[0])*(Muon_pz[0])))*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[1])*(Muon_px[1]) + (Muon_py[1])*(Muon_py[1]) + (Muon_pz[1])*(Muon_pz[1]))))")

dfMuonsZZ = dfMuonsZZ.Filter("Muon_ptZZ[0] > 10 && Muon_ptZZ[1] > 10", "Pt mayores que 10 GeV")
#dfMuonsZZ = dfMuonsZZ.Filter("Z_massZZ > 86 && Z_massZZ < 96", "Masa del ZZ entre 86 y 96 GeV")

# Cuantos sucesos sobreviven a este corte?
report = dfMuonsZZ.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsZZPx = dfMuonsZZ.Histo1D(("hAllMuonsZZPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsZZPt = dfMuonsZZ.Histo1D(("hAllMuonsZZPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_ptZZ")
hAllMuonsZZCharge = dfMuonsZZ.Histo1D(("hAllMuonsZZCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsZZEnergy = dfMuonsZZ.Histo1D(("hAllMuonsZZEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100),"Muon_energyZZ")

hZmassZZ = dfMuonsZZ.Histo1D(("hZmassZZ", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,70,110), "Z_massZZ")


out = ROOT.TFile("histos_cortes.root","RECREATE")   #guardamos los histogramas en un archivo ROOT (se corre aquí, pero se pinta en el código "pintar.py")
out.cd()

hZmassHZ.Write()
hZmassWW.Write()
hZmassZZ.Write()


