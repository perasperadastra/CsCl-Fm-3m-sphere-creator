##building my .xyz file
##this is a building script for create a sphere of CsCl in rock salt form
##Space group: Fm-3m  == NaCl
import random
#import time
import os
#functions
def clear():
    os.system('clear')
def spherecut(cordict, totalatom, longcub):
    ##este funcion va haciendo un loop sobre cada el indice que es la suma de las coordenadas. Si el valor devuelto de tamaño
    ## de cuadrado no permite existir a la esfera dvuelve el false y se aumentará el valor del indice.
    ##ademas se va creando una lista de los indices que permite ordenar del centro hacia fuera la esfera.
    index=0
    indexsub=[]
    contador=0
    while True:
        indexsub.append(index)
        spherecord={}
        for i in indexsub:
            for natom,  cord in cordict.items():
                n0=abs(cord[0])
                n1=abs(cord[1])
                n2=abs(cord[2])
                num=n0+n1+n2
                if num<=i:
                    spherecord[natom]=cord
        sphereatom=0
        for key in spherecord:
                sphereatom=sphereatom+1
        if sphereatom>=totalatom:
            bol=True
            return sphereatom , spherecord,  bol,  index
        if index==longcub:
            bol=False
            sphereatom=0
            spherecord=0
            return sphereatom , spherecord,  bol,  index
        index=index+1/2    
        contador=contador+1
def order(dict):
    dict2={}
    contador=0
    for key, value in dict.items():
        dict2[contador]=value
        contador=contador+1
    return dict2

def sphcenter(cordict):
    maxi=0
    for key ,  values in cordict.items():
        if values[0]>maxi:
            maxi=values[0]
    middle=maxi/2
    sphcenter=[middle, middle, middle]
    return sphcenter,  middle
 
def basechange(coord, middle):
    for key,  values in coord.items():
        cor0=values[0]-middle
        cor1=values[1]-middle
        cor2=values[2]-middle
        coord[key]=[cor0, cor1, cor2]
    return    coord
#############################
clear()    
a =6.923 #A

totalatom=int(input('select an aproximated number of atoms (integer):  '))


##here we make a big square and the we reduce it to a sphere
n=0
m=0
s=0
coord=[n, m, s]
##dimension del cubo
longcub=1 

#x permutation
while True:
    cordict={}
    numeration=0
    numbr0=0
    numbr1=0
    numbr2=0
    while True:
        n1=n+1/2*numbr0   
        for num in range(2*longcub+1):
            m1=m+num*1/2 
            for nums in range(2*longcub+1):
                s1=s+nums*1/2
                cordict[numeration]=[n1, m1, s1]   
                numbr2=numbr2+1
                numeration=numeration+1
            numbr1=numbr1+1
            s1=s
        numbr0=numbr0+1
        m1=m
        if (numbr0)<=(longcub*2):
            continue
        break
    spherecenter,  middle=sphcenter(cordict)
    cordict=basechange(cordict, middle)
    sphereatom, coordsph, bol, maxindex=spherecut(cordict, totalatom, longcub)
    if bol==True:   #voy a poner una condicion de corte para comprobar si la esfera cabe en el cuadrado
        break
    longcub=longcub+1


##counting atoms in the square
numatomsquare=0
for key in cordict:
    numatomsquare=numatomsquare+1

###printing messages
print(str(numatomsquare)+' atoms in the initial square')
print(str(sphereatom)+' atoms in the pre-sphere')

##reordening sphere coordinates
finalcoord=order(coordsph)


##eliminating random atoms to obtain our number
ind=maxindex
spatom=sphereatom

while True:
    remlist=[]
    for key ,  values in finalcoord.items():
        cor0=abs(values[0])
        cor1=abs(values[1])
        cor2=abs(values[2]) 
        num=cor0+cor1+cor2
        if num==ind:
            remlist.append(key)
            spatom=spatom-1
    if spatom<=totalatom:
        break
    for i in remlist:
        del finalcoord[i]
    ind=ind-1/2
spatom=sphereatom

while True:
    num=random.choice(remlist)
    for key in list(finalcoord.keys()):
        if key==num:
            del finalcoord[key]
            remlist.remove(key)
            spatom=spatom-1
    if spatom==totalatom:
        break

###reorder finalcoords
finalcoord=order(finalcoord)

####################################################
##                      Output to a .xyz file                                                                          ##
##                                                                                                                               ##
####################################################

struc=open('mycrystalstructure.xyz','w' )
struc.write(str(totalatom)+'\n')
struc.write('## Cs Cl ,this is m crystal sphere'+'\n')

clindex=maxindex-1/2
csindex=maxindex    
Clx=[]
Csx=[]
while True:
    if clindex>=0:
        Clx.append(clindex)
        clindex=clindex-1
    else:
        break
while True:
    if csindex>=0:
        Csx.append(csindex)
        csindex=csindex-1
    else:
        break

csatom=0
clatom=0
for key, cord in finalcoord.items():
    num=abs(cord[0])+abs(cord[1])+abs(cord[2])
    cor0=cord[0]*a
    cor1=cord[1]*a
    cor2=cord[2]*a
    if num in Csx:
        struc.write('Cs    '+str(cor0)+'    '+str(cor1)+'    '+str(cor2)+'\n')
        csatom=csatom+1
    if num in Clx:
        struc.write('Cl    '+str(cor0)+'    '+str(cor1)+'    '+str(cor2)+'\n')
        clatom=clatom+1
struc.close()
print('')
print('')
#print(sphereatom)
#print(coordsph)
print(str(csatom)+' Cs atoms')
print(str(clatom)+' Cl atoms')
    
    
    
print('final')
