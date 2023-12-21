import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD

import generic
from update_persistences import *
import subprocess
from datetime import datetime

#path = path()

class MasterPanel:
    def __init__(self):
        """
        self.window = tk.Tk()
        self.window.title('Master panel')
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.config(bg='#fcfcfc')
        self.window.resizable(True, True)
        """

        self.window = tk.Tk()
        self.window.title('')
        self.window.geometry('800x800')
        self.window.config(bg='#FFFBE1')
        self.window.resizable(False, False)
        generic.center_window(self.window, 500, 300)

        # frame form title
        frame_form = tk.Frame(self.window, height=10, relief=tk.SOLID, padx=20, pady=5, bg='#FFFBE1')
        frame_form.pack(side="top", fill=tk.BOTH)
        title = tk.Label(frame_form, text="Inicio", font=('times', 40), fg="#666a88", bg='#FFFBE1', pady=5)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        description = tk.Label(frame_form, text="Ingrese el tipo de experimento.", font=('times', 20), fg="black", bg='#FFFBE1', pady=5)
        description.pack(side='top', anchor="w")

        option1 = tk.Button(frame_form, width=18, text="Test Model", font=('Times', 25, BOLD), fg="#8B0000", command=self.call_test_exp)
        option1.pack(expand=tk.YES, padx=1, pady=10)

        option2 = tk.Button(frame_form, width=18, text="Upload Experiment", font=('Times', 25, BOLD), fg="#8B0000",  command=self.call_upload_exp)
        option2.pack(expand=tk.YES, padx=1, pady=10)

        option3 = tk.Button(frame_form, width=18, text="Download Experiment", font=('Times', 25, BOLD), fg="#8B0000", command=self.call_download_exp)
        option3.pack(expand=tk.YES, padx=1, pady=10)

        self.window.mainloop()

    def call_test_exp(self):
        self.window.destroy()
        d = datetime.now()
        date_now = "\n{}.{}.{}-{}:{}:{}\n".format(d.day,d.month,d.year,d.hour,d.minute,d.second)
        update_test_history("\n-------------------")
        update_test_history(date_now)
        test_model()

    def call_upload_exp(self):
        self.window.destroy()
        d = datetime.now()
        date_now = "\n{}.{}.{}-{}:{}:{}\n".format(d.day, d.month, d.year, d.hour, d.minute, d.second)
        update_upload_history("\n-------------------")
        update_upload_history(date_now)
        upload_exp()

    def call_download_exp(self):
        self.window.destroy()
        d = datetime.now()
        date_now = "\n{}.{}.{}-{}:{}:{}\n".format(d.day, d.month, d.year, d.hour, d.minute, d.second)
        update_download_history("\n-------------------")
        update_download_history(date_now)
        download_exp()

