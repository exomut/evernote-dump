import os
import threading

from tkinter import Tk, filedialog, Button, Frame, Checkbutton, IntVar, Label, Listbox, scrolledtext, \
    DISABLED, NORMAL, END

from dump import run_parse
from utilities.settings import Settings

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


class EvernoteDump(Tk):

    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self.iconbitmap(os.path.join(SCRIPT_PATH, 'favicon.ico'))
        self.title('Evernote Dump')
        self.geometry("500x600")


class EvernoteDumpFrame(Frame):

    def __init__(self, master: EvernoteDump):
        super().__init__(master)

        self.master = master
        self.pack(fill="both")

        self.open_button = Button(text='Choose Evernote Export File(s) (.enex)', command=self.open_file_picker)
        self.open_button.pack(fill='x', padx=10, pady=10)

        self.export_files_list = Listbox(height=4)
        self.export_files_list.insert(0, "No files selected.")
        self.export_files_list.pack(fill='x', padx=10, pady=10)

        self.preserve = IntVar()
        self.preserve_names = Checkbutton(text='Preserve file names for attachments if found', variable=self.preserve,
                                          command=self.toggle_preserve)
        self.preserve_names.pack(anchor='nw', padx=10, pady=10)

        self.export_dir_button = Button(text='Choose Export Directory', command=self.open_directory_picker)
        self.export_dir_button.pack(fill='x', padx=10, pady=10)

        self.export_dir_label = Label(text="Please select an export directory")
        self.export_dir_label.pack(fill='x', padx=10, pady=10)

        self.run_button = Button(text='Start Evernote Conversion to Markdown', state=DISABLED, command=self.run)
        self.run_button.pack(fill='x', padx=10, pady=10)

        self.log_box = scrolledtext.ScrolledText()
        self.log_box.pack(fill='x', padx=10, pady=10)

    def check(self):
        if len(self.master.settings.files) > 0 and self.master.settings.export_path != '':
            self.run_button.config(state=NORMAL)
        else:
            self.run_button.config(state=DISABLED)

    def open_directory_picker(self):
        self.master.settings.path = filedialog.askdirectory()
        self.export_dir_label.config(text=f"{self.master.settings.path}")

        self.check()

    def open_file_picker(self):
        self.master.settings.enex = filedialog.askopenfilenames()
        self.export_files_list.delete(0, END)
        for file in self.master.settings.enex:
            self.export_files_list.insert(0, file)

        self.check()

    def run(self):
        self.run_button.config(state=DISABLED)

        def print_callback(print_text: str):
            self.log_box.insert(END, f"{print_text}\n")
            self.log_box.see(END)

        threading.Thread(target=run_parse, args=(self.master.settings, print_callback)).start()

    def toggle_preserve(self):
        self.master.settings.p = bool(self.preserve)


def load_gui():
    root = EvernoteDump()
    app = EvernoteDumpFrame(root)
    app.mainloop()


if __name__ == '__main__':
    load_gui()
