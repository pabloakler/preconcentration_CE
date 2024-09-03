#!/usr/bin/env python3

import numpy as np
import sys, getopt
import distrib

def make_ini(argv):
    inputfile = ''
    pointsfile  = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:",["ifile=","pfile="])
    except getopt.GetoptError:
#        print 'Foam_constants.py -i <inputfile> -p <pointsfile>'
        print('Foam_constants.py -i <inputfile> -p <pointsfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-p","--pfile"):
            pointsfile=arg
    print(inputfile)                 
    print(pointsfile)
    filep=open(pointsfile,'r')
    for j in range(21):
        data=filep.readline()
    npoints=int(filep.readline().split()[0])
    data=filep.readline()
    xnod=np.fromfile(filep,sep=' ',count=npoints).reshape(-1,1)
    

    len=(max(xnod[:,0])-min(xnod[:,0]))*1000
    
    
    nnod,ndim=xnod.shape
       
    arch=open(inputfile,'r',encoding='utf-8')
    data=arch.readline().split()
    ndof=int(data[0])
    an_space=float(data[1])
    cat_space=float(data[2])
    amph=int(data[3])
    solte=np.zeros((nnod,ndof+1))
    if amph:
        ph_data=arch.readline().split()
        n_amph=int(ph_data[1])
        solte=np.zeros((nnod,ndof+n_amph+3))
        ph_min=float(ph_data[2])
        ph_max=float(ph_data[3])
        amph_conc=float(ph_data[4])
    else:
        n_amph=0
    center=0.5*len*(1.0+an_space-cat_space)
    mid_l=(0.5)*len*(1-an_space-cat_space)
    

   
    for i in range(ndof):
        test=arch.readline().split()
        name=test[0]
        conc1=test[1]
        conc2=test[2]
        conc3=test[3]
        b1= conc1==conc2
        b2= conc2==conc3
        b3=not(b1 and b2)
        b4= float(conc1)<0
    
        if b3:
            solte[:,i]=distrib.erfv_stepr(1000*xnod[:,0],2,float(conc3),1.25,(1-cat_space)*len)+distrib.erfv_stepl(1000*xnod[:,0],2,float(conc1),1.25,an_space*len)+distrib.mserf(1000*xnod[:,0],2,float(conc2),1.25,center,mid_l)
            dofaux= 'nonuniform List<scalar>\n'+str(nnod)+'\n (\n'
            dofs=' '.join(str(i)+'\n' for i in solte[:,i])+')\n;'
        else:
            if b4:
                conc4=test[4]
                loc  =float(test[5])
                width=float(test[6])
                print(width)
                solte[:,i]=distrib.mserf(1000*xnod[:,0],40,float(conc4),0.,1000*loc,500*width)
                dofaux= 'nonuniform List<scalar>\n'+str(nnod)+'\n (\n'
                dofs=' '.join(str(i)+'\n' for i in solte[:,i])+')\n;'
                conc1=0.0
                conc3=0.0
                
            else:
            
                dofs=''
                dofaux= 'uniform '+ conc1+';'

        outputfile='./0/ampholyte.'+name

        aux=open(outputfile,'w')
        aux.writelines(header('ampholyte.'+name,nnod))
        aux.writelines(dofaux)
        aux.writelines(dofs)
    #    bounds=0##############OJOOOOOOOOOOOOOOOOOO
        aux.writelines(footer(conc1,conc3)) 
        
        aux.close()
    if amph:    
        for i in range(ndof,ndof+n_amph+1):
            solte[:,i]=distrib.mserf(1000*xnod[:,0],2,1.0*amph_conc/n_amph,1.25,center,mid_l)
            outputfile='./0/ampholyte.'+'A'+str(i-ndof)
            dofaux= 'nonuniform List<scalar>\n'+str(nnod)+'\n (\n'
            dofs=' '.join(str(i)+'\n' for i in solte[:,i])+')\n;'
            aux=open(outputfile,'w')
            aux.writelines(header('ampholyte.A'+str(i-ndof),nnod))
            aux.writelines(dofaux)
            aux.writelines(dofs)
            aux.writelines(footer(0.0,0.0))
            aux.close()
    
    return 



def footer(conc1,conc2):
    footer='\n\nboundaryField\n{\n    front\n    {\n        type            wedge;\n    }\n    back\n    {\n        type            wedge;\n    }\n    wall\n    {\n        type            zeroGradient;\n    }\n    inlet\n    {\n        type            inletOutlet;\n inletValue           uniform '+str(conc1)+';\n    phi             flux;\n   }\n outlet\n    {\n        type            inletOutlet;\n inletValue           uniform '+str(conc2)+';\n    phi             flux;\n   }\n\n    axis    {\n        type            empty;\n    }\n}\n'

    return footer


def header(name,nnod):
    header1='/*--------------------------------*- C++ -*----------------------------------*\ \n| =========                 |                                                 |\n| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n|  \\    /   O peration     | Version:  v3.0+                                 |\n|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |\n|    \\/     M anipulation  |                                                 |\n\*---------------------------------------------------------------------------*/\n FoamFile{\n    version     2.0;\n    format      ascii;\n    class       volScalarField;\n    location    "0";\n    object      '+name+';\n}\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n dimensions      [0 -3 0 0 1 0 0];\n\n internalField  '
    return header1


if __name__ == "__main__":
   make_ini(sys.argv[1:])
