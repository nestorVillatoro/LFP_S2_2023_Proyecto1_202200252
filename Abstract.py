from abc import ABC, abstractmethod

class Expression(ABC):

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    @abstractmethod
    def operar(self, arbol):
        pass

    @abstractmethod
    def getFila(self):
        return self.fila

    @abstractmethod
    def getColumna(self):
        return self.columna
    
class Lexema(Expression):

    def __init__(self, lexema,  fila, columna):
        self.lexema = lexema
        super().__init__(fila, columna)

    def operar(self, arbol):   
        return self.lexema

    def getFila(self):              
        return super().getFila()

    def getColumna(self):           
        return super().getColumna()
    
class Numero(Expression):

    def __init__(self,valor, fila, columna):
        self.valor = valor
        super().__init__(fila, columna)

    def operar(self, arbol):
        return self.valor

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
    
