from tkinter import *
from tkinter import ttk
import mysql.connector

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()


class Relatorio():
    def printCliente(self):
        webbrowser.open("relatorio.pdf")

    def gerarRelatCliente(self):
        self.c = canvas.Canvas("relatorio.pdf")

        self.res0 = self.resultado

        for i in res0:
            self.listaCli.insert("", END, values=i)








        self.c.showPage()
        self.c.save()
        self.printCliente()

        self.limpa_tela()
        self.desconecta_db()


class Funcs():

    def conecta_db(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = 'fab_racao_bugio'

        )
        self.cursor = self.conn.cursor(); print("conectando ao banco de dados")


    def desconecta_db(self):
        self.conn.close() ; print("desconectando ao banco de dados")

    def update(self, lista):
        self.listaCli.delete(*self.listaCli.get_children())
        for i in lista:
            self.listaCli.insert('', END, values=i)

    def limpa_tela(self):
        self.dataInicio_entry.delete(0, END)
        self.data_entry.delete(0, END)




    def select_lista(self):
        self.conecta_db()
        query = (""" SELECT * FROM relatorio ORDER BY Data ASC
                """)
        self.cursor.execute(query)
        lista = self.cursor.fetchall()
        self.update(lista)

    def busca_mes(self):
        self.conecta_db()
        self.listaCli.delete(*self.listaCli.get_children())


        nome = self.dataInicio_entry.get()
        final = self.data_entry.get()
        data = (nome, final)
        self.cursor.execute(
            """ SELECT * FROM relatorio
            WHERE Data between (%s) and (%s) ORDER BY Data ASC  """, data)
        buscaDatainicial = self.cursor.fetchall()
        for i in buscaDatainicial:
            self.listaCli.insert("", END, values=i)

        self.resultado = str(buscaDatainicial)
        print(self.resultado)









    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)




class Application(Funcs, Relatorio):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_de_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.select_lista()





        root.mainloop()


    def tela(self):
        self.root.title("Controle Frigorifico")
        self.root.configure(background= '#B0E0E6')
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.maxsize(width=1200, height=1000)
        self.root.minsize(width=400, height=300)

    def frames_de_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg = '#F0F8FF', highlightbackground = '#C0C0C0', highlightthickness = 3)
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.36)

        self.frame_2 = Frame(self.root, bd=4, bg='#F0F8FF', highlightbackground='#C0C0C0', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.4, relwidth=0.96, relheight=0.55)


    def widgets_frame1(self):
        self.lb_pesquisa = Label(self.frame_1, text="Pesquisa", bg='#F0F8FF', fg='black')
        self.lb_pesquisa.place(relx=0.24, rely=0.28)

        self.lb_dataInicio = Label(self.frame_1, text="Data Inicial ", bg='#F0F8FF', fg='black')
        self.lb_dataInicio.place(relx=0.12, rely=0.40)
        self.dataInicio_entry = Entry(self.frame_1)
        self.dataInicio_entry.place(relx=0.20, rely=0.41, relwidth=0.15)


        self.lb_data = Label(self.frame_1, text="Data Final ", bg='#F0F8FF', fg='black')
        self.lb_data.place(relx=0.12, rely=0.50)
        self.data_entry = Entry(self.frame_1)
        self.data_entry.place(relx=0.20, rely=0.51, relwidth=0.15)

        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command= self.busca_mes)
        self.bt_buscar.place(relx=0.22, rely=0.70, relwidth=0.11, relheight=0.10)

        self.bt_imprimir = Button(self.frame_1, text="Imprimir", bd=2, bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command= self.gerarRelatCliente)
        self.bt_imprimir.place(relx=0.42, rely=0.70, relwidth=0.11, relheight=0.10)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height= 3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9", "col10", "col11"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Id")
        self.listaCli.heading("#2", text="Data")
        self.listaCli.heading("#3", text="Hora")
        self.listaCli.heading("#4", text="Receita")
        self.listaCli.heading("#5", text="Milho")
        self.listaCli.heading("#6", text="Farelo")
        self.listaCli.heading("#7", text="Oleo")
        self.listaCli.heading("#8", text="Nucleo")
        self.listaCli.heading("#9", text="Tempo_Mistura")
        self.listaCli.heading("#10", text="Total")
        self.listaCli.heading("#11", text="Batelada")


        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=50)
        self.listaCli.column("#3", width=50)
        self.listaCli.column("#4", width=90)
        self.listaCli.column("#5", width=50)
        self.listaCli.column("#6", width=50)
        self.listaCli.column("#7", width=50)
        self.listaCli.column("#8", width=50)
        self.listaCli.column("#9", width=80)
        self.listaCli.column("#10", width=50)
        self.listaCli.column("#11", width=50)



        self.listaCli.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.98)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)








Application()

