#!/bin/bash
rm -rf processor*
foamListTimes -rm
rm ./0/ampholyte*
rm ./constant/ampholyteProperties
blockMesh
postProcess -func writeCellCentres
python ./scripts/Foam_constants_IEF.py -i ./constant/electrolytes.txt -o ./constant/ampholyteProperties

python ./scripts/Foam_ini_IEF.py -i ./constant/electrolytes.txt -p ./0/Cz

