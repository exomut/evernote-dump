from tkinter import Tk, filedialog, Button, Frame, Checkbutton, IntVar

from dump import run_parse
from utilities.settings import Settings


class EvernoteDump(Tk):

    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self.iconbitmap('favicon.ico')
        self.title('Evernote Dump')
        self.geometry("500x500")


class EvernoteDumpFrame(Frame):
    def __init__(self, master: EvernoteDump):
        super().__init__(master)
        self.master = master
        self.pack(fill="both")

        self.open_button = Button(text='Choose Evernote Export Files (.enex)', command=self.open_file_picker)
        self.open_button.pack(fill='x', padx=10, pady=10)

        self.preserve = IntVar()
        self.preserve_names = Checkbutton(text='Preserve file names for attachments if found', variable=self.preserve,
                                          command=self.toggle_preserve)
        self.preserve_names.pack(anchor='nw', padx=10, pady=10)

        self.export_dir_button = Button(text='Choose a folder to export to', command=self.choose_export_dir)
        self.export_dir_button.pack(fill='x', padx=10, pady=10)

        self.run = Button(text='Start Evernote Conversion to Markdown', command=self.run)
        self.run.pack(fill='x', padx=10, pady=10)

    def choose_export_dir(self):
        self.master.settings.path = filedialog.askdirectory()

    def open_file_picker(self):
        self.master.settings.enex = filedialog.askopenfilenames()

    def run(self):
        run_parse(self.master.settings)

    def toggle_preserve(self):
        self.master.settings.p = bool(self.preserve)

def load_gui():
    root = EvernoteDump()
    app = EvernoteDumpFrame(root)
    app.mainloop()

if __name__ == '__main__':
    load_gui()
