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
hNMuonsHZ = dfHZ.Histo1D(("hNMuonsHZ", "Muones Por Suceso ;N_{#mu};N_{Events}",10,0,10),
"NMuon")

# Podemos filtrar la muestra para seleccionar parte de
# los sucesos (df.Filter( Seleccion, Explicacion) 
# Por ejemplo, vamos a fijarnos solo en los sucesos con dos muones: 
dfMuonsHZ = dfHZ.Filter("NMuon == 2", "Events with exactly two muons")

# Tambien podemos annadir variables. 
# Dada la geometria del detector es comodo trabajar en cilindricas 
# en vez de cartesianas: vamos a definir el momento del muon en el plano transverso y
# annadirlo al dataframe: 
dfMuonsHZ = dfMuonsHZ.Define("Muon_ptHZ","sqrt( (Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) ) ")
dfMuonsHZ = dfMuonsHZ.Define("Muon_energyHZ","sqrt((Muon_mass)*(Muon_mass) + ((Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) + (Muon_pz)*(Muon_pz)))")
dfMuonsHZ = dfMuonsHZ.Define("Z_massHZ", "sqrt( 2*(Muon_mass)*(Muon_mass) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[0])*(Muon_px[0]) + (Muon_py[0])*(Muon_py[0]) + (Muon_pz[0])*(Muon_pz[0])))*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[1])*(Muon_px[1]) + (Muon_py[1])*(Muon_py[1]) + (Muon_pz[1])*(Muon_pz[1]))))")

dfMuonsHZ = dfMuonsHZ.Define("MuonHZ_mass","Muon_mass")

dfMuonsHZ = dfMuonsHZ.Define("Muon1HZ_px","Muon_px[0]")
dfMuonsHZ = dfMuonsHZ.Define("Muon1HZ_py","Muon_py[0]")
dfMuonsHZ = dfMuonsHZ.Define("Muon1HZ_pz","Muon_pz[0]")

dfMuonsHZ = dfMuonsHZ.Define("Muon2HZ_px","Muon_px[1]")
dfMuonsHZ = dfMuonsHZ.Define("Muon2HZ_py","Muon_py[1]")
dfMuonsHZ = dfMuonsHZ.Define("Muon2HZ_pz","Muon_pz[1]")



# Vamos a volver a imprimir sucesos: ahora puedes ver que esta ahi el Pt
#dfMuons.Display({"Muon_px","Muon_py","Muon_pz","Muon_pt","Muon_charge"},10 ).Print()

dfMuonsHZ = dfMuonsHZ.Filter("Muon_ptHZ[0] > 20 && Muon_ptHZ[1] > 20", "Pt mayores que 20 GeV")


