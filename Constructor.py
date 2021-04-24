import csv, operator
from operator import itemgetter
import os

zynq_nam=[]
zynq=[]
cont=os.listdir('./prueba/')
#p=0
for archivo in cont:
   # if p==2:
   #     break
    if archivo[-4:]== '.csv':
        zynq_nam.append(archivo)
        zynq.append(archivo[:-4])
   # p+=1
#print(zynq)
pin=[]
pin_nam=[]
bank=[]

def leer_pines(k):
    ##Extraer nombre de pines, número y banco
    path='./prueba/'+zynq_nam[k]
    with open(path)  as csvarchivos:
        entrada=csv.reader(csvarchivos)
        lista=[]
        for reg in entrada:
            lista.append(reg)
    lista=lista[3:-2]   #eliminamos las 3 primeras lineas y las dos ultimas, que no continene pines
    lista=sorted(lista, key=itemgetter(1))
    lista=sorted(lista, key=itemgetter(3))  #ordenar por el numero de banco
    #print(lista)
    pin=[]
    pin_nam=[]
    bank=[]
    for i in range(len(lista)): #clasificacion de pines
        pin.append(lista[i][0]) #meter los numeros de los pines en la lista 'pines'
       # print(pin)
        pin_nam.append(lista[i][1]) #meter los nombres de los pines en la lista 'pin_nam''
        bank.append(lista[i][3]) #meter los bancos de cada pin en la lista 'bank'
    return pin, pin_nam, bank
#print(pin)


def num_capas():    #numero de bancos
    bank_prev=""
    cont=0
    banko=sorted(bank)
    for k in range(len(bank)):
        if bank_prev!=banko[k]:
            cont+=1
            bank_prev=banko[k]
    return cont

def num_pines(banco):   #numero de pines por banco
    return bank.count(banco)

bidirec=["PS_MIO", "IO_", "PS_DDR_DQS_N", "PS_DDR_DQS_P", "DONE", "INIT_B", "PS_DDR_DQ", "T0_DQS", "T1_DQS", "T2_DQS", "T3_DQS"]
power=["VCC", "PS_MIO_V", "GND", "PS_DDR_VREF", "VREFP", "VREFN"]
output=["TDO", "PS_DDR_CKP", "PS_DDR_CKN", "PS_DDR_CKE", "PS_DDR_CS_B", "PS_DDR_RAS_B", "PS_DDR_CAS_B", "PS_DDR_WE_B", "PS_DDR_BA", "PS_DDR_A", "PS_DDR_ODT", "PS_DDR_DRST_B", "PS_DDR_DM", "PS_DDR_VRP", "PS_DDR_VRN", \
    "MGTXTXP", "MGTPTXP", "MGTXTXN", "MGTPTXN",]
#creador de pines
def create_pin():
    pin_kicad=""
    bank_prev=""
    capa=0
    visi='I'
    sq_y1=0
    sq_y2=0
    pin_nam_prev=0
    #init=400
    t=0
    ult_capa=0
    def pin_create(pin_nam, num_pin, pos_pin, capa, x='650',  long='200', dir='L', text_tam='50', num_tam='50', Morg='1', visi='I'):
        return "X "+str(pin_nam)+" " +str(num_pin)+ " " + x +" "+str(pos_pin)+ " "+ str(long)+ " " + str(dir) + " " + str(text_tam) + " " +str(num_tam) + " " + str(capa) + " " +str(Morg)+" " +str(visi)

    for j in range(len(pin)):

        ##Asignacion de capas
        t+=1
        visi='I'
        if bank[j]!= bank_prev  :
            capa+=1
            if capa<num_capas():
                visi='I'
                bank_prev=bank[j]
                t=0
                init=num_pines(bank[j])*50
                sq_y1=init+200
                sq_y2=-init-100
                pin_kicad+="\nS 450 "+ str(sq_y1) + " -700 " + str(sq_y2) + " " + str(capa) + " 1 0 f"
            elif capa==num_capas():
                if ult_capa==0:
                    t=0
                    #print("Entro1")
                    ult_capa=1
                    visi='W'
                    gnd=pin_nam.count("GND")
                    init=(gnd)*50
                    sq_y1=init+200
                    sq_y2=-init-100
                    pin_kicad+="\nS 450 "+ str(sq_y1) + " -600 " + str(sq_y2) + " " + str(capa) + " 1 0 f"
            else:
                capa=num_capas()+1
        if ult_capa==1:
            if pin_nam[j]=="GND":
                visi="W"
                capa=num_capas()
                pin_nam_prev=1
            else:
                visi="W"
                if pin_nam_prev==1:
                    #print("entro2")
                    t=0
                    pin_nam_prev=0
                    capa=num_capas()+1
                    init=(num_pines(bank[j])-gnd)*50
                   # print((num_pines(bank[j])-gnd)*50)
                    sq_y1=init+200
                    sq_y2=-init-100 
                    pin_kicad+="\nS 450 "+ str(sq_y1) + " -600 " + str(sq_y2) + " " + str(capa) + " 1 0 f"
       # if pin_nam[j][:6]=="PS_MIO" or  pin_nam[j][:3]=="IO_" or pin_nam[j][:4]=="DONE" or pin_nam[j][:6]=="INIT_B" or pin_nam[j][:9]=="PS_DDR_DQ" or pin_nam[j][:12]=="PS_DDR_DQS_P"or pin_nam[j][:12]=="PS_DDR_DQS_N":
       #     visi='B'
        #elif pin_nam[j][:3]=="VCC" or pin_nam[j][:8]=="PS_MIO_V":
        #    visi="W"
        #elif pin_nam[j][:3]=="TDO" or pin_nam[j][:3]PS_DDR_CKP:
        #    visi="O"
        for l in bidirec:
            if pin_nam[j][:len(l)]==l:
                visi="B"
        for o in power:
            if pin_nam[j][:len(o)]==o:
                visi="W"
        for h in output:
            if pin_nam[j][:len(h)]==h:
                visi="O"
        pin_kicad+="\n"+pin_create(pin_nam[j],pin[j], (init-t*100), capa, visi=visi)
    return pin_kicad


def longitud():
    lon_max=0
    cont=0
    for k in range(len(bank)):
        lon=bank.count(bank[k])
        #print(lon)
        if lon>lon_max:
            lon_max=lon
    return lon_max



#apertura de fichero
f=open("Zynq7000.lib", "w")


wr="EESchema-LIBRARY Version 2.4 \n#encoding utf-8"

#print(dat)
j=0
for i in zynq:
    
    pin, pin_nam, bank=leer_pines(j)
    dat=-int(longitud()*50+150)
    wr+="\n#\n# "+i+"\n#"
    wr+="\nDEF "+i+" U 0 40 Y Y "+str(num_capas()+1)+" L N"
    wr+="\nF0  \"U\" -550 "+str(-dat+100)+" 50 H V C CNN"
    wr+="\nF1  \""+i+"\" -450 "+str(dat)+" 50 H V C CNN"
    wr+="\nF2  \"\" 0 "+str(dat)+" 50 H I C CNN"
    wr+="\nF3  \"\" 0 "+str(dat)+" 50 H I C CNN"
    wr+="\nDRAW"
    wr+=create_pin()
    wr+="\nENDDRAW"
    wr+="\nENDDEF"
    j=j+1
wr+="\n#\n#End library"
#Escritura
f.write(wr)