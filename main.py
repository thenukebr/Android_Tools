#!/usr/bin/python3
# coding: utf-8

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
import save_data as Data
import os

class Aplicativo(App):
    def build(self):
        return Home()

class Home(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def atualizar(self):
        self.ids.aparelhos.clear_widgets()
        self.load_data = Data.f2()
        for x in self.load_data.keys():
            idserial = x
            idmodelo = self.load_data[x]['modelo']
            idversao = self.load_data[x]['dispositivo']
            idconexao = self.load_data[x]['conexao']
            idip = self.load_data[x]['ip']
            idhostnmae = self.load_data[x]['hostname']
            self.ids.aparelhos.add_widget(Dispositivos(serial=idserial,modelo=idmodelo,versao=idversao,conexao=idconexao,ip=idip))
            print(idserial, idmodelo)

class Dispositivos(BoxLayout):
    def __init__(self,serial='',modelo='',versao='',conexao='',ip='', **kwargs):
        super().__init__(**kwargs)
        self.dado = (serial, modelo, versao, conexao, ip)
        
        self.ids.host.text = self.dado[0]
        self.ids.host.values = self.dado
        #self.ids.info.text = self.dado[1]
    def adb_wifi(self):
        if self.dado[3] == 'USB':
            os.popen(f'adb -s {self.dado[0]} tcpip 5555')
            os.popen(f'adb connect {self.dado[4]}:5555')
            Home().atualizar()
        elif self.dado[3] == 'IP':
            os.popen(f'adb reconnect {self.dado[4]:5555}')
            Home().atualizar()
    def adb_usb(self):
        if self.dado[3] == 'IP':
            os.popen(f'adb -s {self.dado[4]}:5555 usb')
            Home().atualizar()
    def remote(self):
        if self.dado[3] == 'USB':
            os.popen(f'nohup scrcpy -w -S -s {self.dado[0]} 1>/dev/null 2>&1 &')
        elif self.dado[3] == 'IP':
            os.popen(f'nohup scrcpy -w -S -s {self.dado[0]} 1>/dev/null 2>&1 &')
if __name__ == '__main__':
    Aplicativo().run()
