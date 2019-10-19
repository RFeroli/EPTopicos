from copy import deepcopy
import hashlib
import base64

class GrafoFF:
    def __init__(self):
        self.nos={}
        self.niveis={}

    #
    # def incluir_noOps(self,estado,nivel):
    #     for predicado in estado:
    #         for args in estado[predicado]:
    #             no = self.NoPred ((predicado, {args}), nivel)
    #             if (not no["hash"] in self.nos):
    #                 self.nos[no["hash"]] = no
    #             no = self.nos[no["hash"]]
    #
    #             noigual=self.NoPred ((predicado, {args}), nivel + 1)
    #             if (not noigual["hash"] in self.nos):
    #                 self.nos[noigual["hash"]] = noigual
    #             noigual = self.nos[noigual["hash"]]
    #             noigual["noOp"]=no

    def incluir_estado_inicial(self,estado_inicial):
        for predicado in estado_inicial:

            for args in estado_inicial[predicado]:
                no = self.NoPred ((predicado, {args}))
                if (not no["hash"] in self.nos):
                    self.nos[no["hash"]] = no
                no = self.nos[no["hash"]]

    def incluir(self,precondicoes,op,efeitos):

        noAc=self.NoOperacao (op)
        if (not noAc["hash"] in self.nos):
            self.nos[noAc["hash"]] = noAc
        noAc = self.nos[noAc["hash"]]


        for efeito in efeitos:
            no = self.NoPred ((efeito, efeitos[efeito]))
            if (not no["hash"] in self.nos):
                self.nos[no["hash"]] = no
                no["anterior"] = self.nos[noAc["hash"]]



        for precond in precondicoes:
            no=self.NoPred((precond, precondicoes[precond]))
            if(not no["hash"] in self.nos ):
                self.nos[no["hash"]]=no
            no=self.nos[no["hash"]]
            noAc["anteriores"].append (self.nos[no["hash"]])
            #no["proximos"].append(self.nos[noAc["hash"]])


    def NoPred(self, valor):
        no={}
        no["valor"]=valor
       #no["proximos"]=[]
        no["anterior"]=None
        no["hash"]=self._gere_hash({"chave":no["valor"]})
        no["operacao"]=False
        no["flag"]=False
        return  no

    def NoOperacao(self, valor):
        no = {}
        no["valor"] = valor
       # no["proximos"] = []
        no["anteriores"] = []
        no["hash"] = self._gere_hash ({"chave": no["valor"]})
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