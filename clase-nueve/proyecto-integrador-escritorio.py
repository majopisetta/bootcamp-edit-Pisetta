import tkinter as tk
from tkinter import ttk, messagebox

# ─── Base de datos en memoria ───────────────────────────────────────────────
db = [
    {
        "id": 1,
        "nombre": "Maria Jose",
        "apellido": "Pisetta",
        "cantidad_cursos": 3,
    }
]


def siguiente_id():
    return max(a["id"] for a in db) + 1 if db else 1


# ─── Paleta y estilos ───────────────────────────────────────────────────────
BG        = "#1e1e2e"
BG_CARD   = "#2a2a3d"
FG        = "#cdd6f4"
ACCENT    = "#89b4fa"
ACCENT_HV = "#74c7ec"
RED       = "#f38ba8"
GREEN     = "#a6e3a1"
BORDER    = "#45475a"
ENTRY_BG  = "#313244"
FONT      = ("Segoe UI", 11)
FONT_H1   = ("Segoe UI Semibold", 18)
FONT_H2   = ("Segoe UI Semibold", 13)
FONT_SM   = ("Segoe UI", 10)


# ─── Aplicación principal ───────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Alumnos")
        self.geometry("820x560")
        self.configure(bg=BG)
        self.minsize(720, 480)

        self._build_header()
        self._build_body()
        self._build_form()
        self._refrescar_tabla()

    # ── Encabezado ──────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG, pady=14, padx=20)
        hdr.pack(fill="x")

        tk.Label(
            hdr, text="📚  Sistema de Gestión de Alumnos",
            font=FONT_H1, bg=BG, fg=ACCENT,
        ).pack(side="left")

    # ── Cuerpo: tabla + botones ─────────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self, bg=BG, padx=20)
        body.pack(fill="both", expand=True)

        # Tabla (Treeview)
        cols = ("id", "nombre", "apellido", "cursos")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_CARD, foreground=FG,
                        fieldbackground=BG_CARD, font=FONT,
                        rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading",
                        background=BORDER, foreground=FG,
                        font=FONT_H2, borderwidth=0)
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", BG)])

        tree_frame = tk.Frame(body, bg=BORDER, bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_frame, columns=cols, show="headings", selectmode="browse"
        )
        for c, w, txt in [
            ("id", 60, "ID"),
            ("nombre", 200, "Nombre"),
            ("apellido", 200, "Apellido"),
            ("cursos", 120, "Cursos"),
        ]:
            self.tree.heading(c, text=txt, anchor="w")
            self.tree.column(c, width=w, anchor="w")

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Barra de botones
        btn_bar = tk.Frame(body, bg=BG, pady=12)
        btn_bar.pack(fill="x")

        self.btn_mod = self._make_btn(btn_bar, "✏️  Modificar", ACCENT, self._abrir_modificar)
        self.btn_del = self._make_btn(btn_bar, "🗑️  Eliminar", RED, self._eliminar)
        self.btn_mod.pack(side="right", padx=(6, 0))
        self.btn_del.pack(side="right", padx=(6, 0))

    # ── Formulario inferior: agregar alumno ─────────────────────────────────
    def _build_form(self):
        card = tk.Frame(self, bg=BG_CARD, padx=16, pady=12)
        card.pack(fill="x", padx=20, pady=(0, 16))

        tk.Label(card, text="Agregar alumno", font=FONT_H2, bg=BG_CARD, fg=GREEN
                 ).grid(row=0, column=0, columnspan=7, sticky="w", pady=(0, 8))

        self.entries: dict[str, tk.Entry] = {}
        for i, (key, label, w) in enumerate([
            ("nombre", "Nombre", 18),
            ("apellido", "Apellido", 18),
            ("cursos", "Cursos", 8),
        ]):
            tk.Label(card, text=label, font=FONT_SM, bg=BG_CARD, fg=FG
                     ).grid(row=1, column=i * 2, sticky="w", padx=(0, 4))
            e = tk.Entry(card, width=w, font=FONT, bg=ENTRY_BG, fg=FG,
                         insertbackground=FG, relief="flat", bd=4)
            e.grid(row=1, column=i * 2 + 1, padx=(0, 12))
            self.entries[key] = e

        self._make_btn(card, "＋  Agregar", GREEN, self._agregar, fg_text=BG
                       ).grid(row=1, column=6, padx=(4, 0))

    # ── Helpers de UI ───────────────────────────────────────────────────────
    def _make_btn(self, parent, text, color, cmd, fg_text=None):
        b = tk.Button(
            parent, text=text, font=FONT_SM, bg=color,
            fg=fg_text or BG, activebackground=ACCENT_HV,
            activeforeground=BG, relief="flat", bd=0,
            padx=14, pady=6, cursor="hand2", command=cmd,
        )
        return b

    def _refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in db:
            self.tree.insert("", "end", iid=a["id"],
                             values=(a["id"], a["nombre"], a["apellido"], a["cantidad_cursos"]))

    def _on_select(self, _event):
        pass  # se podría usar para habilitar/deshabilitar botones

    def _alumno_seleccionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Seleccioná un alumno de la tabla.")
            return None
        aid = int(sel[0])
        return next((a for a in db if a["id"] == aid), None)

    # ── CRUD ────────────────────────────────────────────────────────────────
    def _agregar(self):
        nombre = self.entries["nombre"].get().strip()
        apellido = self.entries["apellido"].get().strip()
        cursos_txt = self.entries["cursos"].get().strip()

        if not nombre or not apellido:
            messagebox.showwarning("Campos vacíos", "Nombre y apellido son obligatorios.")
            return
        try:
            cursos = int(cursos_txt)
        except ValueError:
            messagebox.showwarning("Valor inválido", "La cantidad de cursos debe ser un número entero.")
            return

        nuevo = {
            "id": siguiente_id(),
            "nombre": nombre,
            "apellido": apellido,
            "cantidad_cursos": cursos,
        }
        db.append(nuevo)
        self._refrescar_tabla()

        for e in self.entries.values():
            e.delete(0, "end")
        self.entries["nombre"].focus_set()

    def _eliminar(self):
        alumno = self._alumno_seleccionado()
        if not alumno:
            return
        ok = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar a {alumno['nombre']} {alumno['apellido']}?"
        )
        if ok:
            db.remove(alumno)
            self._refrescar_tabla()

    def _abrir_modificar(self):
        alumno = self._alumno_seleccionado()
        if not alumno:
            return
        EditDialog(self, alumno)

    def refrescar(self):
        self._refrescar_tabla()


