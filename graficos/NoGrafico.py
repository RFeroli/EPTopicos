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
        self.nome=self.canvas.create_text(self.x , self.y , fill="#595757", font="System 4", text=texto, tags=(self.tagPrincipal, "tudo"))

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
        self.nome = self.canvas.create_text (nomeCords[0],nomeCords[1], fill=ColorUtils.toHex(255,0,0), font="System 4", text=self.texto,
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
        def ok_action():
            self.editarNome(node_name.get())
            self.dono.altere_nome(node_name.get())

            tequinho.destroy()

        def change_img():
            game_name = 'appc'
            game_path = os.getcwd().replace('\\', '/').rsplit('/', 1)[0] + '/{}/imagens_cenarios'.format(game_name)
            new_file = filedialog.askopenfilename(initialdir=game_path)
            if new_file:
                new_path = new_file.replace('\\', '/').rsplit('/', 1)[0]
                new_file_name = new_file.replace('\\', '/').rsplit('/', 1)[1]
                print(new_path, new_file_name)
                if new_path != game_path:
                    copy(new_file, game_path)
                self.dono.altere_plano(new_file_name)
                img_label.config(text='Imagem: {}'.format(new_file_name))
            f.pack()

        import os
        tequinho = Tk()
        f = Frame(tequinho)
        tequinho.title(self.dono.obter_nome())
        tequinho.wm_attributes("-topmost", 1)

        Label(f, text='Nome do cenário').grid(row=0)
        node_name = Entry(f)
        node_name.insert(END, self.dono.obter_nome())
        node_name.grid(row=0, column=1)

        img_label = Label(f, text='Imagem: {}'.format(self.dono.obter_plano_de_fundo()))
        img_label.grid(row=1)
        img_button = Button(f,text='Alterar imagem', command=change_img)
        img_button.grid(row=1, column=1)
        confirm_button = Button(f, text='OK',command= ok_action)
        confirm_button.grid(row=2, column=1)
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