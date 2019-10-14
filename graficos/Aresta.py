import tkinter as tk
from numpy import sqrt
class Aresta :

    def __init__(self,origem, destino,canvas):
        self.origem=origem
        self.destino=destino
        self.canvas=canvas

        origemCords=self.canvas.coords(origem.no)
        destinoCords = self.canvas.coords (destino.no)

        pontoDestino=self.pontoAntes(45,origemCords[0]+40, origemCords[1]+40, destinoCords[0]+40, destinoCords[1]+40)
        pontoOrigem=self.pontoAntes2(45,origemCords[0]+40, origemCords[1]+40, destinoCords[0]+40, destinoCords[1]+40)
        self.linha=canvas.create_line (pontoOrigem[0], pontoOrigem[1], pontoDestino[0], pontoDestino[1], width=1, tags="tudo",arrow=tk.LAST,fill='gray')


    def moveOrigem(self,x,y):
        destinoCords = self.canvas.coords (self.destino.no)
        pontoDestino = self.pontoAntes (10,x, y, destinoCords[0] ,
                                        destinoCords[1] )
        pontoOrigem= self.pontoAntes2(10,x, y, destinoCords[0] ,
                                        destinoCords[1] )

        self.canvas.coords (self.linha, pontoOrigem[0], pontoOrigem[1],pontoDestino[0],pontoDestino[1])

    def moveDestino(self, x, y):

        origemCords = self.canvas.coords (self.origem.no)
        pontoDestino = self.pontoAntes (10, origemCords[0] , origemCords[1] , x,
                                       y)
        pontoOrigem=self.pontoAntes2(10, origemCords[0] , origemCords[1], x,y)

        self.canvas.coords (self.linha, pontoOrigem[0],pontoOrigem[1], pontoDestino[0], pontoDestino[1])

    def pontoAntes(self,z,x1,y1,x2,y2):
        delta=sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

        xx = x1+((delta-z)/delta)*(x2-x1)
        yy = y1 + ((delta - z) / delta) * (y2 - y1)

        return (xx,yy)

    def pontoAntes2(self,z,x1,y1,x2,y2):
        delta=sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

        xx = x1+((z)/delta)*(x2-x1)
        yy = y1 + ((z) / delta) * (y2 - y1)

        return (xx,yy)

