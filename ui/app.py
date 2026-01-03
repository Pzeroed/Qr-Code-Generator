import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk
import os
from datetime import datetime

from core.qr_generator import generate_qr_image
from core.history import load_history, save_history
from core.config import load_config, save_config
from core.utils import sanitize_filename, get_unique_path

ASSETS_DIR = "assets"
DEFAULT_LOGO = os.path.join(ASSETS_DIR, "default_logo.png")

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("720x560")
        self.root.resizable(False, False)

        self.config = load_config()
        self.history = load_history()

        self.build_ui()
        self.update_preview()

    def build_ui(self):
        self.text_var = tk.StringVar()
        self.filename_var = tk.StringVar(value="qr_code.png")
        self.folder_var = tk.StringVar(value=self.config["last_folder"])
        self.size_var = tk.IntVar(value=self.config["box_size"])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_generate_tab()
        self.build_history_tab()

    def build_generate_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Generate")

        ttk.Label(tab, text="Text / URL").grid(row=0, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.text_var, width=45).grid(row=0, column=1, columnspan=2)
        self.text_var.trace_add("write", lambda *_: self.update_preview())

        ttk.Label(tab, text="Filename").grid(row=1, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.filename_var, width=45).grid(row=1, column=1, columnspan=2)

        ttk.Label(tab, text="Folder").grid(row=2, column=0, sticky="w")
        ttk.Entry(tab, textvariable=self.folder_var, width=35).grid(row=2, column=1)
        ttk.Button(tab, text="Browse", command=self.choose_folder).grid(row=2, column=2)

        ttk.Label(tab, text="Size").grid(row=3, column=0)
        ttk.Scale(tab, from_=5, to=20, variable=self.size_var,
                  command=lambda _: self.update_preview()).grid(row=3, column=1, columnspan=2, sticky="we")

        self.preview = tk.Label(tab)
        self.preview.grid(row=0, column=3, rowspan=5, padx=10)

        ttk.Button(tab, text="Generate QR", command=self.generate_qr).grid(row=5, column=0, columnspan=4, pady=10)

    def build_history_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="History")

        self.tree = ttk.Treeview(tab, columns=("data", "file", "date"), show="headings")
        self.tree.heading("data", text="Text / URL")
        self.tree.heading("file", text="Filename")
        self.tree.heading("date", text="Date")
        self.tree.pack(fill="both", expand=True)

        self.refresh_history()

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.config["last_folder"] = folder
            save_config(self.config)

    def update_preview(self):
        img = generate_qr_image(
            self.text_var.get(),
            self.size_var.get()
        )
        img.thumbnail((240, 240))
        self.tk_img = ImageTk.PhotoImage(img)
        self.preview.config(image=self.tk_img)

    def generate_qr(self):
        data = self.text_var.get().strip()
        folder = self.folder_var.get()

        if not data or not folder:
            messagebox.showerror("Error", "Missing text or folder")
            return

        filename = sanitize_filename(self.filename_var.get())
        if not filename.endswith(".png"):
            filename += ".png"

        path = get_unique_path(folder, filename)
        img = generate_qr_image(data, self.size_var.get())
        img.save(path)

        self.history.append({
            "data": data,
            "filename": filename,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.history = save_history(self.history)
        self.refresh_history()

        messagebox.showinfo("Saved", f"Saved to:\n{path}")

    def refresh_history(self):
        self.tree.delete(*self.tree.get_children())
        for h in self.history:
            self.tree.insert("", "end", values=(h["data"], h["filename"], h["date"]))
