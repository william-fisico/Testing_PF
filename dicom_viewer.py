from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog,messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pydicom
import numpy as np
from PIL.TiffTags import TAGS
from tkinter import scrolledtext
import subprocess

def on_closing():
    if messagebox.askyesno("Sair", "Deseja fechar o programa?"):
        root.quit()


def draw_image_import(image_array, fig, cax):
    fig.clear()
    fig.add_subplot(111).imshow(image_array)
    plt.axvline(x=cax[0], color='k', linestyle='-')
    plt.axhline(y=cax[1], color='k', linestyle='-')
    plt.gca().invert_yaxis()
    pf_img = FigureCanvasTkAgg(fig, frame_img)
    pf_img.draw()
    pf_img.get_tk_widget().grid(row=1,column=0,rowspan=5, columnspan=3)

def importar_img():
    tipos = (("Imagens DICOM","*.dcm"),("Todos os arquivos","*.*"))
    nome_arquivo = filedialog.askopenfilename(initialdir='./', 
                   title="Selecione o arquivo", filetypes=tipos)

    ds = pydicom.filereader.read_file(nome_arquivo)
    image_array = ds.pixel_array

    try:
        try:
            translacao = ds[0x3002,0x000D].value
        except:
            translacao = [0.0,0.0]
        sad = ds[0x3002,0x0022].value
        sid = ds[0x3002,0x0026].value
        x_res=ds[0x3002,0x0011].value[0]
        x_res_str = x_res
        dpmm = (1/x_res)*sid/sad #pontos por mm no isocentro
        translacao = [translacao[0]/dpmm,translacao[1]/dpmm] # deslocamento em mm no painel
    except:
        messagebox.showwarning("Aviso", "Imagem não possui informações importantes para o teste")



    cax = [image_array.shape[0]/2 - (translacao[0]*dpmm),image_array.shape[1]/2 - (translacao[1]*dpmm)]
    fig_import = plt.figure()
    draw_image_import(image_array, fig_import, cax)


root = Tk()
root.title('Dicom Viewer')
root.state('zoomed') # inicializa a janela principal maximizada
frame_img = LabelFrame(root, text="Análise", height=900, width=900)
frame_importar = LabelFrame(root, text="Importar Imagem", height=60, width=200)
btn_import_dcm = Button(frame_importar, text='Arquivo DICOM', command=importar_img)
btn_import_dcm.grid(row=0, column=0, pady=3, padx=5)

frame_importar.grid(row=0,column=0, padx=30, pady=20)
frame_importar.grid_propagate(False)

frame_img.grid(row=1,column=1,columnspan=4, rowspan=4)
frame_img.grid_propagate(False)




root.protocol("WM_DELETE_WINDOW", on_closing) # Confirma se o usuário deseja fechar a janela

root.mainloop()

