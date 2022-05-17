#!/usr/bin/python3
# coding: utf-8
RELEASE='0.0.1'
'''
ferramentas adb
'''
import os, json, re

def f1(): #listar dispositivos conectados
    A = 'List of devices attached'
    conta = 0
    dados = {}
    dispositivos = []

    os.system('adb devices -l 2>/var/tmp/dispositivos.txt 1>&2')
    with open('/var/tmp/dispositivos.txt', 'r') as DATA:
       dispositivos = DATA.readlines()
    for x in dispositivos:
        if x.strip() != A:
            if 'device' in x.split():
                B = dispositivos[conta].strip()
                serial = B.split()[0]

                if re.findall("[0-9]+[.]+[0-9]+[.]+[0-9]+[.]+[0-9]+[:]+[0-9+]+",serial):
                    modelo = B.split()[3][6:]
                    dispositivo = B.split()[4][7:]
                    conexao = 'IP'
                else:
                    modelo = B.split()[4][6:]
                    dispositivo = B.split()[5][7:]
                    conexao = 'USB'
                dados.update({serial:{'modelo':modelo,'dispositivo':dispositivo,'conexao':conexao}})
                C = dispositivos[conta].strip()
                #print(C.split()[0])
                conta += 1
        else:
            conta += 1
    os.popen('rm -r /var/tmp/dispositivos.txt')
    return dados
def f2(): #listar ip e hostnames dos dispositivos 
    aparelhos = f1()
    for x in aparelhos.keys():
        os.system(f"adb -s {x}"+" shell ip route | awk '{print $9}' 1>/var/tmp/dispositivos_ip.txt 2>&1")
        hostname = os.popen(f'adb -s {x} shell getprop net.hostname')
        with open('/var/tmp/dispositivos_ip.txt', 'r') as json_data:
            ip = json_data.read()
            aparelhos[x].update({'ip':ip.strip(),'hostname':hostname})
    os.popen('rm -r /var/tmp/dispositivos_ip.txt')
    return aparelhos

def f3(serial='192.168.100.161:5555'): #setar adb over wi-fi
    aparelhos = f2()
    print(aparelhos[serial]['ip'])
if __name__ == '__main__':
    #print(f2())
    #print()
    pass
