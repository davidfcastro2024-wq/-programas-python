import json
from datetime import datetime
import flet as ft

CATEGORIAS = [
    "Huecos en vía",
    "Alumbrado público",
    "Basuras",
    "Señalización",
    "Espacios públicos",
    "Alcantarillado"
]

# ─────────────────────────────────────────
#  MODELOS
# ─────────────────────────────────────────

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
    def __init__(self, usuario, tipo, descripcion, ubicacion, estado="Pendiente"):
        self.usuario = usuario
        self.tipo = tipo
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.fecha = datetime.now()
        self.estado = estado

    def cambiar_estado(self, nuevo_estado):
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
    def from_dict(data):
        r = Reporte(
            usuario=data["usuario"],
            tipo=data["tipo"],
            descripcion=data["descripcion"],
            ubicacion=data["ubicacion"],
            estado=data["estado"]
        )
        r.fecha = datetime.strptime(data["fecha"], "%Y-%m-%d %H:%M:%S")
        return r


# ─────────────────────────────────────────
#  SISTEMA DE DATOS
# ─────────────────────────────────────────

class SistemaReportes:
    def __init__(self, archivo="reportes.json", archivo_usuarios="usuarios.json"):
        self._archivo = archivo
        self._archivo_usuarios = archivo_usuarios
        self._reportes = self._cargar_reportes()
        self._usuarios = self._cargar_usuarios()

    def _cargar_reportes(self):
        try:
            with open(self._archivo, "r", encoding="utf-8") as f:
                return [Reporte.from_dict(r) for r in json.load(f)]
        except FileNotFoundError:
            return []

    def _guardar_reportes(self):
        with open(self._archivo, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self._reportes], f, indent=4, ensure_ascii=False)

    def agregar_reporte(self, reporte):
        self._reportes.append(reporte)
        self._guardar_reportes()

    def obtener_reportes_por_usuario(self, nombre):
        return [r for r in self._reportes if r.usuario == nombre]

    def obtener_todos_reportes(self):
        return self._reportes

    def cambiar_estado_reporte(self, indice, nuevo_estado):
        if 0 <= indice < len(self._reportes):
            self._reportes[indice].cambiar_estado(nuevo_estado)
            self._guardar_reportes()
            return True
        return False

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


# ─────────────────────────────────────────
#  COLORES / TEMA
# ─────────────────────────────────────────

COLOR_PRIMARIO  = "#1565C0"   # azul institucional
COLOR_SECUNDARIO = "#E3F2FD"  # azul muy claro para fondos
COLOR_ACENTO    = "#0D47A1"
COLOR_TEXTO     = "#212121"
COLOR_FONDO     = "#F5F5F5"

ESTADOS_COLORES = {
    "Pendiente":   "#FFA000",
    "En revisión": "#1976D2",
    "En proceso":  "#7B1FA2",
    "Resuelto":    "#388E3C",
    "Rechazado":   "#D32F2F",
}


# ─────────────────────────────────────────
#  HELPERS UI
# ─────────────────────────────────────────

def estado_chip(estado: str) -> ft.Container:
    color = ESTADOS_COLORES.get(estado, "#757575")
    return ft.Container(
        content=ft.Text(estado, color="white", size=11, weight=ft.FontWeight.W_600),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=12,
    )


def snack(page: ft.Page, mensaje: str, error=False):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(mensaje),
        bgcolor="#D32F2F" if error else "#388E3C",
    )
    page.snack_bar.open = True
    page.update()


def titulo(texto: str) -> ft.Text:
    return ft.Text(texto, size=22, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARIO)


# ─────────────────────────────────────────
#  VISTA LOGIN
# ─────────────────────────────────────────

