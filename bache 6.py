import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


CATEGORIAS = [
    "Huecos en vía",
    "Alumbrado público",
    "Basuras",
    "Señalización",
    "Espacios públicos",
    "Alcantarillado"
]


class Usuario:
    def __init__(self, nombre: str, correo: str):
        self._nombre = nombre
        self._correo = correo

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo


class Ciudadano(Usuario):
    def crear_reporte(self, tipo: str, descripcion: str, ubicacion: str):
        return Reporte(
            usuario=self.nombre,
            tipo=tipo,
            descripcion=descripcion,
            ubicacion=ubicacion
        )


class Administrador(Usuario):
    pass


class Reporte:
    def __init__(self, usuario: str, tipo: str, descripcion: str, ubicacion: str, estado="Pendiente"):
        self.usuario = usuario
        self.tipo = tipo
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.fecha = datetime.now()
        self.estado = estado

    def cambiar_estado(self, nuevo_estado: str):
        self.estado = nuevo_estado

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "ubicacion": self.ubicacion,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data: dict):
        reporte = Reporte(
            usuario=data["usuario"],
            tipo=data["tipo"],
            descripcion=data["descripcion"],
            ubicacion=data["ubicacion"],
            estado=data["estado"]
        )
        reporte.fecha = datetime.strptime(data["fecha"], "%Y-%m-%d %H:%M:%S")
        return reporte


class SistemaReportes:
    def __init__(self, archivo="reportes.json", archivo_usuarios="usuarios.json"):
        self._archivo = archivo
        self._archivo_usuarios = archivo_usuarios
        self._reportes = self._cargar_reportes()
        self._usuarios = self._cargar_usuarios()

    # ---------- REPORTES ----------
    def _cargar_reportes(self):
        try:
            with open(self._archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return [Reporte.from_dict(r) for r in datos]
        except FileNotFoundError:
            return []

    def _guardar_reportes(self):
        with open(self._archivo, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self._reportes], f, indent=4, ensure_ascii=False)

    def agregar_reporte(self, reporte: Reporte):
        self._reportes.append(reporte)
        self._guardar_reportes()

    def obtener_reportes_por_usuario(self, nombre_usuario):
        return [r for r in self._reportes if r.usuario == nombre_usuario]

    def obtener_todos_reportes(self):
        return self._reportes

    def cambiar_estado_reporte(self, indice, nuevo_estado):
        if 0 <= indice < len(self._reportes):
            self._reportes[indice].cambiar_estado(nuevo_estado)
            self._guardar_reportes()
            return True
        return False

    # ---------- USUARIOS ----------
    def _cargar_usuarios(self):
        try:
            with open(self._archivo_usuarios, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"Ciudadanos": [], "Administradores": []}

    def _guardar_usuarios(self):
        with open(self._archivo_usuarios, "w", encoding="utf-8") as f:
            json.dump(self._usuarios, f, indent=4, ensure_ascii=False)

    def agregar_usuario(self, rol, usuario, password):
        for u in self._usuarios[rol]:
            if u["usuario"] == usuario:
                return False
        self._usuarios[rol].append({"usuario": usuario, "password": password})
        self._guardar_usuarios()
        return True

    def validar_usuario(self, rol, usuario, password):
        for u in self._usuarios[rol]:
            if u["usuario"] == usuario and u["password"] == password:
                return True
        return False


