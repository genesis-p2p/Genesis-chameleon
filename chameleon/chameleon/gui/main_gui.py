import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
from chameleon.engines.embedding.lsb_embedder import LSBEmbedder
from chameleon.engines.extraction.lsb_extractor import LSBExtractor

# ================== THEME ==================
BG = "#0b0f14"
PANEL = "#111820"
GREEN = "#00ff9c"
CYAN = "#00bcd4"
HOVER_BG = "#00bcd4"
HOVER_FG = "#0b0f14"
SELECT_BG = "#1de9b6"
SELECT_FG = "#0b0f14"
NORMAL_BG = BG
NORMAL_FG = CYAN
ENTRY_BG = "#0f1720"
FONT = ("Consolas", 10)
TITLE_FONT = ("Consolas", 16, "bold")

# ================== MATRIX RAIN ==================
class MatrixRain(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg=BG, highlightthickness=0)
        self.columns = []
        self.after(100, self.animate)

    def resize(self, w, h):
        self.config(width=w, height=h)
        self.columns = [(x, random.randint(-h, 0)) for x in range(0, w, 20)]

    def animate(self):
        self.delete("rain")
        h = self.winfo_height()
        for i, (x, y) in enumerate(self.columns):
            self.create_text(
                x, y,
                text=random.choice("01"),
                fill=GREEN,
                font=("Consolas", 11),
                tags="rain"
            )
            y += 20
            if y > h:
                y = random.randint(-200, 0)
            self.columns[i] = (x, y)
        self.after(80, self.animate)

# ================== CYBER BUTTON ==================
class CyberButton(tk.Label):
    def __init__(self, parent, text, command):
        super().__init__(
            parent, text=text,
            bg=NORMAL_BG, fg=NORMAL_FG,
            font=FONT, padx=20, pady=8,
            relief="ridge", borderwidth=2,
            cursor="hand2"
        )
        self.command = command
        self.selected = False

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_hover(self, _):
        if not self.selected:
            self.config(bg=HOVER_BG, fg=HOVER_FG)

    def on_leave(self, _):
        if not self.selected:
            self.config(bg=NORMAL_BG, fg=NORMAL_FG)

    def on_click(self, _):
        self.command()

    def select(self):
        self.selected = True
        self.config(bg=SELECT_BG, fg=SELECT_FG)

    def deselect(self):
        self.selected = False
        self.config(bg=NORMAL_BG, fg=NORMAL_FG)

