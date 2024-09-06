-------------------------------------------------------------------------------
      electroMicroTransport | Copyright (C) 2016-2018 Santiago Marquez Damian
                            |                         Pablo Alejandro Kler 
-------------------------------------------------------------------------------

This tutorial example performs a CZE separation of cations pyridine and aniline
by using a background buffer of Tris-Acetic acid. A 20 cm capillary tube is
used where a 2500 A/m^2 constant curret is applied. In order to change the
electrolyte composition edit the file ./constant/electrolytes.txt.

Regarding the grid, the capillary tube was divided into 16000 linear segments.
The simulation runs for 240 seconds giving the concentration profiles for
pyridine and aniline showing the characteristic triangular shape expected due
to electrodispersion.

-------------------------------------------------------------------------------
Bug reporting and testing by Federico Schaumburg
Tested with OpenFOAM(R) v.1712+