class LoginWindow:
    def __init__(self, master, sistema):
        self.master = master
        self.master.title("Sistema de Reportes - Login")
        self.master.geometry("320x250")
        self.sistema = sistema

        tk.Label(master, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack(pady=5)

        tk.Label(master, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack(pady=5)

        tk.Label(master, text="Rol:").pack(pady=5)
        self.combo_rol = ttk.Combobox(master, values=["Ciudadanos", "Administradores"], state="readonly")
        self.combo_rol.pack(pady=5)
        self.combo_rol.current(0)

        tk.Button(master, text="Ingresar", command=self.login).pack(pady=5)
        tk.Button(master, text="Registrar usuario", command=self.registrar_usuario).pack(pady=5)

    def login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        rol = self.combo_rol.get()

        if self.sistema.validar_usuario(rol, usuario, password):
            messagebox.showinfo("Login", f"Bienvenido {usuario}!")
            self.master.destroy()
            root_main = tk.Tk()

            if rol == "Ciudadanos":
                CiudadanoWindow(root_main, self.sistema, usuario)
            else:
                AdministradorWindow(root_main, self.sistema)

            root_main.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar_usuario(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        rol = self.combo_rol.get()

        if not usuario or not password:
            messagebox.showwarning("Error", "Ingrese usuario y contraseña.")
            return

        if self.sistema.agregar_usuario(rol, usuario, password):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        else:
            messagebox.showerror("Error", "El usuario ya existe.")


class CiudadanoWindow:
    def __init__(self, master, sistema, nombre_usuario):
        self.master = master
        self.master.title(f"Sistema de Reportes - {nombre_usuario}")
        self.master.geometry("500x400")
        self.sistema = sistema
        self.usuario = nombre_usuario

        tk.Label(master, text="Tipo de problema:").pack()

        self.combo_tipo = ttk.Combobox(
            master,
            values=CATEGORIAS,
            state="readonly"
        )
        self.combo_tipo.pack()
        self.combo_tipo.current(0)

        tk.Label(master, text="Descripción:").pack()
        self.entry_descripcion = tk.Entry(master)
        self.entry_descripcion.pack()

        tk.Label(master, text="Ubicación:").pack()
        self.entry_ubicacion = tk.Entry(master)
        self.entry_ubicacion.pack()

        tk.Button(master, text="Crear Reporte", command=self.crear_reporte).pack(pady=10)

        tk.Label(master, text="Mis reportes:").pack(pady=5)
        self.tree = ttk.Treeview(master, columns=("Tipo", "Descripción", "Ubicación", "Fecha", "Estado"), show="headings")

        for col in ("Tipo", "Descripción", "Ubicación", "Fecha", "Estado"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        self.actualizar_treeview()

    def crear_reporte(self):
        tipo = self.combo_tipo.get()
        descripcion = self.entry_descripcion.get()
        ubicacion = self.entry_ubicacion.get()

        if not descripcion or not ubicacion:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        reporte = Ciudadano(self.usuario, "").crear_reporte(tipo, descripcion, ubicacion)
        self.sistema.agregar_reporte(reporte)

        messagebox.showinfo("Éxito", "Reporte creado correctamente.")

        self.entry_descripcion.delete(0, tk.END)
        self.entry_ubicacion.delete(0, tk.END)

        self.actualizar_treeview()

    def actualizar_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        reportes = self.sistema.obtener_reportes_por_usuario(self.usuario)

        for r in reportes:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    r.tipo,
                    r.descripcion,
                    r.ubicacion,
                    r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    r.estado
                )
            )


class AdministradorWindow:
    def __init__(self, master, sistema):
        self.master = master
        self.master.title("Panel de Administrador")
        self.master.geometry("800x550")
        self.sistema = sistema

        tk.Label(master, text="Filtrar por estado:").pack(pady=5)

        self.combo_filtro_estado = ttk.Combobox(
            master,
            values=["Todos", "Pendiente", "En revisión", "En proceso", "Resuelto", "Rechazado"],
            state="readonly"
        )
        self.combo_filtro_estado.current(0)
        self.combo_filtro_estado.pack(pady=5)
        self.combo_filtro_estado.bind("<<ComboboxSelected>>", self.actualizar_treeview)

        tk.Label(master, text="Filtrar por categoría:").pack(pady=5)

        self.combo_filtro_categoria = ttk.Combobox(
            master,
            values=["Todas"] + CATEGORIAS,
            state="readonly"
        )
        self.combo_filtro_categoria.current(0)
        self.combo_filtro_categoria.pack(pady=5)
        self.combo_filtro_categoria.bind("<<ComboboxSelected>>", self.actualizar_treeview)

        self.tree = ttk.Treeview(
            master,
            columns=("Usuario", "Tipo", "Descripción", "Ubicación", "Fecha", "Estado"),
            show="headings"
        )

        for col in ("Usuario", "Tipo", "Descripción", "Ubicación", "Fecha", "Estado"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(master, text="Cambiar estado a:").pack(pady=5)

        self.combo_estado = ttk.Combobox(
            master,
            values=["Pendiente", "En revisión", "En proceso", "Resuelto", "Rechazado"],
            state="readonly"
        )
        self.combo_estado.pack(pady=5)

        tk.Button(master, text="Cambiar Estado", command=self.cambiar_estado).pack(pady=10)

        self.actualizar_treeview()

    def actualizar_treeview(self, event=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtro_estado = self.combo_filtro_estado.get()
        filtro_categoria = self.combo_filtro_categoria.get()

        reportes = self.sistema.obtener_todos_reportes()

        for i, r in enumerate(reportes):
            if (filtro_estado == "Todos" or r.estado == filtro_estado) and \
               (filtro_categoria == "Todas" or r.tipo == filtro_categoria):

                self.tree.insert(
                    "",
                    tk.END,
                    iid=i,
                    values=(
                        r.usuario,
                        r.tipo,
                        r.descripcion,
                        r.ubicacion,
                        r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                        r.estado
                    )
                )

    def cambiar_estado(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Error", "Seleccione un reporte.")
            return

        nuevo_estado = self.combo_estado.get()
        if not nuevo_estado:
            messagebox.showwarning("Error", "Seleccione un estado.")
            return

        indice = int(seleccionado[0])
        self.sistema.cambiar_estado_reporte(indice, nuevo_estado)

        messagebox.showinfo("Éxito", "Estado actualizado correctamente.")
        self.actualizar_treeview()


if __name__ == "__main__":
    sistema = SistemaReportes()
    root = tk.Tk()
    LoginWindow(root, sistema)
    root.mainloop()