# Cuantos sucesos sobreviven a este corte?
report = dfMuonsHZ.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsHZPx = dfMuonsHZ.Histo1D(("hAllMuonsHZPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsHZPt = dfMuonsHZ.Histo1D(("hAllMuonsHZPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_ptHZ")
hAllMuonsHZCharge = dfMuonsHZ.Histo1D(("hAllMuonsHZCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsHZEnergy = dfMuonsHZ.Histo1D(("hAllMuonsHZEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100), "Muon_energyHZ")

hZmassHZ = dfMuonsHZ.Histo1D(("hZmassHZ", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,60,120), "Z_massHZ")


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
dfMuonsWW = dfMuonsWW.Define("Muon_ptWW","sqrt( (Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) ) ")
dfMuonsWW = dfMuonsWW.Define("Muon_energyWW","sqrt((Muon_mass)*(Muon_mass) + ((Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) + (Muon_pz)*(Muon_pz)))")
dfMuonsWW = dfMuonsWW.Define("Z_massWW", "sqrt( 2*(Muon_mass)*(Muon_mass) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[0])*(Muon_px[0]) + (Muon_py[0])*(Muon_py[0]) + (Muon_pz[0])*(Muon_pz[0])))*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[1])*(Muon_px[1]) + (Muon_py[1])*(Muon_py[1]) + (Muon_pz[1])*(Muon_pz[1]))))")

dfMuonsWW = dfMuonsWW.Define("MuonWW_mass","Muon_mass")

dfMuonsWW = dfMuonsWW.Define("Muon1WW_px","Muon_px[0]")
dfMuonsWW = dfMuonsWW.Define("Muon1WW_py","Muon_py[0]")
dfMuonsWW = dfMuonsWW.Define("Muon1WW_pz","Muon_pz[0]")

dfMuonsWW = dfMuonsWW.Define("Muon2WW_px","Muon_px[1]")
dfMuonsWW = dfMuonsWW.Define("Muon2WW_py","Muon_py[1]")
dfMuonsWW = dfMuonsWW.Define("Muon2WW_pz","Muon_pz[1]")

# Vamos a volver a imprimir sucesos: ahora puedes ver que esta ahi el Pt
#dfMuons.Display({"Muon_px","Muon_py","Muon_pz","Muon_pt","Muon_charge"},10 ).Print()

dfMuonsWW = dfMuonsWW.Filter("Muon_ptWW[0] > 20 && Muon_ptWW[1] > 20", "Pt mayores que 20 GeV")


# Cuantos sucesos sobreviven a este corte?
report = dfMuonsWW.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsWWPx = dfMuonsWW.Histo1D(("hAllMuonsWWPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsWWPt = dfMuonsWW.Histo1D(("hAllMuonsWWPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_ptWW")
hAllMuonsWWCharge = dfMuonsWW.Histo1D(("hAllMuonsWWCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsWWEnergy = dfMuonsWW.Histo1D(("hAllMuonsWWEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100), "Muon_energyWW")

hZmassWW = dfMuonsWW.Histo1D(("hZmassWW", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,60,120), "Z_massWW")


## TERCER ARCHIVO ZZ ##

# Vamos a ver cuantos muones hay en cada suceso:
# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna/rama")
hNMuonsZZ = dfZZ.Histo1D(("hNMuonsZZ", "Muones Por Suceso ;N_{#mu};N_{Events}",10,0,10), "NMuon")

# Podemos filtrar la muestra para seleccionar parte de
# los sucesos (df.Filter( Seleccion, Explicacion) 
# Por ejemplo, vamos a fijarnos solo en los sucesos con dos muones: 
dfMuonsZZ = dfZZ.Filter("NMuon == 2", "Events with exactly two muons")

# Tambien podemos annadir variables. 
# Dada la geometria del detector es comodo trabajar en cilindricas 
# en vez de cartesianas: vamos a definir el momento del muon en el plano transverso y
# annadirlo al dataframe:
dfMuonsZZ = dfMuonsZZ.Define("Muon_ptZZ","sqrt( (Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) ) ")
dfMuonsZZ = dfMuonsZZ.Define("Muon_energyZZ","sqrt((Muon_mass)*(Muon_mass) + ((Muon_px)*(Muon_px) + (Muon_py)*(Muon_py) + (Muon_pz)*(Muon_pz)))")
dfMuonsZZ = dfMuonsZZ.Define("Z_massZZ", "sqrt( 2*(Muon_mass)*(Muon_mass) - 2*((Muon_px[0])*(Muon_px[1]) + (Muon_py[0])*(Muon_py[1]) + (Muon_pz[0])*(Muon_pz[1])) + 2*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[0])*(Muon_px[0]) + (Muon_py[0])*(Muon_py[0]) + (Muon_pz[0])*(Muon_pz[0])))*(sqrt((Muon_mass)*(Muon_mass) + (Muon_px[1])*(Muon_px[1]) + (Muon_py[1])*(Muon_py[1]) + (Muon_pz[1])*(Muon_pz[1]))))")

dfMuonsZZ = dfMuonsZZ.Define("MuonZZ_mass","Muon_mass")

dfMuonsZZ = dfMuonsZZ.Define("Muon1ZZ_px","Muon_px[0]")      # creo que esto en principio
                                                             #no nos sirve
dfMuonsZZ = dfMuonsZZ.Define("Muon1ZZ_py","Muon_py[0]")
dfMuonsZZ = dfMuonsZZ.Define("Muon1ZZ_pz","Muon_pz[0]")

dfMuonsZZ = dfMuonsZZ.Define("Muon2ZZ_px","Muon_px[1]")
dfMuonsZZ = dfMuonsZZ.Define("Muon2ZZ_py","Muon_py[1]")
dfMuonsZZ = dfMuonsZZ.Define("Muon2ZZ_pz","Muon_pz[1]")

# Vamos a volver a imprimir sucesos: ahora puedes ver que esta ahi el Pt
#dfMuons.Display({"Muon_px","Muon_py","Muon_pz","Muon_pt","Muon_charge"},10 ).Print()

dfMuonsZZ = dfMuonsZZ.Filter("Muon_ptZZ[0] > 20 && Muon_ptZZ[1] > 20", "Pt mayores que 20 GeV")


# Cuantos sucesos sobreviven a este corte?
report = dfMuonsZZ.Report()
report.Print()

# Dibujemos las variables con Histo1D( ("nombre","titulo;ejeX;ejeY", bines, minX,maxX) ,
# "columna")
hAllMuonsZZPx = dfMuonsZZ.Histo1D(("hAllMuonsZZPx", "MuonPx ; p_{x} (#mu) (GeV) ; N_{Events}", 100,-100,100), "Muon_px")
hAllMuonsZZPt = dfMuonsZZ.Histo1D(("hAllMuonsZZPt", "MuonPt ; p_{T} (#mu) (GeV);N_{Events}", 100,0,100), "Muon_ptZZ")
hAllMuonsZZCharge = dfMuonsZZ.Histo1D(("hAllMuonsZZCharge", "MuonCharge ; Muon or AntiMuon?;N_{Events}",5,-2,2), "Muon_charge")
hAllMuonsZZEnergy = dfMuonsZZ.Histo1D(("hAllMuonsZZEnergy", "MuonEnergy ; E (GeV) ; N_{Events}", 100,0,100), "Muon_energyZZ")

hZmassZZ = dfMuonsZZ.Histo1D(("hZmassZZ", "Zmass ; m_{Z} (GeV) ; N_{Events}", 100,60,120), "Z_massZZ")


out = ROOT.TFile("histos.root","RECREATE")   #guardamos los histogramas en un archivo ROOT
                                             # (se corre aquí, pero se pinta en el código
                                             # pintar)
out.cd()

hZmassHZ.Write()
hZmassWW.Write()
hZmassZZ.Write()


# Proceso HZ

dfMuonsHZ = dfMuonsHZ.Define("totalenergyHZ","ROOT::Math::PxPyPzEVector(0.,0.,0.,240.)")

dfMuonsHZ = dfMuonsHZ.Define("muon1HZ","ROOT::Math::PxPyPzEVector(Muon_px[0],Muon_py[0],Muon_pz[0],Muon_energyHZ[0])")
dfMuonsHZ = dfMuonsHZ.Define("muon2HZ","ROOT::Math::PxPyPzEVector(Muon_px[1],Muon_py[1],Muon_pz[1],Muon_energyHZ[1])")

dfMuonsHZ = dfMuonsHZ.Define("bosonZ_HZ", "muon1HZ + muon2HZ")   # aquí tendríamos el
                                                              # cuadrivector de Z

dfMuonsHZ = dfMuonsHZ.Define("recoilHZ", "totalenergyHZ - bosonZ_HZ")
dfMuonsHZ = dfMuonsHZ.Define("recoilmassHZ","recoilHZ.M()")


#Vamos a sacar el momento transversal Pt del Higgs

dfMuonsHZ = dfMuonsHZ.Define("Higgs_pt","sqrt((recoilHZ.Px())*(recoilHZ.Px()) + (recoilHZ.Py())*(recoilHZ.Py()))")

dfMuonsHZ = dfMuonsHZ.Filter("Higgs_pt > 20", "Pt mayores que 20 GeV")

hHiggsPt = dfMuonsHZ.Histo1D(("hHiggsPt", "Momento transversal del Higgs; P_{t} (H) (GeV); N_{Events}", 100, 0, 100), "Higgs_pt")


hrecoilmassHZ = dfMuonsHZ.Histo1D(("hrecoilmassHZ", "Masa del recoil proceso HZ; m_{recoil} (GeV); N_{Events}", 100, 0, 140), "recoilmassHZ")


#Sacamos el ángulo theta

dfMuonsHZ = dfMuonsHZ.Define("Higgs_ang","recoilHZ.Eta()")
hangHiggs = dfMuonsHZ.Histo1D(("hangHiggs", "Ángulo theta del Higgs proceso HZ; #theta_{H} (rad); N_{Events}", 100, -50, 50))


# Proceso WW

dfMuonsWW = dfMuonsWW.Define("totalenergyWW","ROOT::Math::PxPyPzEVector(0.,0.,0.,240.)")

dfMuonsWW = dfMuonsWW.Define("muon1WW","ROOT::Math::PxPyPzEVector(Muon_px[0],Muon_py[0],Muon_pz[0],Muon_energyWW[0])")
dfMuonsWW = dfMuonsWW.Define("muon2WW","ROOT::Math::PxPyPzEVector(Muon_px[1],Muon_py[1],Muon_pz[1],Muon_energyWW[1])")

dfMuonsWW = dfMuonsWW.Define("bosonZ_WW", "muon1WW + muon2WW")   # aquí tendríamos el
                                                              # cuadrivector de Z

dfMuonsWW = dfMuonsWW.Define("recoilWW", "totalenergyWW - bosonZ_WW")
dfMuonsWW = dfMuonsWW.Define("recoilmassWW","recoilWW.M()")


hrecoilmassWW = dfMuonsWW.Histo1D(("hrecoilmassWW", "Masa del recoil proceso WW; m_{recoil} (GeV); N_{Events}", 100, 0, 140), "recoilmassWW")


# Proceso ZZ

dfMuonsZZ = dfMuonsZZ.Define("totalenergyZZ","ROOT::Math::PxPyPzEVector(0.,0.,0.,240.)")

dfMuonsZZ = dfMuonsZZ.Define("muon1ZZ","ROOT::Math::PxPyPzEVector(Muon_px[0],Muon_py[0],Muon_pz[0],Muon_energyZZ[0])")
dfMuonsZZ = dfMuonsZZ.Define("muon2ZZ","ROOT::Math::PxPyPzEVector(Muon_px[1],Muon_py[1],Muon_pz[1],Muon_energyZZ[1])")

dfMuonsZZ = dfMuonsZZ.Define("bosonZ_ZZ", "muon1ZZ + muon2ZZ")   # aquí tendríamos el
                                                              # cuadrivector de Z

dfMuonsZZ = dfMuonsZZ.Define("recoilZZ", "totalenergyZZ - bosonZ_ZZ")
dfMuonsZZ = dfMuonsZZ.Define("recoilmassZZ","recoilZZ.M()")


hrecoilmassZZ = dfMuonsZZ.Histo1D(("hrecoilmassZZ", "Masa del recoil proceso ZZ; m_{recoil} (GeV); N_{Events}", 100, 0, 140), "recoilmassZZ")



# Recopilamos los histogramas en un archivo

out = ROOT.TFile("histos_higgs.root","RECREATE")   #guardamos los histogramas en un archivo ROOT
                                            #(se corre aquí, pero se pinta en el código "pintar.py")
out.cd()

hrecoilmassHZ.Write()
hrecoilmassWW.Write()
hrecoilmassZZ.Write()
hHiggsPt.Write()
hangHiggs.Write()



