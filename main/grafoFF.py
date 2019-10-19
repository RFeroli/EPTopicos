from copy import deepcopy
import hashlib
import base64

class GrafoFF:
    def __init__(self):
        self.nos={}
        self.niveis={}


    def incluir_noOps(self,estado,nivel):
        for predicado in estado:
            for args in estado[predicado]:
                no = self.No ((predicado, {args}), nivel)
                if (not no["hash"] in self.nos):
                    self.nos[no["hash"]] = no
                no = self.nos[no["hash"]]

                noigual=self.No ((predicado, {args}), nivel+1)
                if (not noigual["hash"] in self.nos):
                    self.nos[noigual["hash"]] = noigual
                noigual = self.nos[noigual["hash"]]
                noigual["noOp"]=no


    def incluir(self,precondicoes,op,efeitos, nivel):

        noAc=self.NoOperacao (op, nivel)
        if (not noAc["hash"] in self.nos):
            self.nos[noAc["hash"]] = noAc
        noAc = self.nos[noAc["hash"]]
        self.niveis[nivel] = self.niveis.get (nivel, dict())[noAc["hash"]]=noAc


        for efeito in efeitos:
            no = self.No ((efeito, efeitos[efeito]), nivel+1)
            if (not no["hash"] in self.nos):
                self.nos[no["hash"]] = no
            no = self.nos[no["hash"]]
            noAc["proximos"].append(self.nos[no["hash"]])
            no["anteriores"].append(self.nos[noAc["hash"]])


        for precond in precondicoes:
            no=self.No((precond,precondicoes[precond]),nivel)
            if(not no["hash"] in self.nos ):
                self.nos[no["hash"]]=no
            no=self.nos[no["hash"]]
            noAc["anteriores"].append (self.nos[no["hash"]])
            no["proximos"].append(self.nos[noAc["hash"]])


    def No(self,valor,nivel):
        no={}
        no["valor"]=valor
        no["proximos"]=[]
        no["anteriores"]=[]
        no["nivel"] = nivel
        no["hash"]=self._gere_hash({"chave":no["valor"],"nivel":no["nivel"]})
        no["operacao"]=False
        no["flag"]=False
        no["noOp"]= None
        return  no

    def NoOperacao(self, valor, nivel):
        no = {}
        no["valor"] = valor
        no["proximos"] = []
        no["anteriores"] = []
        no["nivel"] = nivel
        no["hash"] = self._gere_hash ({"chave": no["valor"], "nivel": no["nivel"]})
        no["operacao"] = True
        no["flag"] = False
        return no


    def _gere_hash(self, o):
        hasher = hashlib.sha256()
        hasher.update(repr(self.make_hashable(o)).encode())
        return base64.b64encode(hasher.digest()).decode()

    def make_hashable(self, o):
        if isinstance(o, (tuple, list)):
            return tuple((self.make_hashable(e) for e in o))

        if isinstance(o, dict):
            return tuple(sorted((k, self.make_hashable(v)) for k, v in o.items()))

        if isinstance(o, (set, frozenset)):
            return tuple(sorted(self.make_hashable(e) for e in o))

        return o