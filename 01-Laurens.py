import pandas as pd
import urllib
'''
Fuel required to launch a given module is based on its mass.
Specifically, to find the fuel required for a module, take its mass,
divide by three, round down, and subtract 2.
'''

def fuelneeded(mass):
    fuelotadd=int(mass/3)-2
    fuel =0
    while fuelotadd>0:
        fuel+=fuelotadd
        fuelotadd=int(fuelotadd/3)-2
    return fuel

link = "http://adventofcode.com/2019/day/1/input"
#req = urllib.request.Request(link)
#print(req.header_items())
#f = urllib.request.urlopen(req)
#html = response.read()


data = pd.read_csv('input.txt', names=['modules'])
needs=0
for mass in data.modules:
    needs+=fuelneeded(mass)
print(needs)