# ================== MAIN GUI ==================
class ChameleonGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CHAMELEON :: Cyber Steganography Platform")
        self.root.geometry("900x540")
        self.root.configure(bg=BG)
        self.root.minsize(800, 480)

        # Matrix background
        self.matrix = MatrixRain(self.root)
        self.matrix.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.on_resize)

        # Main container
        self.main = tk.Frame(self.root, bg=BG)
        self.main.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(
            self.main, text="PROJECT CHAMELEON",
            bg=BG, fg=CYAN, font=TITLE_FONT
        ).pack(pady=10)

        # Mode buttons
        self.mode_frame = tk.Frame(self.main, bg=BG)
        self.mode_frame.pack()

        self.embed_btn = CyberButton(self.mode_frame, "[ EMBED MODE ]", self.show_embed_ui)
        self.extract_btn = CyberButton(self.mode_frame, "[ EXTRACT MODE ]", self.show_extract_ui)
        self.embed_btn.pack(side="left", padx=15)
        self.extract_btn.pack(side="left", padx=15)

        # Panel
        self.panel = tk.Frame(self.main, bg=PANEL, padx=30, pady=30)
        self.panel.pack(pady=20, fill="x")

        # Progress bar
        self.progress = ttk.Progressbar(self.main, mode="indeterminate", length=420)
        self.progress.pack(pady=8)

        # Status
        self.status = tk.StringVar(value="[ SYSTEM READY ]")
        tk.Label(
            self.main, textvariable=self.status,
            bg=BG, fg=GREEN, font=("Consolas", 9)
        ).pack(anchor="w")

        self.show_embed_ui()
        self.root.mainloop()

    # ---------- HELPERS ----------
    def activate_mode(self, btn):
        for b in (self.embed_btn, self.extract_btn):
            b.deselect()
        btn.select()

    def clear_panel(self):
        for w in self.panel.winfo_children():
            w.destroy()

    def entry(self, var):
        e = tk.Entry(
            self.panel, textvariable=var,
            bg=ENTRY_BG, fg=GREEN,
            insertbackground=GREEN,
            relief="flat", font=FONT
        )
        e.pack(fill="x", pady=6)
        return e

    def log(self, msg):
        self.status.set(f"[ {msg} ]")
        self.root.after(2500, lambda: self.status.set("[ SYSTEM READY ]"))

    # ---------- EMBED ----------
    def show_embed_ui(self):
        self.activate_mode(self.embed_btn)
        self.clear_panel()

        self.cover_path_var = tk.StringVar()
        self.payload_path_var = tk.StringVar()

        tk.Label(self.panel, text="Cover Image (.png)", bg=PANEL, fg=GREEN).pack(anchor="w")
        self.entry(self.cover_path_var)
        CyberButton(self.panel, "Browse Cover", self.browse_cover).pack(anchor="w", pady=6)

        tk.Label(self.panel, text="Payload File", bg=PANEL, fg=GREEN).pack(anchor="w")
        self.entry(self.payload_path_var)
        CyberButton(self.panel, "Browse Payload", self.browse_payload).pack(anchor="w", pady=6)

        CyberButton(self.panel, ">>> EXECUTE EMBED <<<", self.hide_payload).pack(anchor="w", pady=12)

    # ---------- EXTRACT ----------
    def show_extract_ui(self):
        self.activate_mode(self.extract_btn)
        self.clear_panel()

        self.stego_path_var = tk.StringVar()

        tk.Label(self.panel, text="Stego Image (.png)", bg=PANEL, fg=GREEN).pack(anchor="w")
        self.entry(self.stego_path_var)
        CyberButton(self.panel, "Browse Stego", self.browse_stego).pack(anchor="w", pady=6)

        CyberButton(self.panel, ">>> EXECUTE EXTRACT <<<", self.extract_payload).pack(anchor="w", pady=12)

    # ---------- FILE ----------
    def browse_cover(self):
        p = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if p:
            self.cover_path_var.set(p)
            self.log("Cover loaded")

    def browse_payload(self):
        p = filedialog.askopenfilename()
        if p:
            self.payload_path_var.set(p)
            self.log("Payload selected")

    def browse_stego(self):
        p = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if p:
            self.stego_path_var.set(p)
            self.log("Stego loaded")

    # ---------- CORE (UNCHANGED) ----------
    def hide_payload(self):
        self.progress.start(10)
        cover = self.cover_path_var.get()
        payload = self.payload_path_var.get()
        if not cover or not payload:
            messagebox.showerror("Error", "Missing inputs")
            self.progress.stop()
            return
        out = filedialog.asksaveasfilename(defaultextension=".png")
        if not out:
            self.progress.stop()
            return
        with open(payload, "rb") as f:
            data = f.read()
        try:
            self.log("Embedding payload...")
            LSBEmbedder.hide(cover, data, out)
            messagebox.showinfo("Success", "Payload embedded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.progress.stop()

    def extract_payload(self):
        self.progress.start(10)
        stego = self.stego_path_var.get()
        if not stego:
            messagebox.showerror("Error", "No stego image selected")
            self.progress.stop()
            return
        out = filedialog.asksaveasfilename()
        if not out:
            self.progress.stop()
            return
        try:
            self.log("Extracting payload...")
            data = LSBExtractor.extract(stego)
            with open(out, "wb") as f:
                f.write(data)
            messagebox.showinfo("Success", "Payload extracted successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.progress.stop()

    def on_resize(self, e):
        self.matrix.resize(e.width, e.height)

# ================== RUN ==================
if __name__ == "__main__":
    ChameleonGUI()