def vista_login(page: ft.Page, sistema: SistemaReportes):
    page.title = "ReportaCity – Acceso"
    page.bgcolor = COLOR_FONDO

    campo_usuario  = ft.TextField(label="Usuario", prefix_icon="person", width=320)
    campo_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True,
                                  prefix_icon="lock", width=320)
    combo_rol = ft.Dropdown(
        label="Rol",
        width=320,
        options=[ft.dropdown.Option("Ciudadanos"), ft.dropdown.Option("Administradores")],
        value="Ciudadanos",
    )
    error_texto = ft.Text("", color="#D32F2F", size=13)

    def on_login(e):
        u = campo_usuario.value.strip()
        p = campo_password.value.strip()
        r = combo_rol.value
        if not u or not p:
            error_texto.value = "Completa todos los campos."
            page.update()
            return
        if sistema.validar_usuario(r, u, p):
            page.controls.clear()
            if r == "Ciudadanos":
                vista_ciudadano(page, sistema, u)
            else:
                vista_administrador(page, sistema)
        else:
            error_texto.value = "Usuario o contraseña incorrectos."
            page.update()

    def on_registrar(e):
        u = campo_usuario.value.strip()
        p = campo_password.value.strip()
        r = combo_rol.value
        if not u or not p:
            error_texto.value = "Completa todos los campos."
            page.update()
            return
        if sistema.agregar_usuario(r, u, p):
            error_texto.value = ""
            snack(page, f"Usuario '{u}' registrado correctamente.")
        else:
            error_texto.value = "Ese usuario ya existe."
            page.update()

    card = ft.Card(
        elevation=8,
        content=ft.Container(
            padding=40,
            width=400,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Icon("location_city", size=52, color=COLOR_PRIMARIO),
                    titulo("ReportaCity"),
                    ft.Text("Sistema de reportes urbanos", color="#757575", size=14),
                    ft.Divider(),
                    campo_usuario,
                    campo_password,
                    combo_rol,
                    error_texto,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.ElevatedButton(
                                "Ingresar",
                                icon="login",
                                on_click=on_login,
                                bgcolor=COLOR_PRIMARIO,
                                color="white",
                                width=140,
                            ),
                            ft.OutlinedButton(
                                "Registrarse",
                                icon="person_add",
                                on_click=on_registrar,
                                width=140,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[card],
        )
    )
    page.update()


# ─────────────────────────────────────────
#  VISTA CIUDADANO
# ─────────────────────────────────────────

def vista_ciudadano(page: ft.Page, sistema: SistemaReportes, nombre_usuario: str):
    page.title = f"ReportaCity – {nombre_usuario}"
    page.bgcolor = COLOR_FONDO

    combo_tipo = ft.Dropdown(
        label="Tipo de problema",
        width=400,
        options=[ft.dropdown.Option(c) for c in CATEGORIAS],
        value=CATEGORIAS[0],
    )
    campo_descripcion = ft.TextField(label="Descripción", multiline=True, min_lines=2, max_lines=4, width=400)
    campo_ubicacion   = ft.TextField(label="Ubicación", prefix_icon="place", width=400)

    tabla = ft.DataTable(
        border=ft.border.all(1, "#E0E0E0"),
        border_radius=8,
        heading_row_color="#E3F2FD",
        columns=[
            ft.DataColumn(ft.Text("Tipo",        weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Descripción", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ubicación",   weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Fecha",       weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado",      weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def cargar_tabla():
        tabla.rows.clear()
        for r in sistema.obtener_reportes_por_usuario(nombre_usuario):
            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(r.tipo, size=12)),
                    ft.DataCell(ft.Text(r.descripcion[:40], size=12)),
                    ft.DataCell(ft.Text(r.ubicacion, size=12)),
                    ft.DataCell(ft.Text(r.fecha.strftime("%Y-%m-%d %H:%M"), size=12)),
                    ft.DataCell(estado_chip(r.estado)),
                ])
            )
        page.update()

    def on_crear(e):
        tipo       = combo_tipo.value
        descripcion = campo_descripcion.value.strip()
        ubicacion  = campo_ubicacion.value.strip()
        if not descripcion or not ubicacion:
            snack(page, "Todos los campos son obligatorios.", error=True)
            return
        reporte = Ciudadano(nombre_usuario, "").crear_reporte(tipo, descripcion, ubicacion)
        sistema.agregar_reporte(reporte)
        campo_descripcion.value = ""
        campo_ubicacion.value   = ""
        snack(page, "Reporte creado correctamente.")
        cargar_tabla()

    def on_logout(e):
        page.controls.clear()
        vista_login(page, sistema)

    # ── Layout ──
    formulario = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=24,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Nuevo reporte", size=16, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARIO),
                    combo_tipo,
                    campo_descripcion,
                    campo_ubicacion,
                    ft.ElevatedButton(
                        "Crear Reporte",
                        icon="send",
                        on_click=on_crear,
                        bgcolor=COLOR_PRIMARIO,
                        color="white",
                    ),
                ],
            ),
        ),
    )

    seccion_tabla = ft.Column(
        spacing=8,
        expand=True,
        controls=[
            ft.Text("Mis reportes", size=16, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARIO),
            ft.Container(
                content=ft.Column(
                    controls=[tabla],
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True,
            ),
        ],
    )

    barra = ft.AppBar(
        title=ft.Text("ReportaCity", color="white"),
        bgcolor=COLOR_PRIMARIO,
        actions=[
            ft.Text(nombre_usuario, color="white", size=13),
            ft.IconButton("logout", icon_color="white", on_click=on_logout, tooltip="Cerrar sesión"),
        ],
    )

    page.appbar = barra
    page.add(
        ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=16,
            controls=[
                ft.Container(padding=ft.padding.symmetric(horizontal=24, vertical=16),
                             content=formulario),
                ft.Container(padding=ft.padding.symmetric(horizontal=24),
                             content=seccion_tabla, expand=True),
            ],
        )
    )
    cargar_tabla()


# ─────────────────────────────────────────
#  VISTA ADMINISTRADOR
# ─────────────────────────────────────────

