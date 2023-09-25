import tkinter as tk
from subprocess import check_output
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import List, Any
import os
from Analizador import intruccion, getErrores,operar_


class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto")

        self.line_number_bar = tk.Text(root, width=4, padx=4, takefocus=0, border=0, background='lightgrey', state='disabled')
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.text_widget = ScrolledText(self.root, wrap=tk.WORD)
        self.text_widget.pack(expand=True, fill='both')

        self.text_widget.bind('<Key>', self.update_line_numbers)
        self.text_widget.bind('<MouseWheel>', self.update_line_numbers)

        self.current_line = 1

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Guardar", command=self.save_file)
        self.file_menu.add_command(label="Guardar Como", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)
        self.menu_bar.add_command(label="Analizar", command=self.analizar)
        self.menu_bar.add_command(label="Errores", command=self.Errores)
        self.menu_bar.add_command(label="Reporte", command=self.reporte)

    global verificador 
    verificador= False
    def open_file(self):
        global file_path
        global verificador
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.JSON")])
        verificador = True
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.data = content
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
            self.update_line_numbers()
        self.data = self.text_widget.get(1.0, tk.END)

    def save_file(self):
        if verificador == True:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w+') as file:
                file.write(content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
        else:
            file_path2 = filedialog.asksaveasfilename(defaultextension=".JSON", filetypes=[("Archivos de texto", "*.JSON")])
            if file_path2:
                content = self.text_widget.get(1.0, tk.END)
                with open(file_path2, 'w') as file:
                    file.write(content)
                messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")

    def save_file_as(self):
        file_path2 = filedialog.asksaveasfilename(defaultextension=".JSON", filetypes=[("Archivos de texto", "*.JSON")])
        if file_path2:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path2, 'w') as file:
                file.write(content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
    
    def update_line_numbers(self, event=None):
        line_count = self.text_widget.get('1.0', tk.END).count('\n')
        if line_count != self.current_line:
            self.line_number_bar.config(state=tk.NORMAL)
            self.line_number_bar.delete(1.0, tk.END)
            for line in range(1, line_count + 1):
                self.line_number_bar.insert(tk.END, f"{line}\n")
            self.line_number_bar.config(state=tk.DISABLED)
            self.current_line = line_count
            
    def analizar(self):
        try:
            instrucciones = intruccion(self.data)
            respuestas_Operaciones = operar_()

            Resultados = ''
            Operacion = 1

            configuracion = 1
            salto = "\n"

            for respuesta in respuestas_Operaciones:

                if isinstance(respuesta.operar(None), int) or isinstance(respuesta.operar(None), float) == True:
                    Resultados += str(f"Operacion {Operacion} --> {respuesta.tipo.operar(None)} = {respuesta.operar(None)}\n")
                    print(respuesta.operar(None))
                    Operacion += 1




            messagebox.showinfo("Analisis Exitoso", Resultados)
        except:
            messagebox.showinfo("Error", "No se ha ingresado ningun archivo")
    
    def Errores(self):
        lista_errores = getErrores()
        archivo = open('Errores.JSON', 'w+')
        archivo.write('''{
            "errores":[
        ''')
        contador = 1
        for error in lista_errores:
            cont = 1
            er = error.operar(cont)
            erC = error.getColumna()
            erF = error.getFila()
            cont += 1
            if contador != len(lista_errores):
                archivo.write('''{
                            "No":'''+ str(contador)+ ''',
                            "descripcion":{
                            "lexema":"'''+str(er)+'''",
                            "tipo": "error lexico",
                            "columna":'''+str(erC)+''',
                            "fila":'''+str(erF)+'''
                            }
                },
    ''')
            else:
                archivo.write('''{
                            "No":'''+ str(contador)+ ''',
                            "descripcion":{
                            "lexema":"'''+str(er)+'''",
                            "tipo": "error lexico",
                            "columna":'''+str(erC)+''',
                            "fila":'''+str(erF)+'''
                            }
                }
    ''') 
            contador += 1
        archivo.write(''']
                      }
        ''')
        archivo.close()
        print("Se generó el archivo Errores.json")
        messagebox.showinfo("Mensaje", "Se generó el archivo Errores.json")
    

    def reporte(self):
        try:
            operar_().clear()

            intrucciones = intruccion(self.data)
            respuestas_Operaciones = operar_()

            contenido = "digraph G {\n\n"                           #CREAMOS NUESTRO ARCHIVO CON COMANDOS
            r = open("Operaciones.dot", "w", encoding="utf-8")
            contenido += str(Graphviz(respuestas_Operaciones))
            contenido += '\n}'

            r.write(contenido)
            r.close()
            os.system("cmd /c dot -Tsvg Operaciones.dot > Operaciones.svg")

            #print("...............................................................")
            #print("            ** COMANDOS DE GRAPHVIZ **               ")
            #print("")
            #print(contenido)
            #print("...............................................................")
            #print("")
            #print("FIN.....")
            # ! dot -Tpng Operaciones.dot -o Operaciones.png
            # ! Generar desde aquí la imagen

        except Exception as e:
            messagebox.showinfo("Se produjo un error: ",str(e))
            messagebox.showinfo("Mensaje", f"Error al generar el archivo de salida, Verificar el Archivo de entrada.")
        else:
            messagebox.showinfo("Mensaje", "Grafica generada con exito")
            respuestas_Operaciones.clear()
            intrucciones.clear()

def Graphviz(respuestas_Operaciones):
        Titulo = ""
        colorNodo = ""
        fuenteNodo = ""
        formaNodo = ""
        try:
            print('---------------------------------------------')
            for respuesta in respuestas_Operaciones:
                if isinstance(respuesta.operar(None), int) or isinstance(respuesta.operar(None), float) == True:
                    pass
                else:
                    temporal = str(respuesta.texto.operar(None)).lower()
                    print(respuesta.texto.operar(None))
                    print(respuesta.ejecutarT())
                    if respuesta.ejecutarT() == "texto":  # Podemos recibir cualquier texto
                        Titulo = str(respuesta.texto.operar(None))
                    if respuesta.ejecutarT() == "fondo":  # Vericar el color del nodo a asignar
                        if temporal == ("amarillo" or "yellow"):
                            temporal = "khaki1"
                            colorNodo = temporal
                        elif temporal == ("verde" or "green"):
                            temporal = "forestgreen"
                            colorNodo = temporal
                        elif temporal == ("azul" or "blue"):
                            temporal = "deepskyblue"
                            colorNodo = temporal
                        elif temporal == ("rojo" or "red"):
                            temporal = "crimson"
                            colorNodo = temporal
                        elif temporal == ("morado" or "purple"):
                            temporal = "slateblue"
                            colorNodo = temporal

                    if respuesta.ejecutarT() == "fuente":  # Vericar la fuente del nodo a asignar

                        if temporal == ("amarillo" or "yellow"):
                            temporal = "khaki1"
                            fuenteNodo = temporal
                        elif temporal == ("verde" or "green"):
                            temporal = "forestgreen"
                            fuenteNodo = temporal
                        elif temporal == ("azul" or "blue"):
                            temporal = "deepskyblue"
                            fuenteNodo = temporal
                        elif temporal == ("rojo" or "red"):
                            temporal = "crimson"
                            fuenteNodo = temporal
                        elif temporal == ("morado" or "purple"):
                            temporal = "slateblue"
                            fuenteNodo = temporal
                        elif temporal == ("negro" or "black"):
                            temporal = "black"
                            fuenteNodo = temporal

                    if respuesta.ejecutarT() == "forma":  # Vericar el formato de nodo a asignar
                        if temporal == ("circulo" or "circle"):
                            temporal = "circle"
                            formaNodo = temporal
                        elif temporal == ("cuadrado" or "square"):
                            temporal = "square"
                            formaNodo = temporal
                        elif temporal == ("triangulo" or "triangle"):
                            temporal = "triangle"
                            formaNodo = temporal
                        elif temporal == ("rectangulo" or "box"):
                            temporal = "box"
                            formaNodo = temporal
                        elif temporal == ("elipse" or "ellipse"):
                            temporal = "ellipse"
                            formaNodo = temporal

            temporal = ''
            CnumIzquierdo = 0
            CnumDerecho = 0
            Crespuesta = 0
            Ctotal = 0

            text = ""
            text += f"\tnode [shape={formaNodo}]\n"
            # text += f"\tnode [shape=box];\n"

            text += f"\tnodo0 [label = \"{Titulo}\"]\n"
            text += f"\tnodo0" + "[" + f"fontcolor = {fuenteNodo}" + "]\n"
            # text += f"\tnodo0 [label = \"CambiarPorTexto\"]\n"    # ESTE DEJAR

            for respuesta in respuestas_Operaciones:
                CnumIzquierdo += 1
                CnumDerecho += 1
                Crespuesta += 1
                Ctotal += 1
                if isinstance(respuesta.operar(None), int) or isinstance(respuesta.operar(None), float) == True:
                    if str(respuesta.tipo.operar(None)) == "seno" or str(respuesta.tipo.operar(None)) == "coseno" or str(respuesta.tipo.operar(None)) == "tangente" or str(respuesta.tipo.operar(None)) == "inverso":
                        text += f"\tnodoRespuesta{Crespuesta}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"
                        text += f"\tnodoIzqu{CnumIzquierdo}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"
                        text += f"\tnodoT{Ctotal}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"

                        text += f"\tnodoRespuesta{Crespuesta}" + f"[label = \"{str(respuesta.tipo.operar(None))}: " + "\"]\n"
                        text += f"\tnodoIzqu{CnumIzquierdo}" + "[label = \"Valor1: " + f" {str(respuesta.left.operar(None))} " + "\"]\n"

                        text += f"\tnodoRespuesta{Crespuesta} -> nodoIzqu{CnumIzquierdo}\n"
                        text += f"\tnodoT{Ctotal}" + f"[label = \"{respuesta.operar(None)}" + "\"]\n"
                        text += f"\tnodoT{Ctotal} -> nodoRespuesta{Crespuesta}\n"
                    else:

                        text += f"\tnodoRespuesta{Crespuesta}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"
                        text += f"\tnodoIzqu{CnumIzquierdo}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"
                        text += f"\tnodoDere{CnumDerecho}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"
                        text += f"\tnodoT{Ctotal}" + "[" + f"style = filled" + f",fillcolor = {colorNodo}" + f",fontcolor = {fuenteNodo}" + "]\n"

                        text += f"\tnodoRespuesta{Crespuesta}" + f"[label = \"{str(respuesta.tipo.operar(None))}: " + "\"]\n"
                        text += f"\tnodoIzqu{CnumIzquierdo}" + "[label = \"Valor1: " + f" {str(respuesta.left.operar(None))} " + "\"]\n"
                        text += f"\tnodoRespuesta{Crespuesta} -> nodoIzqu{CnumIzquierdo}\n"
                        text += f"\tnodoDere{CnumDerecho}" + "[label = \"Valor2: " + f" {str(respuesta.right.operar(None))} " + "\"]\n"
                        text += f"\tnodoRespuesta{Crespuesta} -> nodoDere{CnumDerecho}\n"

                        text += f"\tnodoT{Ctotal}" + f"[label = \"{respuesta.operar(None)}" + "\"]\n"
                        text += f"\tnodoT{Ctotal} -> nodoRespuesta{Crespuesta}\n"

                else:
                    pass

            return text
        except Exception as e:
            messagebox.showinfo("Se produjo un error: ",str(e))
            messagebox.showinfo("Mensaje", "Error en los comandos de Graphviz")
 


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()