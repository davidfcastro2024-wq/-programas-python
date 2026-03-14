import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


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
        # Verifica que no exista
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
                app = CiudadanoWindow(root_main, self.sistema, usuario)
            else:
                # Para admin, se puede implementar luego
                messagebox.showinfo("Admin", "Ventana de administrador aún no implementada")
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
        self.entry_tipo = tk.Entry(master)
        self.entry_tipo.pack()

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
        tipo = self.entry_tipo.get()
        descripcion = self.entry_descripcion.get()
        ubicacion = self.entry_ubicacion.get()

        if not tipo or not descripcion or not ubicacion:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        reporte = Ciudadano(self.usuario, "").crear_reporte(tipo, descripcion, ubicacion)
        self.sistema.agregar_reporte(reporte)
        messagebox.showinfo("Éxito", "Reporte creado correctamente.")
        self.entry_tipo.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_ubicacion.delete(0, tk.END)
        self.actualizar_treeview()

    def actualizar_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        reportes = self.sistema.obtener_reportes_por_usuario(self.usuario)
        for r in reportes:
            self.tree.insert("", tk.END, values=(r.tipo, r.descripcion, r.ubicacion, r.fecha.strftime("%Y-%m-%d %H:%M:%S"), r.estado))


if __name__ == "__main__":
    sistema = SistemaReportes()
    root = tk.Tk()
    login = LoginWindow(root, sistema)
    root.mainloop()