def vista_administrador(page: ft.Page, sistema: SistemaReportes):
    page.title = "ReportaCity – Panel Administrador"
    page.bgcolor = COLOR_FONDO

    indice_seleccionado = {"v": None}   # guardamos el índice real del reporte

    combo_filtro_estado = ft.Dropdown(
        label="Filtrar por estado",
        width=220,
        options=[ft.dropdown.Option(e) for e in ["Todos", "Pendiente", "En revisión", "En proceso", "Resuelto", "Rechazado"]],
        value="Todos",
    )
    combo_filtro_cat = ft.Dropdown(
        label="Filtrar por categoría",
        width=220,
        options=[ft.dropdown.Option("Todas")] + [ft.dropdown.Option(c) for c in CATEGORIAS],
        value="Todas",
    )
    combo_nuevo_estado = ft.Dropdown(
        label="Cambiar estado a",
        width=220,
        options=[ft.dropdown.Option(e) for e in ["Pendiente", "En revisión", "En proceso", "Resuelto", "Rechazado"]],
    )

    tabla = ft.DataTable(
        border=ft.border.all(1, "#E0E0E0"),
        border_radius=8,
        heading_row_color="#E3F2FD",
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(ft.Text("#",           weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Usuario",     weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo",        weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Descripción", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ubicación",   weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Fecha",       weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado",      weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def cargar_tabla(e=None):
        tabla.rows.clear()
        indice_seleccionado["v"] = None
        fe = combo_filtro_estado.get()  if hasattr(combo_filtro_estado, "get") else combo_filtro_estado.value
        fe = combo_filtro_estado.value
        fc = combo_filtro_cat.value
        reportes = sistema.obtener_todos_reportes()

        for i, r in enumerate(reportes):
            if (fe == "Todos" or r.estado == fe) and (fc == "Todas" or r.tipo == fc):
                idx = i  # índice real en la lista de reportes
                def on_sel(e, real_idx=idx):
                    if e.data == "true":
                        indice_seleccionado["v"] = real_idx
                    else:
                        indice_seleccionado["v"] = None

                tabla.rows.append(
                    ft.DataRow(
                        on_select_changed=on_sel,
                        cells=[
                            ft.DataCell(ft.Text(str(i + 1), size=12)),
                            ft.DataCell(ft.Text(r.usuario,  size=12)),
                            ft.DataCell(ft.Text(r.tipo,     size=12)),
                            ft.DataCell(ft.Text(r.descripcion[:35], size=12)),
                            ft.DataCell(ft.Text(r.ubicacion, size=12)),
                            ft.DataCell(ft.Text(r.fecha.strftime("%Y-%m-%d %H:%M"), size=12)),
                            ft.DataCell(estado_chip(r.estado)),
                        ],
                    )
                )
        page.update()

    combo_filtro_estado.on_change = cargar_tabla
    combo_filtro_cat.on_change    = cargar_tabla

    def on_cambiar_estado(e):
        idx = indice_seleccionado["v"]
        if idx is None:
            snack(page, "Selecciona un reporte de la tabla.", error=True)
            return
        nuevo = combo_nuevo_estado.value
        if not nuevo:
            snack(page, "Selecciona el nuevo estado.", error=True)
            return
        sistema.cambiar_estado_reporte(idx, nuevo)
        snack(page, "Estado actualizado correctamente.")
        cargar_tabla()

    def on_logout(e):
        page.appbar = None
        page.controls.clear()
        vista_login(page, sistema)

    barra = ft.AppBar(
        title=ft.Text("Panel Administrador", color="white"),
        bgcolor=COLOR_ACENTO,
        actions=[
            ft.IconButton("logout", icon_color="white", on_click=on_logout, tooltip="Cerrar sesión"),
        ],
    )

    controles_superiores = ft.Card(
        elevation=3,
        content=ft.Container(
            padding=16,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                wrap=True,
                controls=[
                    combo_filtro_estado,
                    combo_filtro_cat,
                    ft.VerticalDivider(),
                    combo_nuevo_estado,
                    ft.ElevatedButton(
                        "Cambiar Estado",
                        icon="edit",
                        on_click=on_cambiar_estado,
                        bgcolor=COLOR_ACENTO,
                        color="white",
                    ),
                ],
            ),
        ),
    )

    page.appbar = barra
    page.add(
        ft.Column(
            expand=True,
            spacing=12,
            controls=[
                ft.Container(padding=ft.padding.symmetric(horizontal=24, vertical=12),
                             content=controles_superiores),
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=24),
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Text("Reportes", size=16, weight=ft.FontWeight.BOLD, color=COLOR_ACENTO),
                            ft.Container(
                                expand=True,
                                content=ft.Column(
                                    controls=[tabla],
                                    scroll=ft.ScrollMode.AUTO,
                                    expand=True,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )
    )
    cargar_tabla()


# ─────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────

def main(page: ft.Page):
    page.window_width  = 900
    page.window_height = 650
    page.window_min_width  = 600
    page.window_min_height = 500
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {}

    sistema = SistemaReportes()
    vista_login(page, sistema)


ft.app(target=main)
