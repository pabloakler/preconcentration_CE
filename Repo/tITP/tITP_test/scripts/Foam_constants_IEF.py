#!/usr/bin/env python3

import numpy as np
import sys, getopt

from electrolytes import database


def read_props(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('Foam_constants.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    arch=open(inputfile,'r',encoding='utf-8')
    data=arch.readline().split()
    ndof=int(data[0])
    an_space=float(data[1])
    cat_space=float(data[2])
    amph=int(data[3])
    nreact=int(data[4])
    Kn=np.zeros((ndof+1,6))
    diffn=np.zeros(ndof+1)
    movn=np.zeros((ndof+1,6))
    

    if amph:
        ph_data=arch.readline().split()
        n_amph=int(ph_data[1])
        ph_min=float(ph_data[2])
        ph_max=float(ph_data[3])
        ph_range=ph_max-ph_min
        mA=1.0*ph_range*np.asarray(range(n_amph+1))/n_amph + ph_min
        mD=(3-abs(2.78*np.asarray(range(n_amph+1))/n_amph-1.2))/2.0
        pkam1=mA+mD
        pkam2=mA+2.5*mD
        pkap1=mA-mD
        pkap2=mA-2.5*mD

        mov_amph=1e-8*(2+abs(1.40*np.asarray(range(n_amph+1))/n_amph-0.8))
        diff_amph=mov_amph*0.02585065036
        Kn=np.zeros((ndof+n_amph+1,6))
        diffn=np.zeros(ndof+n_amph+1)
        movn=np.zeros((ndof+n_amph+1,6))
        dofs1=''
        for i in range(ndof,ndof+n_amph+1):
            Kn[i]=10**(3-np.asarray([-3,pkap2[i-ndof],pkap1[i-ndof],pkam1[i-ndof],pkam2[i-ndof],15]))
            # Kn[i]=10**(3-np.asarray([-3,-2,pkap1[i-ndof],pkam1[i-ndof],15,16]))
            movn[i]=mov_amph[i-ndof]
            diffn[i]=diff_amph[i-ndof]
            dofs1+=' A'+str(i-ndof)+' \n {\n diffusivity diffusivity [0 2 -1 0 0 0 0 ] '+str(diffn[i])+'; \n'
            dofs1+='mobility mobility [ -1 0 2 0 0 1 0 ] '+str(movn[i])+'; \n'
            Kns=' '.join(str(i) for i in Kn[i].flatten())
            dofs1+=' pk 6('+Kns+');\n}\n'
    
    
    
    
        
    n_dis=6
    dofs=''
    dofnames=[]
    for i in range(ndof):
        subs=arch.readline().split()[0]
        dofnames.append(subs)
        
    K2n=np.zeros((ndof,ndof,ndof))
    K1n=np.zeros((ndof,ndof))
    for i in range(nreact):
        data=arch.readline().split()
        kb=0.5*float(data[1])
        ku=float(data[2])
        r1=int(data[3])
        r2=int(data[4])
        prod=int(data[5])
        l1=[(prod,r1,r2),(prod,r2,r1)]
        l2=[(r1,r1,r2),(r1,r2,r1),(r2,r2,r1),(r2,r1,r2)]#,(prod,r1,prod),(prod,prod,r1),(prod,r2,prod),(prod,prod,r2)]
        l3=[(r1,prod),(r2,prod)]
        l4=(prod,prod)
        for j in l1:
            K2n[j]=-kb
        for j in l2:
            K2n[j]=kb
        for j in l3:
            K1n[j]=-ku
        K1n[l4]=+ku
    i=0    
    for name in dofnames:
        props=database[name]
        diffn[i]=props.diffusivity()
        movn[i]=np.asarray(props.mobilities())
        Kn[i]=10**(3-np.asarray(props.pkas()))
        dofs+=name+' \n {\n diffusivity diffusivity [0 2 -1 0 0 0 0 ] '+str(diffn[i])+'; \n'
        KM=' '.join(str(i) for i in movn[i].flatten())
        dofs+=' mobility 6('+KM+'); \n'
        Kns=' '.join(str(i) for i in Kn[i].flatten())
        Kns1=' '.join(str(i) for i in K1n[i].flatten())
        Kns2=' '.join(str(i) for i in K2n[i].flatten())
        dofs+=' pk 6('+Kns+');\n'
        dofs+=' K1 '+str(ndof)+'('+Kns1+');\n'
        dofs+=' K2 '+str(ndof**2)+'('+Kns2+');\n}\n'
        print(name)
        i+=1

        
         




        
    header='/*--------------------------------*- C++ -*----------------------------------*\ \n| =========                 |                                                 |\n| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n|  \\    /   O peration     | Version:  1.7.1                                 |\n|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |\n|    \\/     M anipulation  |                                                 |\n\*---------------------------------------------------------------------------*/\nFoamFile\n{\n    version     2.0;\n    format      ascii;\n    class       dictionary;\n    location    "constant";\n    object      transportProperties;\n}\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n ampholytes\n ( \n'
    footer='    );\n/***************paper parameters*******************/\n sigma_0 sigma_0 [-1 -3 2 0 1 1 0] 0;\n phip            phip [ 0 0 0 0 0 0 0 ] 1;\n taup            taup [ 0 0 0 0 0 0 0 ] 1;\n sc             sc [ 0 1 0 0 0 0 0 ] 0;\n se             se [ 0 1 0 0 0 0 0 ] 0;\n Kperm          Kperm   [ 0 2 0 0 0 0 0 ] 1;\n zeta           zeta [1 2 -3 0 0 -1 0] -0.0;\n rho_fluid rho_fluid  [1 -3 0 0 0 0 0] 1000.0;\n/**************************************************************************/ \n'

    aux=open(outputfile,'w')
    aux.writelines(header)
    aux.writelines(dofs)
    if amph:
        aux.writelines(dofs1)
    aux.writelines(footer)
    aux.close()
    
    
    
    return 


if __name__ == "__main__":
   read_props(sys.argv[1:])
