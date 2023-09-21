from Abstract  import Expression
import math

class Aritmetica(Expression):

    def __init__(self, left, right, tipo, fila, columna):
        self.left = left
        self.right = right
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, arbol):
        leftValue = ''
        rightValue = ''

        if self.left != None:
            leftValue = self.left.operar(arbol)

        if self.right != None:
            rightValue = self.right.operar(arbol)

        if self.tipo.operar(arbol) == 'suma':
            return leftValue + rightValue
        elif self.tipo.operar(arbol) == 'resta':
            return leftValue - rightValue
        elif self.tipo.operar(arbol) == 'multiplicacion':
            return leftValue * rightValue
        elif self.tipo.operar(arbol) == 'division':
            return leftValue / rightValue
        elif self.tipo.operar(arbol) == 'potencia':
            return leftValue ** rightValue
        elif self.tipo.operar(arbol) == 'raiz':
            return leftValue ** (1/rightValue)
        elif self.tipo.operar(arbol) == 'mod':
            return leftValue % rightValue
        else:
            return None

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()

class Trigonometria(Expression):

    def __init__(self, left, tipo, fila, columna):
        self.left = left
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, arbol):
        valor = ''

        if self.left != None:
            valor = self.left.operar(arbol)

        if self.tipo.operar(arbol) == 'inverso':
            return valor ** (-1) 
        elif self.tipo.operar(arbol) == 'seno':
            return math.sin(valor)
        elif self.tipo.operar(arbol) == 'coseno':
            return math.cos(valor) 
        elif self.tipo.operar(arbol) == 'tangente':
            return math.tan(valor) 
        else:
            return None

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()

class Texto(Expression):

    def __init__(self, texto, tipo, fila, columna):
        self.texto = texto
        self.tipo = tipo
        super().__init__(fila, columna)

    def operar(self, arbol):
        pass
    
    def ejecutarT(self):

        if self.texto != None:
            tipo = self.tipo

        if tipo == "texto":
            return tipo

        elif tipo == "fondo":
            return tipo

        elif tipo == "fuente":
            return tipo

        elif tipo == "forma":
            return tipo

        else:
            None

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()