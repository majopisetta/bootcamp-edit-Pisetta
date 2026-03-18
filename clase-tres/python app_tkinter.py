import tkinter as tk
from tkinter import messagebox, ttk


# ── Colores y fuentes ──────────────────────────────────────────────────────────
BG        = "#1e1e2e"
SIDEBAR   = "#181825"
ACCENT    = "#cba6f7"
TEXT      = "#cdd6f4"
SUBTEXT   = "#a6adc8"
SURFACE   = "#313244"
GREEN     = "#a6e3a1"
RED       = "#f38ba8"
FONT_H    = ("Helvetica", 13, "bold")
FONT_N    = ("Helvetica", 11)
FONT_S    = ("Helvetica", 9)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mi App Tkinter")
        self.geometry("750x500")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._build_sidebar()
        self._build_main()
        self._show_frame("inicio")

    # ── Sidebar ────────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=180)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="✦ Mi App", bg=SIDEBAR,
                 fg=ACCENT, font=("Helvetica", 15, "bold"),
                 pady=24).pack()

        self.nav_buttons = {}
        pages = [("🏠  Inicio", "inicio"),
                 ("📋  Formulario", "formulario"),
                 ("📊  Tabla", "tabla"),
                 ("ℹ️  Acerca de", "acerca")]

        for label, key in pages:
            btn = tk.Button(
                self.sidebar, text=label, anchor="w",
                bg=SIDEBAR, fg=TEXT, font=FONT_N,
                bd=0, padx=20, pady=10, cursor="hand2",
                activebackground=SURFACE, activeforeground=ACCENT,
                command=lambda k=key: self._show_frame(k)
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

    def _show_frame(self, key):
        # Resaltar botón activo
        for k, btn in self.nav_buttons.items():
            btn.configure(bg=SURFACE if k == key else SIDEBAR,
                          fg=ACCENT  if k == key else TEXT)
        self.frames[key].tkraise()

    # ── Área principal ─────────────────────────────────────────────────────────
    def _build_main(self):
        container = tk.Frame(self, bg=BG)
        container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for FrameClass, key in [
            (InicioFrame,     "inicio"),
            (FormularioFrame, "formulario"),
            (TablaFrame,      "tabla"),
            (AcercaFrame,     "acerca"),
        ]:
            frame = FrameClass(container, self)
            frame.place(relwidth=1, relheight=1)
            self.frames[key] = frame


# ── Pantalla: Inicio ───────────────────────────────────────────────────────────
class InicioFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        tk.Label(self, text="Bienvenido 👋", bg=BG, fg=ACCENT,
                 font=("Helvetica", 22, "bold")).pack(pady=(60, 8))
        tk.Label(self, text="Esta es una app de ejemplo con Tkinter.",
                 bg=BG, fg=TEXT, font=FONT_N).pack()
        tk.Label(self, text="Explorá las secciones desde el menú lateral.",
                 bg=BG, fg=SUBTEXT, font=FONT_S).pack(pady=4)

        tk.Button(self, text="Ir al Formulario →",
                  bg=ACCENT, fg=BG, font=FONT_H, bd=0,
                  padx=20, pady=10, cursor="hand2",
                  command=lambda: controller._show_frame("formulario")
                  ).pack(pady=30)


# ── Pantalla: Formulario ───────────────────────────────────────────────────────
class FormularioFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        tk.Label(self, text="📋 Formulario", bg=BG, fg=ACCENT,
                 font=("Helvetica", 16, "bold")).pack(pady=(40, 20))

        form = tk.Frame(self, bg=BG)
        form.pack()

        # Campos
        self.entries = {}
        fields = [("Nombre", "nombre"), ("Email", "email"), ("Edad", "edad")]
        for label, key in fields:
            tk.Label(form, text=label, bg=BG, fg=SUBTEXT,
                     font=FONT_S, anchor="w").grid(
                row=fields.index((label, key))*2,
                column=0, sticky="w", pady=(10, 2))

            entry = tk.Entry(form, bg=SURFACE, fg=TEXT,
                             insertbackground=TEXT, font=FONT_N,
                             bd=0, width=28, relief="flat")
            entry.grid(row=fields.index((label, key))*2+1,
                       column=0, ipady=8, padx=4)
            self.entries[key] = entry

        tk.Button(self, text="Enviar", bg=ACCENT, fg=BG,
                  font=FONT_H, bd=0, padx=20, pady=8,
                  cursor="hand2", command=self._enviar).pack(pady=20)

    def _enviar(self):
        nombre = self.entries["nombre"].get().strip()
        email  = self.entries["email"].get().strip()
        edad   = self.entries["edad"].get().strip()

        if not nombre or not email or not edad:
            messagebox.showwarning("Campos vacíos", "Por favor completá todos los campos.")
            return
        messagebox.showinfo("¡Enviado!",
                            f"Hola {nombre}!\nEmail: {email}\nEdad: {edad}")


# ── Pantalla: Tabla ────────────────────────────────────────────────────────────
class TablaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        tk.Label(self, text="📊 Tabla de datos", bg=BG, fg=ACCENT,
                 font=("Helvetica", 16, "bold")).pack(pady=(40, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=SURFACE, foreground=TEXT,
                        fieldbackground=SURFACE, rowheight=28,
                        font=FONT_N)
        style.configure("Treeview.Heading",
                        background=SIDEBAR, foreground=ACCENT,
                        font=FONT_H)
        style.map("Treeview", background=[("selected", ACCENT)],
                  foreground=[("selected", BG)])

        cols = ("Nombre", "Email", "Rol")
        tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor="center")

        datos = [
            ("Ana García",    "ana@mail.com",    "Admin"),
            ("Luis López",    "luis@mail.com",   "Editor"),
            ("María Torres",  "maria@mail.com",  "Viewer"),
            ("Carlos Ruiz",   "carlos@mail.com", "Editor"),
            ("Sofía Medina",  "sofia@mail.com",  "Admin"),
        ]
        for fila in datos:
            tree.insert("", "end", values=fila)

        tree.pack(padx=20)


# ── Pantalla: Acerca de ────────────────────────────────────────────────────────
class AcercaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        tk.Label(self, text="ℹ️ Acerca de", bg=BG, fg=ACCENT,
                 font=("Helvetica", 16, "bold")).pack(pady=(60, 16))

        info = [
            ("Versión",    "1.0.0"),
            ("Librería",   "Tkinter (Python built-in)"),
            ("Autor",      "Tu nombre"),
            ("Lenguaje",   "Python 3"),
        ]
        for key, val in info:
            row = tk.Frame(self, bg=SURFACE, padx=20, pady=10)
            row.pack(fill="x", padx=60, pady=4)
            tk.Label(row, text=key, bg=SURFACE, fg=SUBTEXT,
                     font=FONT_S, width=12, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg=SURFACE, fg=TEXT,
                     font=FONT_N).pack(side="left")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
    