# ─── Diálogo de edición ────────────────────────────────────────────────────
class EditDialog(tk.Toplevel):
    def __init__(self, parent: App, alumno: dict):
        super().__init__(parent)
        self.parent = parent
        self.alumno = alumno
        self.title(f"Modificar alumno #{alumno['id']}")
        self.configure(bg=BG_CARD)
        self.geometry("380x240")
        self.resizable(False, False)
        self.grab_set()

        pad = {"padx": 12, "pady": 6}
        self.entries: dict[str, tk.Entry] = {}

        for i, (key, label, val) in enumerate([
            ("nombre", "Nombre", alumno["nombre"]),
            ("apellido", "Apellido", alumno["apellido"]),
            ("cursos", "Cursos", str(alumno["cantidad_cursos"])),
        ]):
            tk.Label(self, text=label, font=FONT_SM, bg=BG_CARD, fg=FG
                     ).grid(row=i, column=0, sticky="e", **pad)
            e = tk.Entry(self, width=24, font=FONT, bg=ENTRY_BG, fg=FG,
                         insertbackground=FG, relief="flat", bd=4)
            e.insert(0, val)
            e.grid(row=i, column=1, **pad)
            self.entries[key] = e

        btn_frame = tk.Frame(self, bg=BG_CARD)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=14)

        tk.Button(btn_frame, text="Cancelar", font=FONT_SM, bg=BORDER, fg=FG,
                  relief="flat", padx=14, pady=6, command=self.destroy
                  ).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Guardar", font=FONT_SM, bg=ACCENT, fg=BG,
                  relief="flat", padx=14, pady=6, command=self._guardar
                  ).pack(side="left", padx=6)

    def _guardar(self):
        nombre = self.entries["nombre"].get().strip()
        apellido = self.entries["apellido"].get().strip()
        cursos_txt = self.entries["cursos"].get().strip()

        if not nombre or not apellido:
            messagebox.showwarning("Campos vacíos", "Nombre y apellido son obligatorios.")
            return
        try:
            cursos = int(cursos_txt)
        except ValueError:
            messagebox.showwarning("Valor inválido", "La cantidad de cursos debe ser un número entero.")
            return

        self.alumno["nombre"] = nombre
        self.alumno["apellido"] = apellido
        self.alumno["cantidad_cursos"] = cursos
        self.parent.refrescar()
        self.destroy()


# ─── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    App().mainloop()