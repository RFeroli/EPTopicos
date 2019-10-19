import random
import string
from tkinter import *
from tkinter import filedialog
from shutil import copy
from graficos import Aresta
from graficos import ColorUtils
import time
import threading

class NoGrafico:
    def __init__(self, canvas,dono,texto):
        self.canvas=canvas
       # self.x=random.randint(0, 1500)
        #self.y=random.randint(0, 800)

        self.x =20
        self.y=20

        self.texto=texto

        self.dono=dono
        self.filhos=[]

        self.arestasOrigem=[]
        self.arestasDestino=[]

        self.tagPrincipal=self.randomString()


        self.sombra=canvas.create_oval (self.x , self.y , self.x , self.y , outline="#000000",
                                        fill="#000000", width=0, tags=(self.tagPrincipal, "tudo"), stipple="gray25")
        self.no=canvas.create_oval (self.x, self.y, self.x , self.y , outline="#f15e5e",
                                    fill="#f7a987", width=4, tags=(self.tagPrincipal, "tudo"))
        self.nome=self.canvas.create_text(self.x , self.y , fill="#595757", font="System 5", text=texto, tags=(self.tagPrincipal, "tudo"))

        #Listeners

        canvas.tag_bind (self.tagPrincipal, '<B1-Motion>', self.mexer)
        canvas.tag_bind(self.tagPrincipal, '<Enter>', self.Sobre)
        canvas.tag_bind (self.tagPrincipal, '<Leave>', self.SairSobre)
        canvas.tag_bind (self.tagPrincipal, '<Double-Button-1>', self.gerarTelaEdicao)
        canvas.tag_bind (self.tagPrincipal, '<Button-1>', self.Click)

    def addFilho(self,filho):
        self.filhos.append(filho)
        aresta=Aresta.Aresta(self,filho,self.canvas)
        self.arestasOrigem.append(aresta)
        filho.arestasDestino.append(aresta)
        filho.noPorcima()
        self.noPorcima()

    def getCoords(self):
        return self.canvas.coords(self.no)

    def moverPara(self,x,y):

        for a in self.arestasOrigem:
            a.moveOrigem(x,y)

        for a in self.arestasDestino:
            a.moveDestino(x,y)

        self.canvas.coords (self.sombra, x , y ,x ,
                            y )
        self.canvas.coords (self.no, x ,y ,x ,y )
        self.canvas.coords (self.nome, x, y)

        self.x = x
        self.y = y

    def delete(self):
        self.canvas.delete (self.sombra)
        self.canvas.delete (self.no)
        self.canvas.delete (self.nome)

    def revalidar(self):
        self.delete()
        self.sombra = self.canvas.create_oval (self.x , self.y , self.x , self.y , outline="#ffffff",
                                          fill="#ffffff", width=0, tags=(self.tagPrincipal, "tudo"), stipple="gray25")
        self.no = self.canvas.create_oval (self.x, self.y, self.x , self.y, outline="#ffffff",
                                      fill="#f7a987", width=4, tags=(self.tagPrincipal, "tudo"))
        self.nome = self.canvas.create_text (self.x + 40, self.y + 40, fill=ColorUtils.toHex(255,0,0), font="System 20", text=self.dono.obter_nome(),
                                             tags=(self.tagPrincipal, "tudo"))


    def noPorcima(self):
        sombraCords = self.canvas.coords (self.sombra)
        noCords = self.canvas.coords (self.no)
        nomeCords = self.canvas.coords (self.nome)
        self.delete()
        self.sombra = self.canvas.create_oval (sombraCords[0],sombraCords[1],sombraCords[2],sombraCords[3], outline="#ffffff",
                                          fill="#ffffff", width=0, tags=(self.tagPrincipal, "tudo"), stipple="gray25")
        self.no = self.canvas.create_oval (noCords[0],noCords[1],noCords[2],noCords[3], outline="#ffffff",
                                      fill="#ffffff", width=4, tags=(self.tagPrincipal, "tudo"))
        self.nome = self.canvas.create_text (nomeCords[0],nomeCords[1], fill=ColorUtils.toHex(255,0,0), font="System 5", text=self.texto,
                                          tags=(self.tagPrincipal, "tudo"))

    def editarNome(self,nome):
        self.canvas.itemconfig(self.nome,text=nome)

    def mudarCorBorda(self,cor):
        self.canvas.itemconfig(self.no,outline=cor)

    #funcoes de listener
    def mexer(self, event):
        self.moverPara(event.x,event.y)
    def Click(self, event):
        if self.canvas.initAresta == True:
            if(self.canvas.origem is not None):
                self.canvas.destino=self
            else:
                self.canvas.origem=self
            self.canvas.ColocarAresta()


    def randomString(self,stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join (random.choice (letters) for i in range (stringLength))

    def Sobre(self, event):
        self.canvas.itemconfig(self.no, fill="#f0a080")

    def SairSobre(self, event):
        self.canvas.itemconfig(self.no, fill="#f7a987")
    def gerarTelaEdicao(self, event):

        import os
        tequinho = Tk()
        f = Frame(tequinho)
        tequinho.wm_attributes("-topmost", 1)

        string=""

        for predicado in self.dono.dict:
            string+=predicado+"  "+str(self.dono.dict[predicado])+"\n"
        print(string)
        img_label = Label(f, text=string+"\n "+str(self.dono.contador))
        img_label.pack()
        f.pack()

        tequinho.mainloop()

    def mudarCor(self):
        deltaR=(255-ColorUtils.bordaPadraoRGB[0])/50
        deltaG=(215-ColorUtils.bordaPadraoRGB[1])/50
        deltaB=(255 - ColorUtils.bordaPadraoRGB[0]) / 50
        for i in range(50):
            self.mudarCorBorda(ColorUtils.toHex(int(ColorUtils.bordaPadraoRGB[0]+i*deltaR),int(ColorUtils.bordaPadraoRGB[1]+i*deltaG),int(ColorUtils.bordaPadraoRGB[2]+i*deltaB)))
            time.sleep(.005)

    def dourar(self):
        threading.Thread (target=self.mudarCor).start()

    def mudarCorTexto(self,cor):
        self.canvas.itemconfig(self.nome,fill=cor)