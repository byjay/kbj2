"""
KBJ2 R2 Cloud Storage Explorer
File Explorer UI for Cloudflare R2 Storage (Korean, Windows Explorer Style)
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
from datetime import datetime
from threading import Thread
import shutil

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from r2_client import R2Client


class R2Explorer:
    """R2 Cloud Storage File Explorer GUI (한글)"""

    # Color Scheme (Light Theme - Windows Style)
    COLORS = {
        'bg': '#ffffff',
        'fg': '#000000',
        'select_bg': '#0078d4',
        'select_fg': '#ffffff',
        'tree_bg': '#ffffff',
        'tree_fg': '#000000',
        'header_bg': '#f3f3f3',
        'header_fg': '#000000',
        'accent': '#0078d4',
        'success': '#107c10',
        'error': '#d13438',
        'border': '#e1e1e1'
    }

    # File icons
    ICONS = {
        'folder': '📁',
        'pdf': '📄',
        'image': '🖼️',
        'video': '🎬',
        'archive': '📦',
        'code': '📝',
        'default': '📄'
    }

    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.root.title("KBJ2 R2 클라우드 탐색기")
        self.root.geometry("1000x600")
        self.root.configure(bg=self.COLORS['bg'])

        # R2 Client
        self.client = None
        self.current_path = ""  # R2 current path
        self.selected_items = []  # Selected items
        self.clipboard = None  # For copy/paste: (key, operation)
        self.history = []  # Navigation history
        self.history_index = -1

        # File cache for display
        self.file_cache = {}

        # Setup UI
        self._setup_styles()
        self._create_widgets()

        # Initialize R2 connection
        self._init_r2()

    def _setup_styles(self):
        """Setup ttk styles (Windows 11 style)"""
        style = ttk.Style()
        style.theme_use('winnative')

        # Configure styles
        style.configure('TFrame', background=self.COLORS['bg'])
        style.configure('TLabel', background=self.COLORS['bg'], foreground=self.COLORS['fg'])
        style.configure('TButton', padding=5)

        style.configure('Header.TLabel', font=('맑은 고딕', 9, 'bold'), foreground=self.COLORS['accent'])
        style.configure('Path.TLabel', font=('Consolas', 9))

        style.configure('Treeview',
                       background=self.COLORS['tree_bg'],
                       foreground=self.COLORS['tree_fg'],
                       fieldbackground=self.COLORS['tree_bg'],
                       borderwidth=1,
                       rowheight=25)
        style.map('Treeview', background=[('selected', self.COLORS['select_bg'])],
                  foreground=[('selected', self.COLORS['select_fg'])])

        style.configure('Treeview.Heading',
                       background=self.COLORS['header_bg'],
                       foreground=self.COLORS['header_fg'],
                       borderwidth=1,
                       relief='flat')
        style.map('Treeview.Heading', background=[('active', self.COLORS['accent'])])

        style.configure('Status.TLabel', font=('맑은 고딕', 9), foreground=self.COLORS['success'])
        style.configure('Error.TLabel', font=('맑은 고딕', 9), foreground=self.COLORS['error'])

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Toolbar (상단 도구 모음)
        self._create_toolbar(main_frame)

        # Address bar (주소 표시줄)
        self._create_address_bar(main_frame)

        # Content Area (파일 목록)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self._create_file_list(content_frame)

        # Status Bar
        self._create_status_bar(main_frame)

        # Context Menu (우클릭 메뉴)
        self._create_context_menu()

    def _create_toolbar(self, parent):
        """Create toolbar (상단 도구 모음)"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill='x', padx=5, pady=5)

        # Navigation buttons
        nav_frame = ttk.Frame(toolbar)
        nav_frame.pack(side='left')

        ttk.Button(nav_frame, text="◀ 뒤로", width=10, command=self.go_back).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="앞으로 ▶", width=10, command=self.go_forward).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="⬆️ 상위", width=10, command=self.go_up).pack(side='left', padx=2)
        ttk.Button(nav_frame, text="🏠 홈", width=10, command=self.go_home).pack(side='left', padx=2)

        # Action buttons
        action_frame = ttk.Frame(toolbar)
        action_frame.pack(side='left', padx=20)

        ttk.Button(action_frame, text="📂 새 폴더", command=self.create_folder).pack(side='left', padx=2)
        ttk.Button(action_frame, text="📤 업로드", command=self.upload_files).pack(side='left', padx=2)
        ttk.Button(action_frame, text="⬇️ 다운로드", command=self.download_file).pack(side='left', padx=2)
        ttk.Button(action_frame, text="🗑️ 삭제", command=self.delete_selected).pack(side='left', padx=2)

        # View buttons
        view_frame = ttk.Frame(toolbar)
        view_frame.pack(side='right')

        ttk.Button(view_frame, text="🔄 새로고침", command=self.refresh).pack(side='left', padx=2)

    def _create_address_bar(self, parent):
        """Create address bar (주소 표시줄)"""
        addr_frame = ttk.Frame(parent)
        addr_frame.pack(fill='x', padx=5, pady=2)

        ttk.Label(addr_frame, text="주소:", style='Header.TLabel').pack(side='left', padx=(0, 5))

        self.address_var = tk.StringVar(value="R2:/")
        address_entry = ttk.Entry(addr_frame, textvariable=self.address_var)
        address_entry.pack(side='left', fill='x', expand=True)
        address_entry.bind('<Return>', lambda e: self.navigate_to_path())

        ttk.Button(addr_frame, text="이동", width=8, command=self.navigate_to_path).pack(side='left', padx=(5, 0))

    def _create_file_list(self, parent):
        """Create file list view (Windows Explorer 스타일)"""
        # 단일 트리뷰: 폴더와 파일 함께 표시
        columns = ('name', 'size', 'type', 'modified')
        self.file_list = ttk.Treeview(parent, columns=columns, show='tree headings', selectmode='extended')

        # 헤더 (한글)
        self.file_list.heading('#0', text='')
        self.file_list.heading('name', text='이름')
        self.file_list.heading('size', text='크기')
        self.file_list.heading('type', text='유형')
        self.file_list.heading('modified', text='수정한 날짜')

        # 컬럼 너비
        self.file_list.column('#0', width=50, stretch=False)
        self.file_list.column('name', width=400, anchor='w')
        self.file_list.column('size', width=100, anchor='e')
        self.file_list.column('type', width=120, anchor='w')
        self.file_list.column('modified', width=180, anchor='w')

        self.file_list.pack(fill='both', expand=True)

        # 이벤트 바인딩
        self.file_list.bind('<<TreeviewSelect>>', self._on_select)
        self.file_list.bind('<Double-1>', self._on_double)
        self.file_list.bind('<Button-3>', self._show_context_menu)  # 우클릭

        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient='vertical', command=self.file_list.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(parent, orient='horizontal', command=self.file_list.xview)
        hsb.pack(side='bottom', fill='x')

        self.file_list.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def _create_status_bar(self, parent):
        """Create status bar (상태 표시줄)"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', padx=5, pady=2)

        self.status_label = ttk.Label(status_frame, text="준비", style='Status.TLabel')
        self.status_label.pack(side='left')

        self.info_label = ttk.Label(status_frame, text="", style='Path.TLabel')
        self.info_label.pack(side='right')

    def _create_context_menu(self):
        """Create right-click context menu (우클릭 메뉴)"""
        self.context_menu = tk.Menu(self.root, tearoff=0)

        self.context_menu.add_command(label="📂 열기", command=self.open_item)
        self.context_menu.add_command(label="⬇️ 다운로드", command=self.download_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 복사", command=self.copy_item)
        self.context_menu.add_command(label="✂️ 잘라내기", command=self.cut_item)
        self.context_menu.add_command(label="📋 붙여넣기", command=self.paste_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✏️ 이름 바꾸기", command=self.rename_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔗 공유 링크", command=self.share_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ 삭제", command=self.delete_selected)

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def _init_r2(self):
        """Initialize R2 client"""
        def init():
            try:
                self.client = R2Client()
                self._update_status("R2 연결됨", "success")
                self.refresh()
            except Exception as e:
                self._update_status(f"연결 실패: {e}", "error")
                messagebox.showerror("연결 오류", f"R2에 연결할 수 없습니다.\n\n환경변수를 설정하세요:\nR2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY")

        Thread(target=init, daemon=True).start()

    # ============================================================
    # NAVIGATION
    # ============================================================

    def go_back(self):
        """뒤로 가기"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            self._load_path(self.current_path, add_history=False)

    def go_forward(self):
        """앞으로 가기"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            self._load_path(self.current_path, add_history=False)

    def go_up(self):
        """상위 폴더로 이동"""
        if self.current_path:
            parent = '/'.join(self.current_path.split('/')[:-1])
            self.current_path = parent
            self._load_path(parent)

    def go_home(self):
        """홈으로 이동"""
        self.current_path = ""
        self._load_path("")

    def navigate_to_path(self):
        """주소창에서 경로 이동"""
        path = self.address_var.get().replace("R2:/", "")
        self.current_path = path
        self._load_path(path)

    # ============================================================
    # FILE OPERATIONS
    # ============================================================

    def refresh(self):
        """새로고침"""
        if not self.client:
            return
        self._load_path(self.current_path, add_history=False)

    def upload_files(self):
        """파일 업로드"""
        files = filedialog.askopenfilenames(
            title="업로드할 파일 선택",
            filetypes=[
                ("모든 파일", "*.*"),
                ("문서", "*.pdf;*.doc;*.docx;*.txt;*.xlsx"),
                ("이미지", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("압축", "*.zip;*.rar;*.7z")
            ]
        )
        if files:
            def do_upload():
                for i, file_path in enumerate(files):
                    name = Path(file_path).name
                    key = f"{self.current_path}/{name}".strip("/") if self.current_path else name

                    self._update_status(f"업로드 중: {name}")
                    if self.client.upload_file(file_path, key):
                        self._update_status(f"업로드 완료: {name}", "success")
                    else:
                        self._update_status(f"업로드 실패: {name}", "error")

                self.refresh()

            Thread(target=do_upload, daemon=True).start()

    def download_file(self):
        """파일 다운로드"""
        selection = self.file_list.selection()
        if not selection:
            messagebox.showwarning("선택 없음", "파일을 먼저 선택하세요")
            return

        items = [self.file_list.item(s) for s in selection]

        if len(items) == 1:
            # 단일 파일 다운로드
            item_data = items[0]['tags'][0] if items[0]['tags'] else None
            if not item_data or item_data.get('is_dir'):
                return

            dest = filedialog.asksaveasfilename(
                title="다운로드",
                initialfile=items[0]['values'][0]
            )
            if dest:
                def do_download():
                    self._update_status(f"다운로드 중: {items[0]['values'][0]}")
                    if self.client.download_file(item_data['key'], dest):
                        self._update_status("다운로드 완료", "success")
                    else:
                        self._update_status("다운로드 실패", "error")

                Thread(target=do_download, daemon=True).start()
        else:
            # 다중 파일 다운로드 - 폴더 선택
            dest_dir = filedialog.askdirectory(title="다운로드 위치")
            if dest_dir:
                def do_download_multi():
                    for item in items:
                        item_data = item['tags'][0] if item['tags'] else None
                        if item_data and not item_data.get('is_dir'):
                            dest = Path(dest_dir) / item['values'][0]
                            self.client.download_file(item_data['key'], str(dest))

                    self._update_status("다운로드 완료", "success")

                Thread(target=do_download_multi, daemon=True).start()

    def create_folder(self):
        """새 폴더 만들기"""
        name = simpledialog.askstring("새 폴더", "폴더 이름:")
        if name:
            folder_key = f"{self.current_path}/{name}/".replace("//", "/") if self.current_path else f"{name}/"

            try:
                self.client.s3_client.put_object(
                    Bucket=self.client.bucket_name,
                    Key=folder_key,
                    Body=b""
                )
                self.refresh()
            except Exception as e:
                messagebox.showerror("오류", f"폴더 생성 실패: {e}")

    def delete_selected(self):
        """선택 항목 삭제"""
        selection = self.file_list.selection()
        if not selection:
            return

        items = [self.file_list.item(s) for s in selection]
        count = len(items)

        if messagebox.askyesno("삭제 확인", f"{count}개 항목을 삭제하시겠습니까?"):
            def do_delete():
                for item in items:
                    item_data = item['tags'][0] if item['tags'] else None
                    if item_data:
                        key = item_data['key']
                        if item_data.get('is_dir'):
                            # 폴더 삭제 - 모든 항목 삭제
                            self.client.delete_prefix(key.rstrip('/') + '/')
                        else:
                            self.client.delete_file(key)

                self.refresh()
                self._update_status(f"{count}개 항목 삭제됨", "success")

            Thread(target=do_delete, daemon=True).start()

    def rename_item(self):
        """이름 바꾸기"""
        selection = self.file_list.selection()
        if not selection or len(selection) > 1:
            return

        item = self.file_list.item(selection[0])
        item_data = item['tags'][0] if item['tags'] else None
        if not item_data:
            return

        old_name = item['values'][0]
        new_name = simpledialog.askstring("이름 바꾸기", "새 이름:", initialvalue=old_name)

        if new_name and new_name != old_name:
            old_key = item_data['key']
            new_key = '/'.join(old_key.split('/')[:-1]) + '/' + new_name

            try:
                # R2는 직접 rename이 없으므로 copy + delete
                self.client.s3_client.copy_object(
                    CopySource={'Bucket': self.client.bucket_name, 'Key': old_key},
                    Bucket=self.client.bucket_name,
                    Key=new_key
                )
                self.client.s3_client.delete_object(Bucket=self.client.bucket_name, Key=old_key)
                self.refresh()
            except Exception as e:
                messagebox.showerror("오류", f"이름 바꾸기 실패: {e}")

    def copy_item(self):
        """복사"""
        selection = self.file_list.selection()
        if selection:
            item = self.file_list.item(selection[0])
            item_data = item['tags'][0] if item['tags'] else None
            if item_data:
                self.clipboard = (item_data, 'copy')
                self._update_status("클립보드에 복사됨")

    def cut_item(self):
        """잘라내기"""
        selection = self.file_list.selection()
        if selection:
            item = self.file_list.item(selection[0])
            item_data = item['tags'][0] if item['tags'] else None
            if item_data:
                self.clipboard = (item_data, 'cut')
                self._update_status("클립보드에 잘라내기됨")

    def paste_item(self):
        """붙여넣기"""
        if not self.clipboard:
            return

        item_data, op = self.clipboard
        old_key = item_data['key']
        name = Path(old_key).name
        new_key = f"{self.current_path}/{name}".replace("//", "/") if self.current_path else name

        try:
            self.client.s3_client.copy_object(
                CopySource={'Bucket': self.client.bucket_name, 'Key': old_key},
                Bucket=self.client.bucket_name,
                Key=new_key
            )

            if op == 'cut':
                self.client.s3_client.delete_object(Bucket=self.client.bucket_name, Key=old_key)
                self.clipboard = None

            self.refresh()
            self._update_status("붙여넣기 완료", "success")
        except Exception as e:
            messagebox.showerror("오류", f"붙여넣기 실패: {e}")

    def open_item(self):
        """항목 열기 (폴더 이동)"""
        selection = self.file_list.selection()
        if selection:
            item = self.file_list.item(selection[0])
            item_data = item['tags'][0] if item['tags'] else None

            if item_data and item_data.get('is_dir'):
                # 폴더 열기
                folder_path = item_data['key'].rstrip('/')
                self.current_path = folder_path
                self._load_path(folder_path)
            else:
                # 파일 다운로드 후 열기
                self.download_file()

    def share_file(self):
        """공유 링크 생성"""
        selection = self.file_list.selection()
        if not selection:
            return

        item = self.file_list.item(selection[0])
        item_data = item['tags'][0] if item['tags'] else None
        if not item_data or item_data.get('is_dir'):
            return

        expires = simpledialog.askinteger("공유 링크", "유효 시간 (초):", initialvalue=3600, minvalue=60, maxvalue=604800)
        if expires:
            url = self.client.get_signed_url(item_data['key'], expires)
            if url:
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                messagebox.showinfo("공유 링크", f"링크가 클립보드에 복사되었습니다!\n\n유효 시간: {expires}초")

    # ============================================================
    # INTERNAL METHODS
    # ============================================================

    def _load_path(self, path, add_history=True):
        """Load path contents"""
        self.current_path = path
        self.address_var.set(f"R2:/{path}" if path else "R2:/")

        if add_history:
            # 히스토리 추가
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            self.history_index = len(self.history) - 1

        def do_load():
            # Clear existing
            for item in self.file_list.get_children():
                self.file_list.delete(item)

            # Load folders and files
            folders = self.client.list_folders(path if path else "")
            files = self.client.list_objects(path if path else "", max_keys=1000)

            # Add parent folder if not root
            if path:
                self.file_list.insert('', 'end', text='..',
                    values=('.. (상위 폴더)', '', '폴더', ''),
                    tags=[{'is_dir': True, 'key': '/'.join(path.split('/')[:-1])}])

            # Add folders first
            for folder in folders:
                name = folder.split('/')[-1] or folder
                self.file_list.insert('', 'end', text=self.ICONS['folder'],
                    values=(name, '', '폴더', ''),
                    tags=[{'is_dir': True, 'key': folder}])

            # Add files
            for file in files:
                name = Path(file['key']).name
                size = self._format_size(file['size'])
                modified = file['last_modified'].strftime("%Y-%m-%d %H:%M")
                file_type = self._get_file_type(name)

                icon = self._get_file_icon(name)

                self.file_list.insert('', 'end', text=icon,
                    values=(name, size, file_type, modified),
                    tags=[{'is_dir': False, 'key': file['key']}])

            total = len(folders) + len(files)
            self._update_info(f"{total}개 항목")

        Thread(target=do_load, daemon=True).start()

    def _get_file_type(self, filename):
        """Get file type description"""
        ext = Path(filename).suffix.lower()
        types = {
            '.pdf': 'PDF 문서',
            '.doc': 'Word 문서',
            '.docx': 'Word 문서',
            '.xls': 'Excel 시트',
            '.xlsx': 'Excel 시트',
            '.txt': '텍스트',
            '.jpg': '이미지',
            '.jpeg': '이미지',
            '.png': '이미지',
            '.gif': '이미지',
            '.bmp': '이미지',
            '.mp4': '비디오',
            '.avi': '비디오',
            '.mkv': '비디오',
            '.mp3': '오디오',
            '.zip': '압축 파일',
            '.rar': '압축 파일',
            '.7z': '압축 파일',
        }
        return types.get(ext, f'{ext[1:].upper()} 파일')

    def _get_file_icon(self, filename):
        """Get file icon emoji"""
        ext = Path(filename).suffix.lower()
        if ext in ['.pdf']:
            return self.ICONS['pdf']
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return self.ICONS['image']
        elif ext in ['.mp4', '.avi', '.mkv']:
            return self.ICONS['video']
        elif ext in ['.zip', '.rar', '.7z']:
            return self.ICONS['archive']
        elif ext in ['.py', '.js', '.html', '.css']:
            return self.ICONS['code']
        return self.ICONS['default']

    def _on_select(self, event):
        """Handle selection"""
        selection = self.file_list.selection()
        self.selected_items = selection

    def _on_double(self, event):
        """Handle double-click"""
        self.open_item()

    def _show_context_menu(self, event):
        """Show context menu"""
        item = self.file_list.identify_row(event.y)
        if item:
            self.file_list.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _update_status(self, text, style="Status"):
        """Update status label"""
        self.status_label.config(text=text, style=f'{style}.TLabel')

    def _update_info(self, text):
        """Update info label"""
        self.info_label.config(text=text)

    def _format_size(self, bytes_size):
        """Format bytes to human readable (한글)"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f} PB"


def main():
    """Main entry point"""
    try:
        root = TkinterDnD.Tk()
    except:
        root = tk.Tk()

    app = R2Explorer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
