"""
KBJ2 R2 Cloud Storage Explorer
File Explorer UI for Cloudflare R2 Storage
"""
import os
import sys
import asyncio
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
from datetime import datetime
from threading import Thread
import webbrowser

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from r2_client import R2Client


class R2Explorer:
    """R2 Cloud Storage File Explorer GUI"""

    # Color Scheme (Dark Theme)
    COLORS = {
        'bg': '#1e1e1e',
        'fg': '#e0e0e0',
        'select_bg': '#007acc',
        'select_fg': '#ffffff',
        'tree_bg': '#252526',
        'tree_fg': '#cccccc',
        'header_bg': '#333333',
        'header_fg': '#ffffff',
        'accent': '#007acc',
        'success': '#4ec9b0',
        'error': '#f48771',
        'border': '#3e3e42'
    }

    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.root.title("KBJ2 R2 Cloud Explorer")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.COLORS['bg'])

        # R2 Client
        self.client = None
        self.current_prefix = ""
        self.selected_file = None
        self.upload_queue = []

        # Setup UI
        self._setup_styles()
        self._create_widgets()

        # Initialize R2 connection
        self._init_r2()

    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles with dark theme
        style.configure('TFrame', background=self.COLORS['bg'])
        style.configure('TLabel', background=self.COLORS['bg'], foreground=self.COLORS['fg'])
        style.configure('TButton', background=self.COLORS['header_bg'], foreground=self.COLORS['header_fg'],
                      borderwidth=1, focuscolor='none')
        style.map('TButton', background=[('active', self.COLORS['accent'])])

        style.configure('Header.TLabel', font=('Segoe UI', 10, 'bold'), foreground=self.COLORS['accent'])
        style.configure('Path.TLabel', font=('Consolas', 9))

        style.configure('Treeview',
                       background=self.COLORS['tree_bg'],
                       foreground=self.COLORS['tree_fg'],
                       fieldbackground=self.COLORS['tree_bg'],
                       borderwidth=0,
                       rowheight=28)
        style.map('Treeview', background=[('selected', self.COLORS['select_bg'])],
                  foreground=[('selected', self.COLORS['select_fg'])])

        style.configure('Treeview.Heading',
                       background=self.COLORS['header_bg'],
                       foreground=self.COLORS['header_fg'],
                       borderwidth=1,
                       relief='flat')
        style.map('Treeview.Heading', background=[('active', self.COLORS['accent'])])

        style.configure('Status.TLabel', font=('Segoe UI', 9), foreground=self.COLORS['success'])
        style.configure('Error.TLabel', font=('Segoe UI', 9), foreground=self.COLORS['error'])

        # Progress bar
        style.configure('Horizontal.TProgressbar',
                       background=self.COLORS['accent'],
                       troughcolor=self.COLORS['header_bg'],
                       borderwidth=0,
                       thickness=8)

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header
        self._create_header(main_frame)

        # Toolbar
        self._create_toolbar(main_frame)

        # Content Area (Split)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, pady=(10, 0))

        # Left: Folder Tree
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side='left', fill='both', expand=(False, False), padx=(0, 5))
        self._create_folder_tree(left_panel)

        # Right: File List
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side='left', fill='both', expand=True)
        self._create_file_list(right_panel)

        # Upload Zone (Bottom)
        self._create_upload_zone(main_frame)

        # Status Bar
        self._create_status_bar(main_frame)

    def _create_header(self, parent):
        """Create header section"""
        header = ttk.Frame(parent)
        header.pack(fill='x', pady=(0, 10))

        # Title
        title = ttk.Label(header, text="R2 Cloud Storage Explorer", style='Header.TLabel')
        title.pack(side='left')

        # Connection status
        self.conn_label = ttk.Label(header, text="Initializing...", style='Status.TLabel')
        self.conn_label.pack(side='right')

    def _create_toolbar(self, parent):
        """Create toolbar with actions"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill='x', pady=(0, 5))

        buttons = [
            ("🔃 Refresh", self.refresh),
            ("📤 Upload", self.upload_files),
            ("⬇️ Download", self.download_file),
            ("📁 New Folder", self.create_folder),
            ("🗑️ Delete", self.delete_file),
            ("🔗 Share URL", self.share_file),
            ("🏠 Home", self.go_home)
        ]

        for text, cmd in buttons:
            btn = ttk.Button(toolbar, text=text, command=cmd)
            btn.pack(side='left', padx=2)

        # Breadcrumb
        self.breadcrumb = ttk.Label(toolbar, text="/", style='Path.TLabel')
        self.breadcrumb.pack(side='left', padx=(20, 0))

    def _create_folder_tree(self, parent):
        """Create folder tree view"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True)

        header = ttk.Label(container, text="Folders", style='Header.TLabel')
        header.pack(fill='x', pady=(0, 5))

        self.folder_tree = ttk.Treeview(container, show='tree', selectmode='browse')
        self.folder_tree.pack(fill='both', expand=True)

        self.folder_tree.bind('<<TreeviewSelect>>', self._on_folder_select)
        self.folder_tree.bind('<Double-1>', self._on_folder_double)

        # Scrollbar
        vsb = ttk.Scrollbar(container, orient='vertical', command=self.folder_tree.yview)
        vsb.pack(side='right', fill='y')
        self.folder_tree.configure(yscrollcommand=vsb.set)

    def _create_file_list(self, parent):
        """Create file list view"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True)

        header = ttk.Label(container, text="Files", style='Header.TLabel')
        header.pack(fill='x', pady=(0, 5))

        # Treeview with columns
        columns = ('name', 'size', 'modified')
        self.file_list = ttk.Treeview(container, columns=columns, show='headings', selectmode='browse')

        self.file_list.heading('name', text='Name', command=lambda c='name': self._sort_by(c))
        self.file_list.heading('size', text='Size', command=lambda c='size': self._sort_by(c))
        self.file_list.heading('modified', text='Modified', command=lambda c='modified': self._sort_by(c))

        self.file_list.column('name', width=300, anchor='w')
        self.file_list.column('size', width=100, anchor='e')
        self.file_list.column('modified', width=180, anchor='w')

        self.file_list.pack(fill='both', expand=True)

        self.file_list.bind('<<TreeviewSelect>>', self._on_file_select)
        self.file_list.bind('<Double-1>', self._on_file_double)

        # Scrollbars
        vsb = ttk.Scrollbar(container, orient='vertical', command=self.file_list.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(container, orient='horizontal', command=self.file_list.xview)
        hsb.pack(side='bottom', fill='x')

        self.file_list.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def _create_upload_zone(self, parent):
        """Create drag-and-drop upload zone"""
        zone_frame = ttk.LabelFrame(parent, text="Upload Zone (Drag & Drop)", padding=10)
        zone_frame.pack(fill='x', pady=(10, 5))

        self.upload_label = ttk.Label(zone_frame, text="Drop files here to upload",
                                    background=self.COLORS['tree_bg'],
                                    foreground=self.COLORS['tree_fg'],
                                    padding=20)
        self.upload_label.pack(fill='both', expand=True)

        # Progress bar
        self.progress = ttk.Progressbar(zone_frame, style='Horizontal.TProgressbar', mode='determinate')
        self.progress.pack(fill='x', pady=(10, 0))

        # Try to enable drag-and-drop
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self._on_drop)
            self.upload_label.configure(text="Drop files here to upload - READY")
        except:
            self.upload_label.configure(text="Upload zone (tkinterdnd2 not installed)")

    def _create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', pady=(10, 0))

        self.status_label = ttk.Label(status_frame, text="Ready", style='Status.TLabel')
        self.status_label.pack(side='left')

        self.info_label = ttk.Label(status_frame, text="", style='Path.TLabel')
        self.info_label.pack(side='right')

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def _init_r2(self):
        """Initialize R2 client in background"""
        def init():
            try:
                self.client = R2Client()
                self._update_status("Connected to R2", "success")
                self.refresh()
            except Exception as e:
                self._update_status(f"Connection failed: {e}", "error")

        Thread(target=init, daemon=True).start()

    # ============================================================
    # ACTIONS
    # ============================================================

    def refresh(self):
        """Refresh folder tree and file list"""
        if not self.client:
            return

        def do_refresh():
            self._load_folders()
            self._load_files(self.current_prefix)

        Thread(target=do_refresh, daemon=True).start()

    def upload_files(self):
        """Open file dialog for upload"""
        files = filedialog.askopenfilenames(
            title="Select files to upload",
            filetypes=[
                ("All files", "*.*"),
                ("Documents", "*.pdf;*.doc;*.docx;*.txt"),
                ("Images", "*.png;*.jpg;*.jpeg;*.gif"),
                ("Archives", "*.zip;*.rar;*.7z")
            ]
        )
        if files:
            self._upload_files(list(files))

    def download_file(self):
        """Download selected file"""
        if not self.selected_file:
            messagebox.showwarning("No Selection", "Please select a file first")
            return

        dest = filedialog.asksaveasfilename(
            title="Save file",
            initialvalue=Path(self.selected_file['key']).name
        )
        if dest:
            def do_download():
                self._update_status(f"Downloading {self.selected_file['key']}...")
                success = self.client.download_file(self.selected_file['key'], dest)
                if success:
                    self._update_status("Download complete", "success")
                else:
                    self._update_status("Download failed", "error")

            Thread(target=do_download, daemon=True).start()

    def create_folder(self):
        """Create new folder"""
        from tkinter import simpledialog
        name = simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            folder_key = f"{self.current_prefix}/{name}/".replace("//", "/")
            # Create empty folder by uploading empty content
            try:
                self.client.s3_client.put_object(
                    Bucket=self.client.bucket_name,
                    Key=folder_key,
                    Body=b""
                )
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create folder: {e}")

    def delete_file(self):
        """Delete selected file/folder"""
        if not self.selected_file:
            messagebox.showwarning("No Selection", "Please select a file first")
            return

        if messagebox.askyesno("Confirm Delete", f"Delete {self.selected_file['key']}?"):
            success = self.client.delete_file(self.selected_file['key'])
            if success:
                self.refresh()
                self._update_status("Deleted successfully", "success")
            else:
                self._update_status("Delete failed", "error")

    def share_file(self):
        """Generate and copy share URL"""
        if not self.selected_file:
            messagebox.showwarning("No Selection", "Please select a file first")
            return

        from tkinter import simpledialog
        expires = simpledialog.askinteger("Share URL", "Expiration (seconds):", initialvalue=3600, minvalue=60, maxvalue=604800)
        if expires:
            url = self.client.get_signed_url(self.selected_file['key'], expires)
            if url:
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                messagebox.showinfo("Share URL", f"URL copied to clipboard!\n\nValid for {expires}s")
            else:
                messagebox.showerror("Error", "Failed to generate URL")

    def go_home(self):
        """Navigate to root"""
        self.current_prefix = ""
        self.breadcrumb.config(text="/")
        self.refresh()

    # ============================================================
    # INTERNAL METHODS
    # ============================================================

    def _load_folders(self):
        """Load folder tree"""
        # Clear existing
        for item in self.folder_tree.get_children():
            self.folder_tree.delete(item)

        # Load root folders
        folders = self.client.list_folders("")
        for folder in folders:
            self.folder_tree.insert('', 'end', text=folder, values=(folder,))

    def _load_files(self, prefix):
        """Load files for current prefix"""
        # Clear existing
        for item in self.file_list.get_children():
            self.file_list.delete(item)

        files = self.client.list_files(prefix)
        for file in files:
            name = Path(file['key']).name
            size = self._format_size(file['size'])
            modified = file['last_modified'].strftime("%Y-%m-%d %H:%M")

            self.file_list.insert('', 'end', values=(name, size, modified), tags=(file['key'],))

        self._update_info(f"{len(files)} items")

    def _upload_files(self, files):
        """Upload files in background"""
        def do_upload():
            total = len(files)
            for i, file_path in enumerate(files):
                name = Path(file_path).name
                key = f"{self.current_prefix}/{name}".replace("//", "/")

                self._update_status(f"Uploading {name}...")
                self.progress['value'] = (i / total) * 100

                self.client.upload_file(file_path, key)

            self.progress['value'] = 100
            self._update_status(f"Uploaded {total} files", "success")
            self.refresh()

        Thread(target=do_upload, daemon=True).start()

    def _on_drop(self, event):
        """Handle drag-and-drop"""
        files = self.root.tk.splitlist(event.data)
        self._upload_files(files)

    def _on_folder_select(self, event):
        """Handle folder selection"""
        selection = self.folder_tree.selection()
        if selection:
            folder = self.folder_tree.item(selection[0])['values'][0]
            self.current_prefix = folder

    def _on_folder_double(self, event):
        """Handle folder double-click"""
        selection = self.folder_tree.selection()
        if selection:
            folder = self.folder_tree.item(selection[0])['values'][0]
            self.current_prefix = folder
            self.breadcrumb.config(text=f"/{folder}")
            self._load_files(folder)

    def _on_file_select(self, event):
        """Handle file selection"""
        selection = self.file_list.selection()
        if selection:
            item = self.file_list.item(selection[0])
            key = item['tags'][0]
            size = item['values'][1]
            self.selected_file = {'key': key, 'size': size}

    def _on_file_double(self, event):
        """Handle file double-click - download"""
        self.download_file()

    def _sort_by(self, column):
        """Sort by column (placeholder)"""
        pass

    def _update_status(self, text, style="Status"):
        """Update status label"""
        self.status_label.config(text=text, style=f'{style}.TLabel')

    def _update_info(self, text):
        """Update info label"""
        self.info_label.config(text=text)

    def _format_size(self, bytes_size):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f} PB"


def main():
    """Main entry point"""
    root = TkinterDnD.Tk() if 'TkinterDnD' in dir() else tk.Tk()
    app = R2Explorer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
