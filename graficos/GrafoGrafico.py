from tkinter import *
from tkinter.ttk import *
import threading

from graficos import TelaGrafo
from graficos import  ColorUtils
import time;


class GrafoGrafico:
    def __init__(self):
        this=self
        def initialization():
            this.raiz = Tk ()
            this.raiz.geometry ("{0}x{1}+0+0".format (self.raiz.winfo_screenwidth (), self.raiz.winfo_screenheight ()))

            this.canvas = Canvas (self.raiz, bg=ColorUtils.toHex(255,255,255))
            this.canvas.initAresta=False
            this.canvas.pack(fill=BOTH,expand=1)
            this.tela=TelaGrafo.TelaGrafo(self.canvas, "", self.raiz)
            this.raiz.mainloop()

        threading.Thread (target=initialization).start()
        time.sleep(0.1)



    def incluir_raiz(self,raiz,texto):
        self.tela.incluirRaiz(raiz,texto)
    def incluir_no(self,pai,no,texto):
        self.tela.incluirNo(pai,no,texto)


    def zeladoria(self):
        while True:
            self.raiz.update_idletasks ()
            self.raiz.update ()



