import threading
from os import times
import time
from tkinter import PhotoImage, Button, NW

from graficos import NoGrafico
from numpy import random
#from graficos import ToggleButton
from graficos import ColorUtils

class TelaGrafo:

    def __init__(self, canvas, historia, raiz):
        self.canvas=canvas
        self.raiz = raiz
        self.historia=historia
        self.listaNo=[]
        self.tradutorNo={}
        self.niveis={}
        #self.colocarNosGraficos()
        #self.conectar()
        self.configuraCanvas ()
        self.canvas.bind('<Configure>',self.reconfigureCanvas)



        self.canvas.origem=None
        self.canvas.destino=None
        self.canvas.ColocarAresta=self.ColocarAresta
        self.canvasinitAresta = False

    def reordenarArvore(self):
        self.niveis={}
        self.montarArvoreBonita(self.copa)

    def montarArvoreBonita(self,root):
        if root.nivel not in self.niveis:
            self.niveis[root.nivel]=[]
        self.niveis[root.nivel].append(root)
        self.posicionar(root.nivel)
        for no in root.prox:
            self.montarArvoreBonita(no)

    def incluirNo(self,pai,no,texto):

        novo_no_g=NoGrafico.NoGrafico(self.canvas,no,texto)
        novo_no_g.prox=[]
        novo_no_g.nivel=self.tradutorNo[pai].nivel+1
        if(novo_no_g.nivel not in self.niveis):
            self.niveis[novo_no_g.nivel]=[]
        self.niveis[novo_no_g.nivel].append(novo_no_g)
        self.tradutorNo[pai].prox.append(novo_no_g)
        self.tradutorNo[pai].addFilho(novo_no_g)
        self.tradutorNo[no]=novo_no_g
        self.posicionar(novo_no_g.nivel)

    def mudarCorArvore(self,cor):
        maxi= max([len(x) for x in self.niveis.values()])
        for nivel in self.niveis:
            valorNivel=len(self.niveis[nivel])
            c=valorNivel/maxi
            for no in self.niveis[nivel]:
                no.mudarCorTexto(ColorUtils.toHex(int(c*105)+150,0,0))

    def incluirRaiz(self,no,texto):

        novo_no_g=NoGrafico.NoGrafico(self.canvas,no,texto)
        self.copa=novo_no_g
        novo_no_g.prox = []
        novo_no_g.nivel=0
        if(novo_no_g.nivel not in self.niveis):
            self.niveis[novo_no_g.nivel]=[]
        self.niveis[novo_no_g.nivel].append(novo_no_g)
        self.tradutorNo[no] = novo_no_g
        self.posicionar(0)

    def posicionar(self,nivel):
            n=len(self.niveis[nivel])
            a=1200/(n+1)
            for no,i in zip(self.niveis[nivel],range(1,n+1)):
                no.moverPara(a*i,(nivel*70)+10)



    def colocarNosGraficos(self):

        for indice in self.historia.obter_lista_cenarios():
            no=self.historia.obter_lista_cenarios()[indice]
            noGrafico=NoGrafico.NoGrafico(self.canvas,no,no.obter_nome())
            self.listaNo.append(noGrafico)
            no.grafico=noGrafico
            no.index=indice

    def conectar(self):
        for indice in self.historia.obter_lista_cenarios():
            no = self.historia.obter_lista_cenarios ()[indice]
            for indiceFilho in no.obter_conexoes():
                filho=self.historia.obter_lista_cenarios ()[indiceFilho]
                no.grafico.addFilho(filho.grafico)
                filho.grafico.addFilho(no.grafico)


    def revalidar(self):
        for noGrafico in self.listaNo:
            noGrafico.revalidar()

    def configuraCanvas(self):

        def moveTela(event):
            threading.Thread (target=self.mexerThread).start ()

        def moveTelaL(event):
            threading.Thread (target=self.mexerThreadL).start ()

        def moveTelaB(event):
            threading.Thread (target=self.mexerThreadB).start ()

        def moveTelaR(event):
            threading.Thread (target=self.mexerThreadR).start ()

        def paraMover(event):
            self.boolean = False;

        self.raiz.update()

        w=self.canvas.winfo_width()
        h=self.canvas.winfo_height()

        # self.b1=self.canvas.create_rectangle(200,0,w-200,50,tags="listenerC",fill="#f15e5e",outline="#72b5a4",stipple="gray12",width=0)
        # self.canvas.tag_bind("listenerC",'<Enter>',moveTela)
        # self.canvas.tag_bind ("listenerC", '<Leave>',paraMover)
        #
        # self.b2=self.canvas.create_rectangle (0, 200, 50, h-200,tags="listenerL",fill="#f15e5e",outline="#72b5a4",stipple="gray12",width=0)
        # self.canvas.tag_bind ("listenerL", '<Enter>', moveTelaL)
        # self.canvas.tag_bind ("listenerL", '<Leave>', paraMover)
        #
        # self.b3=self.canvas.create_rectangle (200, h-50, w-200, h, tags="listenerB", fill="#f15e5e", outline="#72b5a4",
        #                               stipple="gray12", width=0)
        # self.canvas.tag_bind ("listenerB", '<Enter>', moveTelaB)
        # self.canvas.tag_bind ("listenerB", '<Leave>', paraMover)
        #
        # self.b4 =self.canvas.create_rectangle (w-50, 200, w, h-200, tags="listenerR", fill="#f15e5e", outline="#72b5a4",
        #                               stipple="gray12", width=0)
        # self.canvas.tag_bind ("listenerR", '<Enter>', moveTelaR)
        # self.canvas.tag_bind ("listenerR", '<Leave>', paraMover)

    def reconfigureCanvas(self,event):
        self.canvas.delete(self.b1)
        self.canvas.delete (self.b2)
        self.canvas.delete (self.b3)
        self.canvas.delete (self.b4)
        self.configuraCanvas()

    def ColocarAresta(self):
        if(self.canvas.origem is not None and self.canvas.destino is None):
            self.canvas.origem.dourar()

        if(self.canvas.origem is not None and self.canvas.destino is not None):
            self.canvas.origem.addFilho(self.canvas.destino)
            self.canvas.destino.addFilho (self.canvas.origem)
            self.historia.adicione_conexao_entre_dois_cenarios(self.canvas.origem.dono.index,self.canvas.destino.dono.index)

            self.canvas.origem=None
            self.canvas.destino=None


    def retirarAresta(self):
        if (self.canvas.origem is not None):
            self.canvas.origem.mudarCorBorda (ColorUtils.toHex (200, 20, 120))
            if (self.canvas.origem is not None and self.canvas.destino is not None):
                self.canvas.origem.addFilho (self.canvas.destino)
                self.canvas.destino.addFilho (self.canvas.origem)
                self.historia.adicione_conexao_entre_dois_cenarios (self.canvas.origem.dono.index,
                                                                        self.canvas.destino.dono.index)
                self.canvas.origem = None
                self.canvas.destino = None



            #algoritmo de inserir nó
            #TODO metodo de inserir aresta

    def incluirNovoNo(self):
        indice=self.historia.adicione_novo_cenario()
        no = self.historia.obter_lista_cenarios ()[indice]
        nome=no.obter_nome()
        no.grafico =NoGrafico.NoGrafico(self.canvas,no,nome)
        no.index=indice


    def initArestaTrue(self):
        print ("s")
        self.canvas.initAresta = True

    def initArestaFalse(self):
        print ("n")
        self.canvas.initAresta = False

    def testPrintar(self):
        self.historia.mostre_cenarios()


    def mexerThread(self):
        self.boolean = True;
        while self.boolean:
            self.canvas.move ("tudo", 0, 10)
            time.sleep(0.01)

    def mexerThreadB(self):
        self.boolean = True;
        while self.boolean:
            self.canvas.move ("tudo", 0, -10)
            time.sleep(0.01)

    def mexerThreadL(self):
        self.boolean = True;
        while self.boolean:
            self.canvas.move ("tudo", 10, 0)
            time.sleep (0.01)

    def mexerThreadR(self):
        self.boolean = True;
        while self.boolean:
            self.canvas.move ("tudo", -10, 0)
            time.sleep(0.01)


