import os
import struct
from collections import namedtuple

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

entry = namedtuple('Entry', 'sv offset fmt max')


class App(Tk):
    def __init__(self):
        super().__init__()
        self.vcmd = self.register(self.validate), '%d', '%P'

        def callback(attribute):
            value = attribute.sv.get()
            if value and int(value) > attribute.max:
                attribute.sv.set(str(attribute.max))

        self.macca = entry(StringVar(), 0x10C, '<i', 999999999)
        self.macca.sv.set('0')
        self.macca.sv.trace('w', lambda *args: callback(self.macca))

        self.app_points = entry(StringVar(), 0x2E38, '<I', 9999)
        self.app_points.sv.set('0')
        self.app_points.sv.trace('w', lambda *args: callback(self.app_points))

        self.title('Demonica')
        self.iconbitmap('icon.ico')
        self.create_widgets()

    def validate(self, action, value_if_allowed):
        if action != '1':
            return True
        try:
            value = int(value_if_allowed)
        except ValueError:
            return False
        else:
            return True

    def create_widgets(self):
        menubar = Menu(self)

        file_menu = Menu(menubar, tearoff=0)

        file_menu.add_command(label="Open Save File", underline=0,
                              accelerator='Ctrl+O', command=self.open_file)
        self.bind('<Control-o>', lambda event: self.open_file())

        file_menu.add_command(label="Save", underline=0, accelerator='Ctrl+S',
                              command=self.save_file)
        self.bind('<Control-s>', lambda event: self.save_file())

        file_menu.add_separator()
        file_menu.add_command(label="Exit", underline=0, command=self.quit)
        menubar.add_cascade(label="File", underline=0, menu=file_menu)
        self.config(menu=menubar)

        tabs = Notebook(self)

        page_1 = Frame(tabs)

        Label(page_1, text="Macca: ").grid(sticky="E", pady="10 0")
        Entry(page_1, textvariable=self.macca.sv, validate="key",
              validatecommand=self.vcmd).grid(column=1, row=0, sticky="EW",
                                              padx="5 0", pady="10 0")

        Label(page_1, text="App Points: ").grid(row=1, sticky="E", pady="5 0")
        Entry(page_1, textvariable=self.app_points.sv, validate="key",
              validatecommand=self.vcmd).grid(column=1, row=1, sticky="EW",
                                              padx="5 0", pady="5 0")

        Button(page_1, text="Apply",
               command=self.apply_changes).grid(row=2, columnspan=2,
                                                pady="10 0")

        tabs.add(page_1, text='Macca/App Points')
        tabs.pack(expand=1, fill='both')

    def open_file(self):
        filetypes = [('Save Files', '*.sav'), ('All Files', '*.*')]
        save_file = filedialog.askopenfilenames(parent=self,
                                                initialdir=os.getcwd(),
                                                filetypes=filetypes)

        if not save_file:
            return

        save_file = save_file[0]
        with open(save_file, 'rb') as f:
            data = bytearray(f.read())

        self._file = save_file
        self._data = data

        macca = self.get_value(self.macca)
        self.macca.sv.set(str(macca))

        app_points = self.get_value(self.app_points)
        self.app_points.sv.set(str(app_points))

    def save_file(self):
        if self._file:
            with open(self._file, 'wb') as f:
                f.write(self._data)

    def get_value(self, attribute):
        return struct.unpack_from(attribute.fmt, self._data, attribute.offset)[0]

    def set_value(self, attribute, value):
        struct.pack_into(attribute.fmt, self._data, attribute.offset, value)

    def apply_changes(self):
        if self._data:
            macca = self.macca.sv.get() or 0
            self.set_value(self.macca, int(macca))

            app_points = self.app_points.sv.get() or 0
            self.set_value(self.app_points, int(app_points))


if __name__ == '__main__':
    app = App()
    app.mainloop()