class test_model:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Inicio de sesion')
        self.window.geometry('800x800')
        self.window.config(bg='#FFFBE1')
        self.window.resizable(True, True)
        generic.center_window(self.window,700,700)

        self.set_models = set()
        self.color_spaces = set()
        self.degradations = set()
        self.dic_optimizers = {}
        self.dic_math_models = {}
        self.built_dic_models()

        # Structural frames--------------------------
        # Frame for title
        self.frame_form_title = tk.Frame(self.window, bd=0, height=10, relief=tk.SOLID, padx=5, pady=0, bg='#FFFBE1')
        self.frame_form_title.pack(side="top", fill=tk.BOTH)
        self.title = tk.Label(self.frame_form_title, text="Test model", font=('times',30), fg="#666a88", bg='#FFFBE1', pady=5)
        self.title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame for terminal
        self.frame_form_terminal = tk.Frame(self.window, bd=0, relief=tk.SOLID, width=450, padx=5, pady=5, bg='#272727')
        self.frame_form_terminal.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # Crear un cuadro de texto
        self.cuadro_texto = tk.Text(self.frame_form_terminal, width=43, wrap="word")
        self.cuadro_texto.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=10)

        # Frame for buttons
        self.frame_form_buttons = tk.Frame(self.window, height=20, relief=tk.SOLID, padx=5, pady=5, bg='#FFFBE1')
        self.frame_form_buttons.pack(side="bottom", fill=tk.BOTH)

        # Frame for fill
        self.frame_form_fill = tk.Frame(self.window, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_fill.pack(side="left", fill=tk.BOTH)
        self.frame_form_model = tk.Frame(self.frame_form_fill, height=25, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_model.pack(side="top", fill=tk.BOTH)
        self.frame_form_image = tk.Frame(self.frame_form_fill, height=25, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_image.pack(side="top", fill=tk.BOTH)
        self.frame_form_tol_nIter = tk.Frame(self.frame_form_fill, height=50, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_tol_nIter.pack(side="top", fill=tk.BOTH)
        self.frame_form_tol = tk.Frame(self.frame_form_tol_nIter, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_tol.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_nIter = tk.Frame(self.frame_form_tol_nIter, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_nIter.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_left_right = tk.Frame(self.frame_form_fill, height=50, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_left_right.pack(side="top", fill=tk.BOTH)
        self.frame_form_param_left = tk.Frame(self.frame_form_left_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_left.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right = tk.Frame(self.frame_form_left_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        # ---------------------------------------------

        # Entry for model
        self.label_model = tk.Label(self.frame_form_model, text="Model name:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.label_model.pack(fill=tk.X, padx=20, pady=5)
        self.model = ttk.Entry(self.frame_form_model, width=30, font=('Times',14))
        self.model.pack(fill=tk.X, padx=20, pady=5)
        # States of correctness of each part of the model
        # 0 is form no correct and 1 is for correct
        self.last_model = ''
        self.state_op_params = 0
        self.state_mm_params = 0
        self.state_tol_nIter = 0

        # frame_form_buttons
        frame_form_buttons_triple = tk.Frame(self.frame_form_buttons, relief=tk.SOLID, bg='red')
        frame_form_buttons_triple.pack(side="top", fill=tk.X)

        load_experiment = tk.Button(frame_form_buttons_triple, text="load", font=('Times', 15, BOLD), fg="#2699E6", command=self.set_model)
        load_experiment.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        run = tk.Button(frame_form_buttons_triple, text="run", font=('Times', 15, BOLD), width=2, fg="#2699E6", command=self.run_model)
        run.pack(side="left", fill=tk.X, padx=1, pady=5)

        check = tk.Button(frame_form_buttons_triple, text="check", font=('Times', 15, BOLD), fg="#2699E6", command=self.check)
        check.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        frame_form_buttons_double = tk.Frame(self.frame_form_buttons, relief=tk.SOLID, bg='#FFFBE1')
        frame_form_buttons_double.pack(side="bottom", fill=tk.X)

        back = tk.Button(frame_form_buttons_double, text="back", font=('Times', 15, BOLD), fg="#2699E6", command=self.back)
        back.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        cancel = tk.Button(frame_form_buttons_double, text="cancel", font=('Times', 15, BOLD), fg="#8B0000", command=self.cancel)
        cancel.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        # Configurar la acción de cerrar la ventana
        #self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        #self.window.protocol("WM_DELETE_WINDOW", self.back)
        self.read_test_history()
        self.window.mainloop()

    def built_dic_models(self):
        # The files must end in new file
        f_list_model = open(path.LIST_MODEL_TXT, "r")
        f_list_color_space = open(path.LIST_COLOR_SPACE_TXT, "r")
        f_list_degradation = open(path.LIST_DEGRADATION_TXT, "r")
        f_list_optimizer = open(path.LIST_OPTIMIZER_TXT, "r")
        f_list_math_model = open(path.LIST_MATH_MODEL_TXT, "r")

        models = set()
        for line in f_list_model:
            models.add(line[:-1])

        color_spaces = set()
        for line in f_list_color_space:
            color_spaces.add(line[:-1])

        degradations = set()
        for line in f_list_degradation:
            degradations.add(line[:-1])
        print(degradations)

        dic_optimizers = {}
        for line in f_list_optimizer:
            line_split = line.split(' ')
            dic_optimizers[line_split[0]] = line_split[1:-1]
            dic_optimizers[line_split[0]].append(line_split[-1][:-1])

        dic_math_models = {}
        for line in f_list_math_model:
            line_split = line.split(' ')
            dic_math_models[line_split[0]] = line_split[1:-1]
            dic_math_models[line_split[0]].append(line_split[-1][:-1])

        self.set_models = models
        self.color_spaces = color_spaces
        self.degradations = degradations
        self.dic_optimizers = dic_optimizers
        self.dic_math_models = dic_math_models

        f_list_model.close()
        f_list_optimizer.close()
        f_list_math_model.close()

    def set_model(self):
        update_test_history("LOAD:\n")
        # Get the model
        model = self.model.get()
        model_split = model.split('_')
        optimizer = model_split[0]
        color_space = model_split[1]
        degradation = model_split[2]
        math_model = '_'.join(model_split[3:])

        # frame form tol nIter
        if len(model_split) < 4:
            messagebox.showerror(message="Missing arguments in model.")
            update_test_history("\nMissing arguments in model: ")
        else:
            model_correct = 0
            if optimizer not in self.dic_optimizers.keys():
                messagebox.showerror(message="Incorrect optimizer.")
                model_correct = 1
            if color_space not in self.color_spaces:
                messagebox.showerror(message="Incorrect color space.")
                model_correct = 1
            if degradation not in self.degradations:
                messagebox.showerror(message="Incorrect degradation.")
                model_correct = 1
            if math_model not in self.dic_math_models.keys():
                messagebox.showerror(message="Incorrect math model.")
                model_correct = 1
            if (model not in self.set_models) and (model_correct == 0):
                messagebox.showerror(message="Incorrect model.")
                model_correct = 1

            if model_correct == 0:
                op_param = self.dic_optimizers[optimizer]
                mm_param = self.dic_math_models[math_model]
                # -------------------------------------
                # This part helps to update the parameters for every change of model.
                # If the model is the same, the parameters does not change.
                if self.last_model != model and self.state_op_params==1 and self.state_mm_params==1:
                    self.clear_op_param_mm_param()
                    self.state_op_params = 0
                    self.state_mm_params = 0
                # -------------------------------------
                if self.state_tol_nIter == 0:
                    # Once created these entries they won't disappear until cancel
                    # -------------------------------------
                    # Put the entry for the image name
                    self.image = ttk.Entry(self.frame_form_image, font=('Times', 14))
                    self.image.pack(side='bottom', fill=tk.X, padx=20, pady=5)
                    self.label_image = tk.Label(self.frame_form_image, text="Image (e.g. kodim1):", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_image.pack(side='bottom', fill=tk.X, padx=20, pady=5)
                    # -------------------------------------
                    # Put the entry for the tolerance and the number of iterations
                    self.label_tol = tk.Label(self.frame_form_tol, text="tol", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_tol.pack(fill=tk.X, padx=20, pady=5)
                    self.tol = ttk.Entry(self.frame_form_tol, font=('Times', 14), width=9)
                    self.tol.pack(fill=tk.X, padx=20, pady=1)
                    self.label_nIter = tk.Label(self.frame_form_nIter, text="nIter (>50)", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_nIter.pack(fill=tk.X, padx=20, pady=5)
                    self.nIter = ttk.Entry(self.frame_form_nIter, font=('Times', 14), width=9)
                    self.nIter.pack(fill=tk.X, padx=20, pady=1)
                    self.state_tol_nIter = 1
                    # -------------------------------------
                tol = self.tol.get()
                nIter = self.nIter.get()
                # Put the entries for parameters
                if self.state_op_params == 0:
                    self.op_param_label = [tk.Label(self.frame_form_param_left, text=op_param, font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for op_param in op_param]
                    self.op_param = [ttk.Entry(self.frame_form_param_left, font=('Times', 14),  width=9) for op_param in op_param]
                    for i in range(len(op_param)):
                        self.op_param_label[i].pack(fill=tk.X, padx=20, pady=5)
                        self.op_param[i].pack(fill=tk.X, padx=20, pady=5)
                self.state_op_params = 1
                if self.state_mm_params == 0:
                    self.mm_param_label = [tk.Label(self.frame_form_param_right, text=mm_param, font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param = [ttk.Entry(self.frame_form_param_right, font=('Times', 14),  width=9) for mm_param in mm_param]
                    for i in range(len(mm_param)):
                        self.mm_param_label[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param[i].pack(fill=tk.X, padx=20, pady=5)
                op_param_get = [op.get() for op in self.op_param]
                mm_param_get = [mm.get() for mm in self.mm_param]
                image_name = self.image.get()
                # Update the history and test_exp
                update_test = '_'.join(model_split[1:3]) + '.py ' + model + ' '
                update_test = update_test + image_name + ' '
                update_test = update_test + ' '.join(mm_param_get) + ' '
                update_test = update_test + ' '.join(op_param_get) + ' '
                update_test = update_test + tol + ' ' + nIter + '\n'
                update_test_history(update_test)
                update_test_exp(update_test)
                print(op_param_get,mm_param_get)
                self.state_mm_params = 1

        self.last_model = model

    def cancel(self):
        self.clear_op_param_mm_param()
        self.label_nIter.destroy()
        self.nIter.destroy()
        self.label_tol.destroy()
        self.tol.destroy()
        self.label_image.destroy()
        self.image.destroy()

        self.state_op_params = 0
        self.state_mm_params = 0
        self.state_tol_nIter = 0

    def clear_op_param_mm_param(self):
        for op_param_label in self.op_param_label:
            op_param_label.destroy()
        for op_param in self.op_param:
            op_param.destroy()
        for mm_param_label in self.mm_param_label:
            mm_param_label.destroy()
        for mm_param in self.mm_param:
            mm_param.destroy()

    def run_model(self):
        self.top = tk.Toplevel(self.window)
        self.top.geometry("250x250")
        self.top.title("")
        self.top.config(bg='#FFFBE1')
        self.top.resizable(False, False)
        generic.center_window(self.top, 200, 100)

        frame_text = tk.Frame(self.top, bd=0, height=5, relief=tk.SOLID, padx=5, pady=0, bg='#FFFBE1')
        frame_text.pack(side="top", fill=tk.BOTH)
        text = tk.Label(frame_text, text="Will you want \n to run this model?", font=('times', 20), fg="black", bg='#FFFBE1', pady=5)
        text.pack(expand=tk.YES, fill=tk.BOTH)

        # frame form buttons
        frame_buttons_double = tk.Frame(self.top, bd=0, height=50, relief=tk.SOLID, bg='red')
        frame_buttons_double.pack(side="bottom", fill=tk.BOTH)

        yes = tk.Button(frame_buttons_double, text="YES", font=('Times', 15, BOLD), width=4, fg="#2699E6",command=self.run)
        yes.pack(side="left", fill=tk.X, padx=1, pady=5)

        no = tk.Button(frame_buttons_double, text="NO", font=('Times', 15, BOLD), fg="#8B0000", command=self.top.destroy)
        no.pack(fill=tk.X, padx=1, pady=5)

    def run(self):
        update_test_history("RUN:\n")
        f = open(path.TEST_EXP_TXT, "r")
        last_line = f.readlines()[-1]
        #print('cd set_models; python3 ' + last_line)
        update_test_history("Executing model...")
        process = subprocess.run('cd models; python3 ' + last_line, shell=True, check=True, capture_output=True, encoding='utf-8')
        if process.returncode == 0:
            update_test_history("Model executed successfully.\n")
            if len(process.stdout) > 0:
                print(process.stdout.split("\n")[-2])
        f.close()

    def back(self):
        self.window.destroy()
        MasterPanel()

    def check(self):
        update_test_history("CHECK:\n")

    def read_test_history(self):
        try:
            with open(path.TEST_HISTORY_TXT, 'r') as archivo:
                contenido = archivo.read()
                self.cuadro_texto.delete('1.0', tk.END)  # Borra el contenido actual del cuadro de texto
                self.cuadro_texto.insert(tk.END, contenido)  # Inserta el nuevo contenido
                self.cuadro_texto.see(tk.END)  # Desplaza al final del texto
        except FileNotFoundError:
            self.cuadro_texto.delete('1.0', tk.END)  # Borra el contenido actual del cuadro de texto
            self.cuadro_texto.insert(tk.END, "Archivo 'test_history.txt' no encontrado.")
        # Programar la próxima actualización después de 1000 milisegundos (1 segundo)
        # Verificar si la ventana aún está abierta antes de programar la próxima actualización
        if self.window.winfo_exists():
            self.window.after(500, self.read_test_history)

class upload_exp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Inicio de sesion')
        self.window.geometry('800x800')
        self.window.config(bg='#FFFBE1')
        self.window.resizable(True, True)
        generic.center_window(self.window,900,700)

        self.set_models = set()
        self.color_spaces = set()
        self.degradations = set()
        self.dic_optimizers = {}
        self.dic_math_models = {}
        self.built_dic_models()

        # Structural frames--------------------------
        # Frame for title
        self.frame_form_title = tk.Frame(self.window, bd=0, height=10, relief=tk.SOLID, padx=5, pady=0, bg='#FFFBE1')
        self.frame_form_title.pack(side="top", fill=tk.BOTH)
        self.title = tk.Label(self.frame_form_title, text="Upload experiments", font=('times',30), fg="#666a88", bg='#FFFBE1', pady=5)
        self.title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame for terminal
        self.frame_form_terminal = tk.Frame(self.window, bd=0, width=450, relief=tk.SOLID, padx=5, pady=5, bg='#272727')
        self.frame_form_terminal.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # Crear un cuadro de texto
        self.cuadro_texto = tk.Text(self.frame_form_terminal, width=43, wrap="word")
        self.cuadro_texto.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=10)

        # Frame for buttons
        self.frame_form_buttons = tk.Frame(self.window, bd=0, height=20, relief=tk.SOLID, padx=5, pady=5, bg='#FFFBE1')
        self.frame_form_buttons.pack(side="bottom", fill=tk.BOTH)

        # Frame for fill
        self.frame_form_fill = tk.Frame(self.window, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_fill.pack(side="left", fill=tk.BOTH)
        self.frame_form_model = tk.Frame(self.frame_form_fill, height=25, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_model.pack(side="top", fill=tk.BOTH)

        self.frame_form_script_config = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_script_config.pack(side="top", fill=tk.BOTH)
        self.frame_form_script = tk.Frame(self.frame_form_script_config, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_script.pack(side="left",expand=tk.YES, fill=tk.BOTH)
        self.frame_form_config = tk.Frame(self.frame_form_script_config, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_config.pack(side="left",expand=tk.YES, fill=tk.BOTH)
        #self.frame_form_image = tk.Frame(self.frame_form_fill, height=25, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        #self.frame_form_image.pack(side="top", fill=tk.BOTH)

        self.frame_form_job_log = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_job_log.pack(side="top", fill=tk.BOTH)
        self.frame_form_job = tk.Frame(self.frame_form_job_log, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_job.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_log = tk.Frame(self.frame_form_job_log, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_log.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        self.frame_form_tol_nIter = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_tol_nIter.pack(side="top", fill=tk.BOTH)
        self.frame_form_tol = tk.Frame(self.frame_form_tol_nIter, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_tol.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_nIter = tk.Frame(self.frame_form_tol_nIter, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_nIter.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        self.frame_form_left_right = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_left_right.pack(side="top", fill=tk.BOTH)
        self.frame_form_param_left = tk.Frame(self.frame_form_left_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_left.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right = tk.Frame(self.frame_form_left_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right_1 = tk.Frame(self.frame_form_param_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right_1.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right_2 = tk.Frame(self.frame_form_param_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right_2.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right_3 = tk.Frame(self.frame_form_param_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right_3.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        # ---------------------------------------------

        # Entry for model
        self.label_model = tk.Label(self.frame_form_model, text="Model name:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.label_model.pack(fill=tk.X, padx=20, pady=5)
        self.model = ttk.Entry(self.frame_form_model,  width=50, font=('Times',14))
        self.model.pack(fill=tk.X, padx=20, pady=5)
        # States of correctness of each part of the model
        # 0 is form no correct and 1 is for correct
        self.last_model = ''
        self.state_op_params = 0
        self.state_mm_params = 0
        self.state_tol_nIter = 0

        # frame_form_buttons
        frame_form_buttons_triple = tk.Frame(self.frame_form_buttons, relief=tk.SOLID, bg='red')
        frame_form_buttons_triple.pack(side="top", fill=tk.X)

        load_experiment = tk.Button(frame_form_buttons_triple, text="load", font=('Times', 15, BOLD), fg="#2699E6", command=self.set_model)
        load_experiment.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        run = tk.Button(frame_form_buttons_triple, text="run", font=('Times', 15, BOLD), width=2, fg="#2699E6", command=self.run_model)
        run.pack(side="left", fill=tk.X, padx=1, pady=5)

        check = tk.Button(frame_form_buttons_triple, text="check", font=('Times', 15, BOLD), fg="#2699E6", command=self.check)
        check.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        frame_form_buttons_double = tk.Frame(self.frame_form_buttons, relief=tk.SOLID, bg='#FFFBE1')
        frame_form_buttons_double.pack(side="bottom", fill=tk.X)

        back = tk.Button(frame_form_buttons_double, text="back", font=('Times', 15, BOLD), fg="#2699E6", command=self.back)
        back.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        cancel = tk.Button(frame_form_buttons_double, text="cancel", font=('Times', 15, BOLD), fg="#8B0000", command=self.cancel)
        cancel.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        self.read_upload_history()
        self.window.mainloop()

    def built_dic_models(self):
        # The files must end in new file
        f_list_model = open(path.LIST_MODEL_TXT, "r")
        f_list_color_space = open(path.LIST_COLOR_SPACE_TXT, "r")
        f_list_degradation = open(path.LIST_DEGRADATION_TXT, "r")
        f_list_optimizer = open(path.LIST_OPTIMIZER_TXT, "r")
        f_list_math_model = open(path.LIST_MATH_MODEL_TXT, "r")

        models = set()
        for line in f_list_model:
            models.add(line[:-1])

        color_spaces = set()
        for line in f_list_color_space:
            color_spaces.add(line[:-1])

        degradations = set()
        for line in f_list_degradation:
            degradations.add(line[:-1])
        print(degradations)

        dic_optimizers = {}
        for line in f_list_optimizer:
            line_split = line.split(' ')
            dic_optimizers[line_split[0]] = line_split[1:-1]
            dic_optimizers[line_split[0]].append(line_split[-1][:-1])

        dic_math_models = {}
        for line in f_list_math_model:
            line_split = line.split(' ')
            dic_math_models[line_split[0]] = line_split[1:-1]
            dic_math_models[line_split[0]].append(line_split[-1][:-1])

        self.set_models = models
        self.color_spaces = color_spaces
        self.degradations = degradations
        self.dic_optimizers = dic_optimizers
        self.dic_math_models = dic_math_models

        f_list_model.close()
        f_list_optimizer.close()
        f_list_math_model.close()

    def set_model(self):
        update_upload_history("LOAD:\n")
        # Get the model
        model = self.model.get()
        model_split = model.split('_')
        optimizer = model_split[0]
        color_space = model_split[1]
        degradation = model_split[2]
        math_model = '_'.join(model_split[3:])

        # frame form tol nIter
        if len(model_split) < 4:
            messagebox.showerror(message="Missing arguments in model.")
            update_upload_history("\nMissing arguments in model: ")
        else:
            model_correct = 0
            if optimizer not in self.dic_optimizers.keys():
                messagebox.showerror(message="Incorrect optimizer.")
                model_correct = 1
            if color_space not in self.color_spaces:
                messagebox.showerror(message="Incorrect color space.")
                model_correct = 1
            if degradation not in self.degradations:
                messagebox.showerror(message="Incorrect degradation.")
                model_correct = 1
            if math_model not in self.dic_math_models.keys():
                messagebox.showerror(message="Incorrect math model.")
                model_correct = 1
            if (model not in self.set_models) and (model_correct == 0):
                messagebox.showerror(message="Incorrect model.")
                model_correct = 1

            if model_correct == 0:
                op_param = self.dic_optimizers[optimizer]
                mm_param = self.dic_math_models[math_model]
                # -------------------------------------
                # This part helps to update the parameters for every change of model.
                # If the model is the same, the parameters does not change.
                if self.last_model != model and self.state_op_params==1 and self.state_mm_params==1:
                    self.clear_op_param_mm_param()
                    self.state_op_params = 0
                    self.state_mm_params = 0
                # -------------------------------------
                if self.state_tol_nIter == 0:
                    # Once created these entries they won't disappear until cancel
                    # -------------------------------------
                    # -------------------------------------
                    self.label_script = tk.Label(self.frame_form_script, text="Built_bash_script:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_script.pack(fill=tk.X, padx=20, pady=5)
                    self.script = ttk.Entry(self.frame_form_script, font=('Times', 14))
                    self.script.pack(fill=tk.X, padx=20, pady=5)
                    self.label_config = tk.Label(self.frame_form_config, text="Config (123456):", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_config.pack(fill=tk.X, padx=20, pady=5)
                    self.config = ttk.Entry(self.frame_form_config, font=('Times', 14))
                    self.config.pack(fill=tk.X, padx=20, pady=5)
                    # -------------------------------------
                    self.label_job = tk.Label(self.frame_form_job, text="Name job:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_job.pack(fill=tk.X, padx=20, pady=5)
                    self.job = ttk.Entry(self.frame_form_job, font=('Times', 14), width=9)
                    self.job.pack(fill=tk.X, padx=20, pady=1)
                    self.label_log = tk.Label(self.frame_form_log, text="Name log", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_log.pack(fill=tk.X, padx=20, pady=5)
                    self.log = ttk.Entry(self.frame_form_log, font=('Times', 14), width=9)
                    self.log.pack(fill=tk.X, padx=20, pady=1)
                    # -------------------------------------
                    # Put the entry for the tolerance and the number of iterations
                    self.label_tol = tk.Label(self.frame_form_tol, text="tol", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_tol.pack(fill=tk.X, padx=20, pady=5)
                    self.tol = ttk.Entry(self.frame_form_tol, font=('Times', 14), width=9)
                    self.tol.pack(fill=tk.X, padx=20, pady=1)
                    self.label_nIter = tk.Label(self.frame_form_nIter, text="nIter (>50)", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_nIter.pack(fill=tk.X, padx=20, pady=5)
                    self.nIter = ttk.Entry(self.frame_form_nIter, font=('Times', 14), width=9)
                    self.nIter.pack(fill=tk.X, padx=20, pady=1)
                    self.state_tol_nIter = 1
                    # -------------------------------------
                script = self.script.get()
                config = self.config.get()
                job = self.job.get()
                log = self.log.get()
                tol = self.tol.get()
                nIter = self.nIter.get()
                # Put the entries for parameters
                if self.state_op_params == 0:
                    self.op_param_label = [tk.Label(self.frame_form_param_left, text=op_param, font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for op_param in op_param]
                    self.op_param = [ttk.Entry(self.frame_form_param_left, font=('Times', 14),  width=9) for op_param in op_param]
                    for i in range(len(op_param)):
                        self.op_param_label[i].pack(fill=tk.X, padx=20, pady=5)
                        self.op_param[i].pack(fill=tk.X, padx=20, pady=5)
                self.state_op_params = 1
                if self.state_mm_params == 0:
                    self.mm_param_label_1 = [tk.Label(self.frame_form_param_right_1, text=mm_param+'_0', font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param_1 = [ttk.Entry(self.frame_form_param_right_1, font=('Times', 14), width=3) for mm_param in mm_param]
                    self.mm_param_label_2 = [tk.Label(self.frame_form_param_right_2, text=mm_param+'_h', font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param_2 = [ttk.Entry(self.frame_form_param_right_2, font=('Times', 14), width=3) for mm_param in mm_param]
                    self.mm_param_label_3 = [tk.Label(self.frame_form_param_right_3, text=mm_param+'_N', font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param_3 = [ttk.Entry(self.frame_form_param_right_3, font=('Times', 14), width=3) for mm_param in mm_param]
                    for i in range(len(mm_param)):
                        self.mm_param_label_1[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_1[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_label_2[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_2[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_label_3[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_3[i].pack(fill=tk.X, padx=20, pady=5)
                mm_param_get_1 = [mm.get() for mm in self.mm_param_1]
                mm_param_get_2 = [mm.get() for mm in self.mm_param_2]
                mm_param_get_3 = [mm.get() for mm in self.mm_param_3]
                op_param_get = [op.get() for op in self.op_param]
                # ----------------------------------------
                # Update the history and test_exp
                update_upload = script + ' ' + job + ' ' + log + ' ' + config + ' ' + model + ' '
                # Versión modificada para guardar solo la partición de gamma y un valor de beta
                update_upload = update_upload + mm_param_get_1[0] + ' '
                update_upload = update_upload + mm_param_get_2[0] + ' '
                update_upload = update_upload + mm_param_get_3[0] + ' '
                if len(mm_param_get_3) > 1:
                    update_upload = update_upload + mm_param_get_1[1] + ' '
                # ----------------------------------------
                update_upload = update_upload + ' '.join(op_param_get) + ' '
                update_upload = update_upload + tol + ' ' + nIter + '\n'
                update_upload_history(update_upload)
                update_upload_exp(update_upload)
                print(op_param_get, mm_param_get_1, mm_param_get_2, mm_param_get_3)
                self.state_mm_params = 1

        self.last_model = model

    def cancel(self):
        self.clear_op_param_mm_param()
        self.label_script.destroy()
        self.script.destroy()
        self.label_config.destroy()
        self.config.destroy()
        self.label_job.destroy()
        self.job.destroy()
        self.label_log.destroy()
        self.log.destroy()
        self.label_nIter.destroy()
        self.nIter.destroy()
        self.label_tol.destroy()
        self.tol.destroy()

        self.state_op_params = 0
        self.state_mm_params = 0
        self.state_tol_nIter = 0

    def clear_op_param_mm_param(self):
        for op_param_label in self.op_param_label:
            op_param_label.destroy()
        for op_param in self.op_param:
            op_param.destroy()
        for mm_param_label in self.mm_param_label_1:
            mm_param_label.destroy()
        for mm_param in self.mm_param_1:
            mm_param.destroy()
        for mm_param_label in self.mm_param_label_2:
            mm_param_label.destroy()
        for mm_param in self.mm_param_2:
            mm_param.destroy()
        for mm_param_label in self.mm_param_label_3:
            mm_param_label.destroy()
        for mm_param in self.mm_param_3:
            mm_param.destroy()

    def run_model(self):
        self.top = tk.Toplevel(self.window)
        self.top.geometry("250x250")
        self.top.title("")
        self.top.config(bg='#FFFBE1')
        self.top.resizable(False, False)
        generic.center_window(self.top, 200, 100)

        frame_text = tk.Frame(self.top, bd=0, height=5, relief=tk.SOLID, padx=5, pady=0, bg='#FFFBE1')
        frame_text.pack(side="top", fill=tk.BOTH)
        text = tk.Label(frame_text, text="Will you want \n to upload the experiment?", font=('times', 20), fg="black", bg='#FFFBE1', pady=5)
        text.pack(expand=tk.YES, fill=tk.BOTH)

        # frame form buttons
        frame_buttons_double = tk.Frame(self.top, bd=0, height=50, relief=tk.SOLID, bg='red')
        frame_buttons_double.pack(side="bottom", fill=tk.BOTH)

        yes = tk.Button(frame_buttons_double, text="YES", font=('Times', 15, BOLD), width=4, fg="#2699E6",command=self.run)
        yes.pack(side="left", fill=tk.X, padx=1, pady=5)

        no = tk.Button(frame_buttons_double, text="NO", font=('Times', 15, BOLD), fg="#8B0000", command=self.top.destroy)
        no.pack(fill=tk.X, padx=1, pady=5)

    def run(self):
        update_upload_history("RUN:\n")
        f = open(path.UPLOAD_EXP_TXT, "r")
        last_line = f.readlines()[-1]
        #print('cd models; python3 ' + last_line)
        process = subprocess.run('python3 upload_exp.py ' + last_line, shell=True, check=True, capture_output=True, encoding='utf-8')
        if process.returncode == 0:
            if len(process.stdout) > 0:
                print(process.stdout.split("\n")[-2])
        f.close()

    def back(self):
        self.window.destroy()
        MasterPanel()

    def check(self):
        update_upload_history("CHECK:\n")

    def read_upload_history(self):
        try:
            with open(path.UPLOAD_HISTORY_TXT, 'r') as archivo:
                contenido = archivo.read()
                self.cuadro_texto.delete('1.0', tk.END)  # Borra el contenido actual del cuadro de texto
                self.cuadro_texto.insert(tk.END, contenido)  # Inserta el nuevo contenido
                self.cuadro_texto.see(tk.END)  # Desplaza al final del texto
        except FileNotFoundError:
            self.cuadro_texto.delete('1.0', tk.END)  # Borra el contenido actual del cuadro de texto
            self.cuadro_texto.insert(tk.END, "Archivo 'upload_history.txt' no encontrado.")
        # Programar la próxima actualización después de 1000 milisegundos (1 segundo)
        # Verificar si la ventana aún está abierta antes de programar la próxima actualización
        if self.window.winfo_exists():
            self.window.after(500, self.read_upload_history)

class download_exp:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title('Inicio de sesion')
        self.window.geometry('800x800')
        self.window.config(bg='#FFFBE1')
        self.window.resizable(True, True)
        generic.center_window(self.window,900,700)

        self.set_models = set()
        self.color_spaces = set()
        self.degradations = set()
        self.dic_optimizers = {}
        self.dic_math_models = {}
        self.built_dic_models()

        # Structural frames--------------------------
        # Frame for title
        self.frame_form_title = tk.Frame(self.window, height=10, relief=tk.SOLID, padx=5, pady=0, bg='#FFFBE1')
        self.frame_form_title.pack(side="top", fill=tk.BOTH)
        self.title = tk.Label(self.frame_form_title, text="Download experiments", font=('times',30), fg="#666a88", bg='#FFFBE1', pady=5)
        self.title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame for terminal
        self.frame_form_terminal = tk.Frame(self.window, width=450, relief=tk.SOLID, padx=5, pady=5, bg='#272727')
        self.frame_form_terminal.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # Crear un cuadro de texto
        self.cuadro_texto = tk.Text(self.frame_form_terminal, width=43, wrap="word")
        self.cuadro_texto.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=10)

        # Frame for buttons
        self.frame_form_buttons = tk.Frame(self.window, bd=0, height=20, relief=tk.SOLID, padx=5, pady=5, bg='#FFFBE1')
        self.frame_form_buttons.pack(side="bottom", fill=tk.BOTH)

        # Frame for fill
        self.frame_form_fill = tk.Frame(self.window, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_fill.pack(side="left", fill=tk.BOTH)
        self.frame_form_model = tk.Frame(self.frame_form_fill, height=25, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_model.pack(side="top", fill=tk.BOTH)

        self.frame_form_script_config = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_script_config.pack(side="top", fill=tk.BOTH)
        self.frame_form_script = tk.Frame(self.frame_form_script_config, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_script.pack(side="left",expand=tk.YES, fill=tk.BOTH)
        self.frame_form_config = tk.Frame(self.frame_form_script_config, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_config.pack(side="left",expand=tk.YES, fill=tk.BOTH)
        #self.frame_form_image = tk.Frame(self.frame_form_fill, height=25, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        #self.frame_form_image.pack(side="top", fill=tk.BOTH)

        self.frame_form_job_log = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_job_log.pack(side="top", fill=tk.BOTH)
        self.frame_form_job = tk.Frame(self.frame_form_job_log, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_job.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_log = tk.Frame(self.frame_form_job_log, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_log.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        self.frame_form_tol_nIter = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_tol_nIter.pack(side="top", fill=tk.BOTH)
        self.frame_form_tol = tk.Frame(self.frame_form_tol_nIter, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_tol.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_nIter = tk.Frame(self.frame_form_tol_nIter, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_nIter.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        self.frame_form_left_right = tk.Frame(self.frame_form_fill, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_left_right.pack(side="top", fill=tk.BOTH)
        self.frame_form_param_left = tk.Frame(self.frame_form_left_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_left.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right = tk.Frame(self.frame_form_left_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right_1 = tk.Frame(self.frame_form_param_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right_1.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right_2 = tk.Frame(self.frame_form_param_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right_2.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.frame_form_param_right_3 = tk.Frame(self.frame_form_param_right, relief=tk.SOLID, bg='#fcfcfc')
        self.frame_form_param_right_3.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        # ---------------------------------------------

        # Entry for model
        self.label_model = tk.Label(self.frame_form_model, text="Model name:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.label_model.pack(fill=tk.X, padx=20, pady=5)
        self.model = ttk.Entry(self.frame_form_model,  width=50, font=('Times',14))
        self.model.pack(fill=tk.X, padx=20, pady=5)
        # States of correctness of each part of the model
        # 0 is form no correct and 1 is for correct
        self.last_model = ''
        self.state_op_params = 0
        self.state_mm_params = 0
        self.state_tol_nIter = 0

        # frame_form_buttons
        frame_form_buttons_triple = tk.Frame(self.frame_form_buttons, relief=tk.SOLID, bg='red')
        frame_form_buttons_triple.pack(side="top", fill=tk.X)

        load_experiment = tk.Button(frame_form_buttons_triple, text="load", font=('Times', 15, BOLD), fg="#2699E6", command=self.set_model)
        load_experiment.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        run = tk.Button(frame_form_buttons_triple, text="run", font=('Times', 15, BOLD), width=2, fg="#2699E6", command=self.run_model)
        run.pack(side="left", fill=tk.X, padx=1, pady=5)

        check = tk.Button(frame_form_buttons_triple, text="check", font=('Times', 15, BOLD), fg="#2699E6", command=self.check)
        check.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        frame_form_buttons_double = tk.Frame(self.frame_form_buttons, relief=tk.SOLID, bg='#FFFBE1')
        frame_form_buttons_double.pack(side="bottom", fill=tk.X)

        back = tk.Button(frame_form_buttons_double, text="back", font=('Times', 15, BOLD), fg="#2699E6", command=self.back)
        back.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        cancel = tk.Button(frame_form_buttons_double, text="cancel", font=('Times', 15, BOLD), fg="#8B0000", command=self.cancel)
        cancel.pack(side="left", expand=tk.YES, fill=tk.X, padx=1, pady=5)

        self.read_download_history()
        self.window.mainloop()

    def built_dic_models(self):
        # The files must end in new file
        f_list_model = open(path.LIST_MODEL_TXT, "r")
        f_list_color_space = open(path.LIST_COLOR_SPACE_TXT,"r")
        f_list_degradation = open(path.LIST_DEGRADATION_TXT,"r")
        f_list_optimizer = open(path.LIST_OPTIMIZER_TXT, "r")
        f_list_math_model = open(path.LIST_MATH_MODEL_TXT, "r")

        models = set()
        for line in f_list_model:
            models.add(line[:-1])

        color_spaces = set()
        for line in f_list_color_space:
            color_spaces.add(line[:-1])

        degradations = set()
        for line in f_list_degradation:
            degradations.add(line[:-1])
        print(degradations)

        dic_optimizers = {}
        for line in f_list_optimizer:
            line_split = line.split(' ')
            dic_optimizers[line_split[0]] = line_split[1:-1]
            dic_optimizers[line_split[0]].append(line_split[-1][:-1])

        dic_math_models = {}
        for line in f_list_math_model:
            line_split = line.split(' ')
            dic_math_models[line_split[0]] = line_split[1:-1]
            dic_math_models[line_split[0]].append(line_split[-1][:-1])

        self.set_models = models
        self.color_spaces = color_spaces
        self.degradations = degradations
        self.dic_optimizers = dic_optimizers
        self.dic_math_models = dic_math_models

        f_list_model.close()
        f_list_optimizer.close()
        f_list_math_model.close()

    def set_model(self):
        update_download_history("LOAD:\n")
        # Get the model
        model = self.model.get()
        model_split = model.split('_')
        optimizer = model_split[0]
        color_space = model_split[1]
        degradation = model_split[2]
        math_model = '_'.join(model_split[3:])

        # frame form tol nIter
        if len(model_split) < 4:
            messagebox.showerror(message="Missing arguments in model.")
            update_download_history("\nMissing arguments in model: ")
        else:
            model_correct = 0
            if optimizer not in self.dic_optimizers.keys():
                messagebox.showerror(message="Incorrect optimizer.")
                model_correct = 1
            if color_space not in self.color_spaces:
                messagebox.showerror(message="Incorrect color space.")
                model_correct = 1
            if degradation not in self.degradations:
                messagebox.showerror(message="Incorrect degradation.")
                model_correct = 1
            if math_model not in self.dic_math_models.keys():
                messagebox.showerror(message="Incorrect math model.")
                model_correct = 1
            if (model not in self.set_models) and (model_correct == 0):
                messagebox.showerror(message="Incorrect model.")
                model_correct = 1

            if model_correct == 0:
                op_param = self.dic_optimizers[optimizer]
                mm_param = self.dic_math_models[math_model]
                # -------------------------------------
                # This part helps to update the parameters for every change of model.
                # If the model is the same, the parameters does not change.
                if self.last_model != model and self.state_op_params==1 and self.state_mm_params==1:
                    self.clear_op_param_mm_param()
                    self.state_op_params = 0
                    self.state_mm_params = 0
                # -------------------------------------
                if self.state_tol_nIter == 0:
                    # Once created these entries they won't disappear until cancel
                    # -------------------------------------
                    # -------------------------------------
                    self.label_script = tk.Label(self.frame_form_script, text="Built_data_script:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_script.pack(fill=tk.X, padx=20, pady=5)
                    self.script = ttk.Entry(self.frame_form_script, font=('Times', 14))
                    self.script.pack(fill=tk.X, padx=20, pady=5)
                    self.label_config = tk.Label(self.frame_form_config, text="Config (123):", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_config.pack(fill=tk.X, padx=20, pady=5)
                    self.config = ttk.Entry(self.frame_form_config, font=('Times', 14))
                    self.config.pack(fill=tk.X, padx=20, pady=5)
                    # -------------------------------------
                    self.label_job = tk.Label(self.frame_form_job, text="Name job:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_job.pack(fill=tk.X, padx=20, pady=5)
                    self.job = ttk.Entry(self.frame_form_job, font=('Times', 14), width=9)
                    self.job.pack(fill=tk.X, padx=20, pady=1)
                    self.label_log = tk.Label(self.frame_form_log, text="Name log", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_log.pack(fill=tk.X, padx=20, pady=5)
                    self.log = ttk.Entry(self.frame_form_log, font=('Times', 14), width=9)
                    self.log.pack(fill=tk.X, padx=20, pady=1)
                    # -------------------------------------
                    # Put the entry for the tolerance and the number of iterations
                    self.label_tol = tk.Label(self.frame_form_tol, text="tol", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_tol.pack(fill=tk.X, padx=20, pady=5)
                    self.tol = ttk.Entry(self.frame_form_tol, font=('Times', 14), width=9)
                    self.tol.pack(fill=tk.X, padx=20, pady=1)
                    self.label_nIter = tk.Label(self.frame_form_nIter, text="nIter (>50)", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
                    self.label_nIter.pack(fill=tk.X, padx=20, pady=5)
                    self.nIter = ttk.Entry(self.frame_form_nIter, font=('Times', 14), width=9)
                    self.nIter.pack(fill=tk.X, padx=20, pady=1)
                    self.state_tol_nIter = 1
                    # -------------------------------------
                script = self.script.get()
                config = self.config.get()
                job = self.job.get()
                log = self.log.get()
                tol = self.tol.get()
                nIter = self.nIter.get()
                # Put the entries for parameters
                if self.state_op_params == 0:
                    self.op_param_label = [tk.Label(self.frame_form_param_left, text=op_param, font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for op_param in op_param]
                    self.op_param = [ttk.Entry(self.frame_form_param_left, font=('Times', 14),  width=9) for op_param in op_param]
                    for i in range(len(op_param)):
                        self.op_param_label[i].pack(fill=tk.X, padx=20, pady=5)
                        self.op_param[i].pack(fill=tk.X, padx=20, pady=5)
                self.state_op_params = 1
                if self.state_mm_params == 0:
                    self.mm_param_label_1 = [tk.Label(self.frame_form_param_right_1, text=mm_param+'_0', font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param_1 = [ttk.Entry(self.frame_form_param_right_1, font=('Times', 14), width=3) for mm_param in mm_param]
                    self.mm_param_label_2 = [tk.Label(self.frame_form_param_right_2, text=mm_param+'_h', font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param_2 = [ttk.Entry(self.frame_form_param_right_2, font=('Times', 14), width=3) for mm_param in mm_param]
                    self.mm_param_label_3 = [tk.Label(self.frame_form_param_right_3, text=mm_param+'_N', font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w") for mm_param in mm_param]
                    self.mm_param_3 = [ttk.Entry(self.frame_form_param_right_3, font=('Times', 14), width=3) for mm_param in mm_param]
                    for i in range(len(mm_param)):
                        self.mm_param_label_1[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_1[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_label_2[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_2[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_label_3[i].pack(fill=tk.X, padx=20, pady=5)
                        self.mm_param_3[i].pack(fill=tk.X, padx=20, pady=5)
                mm_param_get_1 = [mm.get() for mm in self.mm_param_1]
                mm_param_get_2 = [mm.get() for mm in self.mm_param_2]
                mm_param_get_3 = [mm.get() for mm in self.mm_param_3]
                op_param_get = [op.get() for op in self.op_param]
                # ----------------------------------------
                # Update the history and test_exp
                update_download = script + ' ' + job + ' ' + log + ' ' + config + ' ' + model + ' '
                # Versión modificada para guardar solo la partición de gamma y un valor de beta
                update_download = update_download + mm_param_get_1[0] + ' '
                update_download = update_download + mm_param_get_2[0] + ' '
                update_download = update_download + mm_param_get_3[0] + ' '
                if len(mm_param_get_3)>1:
                    update_download = update_download + mm_param_get_1[1] + ' '
                # ----------------------------------------
                update_download = update_download + ' '.join(op_param_get) + ' '
                update_download = update_download + tol + ' ' + nIter + '\n'
                update_download_history(update_download)
                update_download_exp(update_download)
                print(op_param_get, mm_param_get_1, mm_param_get_2, mm_param_get_3)
                self.state_mm_params = 1

        self.last_model = model

    def cancel(self):
        self.clear_op_param_mm_param()
        self.label_script.destroy()
        self.script.destroy()
        self.label_config.destroy()
        self.config.destroy()
        self.label_job.destroy()
        self.job.destroy()
        self.label_log.destroy()
        self.log.destroy()
        self.label_nIter.destroy()
        self.nIter.destroy()
        self.label_tol.destroy()
        self.tol.destroy()

        self.state_op_params = 0
        self.state_mm_params = 0
        self.state_tol_nIter = 0

    def clear_op_param_mm_param(self):
        for op_param_label in self.op_param_label:
            op_param_label.destroy()
        for op_param in self.op_param:
            op_param.destroy()
        for mm_param_label in self.mm_param_label_1:
            mm_param_label.destroy()
        for mm_param in self.mm_param_1:
            mm_param.destroy()
        for mm_param_label in self.mm_param_label_2:
            mm_param_label.destroy()
        for mm_param in self.mm_param_2:
            mm_param.destroy()
        for mm_param_label in self.mm_param_label_3:
            mm_param_label.destroy()
        for mm_param in self.mm_param_3:
            mm_param.destroy()

    def run_model(self):
        self.top = tk.Toplevel(self.window)
        self.top.geometry("250x250")
        self.top.title("")
        self.top.config(bg='#FFFBE1')
        self.top.resizable(False, False)
        generic.center_window(self.top, 200, 100)

        frame_text = tk.Frame(self.top, bd=0, height=5, relief=tk.SOLID, padx=5, pady=0, bg='#FFFBE1')
        frame_text.pack(side="top", fill=tk.BOTH)
        text = tk.Label(frame_text, text="Will you want \n to upload the experiment?", font=('times', 20), fg="black", bg='#FFFBE1', pady=5)
        text.pack(expand=tk.YES, fill=tk.BOTH)

        # frame form buttons
        frame_buttons_double = tk.Frame(self.top, bd=0, height=50, relief=tk.SOLID, bg='red')
        frame_buttons_double.pack(side="bottom", fill=tk.BOTH)

        yes = tk.Button(frame_buttons_double, text="YES", font=('Times', 15, BOLD), width=4, fg="#2699E6",command=self.run)
        yes.pack(side="left", fill=tk.X, padx=1, pady=5)

        no = tk.Button(frame_buttons_double, text="NO", font=('Times', 15, BOLD), fg="#8B0000", command=self.top.destroy)
        no.pack(fill=tk.X, padx=1, pady=5)

    def run(self):
        update_download_history("RUN:\n")
        f = open(path.DOWNLOAD_EXP_TXT, "r")
        last_line = f.readlines()[-1]
        #print('cd models; python3 ' + last_line)
        process = subprocess.run('python3 download_exp.py ' + last_line, shell=True, check=True, capture_output=True, encoding='utf-8')
        if process.returncode == 0:
            if len(process.stdout) > 0:
                print(process.stdout.split("\n")[-2])
        f.close()

    def back(self):
        self.window.destroy()
        MasterPanel()

    def check(self):
        update_download_history("CHECK:\n")

    def read_download_history(self):
        try:
            with open(path.DOWNLOAD_HISTORY_TXT, 'r') as archivo:
                contenido = archivo.read()
                self.cuadro_texto.delete('1.0', tk.END)  # Borra el contenido actual del cuadro de texto
                self.cuadro_texto.insert(tk.END, contenido)  # Inserta el nuevo contenido
                self.cuadro_texto.see(tk.END)  # Desplaza al final del texto
        except FileNotFoundError:
            self.cuadro_texto.delete('1.0', tk.END)  # Borra el contenido actual del cuadro de texto
            self.cuadro_texto.insert(tk.END, "Archivo 'download_history.txt' no encontrado.")
        # Programar la próxima actualización después de 1000 milisegundos (1 segundo)
        # Verificar si la ventana aún está abierta antes de programar la próxima actualización
        if self.window.winfo_exists():
            self.window.after(500, self.read_download_history)
