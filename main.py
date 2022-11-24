from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
from cryptography.fernet import Fernet

ruta = "" # La utilizaremos para almacenar la ruta del fichero
titulo = "Editor de texto. Power By Samuel Soto 2k22."

# Generar la clave del fichero asociado (Asi se genera la clave de codificacion para crear tu propia extension)
# def generar_key():
#     clave = Fernet.generate_key()
#     with open("clave.key","wb") as archivo_clave:
#         archivo_clave.write(clave)

# Leer la clave del fichero asociado
def read_key():
    return open("clave.key","rb").read()

def asociar_atajos(interfaz):
    interfaz.bind("<Control-s>", guardar)
    interfaz.bind("<Control-o>",abrir)
    interfaz.bind("<Control-n>",nuevo)
    interfaz.bind("<Alt-s>",guardar_como)
    interfaz.bind("<Control-k>",guardar_como_nocrypt)

def nuevo(event=None):
    global ruta
    root.event_generate('<<Nuevo>>')
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title(titulo)

def abrir(event=None):
    global ruta
    root.event_generate('<<Abrir>>')
    mensaje.set("Abrir fichero")
    ruta = FileDialog.askopenfilename(
        initialdir='.',
        filetypes=(("Ficheros Samuel Soto", "*.stx"),),
        title="Abrir un fichero")

    if ruta != "":
        fichero = open(ruta, 'rb')
        contenido = fichero.read().decode('utf-8')
        texto.delete(1.0,'end')
        contenido = Fernet(read_key()).decrypt(contenido.encode())
        contenido = contenido.decode('utf-8')
        texto.insert('insert', contenido)
        fichero.close()
        root.title(ruta + " - " + titulo)

def guardar(event=None):
    root.event_generate('<<Guardar>>')
    mensaje.set("Guardar fichero")
    if ruta != "":
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'wb+')
        contenido = Fernet(read_key()).encrypt(contenido.encode())
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        guardar_como()

def guardar_como(event=None):
    global ruta
    root.event_generate('<<Guardar_como>>')
    mensaje.set("Guardar fichero como")

    fichero = FileDialog.asksaveasfile(title="Guardar fichero",
        mode="w", defaultextension=".stx",filetypes=[("Ficheros Samuel Soto",".stx")])

    if fichero is not None:
        ruta = fichero.name
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'wb+')
        contenido = Fernet(read_key()).encrypt(contenido.encode())
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""

def guardar_como_nocrypt(event=None):
    global ruta
    root.event_generate('<<Guardar_como_nocrypt>>')
    mensaje.set("Guardar fichero como")

    fichero = FileDialog.asksaveasfile(title="Guardar fichero",
        mode="w+", defaultextension=".txt",filetypes=[("Texto plano",".txt")])

    if fichero is not None:
        ruta = fichero.name
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+',encoding="utf-8")
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""

# Configuración de la raíz
root = Tk()
root.title(titulo)
root.config(bg='grey')
root.iconbitmap("resources/icons/snake-icon.ico")
asociar_atajos(root)

# Menú superior
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=nuevo)
filemenu.add_command(label="Abrir", command=abrir)
filemenu.add_command(label="Guardar", command=guardar)
filemenu.add_command(label="Guardar como", command=guardar_como)
filemenu.add_command(label="Guardar sin encriptar", command=guardar_como_nocrypt)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(menu=filemenu, label="Archivo")

# Caja de texto central
texto = Text(root,insertbackground='white',undo=True)
texto.pack(fill="both", expand=1)
texto.config(bg='#454545',bd=0, padx=6, pady=4, font=("Consolas",12),fg='white')

# Monitor inferior
mensaje = StringVar()
mensaje.set("Creado por Samuel Soto para la lectura de ficheros encriptados con extension \".stx\"")
monitor = Label(root, textvar=mensaje, justify='left')
monitor.pack(side="left")

root.config(menu=menubar)

# Finalmente bucle de la apliación
root.mainloop()