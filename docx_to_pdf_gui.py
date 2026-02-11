import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from docx_to_pdf_skill import docx_to_pdf
import threading
from pathlib import Path

class DocxToPdfGui:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 KBJ2 - Supreme DOCX to PDF Converter")
        self.root.geometry("600x450")
        self.root.configure(bg="#1e1e1e")
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark Theme Configuration
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#007acc")
        style.configure("Footer.TLabel", font=("Segoe UI", 8), foreground="#888888")
        
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.map("TButton",
                  background=[('active', '#005a9e'), ('!', 'active', '#007acc')],
                  foreground=[('!', 'active', '#ffffff')])

    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)
        
        ttk.Label(header_frame, text="KBJ2 Supreme Converter", style="Header.TLabel").pack()
        ttk.Label(header_frame, text="Premium Background PDF Export Engine").pack()

        # Drag and Drop Zone
        self.drop_frame = tk.Frame(self.root, bg="#2d2d2d", highlightthickness=2, highlightbackground="#007acc")
        self.drop_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.drop_label = tk.Label(
            self.drop_frame, 
            text="🤝 Drag & Drop DOCX Files Here\n(Batch processing supported)",
            bg="#2d2d2d", 
            fg="#cccccc",
            font=("Segoe UI", 12, "italic"),
            justify="center"
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        # Register Drag & Drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_var = tk.StringVar(value="Ready to mobilize...")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=5)

        # Footer
        ttk.Label(self.root, text="Powered by KBJ2 Agentic Engine", style="Footer.TLabel").pack(side="bottom", pady=10)

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        docx_files = [f for f in files if f.lower().endswith('.docx')]
        
        if not docx_files:
            messagebox.showwarning("No DOCX", "Please drop .docx files only, Commander.")
            return
        
        self.status_var.set(f"Mobilizing agents for {len(docx_files)} files...")
        threading.Thread(target=self.process_files, args=(docx_files,), daemon=True).start()

    def process_files(self, files):
        self.progress["maximum"] = len(files)
        self.progress["value"] = 0
        
        success_count = 0
        for i, file in enumerate(files):
            file_name = os.path.basename(file)
            self.status_var.set(f"Converting ({i+1}/{len(files)}): {file_name}")
            
            if docx_to_pdf(file):
                success_count += 1
            
            self.progress["value"] = i + 1
            
        self.status_var.set(f"Operation Complete: {success_count}/{len(files)} optimized.")
        messagebox.showinfo("Success", f"Successfully converted {success_count} files to PDF.")
        self.progress["value"] = 0

def launch_gui():
    root = TkinterDnD.Tk()
    app = DocxToPdfGui(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
