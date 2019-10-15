from copy import deepcopy


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

                noOp = self.NoOp (("NO-OP", (predicado, {args})), nivel)
                if (not noOp["hash"] in self.nos):
                    self.nos[noOp["hash"]] = noOp
                noOp = self.nos[noOp["hash"]]
                noOp["anteriores"].append(no)
                noOp["proximos"].append(noigual)

                no["proximos"].append(noOp)
                noigual["anteriores"].append(noOp)

    def incluir(self,precondicoes,op,efeitos, nivel):

        noAc=self.NoOp (op, nivel)
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
        return  no

    def NoOp(self, valor, nivel):
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
        if isinstance (o, (set, tuple, list)):
            return tuple ([self._gere_hash (e) for e in o])

        elif not isinstance (o, dict):
            return hash (o)

        new_o = deepcopy(o)
        for k, v in new_o.items ():
            new_o[k] = self._gere_hash (v)

        return hash (tuple (frozenset (sorted (new_o.items ()))))