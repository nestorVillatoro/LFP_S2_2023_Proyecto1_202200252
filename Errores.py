from Abstract import Expression

class Errores(Expression):
    def __init__(self, lexema, fila, columna):
        self.lexema = lexema
        super().__init__(fila, columna)

    def operar(self, no):
        lex = self.lexema
        return lex

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()