"""
KBJ2 R2 Storage Dashboard
R2 스토리지 정보, 용량, 사용량을 보여주는 대시보드
"""
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from r2_client import R2Client


class R2Dashboard:
    """R2 Storage Dashboard"""

    COLORS = {
        'bg': '#1e1e1e',
        'fg': '#e0e0e0',
        'card_bg': '#252526',
        'accent': '#007acc',
        'success': '#4ec9b0',
        'warning': '#f0ad4e',
        'error': '#f48771'
    }

    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.root.title("KBJ2 R2 스토리지 대시보드")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.COLORS['bg'])

        # R2 Client
        self.client = None
        self.storage_info = {}

        # Setup UI
        self._setup_styles()
        self._create_widgets()

        # Initialize
        self._init_r2()

    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=self.COLORS['bg'])
        style.configure('TLabel', background=self.COLORS['bg'], foreground=self.COLORS['fg'])
        style.configure('Card.TFrame', background=self.COLORS['card_bg'], relief='flat')
        style.configure('Status.TLabel', font=('맑은 고딕', 10), foreground=self.COLORS['success'])
        style.configure('Warning.TLabel', font=('맑은 고딕', 10), foreground=self.COLORS['warning'])
        style.configure('Error.TLabel', font=('맑은 고딕', 10), foreground=self.COLORS['error'])
        style.configure('Header.TLabel', font=('맑은 고딕', 12, 'bold'), foreground=self.COLORS['accent'])

        # Progress bar
        style.configure('Horizontal.TProgressbar',
                       background=self.COLORS['accent'],
                       troughcolor=self.COLORS['card_bg'],
                       thickness=10)

    def _create_widgets(self):
        """Create all widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        self._create_header(main_frame)

        # Stats Cards
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill='x', pady=(0, 20))
        self._create_stats_cards(stats_frame)

        # Storage Usage
        usage_frame = ttk.LabelFrame(main_frame, text="스토리지 사용량", padding=15)
        usage_frame.pack(fill='both', expand=True, pady=(0, 20))
        self._create_usage_panel(usage_frame)

        # Recent Files
        files_frame = ttk.LabelFrame(main_frame, text="최근 파일", padding=15)
        files_frame.pack(fill='both', expand=True, pady=(0, 20))
        self._create_files_panel(files_frame)

        # Status Bar
        self._create_status_bar(main_frame)

        # Refresh Button
        refresh_btn = ttk.Button(main_frame, text="🔄 새로고침", command=self.refresh_all)
        refresh_btn.pack(pady=10)

    def _create_header(self, parent):
        """Create header"""
        header = ttk.Frame(parent)
        header.pack(fill='x', pady=(0, 20))

        title = ttk.Label(header, text="KBJ2 R2 클라우드 스토리지", style='Header.TLabel')
        title.pack(side='left')

        self.connection_label = ttk.Label(header, text="연결 안됨", style='Warning.TLabel')
        self.connection_label.pack(side='right')

    def _create_stats_cards(self, parent):
        """Create statistics cards"""
        # Cards container
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill='x')

        # Define cards
        cards = [
            ("📁 총 파일", "total_files", "0개"),
            ("📊 총 용량", "total_size", "0 KB"),
            ("📤 업로드", "uploads", "0회"),
            ("⬇️ 다운로드", "downloads", "0회")
        ]

        for i, (title, key, default) in enumerate(cards):
            card = ttk.Frame(cards_frame, style='Card.TFrame', padding=15)
            card.pack(side='left', expand=True, fill='both', padx=5)

            ttk.Label(card, text=title, font=('맑은 고딕', 10)).pack(anchor='w')
            ttk.Label(card, text=default, style='Status.TLabel', font=('맑은 고딕', 14, 'bold')).pack(anchor='e')

            setattr(self, f"stat_{key}", card.children['!frame'])

    def _create_usage_panel(self, parent):
        """Create storage usage panel"""
        # Progress bars
        self.size_bar = self.create_progress_bar(parent, "스토리지 용량", 0, 100)
        self.size_bar.pack(fill='x', pady=5)

        self.count_bar = self_progress_bar(parent, "파일 개수", 0, 10000)
        self.count_bar.pack(fill='x', pady=5)

        # Info labels
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill='x', pady=10)

        ttk.Label(info_frame, text="무료 계정: 10GB", style='Status.TLabel').pack(side='left')
        ttk.Label(info_frame, text="유료 계정: 무제한", style='Status.TLabel').pack(side='right')

    def _create_files_panel(self, parent):
        """Create recent files panel"""
        # Treeview
        columns = ('name', 'size', 'date')
        self.files_tree = ttk.Treeview(parent, columns=columns, show='headings', selectmode='browse')

        self.files_tree.heading('name', text='파일 이름')
        self.files_tree.heading('size', text='크기')
        self.files_tree.heading('date', text='업로드 날짜')

        self.files_tree.column('name', width=400, anchor='w')
        self.files_tree.column('size', width=150, anchor='e')
        self.files_tree.column('date', width=200, anchor='w')

        self.files_tree.pack(fill='both', expand=True)

        # Scrollbar
        vsb = ttk.Scrollbar(parent, orient='vertical', command=self.files_tree.yview)
        vsb.pack(side='right', fill='y')
        self.files_tree.configure(yscrollcommand=vsb.set)

    def _create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', pady=(10, 0))

        self.status_label = ttk.Label(status_frame, text="준비", style='Status.TLabel')
        self.status_label.pack(side='left')

        self.account_label = ttk.Label(status_frame, text="R2 계정: 연결 안됨", style='Warning.TLabel')
        self.account_label.pack(side='right')

    def create_progress_bar(self, parent, label_text, value, max_value):
        """Helper to create progress bar"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x')

        ttk.Label(frame, text=label_text).pack(side='left')

        progress = ttk.Progressbar(frame, style='Horizontal.TProgressbar',
                                    mode='determinate', maximum=max_value, value=value)
        progress.pack(side='left', fill='x', expand=True, padx=(10, 0))

        value_label = ttk.Label(frame, text=f"{value:,}")
        value_label.pack(side='right')

        return progress, value_label, frame

    def _init_r2(self):
        """Initialize R2 connection"""
        try:
            self.client = R2Client()
            self._update_status("R2 연결됨", "success")
            self.connection_label.configure(text="✅ 연결됨", style='Status.TLabel')
            self.account_label.configure(text=f"버킷: {self.client.bucket_name}", style='Status.TLabel')
            self.refresh_all()
        except Exception as e:
            self._update_status(f"연결 실패: {e}", "error")
            self.connection_label.configure(text="❌ 연결 실패", style='Error.TLabel')

    def refresh_all(self):
        """Refresh all data"""
        if not self.client:
            messagebox.showwarning("연결 오류", "R2에 연결되지 않았습니다")
            return

        def do_refresh():
            try:
                # Get storage info
                buckets = self.client.s3_client.list_buckets()
                total_size = 0
                file_count = 0

                # Clear files list
                for item in self.files_tree.get_children():
                    self.files_tree.delete(item)

                # List files (limit 100)
                for obj in self.client.list_files("", max_keys=100):
                    file_count += 1
                    total_size += obj['size']

                    name = Path(obj['key']).name
                    size = self._format_size(obj['size'])
                    date = obj['last_modified'].strftime("%Y-%m-%d %H:%M")

                    self.files_tree.insert('', 'end', values=(name, size, date))

                # Update stats
                self._update_stat_card("total_files", f"{file_count:,}개")
                self._update_stat_card("total_size", self._format_size(total_size))

                # Update progress bars
                # Assume 10GB limit for free tier
                gb_limit = 10 * 1024 * 1024 * 1024
                size_percent = min((total_size / gb_limit) * 100, 100)
                count_percent = min((file_count / 10000) * 100, 100)

                self.size_bar['value'] = size_percent
                self.count_bar['value'] = count_percent

                self._update_status(f"새로고침 완료: {file_count}개 파일", "success")

            except Exception as e:
                self._update_status(f"새로고침 실패: {e}", "error")

        import threading
        threading.Thread(target=do_refresh, daemon=True).start()

    def _update_stat_card(self, key, value):
        """Update stat card value"""
        card = getattr(self, f"stat_{key}")
        for widget in card.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(text=value)

    def _update_status(self, text, style="Status"):
        """Update status label"""
        self.status_label.configure(text=text, style=f'{style}.TLabel')

    def _format_size(self, bytes_size):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f} PB"


def main():
    root = tk.Tk()
    app = R2Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
