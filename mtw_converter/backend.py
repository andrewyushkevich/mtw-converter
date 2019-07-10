from Tkinter import *
import ttk
import tkFileDialog
import os
from functools import partial, wraps


def init_ui(box_value, label_update, matrix_path):
    create_labels(label_update)
    create_open_button()
    create_combobox(box_value)


def create_labels(label_update):
    label_text = "Add .MTW matrix"
    update_status(label_text)
    label_update = Label(textvariable=label_update,
                         font=("Helvetica", 14), fg="green")
    label_update.pack()


def update_status(label_text):
    label_update.set(label_text)


def create_open_button():
    open_button = Button(text="Open .MTW file", width=100, command=on_open)
    open_button.pack()


def on_open():
    ftypes = [('Panorama Matrix files', '.mtw')]
    dialog = tkFileDialog.Open(filetypes=ftypes)
    matrix = dialog.show()

    if matrix != '':
        mtw_matrix = read_mtw_matrix(matrix)
        label_text = "Matrix has been added \n Choose format and press Convert"
        update_status(label_text)
        create_process_button(matrix)


def read_mtw_matrix(matrix):
    f = open(matrix, "r")
    matrix_mtw = f.read()

    return matrix_mtw


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False

    return wrapper


@run_once
def create_process_button(matrix_path):
    convert_mtw_matrix_command = partial(convert_mtw_matrix, matrix_path)
    process_button = Button(text="Convert", width=100,
                            command=convert_mtw_matrix_command)
    process_button.pack()


def convert_mtw_matrix(matrix):
    label_text = "Converting..."
    update_status(label_text)
    create_progress_bar().start()
    formats = box_value.get()
    backend.way_of_converting(matrix, formats)


def create_progress_bar():
    progress_bar = ttk.Progressbar(orient=HORIZONTAL, mode='indeterminate')
    progress_bar.pack()

    return progress_bar


def create_combobox(box_value):
    label_formats = Label(text="Choose output format", font=("Helvetica", 10))
    label_formats.pack()
    formats = (".stl", ".raw", ".tif")
    box = ttk.Combobox(textvariable=box_value, values=formats)
    box_value = box.bind('<<ComboboxSelected>>', get_format)
    box.current(0)
    box.pack()


def get_format(event):
    picked_format = box_value.get()

    return picked_format

root = Tk()
root.title("VAS GeoConverter")
root.geometry("300x350")

box_value = StringVar()
box_value.set('')
label_update = StringVar()
label_update.set('STATUS')
matrix_path = StringVar()
matrix_path.set('')

init_ui(box_value, label_update, matrix_path)
root.mainloop()
