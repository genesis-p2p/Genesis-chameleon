import tkinter as tk
from tkinter import filedialog, messagebox
from chameleon.engines.embedding.lsb_embedder import LSBEmbedder
from chameleon.engines.extraction.lsb_extractor import LSBExtractor

class ChameleonGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Chameleon - Phase 1")
        self.root.geometry("500x250")

        # Menu
        menubar = tk.Menu(self.root)
        action_menu = tk.Menu(menubar, tearoff=0)
        action_menu.add_command(label="Embed Payload", command=self.show_embed_ui)
        action_menu.add_command(label="Extract Payload", command=self.show_extract_ui)
        menubar.add_cascade(label="Action", menu=action_menu)
        self.root.config(menu=menubar)

        # Frame for dynamic UI
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Initialize UI with Embed by default
        self.show_embed_ui()

        self.root.mainloop()

    # --- Embed UI ---
    def show_embed_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Cover Image:").pack()
        self.cover_path_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.cover_path_var, width=60).pack()
        tk.Button(self.frame, text="Browse", command=self.browse_cover).pack()

        tk.Label(self.frame, text="Payload File:").pack()
        self.payload_path_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.payload_path_var, width=60).pack()
        tk.Button(self.frame, text="Browse", command=self.browse_payload).pack()

        tk.Button(self.frame, text="Embed Payload", command=self.hide_payload).pack(pady=10)

    # --- Extract UI ---
    def show_extract_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Select Stego Image:").pack()
        self.stego_path_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.stego_path_var, width=60).pack()
        tk.Button(self.frame, text="Browse", command=self.browse_stego).pack()
        tk.Button(self.frame, text="Extract Payload", command=self.extract_payload).pack(pady=10)

    # --- Utility ---
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    # --- Browse functions ---
    def browse_cover(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            self.cover_path_var.set(path)

    def browse_payload(self):
        path = filedialog.askopenfilename()
        if path:
            self.payload_path_var.set(path)

    def browse_stego(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            self.stego_path_var.set(path)

    # --- Hide / Extract functions ---
    def hide_payload(self):
        cover = self.cover_path_var.get()
        payload = self.payload_path_var.get()
        if not cover or not payload:
            messagebox.showerror("Error", "Please select cover image and payload file")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if not output_path:
            return
        with open(payload, "rb") as f:
            data = f.read()
        try:
            LSBEmbedder.hide(cover, data, output_path)
            messagebox.showinfo("Success", f"Payload hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_payload(self):
        stego = self.stego_path_var.get()
        if not stego:
            messagebox.showerror("Error", "Please select stego image")
            return
        output_path = filedialog.asksaveasfilename()
        if not output_path:
            return
        try:
            data = LSBExtractor.extract(stego)
            with open(output_path, "wb") as f:
                f.write(data)
            messagebox.showinfo("Success", f"Payload extracted to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    ChameleonGUI()
