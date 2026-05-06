import flet as ft

# ── COLORES ──────────────────────────────────────────────
VERDE_PROFUNDO = "#0d2b1a"
VERDE_OSCURO   = "#12391f"
VERDE_MEDIO    = "#1c5c30"
VERDE_VIVO     = "#2e8b4a"
VERDE_CLARO    = "#4db86a"
VERDE_BRILLO   = "#6fcf7e"
CARBON         = "#0a0f0c"
GRIS_OSCURO    = "#111c14"
GRIS_NIEBLA    = "#c8d9cc"
BLANCO         = "#f4f9f5"
DORADO         = "#c8a84b"


# ── HELPERS ───────────────────────────────────────────────
def tag_seccion(texto: str) -> ft.Row:
    """Etiqueta pequeña estilo 'SISTEMA DE REPORTES'"""
    return ft.Row(
        controls=[
            ft.Container(width=22, height=1, bgcolor=VERDE_CLARO),
            ft.Text(
                texto.upper(),
                size=11,
                weight=ft.FontWeight.BOLD,
                color=VERDE_CLARO,
            ),
        ],
        spacing=10,
    )


def titulo_seccion(texto: str) -> ft.Text:
    return ft.Text(
        texto,
        size=32,
        weight=ft.FontWeight.BOLD,
        color=BLANCO,
    )


def desc_seccion(texto: str) -> ft.Text:
    return ft.Text(texto, size=15, color=GRIS_NIEBLA, width=520)


# ── SECCIONES ─────────────────────────────────────────────

def navbar() -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("🏙️", size=20),
                        ft.Text(
                            "Ciudad",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=VERDE_BRILLO,
                        ),
                        ft.Text(
                            "Activa",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=BLANCO,
                        ),
                    ],
                    spacing=4,
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("Problema",      style=ft.ButtonStyle(color=GRIS_NIEBLA)),
                        ft.TextButton("Funciones",     style=ft.ButtonStyle(color=GRIS_NIEBLA)),
                        ft.TextButton("Cómo funciona", style=ft.ButtonStyle(color=GRIS_NIEBLA)),
                        ft.TextButton("Roles",         style=ft.ButtonStyle(color=GRIS_NIEBLA)),
                        ft.Container(
                            content=ft.Text(
                                "BETA",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=VERDE_BRILLO,
                            ),
                            bgcolor=VERDE_MEDIO,
                            border_radius=100,
                            padding=ft.padding.symmetric(horizontal=14, vertical=6),
                            border=ft.border.all(1, "#4db86a55"),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#0a0f0ccc",
        padding=ft.padding.symmetric(horizontal=60, vertical=18),
        border=ft.border.only(bottom=ft.BorderSide(1, "#2e8b4a33")),
    )


def seccion_hero() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                # Eyebrow
                ft.Row(
                    controls=[
                        ft.Container(width=28, height=1, bgcolor=VERDE_CLARO),
                        ft.Text(
                            "SISTEMA DE REPORTES URBANOS",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            color=VERDE_CLARO,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=20),

                # Título principal
                ft.Column(
                    controls=[
                        ft.Text(
                            "Tu ciudad,",
                            size=64,
                            weight=ft.FontWeight.W_900,
                            color=BLANCO,
                        ),
                        ft.Text(
                            "tu voz.",
                            size=64,
                            weight=ft.FontWeight.W_900,
                            color=VERDE_BRILLO,
                        ),
                        ft.Text(
                            "tu reporte.",
                            size=64,
                            weight=ft.FontWeight.W_900,
                            color="#f4f9f572",
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=24),

                # Subtítulo
                ft.Text(
                    "CiudadActiva permite a los ciudadanos reportar problemas urbanos\n"
                    "y a las autoridades gestionarlos con eficiencia. Un puente digital\n"
                    "entre comunidad y gobierno local.",
                    size=16,
                    color=GRIS_NIEBLA,
                    width=520,
                ),
                ft.Container(height=36),

                # Botones
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Ver en GitHub →",
                            bgcolor=VERDE_VIVO,
                            color=BLANCO,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=3),
                                padding=ft.padding.symmetric(horizontal=28, vertical=18)
                            ),
                        ),
                        ft.OutlinedButton(
                            "Cómo funciona",
                            style=ft.ButtonStyle(
                                color=GRIS_NIEBLA,
                                side=ft.BorderSide(1, "#c8d9cc33"),
                                shape=ft.RoundedRectangleBorder(radius=3),
                                padding=ft.padding.symmetric(horizontal=28, vertical=18)
                            ),
                        ),
                    ],
                    spacing=12,
                ),
                ft.Container(height=48),

                # Stats
                ft.Row(
                    controls=[
                        _stat_chip("6", "Categorías\nde reporte"),
                        _stat_chip("2", "Roles de\nusuario"),
                        _stat_chip("∞", "Reportes\ngestionables"),
                    ],
                    spacing=12,
                ),
            ],
            spacing=0,
        ),
        bgcolor=CARBON,
        padding=ft.padding.only(left=60, right=60, top=100, bottom=80),
    )


def _stat_chip(numero: str, etiqueta: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(numero, size=24, weight=ft.FontWeight.W_900, color=VERDE_BRILLO),
                ft.Text(etiqueta, size=12, color=GRIS_NIEBLA),
            ],
            spacing=12,
        ),
        bgcolor="#12391f99",
        border=ft.border.all(1, "#2e8b4a4d"),
        border_radius=4,
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
    )


def seccion_problema() -> ft.Container:
    cards_left = ft.Column(
        controls=[
            _issue_card("🕳️", "Huecos en vía", "Más reportados"),
            _issue_card("🗑️", "Basuras", "Alta frecuencia"),
        ],
        spacing=12,
    )
    cards_right = ft.Column(
        controls=[
            _issue_card("💡", "Alumbrado", "Frecuente"),
            _issue_card("🚧", "Señalización", "Moderado"),
        ],
        spacing=12,
    )

    texto = ft.Column(
        controls=[
            tag_seccion("El problema"),
            ft.Container(height=16),
            titulo_seccion("Los problemas urbanos\nno tienen canal oficial."),
            ft.Container(height=20),
            desc_seccion(
                "Los ciudadanos no tienen una forma estructurada de reportar "
                "problemas. Las quejas se pierden en redes sociales o llamadas "
                "telefónicas sin seguimiento real."
            ),
            ft.Container(height=24),
            ft.Column(
                controls=[
                    _problema_item("Sin trazabilidad ni estado visible del reporte"),
                    _problema_item("Sin categorización de los problemas"),
                    _problema_item("Sin datos para priorizar intervenciones"),
                    _problema_item("Ciudadano sin poder real de seguimiento"),
                ],
                spacing=12,
            ),
        ],
        spacing=0,
    )

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(controls=[cards_left, cards_right], spacing=12),
                texto,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=60,
        ),
        bgcolor=GRIS_OSCURO,
        padding=ft.padding.symmetric(horizontal=60, vertical=80),
        border=ft.border.only(top=ft.BorderSide(1, "#2e8b4a26")),
    )


def _issue_card(icon: str, nombre: str, conteo: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(icon, size=28),
                ft.Text(nombre, size=13, weight=ft.FontWeight.BOLD, color=BLANCO),
                ft.Text(conteo, size=11, color=VERDE_CLARO),
            ],
            spacing=6,
        ),
        bgcolor="#0d2b1ab2",
        border=ft.border.all(1, "#2e8b4a33"),
        border_radius=8,
        padding=ft.padding.all(18),
        width=155,
    )


def _problema_item(texto: str) -> ft.Row:
    return ft.Row(
        controls=[
            ft.Text("→", size=14, color=VERDE_CLARO, weight=ft.FontWeight.BOLD),
            ft.Text(texto, size=14, color=GRIS_NIEBLA, width=380),
        ],
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def seccion_funcionalidades() -> ft.Container:
    funciones = [
        ("01", "🔐", "Autenticación por rol",
         "Login seguro con validación de credenciales. Ciudadano o Administrador, cada uno ve solo lo que le corresponde."),
        ("02", "📋", "Crear reportes",
         "El ciudadano describe el problema, selecciona el tipo y especifica la ubicación. Todo queda registrado."),
        ("03", "🔍", "Consultar historial",
         "Cada ciudadano ve sus reportes con estado actualizado: Pendiente, En proceso o Resuelto."),
        ("04", "🛡️", "Panel de administración",
         "El administrador ve todos los reportes del sistema y puede filtrar por estado y categoría."),
        ("05", "🔄", "Cambio de estado",
         "El admin actualiza el estado de cada reporte. El sistema registra el cambio y persiste en JSON."),
        ("06", "💾", "Persistencia local",
         "Datos almacenados en reportes.json y usuarios.json. Sin base de datos externa requerida."),
    ]

    cards = [_func_card(n, ic, t, d) for n, ic, t, d in funciones]

    grid = ft.Row(
        controls=[
            ft.Column(controls=cards[:3], spacing=2),
            ft.Column(controls=cards[3:], spacing=2),
        ],
        spacing=2,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        tag_seccion("Solución"),
                        ft.Container(height=16),
                        titulo_seccion("Todo lo que CiudadActiva hace"),
                        ft.Container(height=10),
                        desc_seccion(
                            "Un sistema completo de gestión de reportes con roles, "
                            "persistencia y flujos definidos."
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=48),
                grid,
            ],
            spacing=0,
        ),
        bgcolor=CARBON,
        padding=ft.padding.symmetric(horizontal=60, vertical=80),
    )


def _func_card(numero: str, icono: str, titulo: str, desc: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(numero, size=11, color="#4db86a66", weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                ft.Text(icono, size=32),
                ft.Container(height=8),
                ft.Text(titulo, size=15, weight=ft.FontWeight.BOLD, color=BLANCO),
                ft.Container(height=8),
                ft.Text(desc, size=13, color=GRIS_NIEBLA, width=240),
            ],
            spacing=0,
        ),
        bgcolor=GRIS_OSCURO,
        padding=ft.padding.all(28),
        border=ft.border.all(1, "#2e8b4a1a"),
        width=270,
        height=220,
    )


def seccion_como_funciona() -> ft.Container:
    pasos = [
        ("1", "📝", "Registrarse", "El ciudadano crea su cuenta con nombre y correo."),
        ("2", "🔐", "Iniciar sesión", "Autenticación por rol: ciudadano o administrador."),
        ("3", "📍", "Crear reporte", "Describe el problema, tipo y ubicación."),
        ("4", "🔄", "Gestión admin", "El admin revisa y actualiza el estado."),
        ("5", "✅", "Resolución", "El reporte queda marcado como resuelto."),
    ]

    steps_row = ft.Row(
        controls=[_flujo_step(n, ic, t, d) for n, ic, t, d in pasos],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "FLUJO DEL SISTEMA",
                                    size=11,
                                    weight=ft.FontWeight.BOLD,
                                    color=VERDE_CLARO,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(height=16),
                        ft.Text(
                            "¿Cómo funciona?",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=BLANCO,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                ft.Container(height=60),
                steps_row,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor=VERDE_PROFUNDO,
        padding=ft.padding.symmetric(horizontal=60, vertical=80),
        border=ft.border.only(
            top=ft.BorderSide(1, "#4db86a1a"),
            bottom=ft.BorderSide(1, "#4db86a1a"),
        ),
    )


def _flujo_step(numero: str, icono: str, titulo: str, desc: str) -> ft.Column:
    return ft.Column(
        controls=[
            ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Text(icono, size=28, text_align=ft.TextAlign.CENTER),
                        width=76,
                        height=76,
                        border_radius=38,
                        bgcolor=VERDE_OSCURO,
                        border=ft.border.all(2, "#4db86a66"),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text(numero, size=11, color=BLANCO, weight=ft.FontWeight.BOLD),
                        width=22,
                        height=22,
                        border_radius=11,
                        bgcolor=VERDE_VIVO,
                        alignment=ft.alignment.center,
                        left=54,
                        top=0,
                    ),
                ],
                width=76,
                height=76,
            ),
            ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=BLANCO, text_align=ft.TextAlign.CENTER, width=130),
            ft.Text(desc, size=12, color=GRIS_NIEBLA, text_align=ft.TextAlign.CENTER, width=130),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        width=150,
    )


def seccion_roles() -> ft.Container:
    ciudadano = _rol_card(
        "👤 Ciudadano",
        "El reportante",
        [
            "Registrarse e iniciar sesión de forma segura",
            "Crear reportes con tipo, descripción y ubicación",
            "Consultar el historial de sus propios reportes",
            "Ver el estado actualizado de cada reporte",
        ],
        borde=VERDE_CLARO,
        badge_color=VERDE_BRILLO,
        badge_bg="#4db86a26",
        marker="✓",
    )
    admin = _rol_card(
        "🛡️ Administrador",
        "El gestor",
        [
            "Ver todos los reportes del sistema en un panel",
            "Filtrar por estado y categoría simultáneamente",
            "Cambiar el estado de cualquier reporte",
            "Gestionar la priorización de problemas urbanos",
        ],
        borde=DORADO,
        badge_color=DORADO,
        badge_bg="#c8a84b26",
        marker="◆",
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                tag_seccion("Roles del sistema"),
                ft.Container(height=16),
                titulo_seccion("Dos perfiles, un mismo objetivo"),
                ft.Container(height=48),
                ft.Row(controls=[ciudadano, admin], spacing=24),
            ],
            spacing=0,
        ),
        bgcolor=CARBON,
        padding=ft.padding.symmetric(horizontal=60, vertical=80),
    )


def _rol_card(badge: str, titulo: str, features: list,
              borde: str, badge_color: str, badge_bg: str, marker: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(badge, size=11, color=badge_color,
                                    weight=ft.FontWeight.BOLD),
                    bgcolor=badge_bg,
                    border_radius=100,
                    padding=ft.padding.symmetric(horizontal=14, vertical=6),
                ),
                ft.Container(height=16),
                ft.Text(titulo, size=22, weight=ft.FontWeight.BOLD, color=BLANCO),
                ft.Container(height=14),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(marker, size=13, color=borde, weight=ft.FontWeight.BOLD),
                                ft.Text(f, size=14, color=GRIS_NIEBLA, width=320),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        )
                        for f in features
                    ],
                    spacing=10,
                ),
            ],
            spacing=0,
        ),
        bgcolor="#12391f99" if marker == "✓" else "#19190f cc",
        border=ft.border.all(1, borde + "40"),
        border_radius=8,
        padding=ft.padding.all(32),
        width=400,
    )


def seccion_categorias() -> ft.Container:
    cats = [
        ("🕳️", "Huecos en vía"),
        ("💡", "Alumbrado público"),
        ("🗑️", "Basuras"),
        ("🚧", "Señalización"),
        ("🌳", "Espacios públicos"),
        ("🚰", "Alcantarillado"),
    ]

    pills = ft.Row(
        controls=[_cat_pill(ic, n) for ic, n in cats],
        spacing=12,
        wrap=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                tag_seccion("Categorías"),
                ft.Container(height=16),
                titulo_seccion("¿Qué tipo de problemas se reportan?"),
                ft.Container(height=40),
                pills,
            ],
            spacing=0,
        ),
        bgcolor=GRIS_OSCURO,
        padding=ft.padding.symmetric(horizontal=60, vertical=80),
        border=ft.border.only(top=ft.BorderSide(1, "#2e8b4a1a")),
    )


def _cat_pill(icono: str, nombre: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(icono, size=20),
                ft.Text(nombre, size=14, color=BLANCO, weight=ft.FontWeight.W_500),
            ],
            spacing=10,
        ),
        bgcolor="#12391f",
        border=ft.border.all(1, "#2e8b4a33"),
        border_radius=100,
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
    )


def seccion_tecnologia() -> ft.Container:
    diagrama = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("// Jerarquía de clases", size=12, color=VERDE_CLARO, font_family="monospace"),
                ft.Container(height=12),
                _oop_clase("👤 Usuario (base)", ["props: nombre, correo", "@property: getters seguros"]),
                ft.Text("↓ hereda", size=12, color="#4db86a66", text_align=ft.TextAlign.CENTER),
                ft.Row(
                    controls=[
                        _oop_clase("🏙️ Ciudadano", ["crear_reporte()"]),
                        _oop_clase("🛡️ Admin",     ["gestión total"]),
                    ],
                    spacing=8,
                ),
                ft.Text("↓ gestiona", size=12, color="#4db86a66", text_align=ft.TextAlign.CENTER),
                _oop_clase("📋 Reporte", ["attrs: tipo, descripción, ubicación, estado", "cambiar_estado() · to_dict()"]),
                ft.Text("↓ administrado por", size=12, color="#4db86a66", text_align=ft.TextAlign.CENTER),
                _oop_clase("⚙️ SistemaReportes", ["agregar_reporte()", "cambiar_estado_reporte()", "_guardar / _cargar (JSON)"]),
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#0d2b1a",
        border=ft.border.all(1, "#2e8b4a33"),
        border_radius=8,
        padding=ft.padding.all(24),
        width=340,
    )

    puntos = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(width=8, height=8, border_radius=4, bgcolor=VERDE_BRILLO),
                    ft.Text(txt, size=14, color=GRIS_NIEBLA, width=380),
                ],
                spacing=12,
            )
            for txt in [
                "Datos almacenados en reportes.json y usuarios.json",
                "Interfaz gráfica construida con Flet 0.28.3",
                "Autenticación por rol con validación de credenciales",
            ]
        ],
        spacing=14,
    )

    pills = ft.Row(
        controls=[
            _tech_pill(p)
            for p in ["Python 3", "POO", "Herencia", "Encapsulamiento",
                      "JSON", "Persistencia local", "Flet 0.28.3", "Patrón MVC"]
        ],
        wrap=True,
        spacing=8,
    )

    texto = ft.Column(
        controls=[
            tag_seccion("Detrás del código"),
            ft.Container(height=16),
            titulo_seccion("Arquitectura orientada\na objetos"),
            ft.Container(height=16),
            ft.Text(
                "El sistema aplica los principios de la Programación Orientada a Objetos: "
                "herencia entre clases de usuario, encapsulamiento con propiedades privadas "
                "y métodos de acceso, y una arquitectura en capas que separa la lógica del "
                "negocio de la interfaz gráfica.",
                size=14,
                color=GRIS_NIEBLA,
                width=440,
            ),
            ft.Container(height=20),
            pills,
            ft.Container(height=24),
            ft.Container(
                content=ft.Text(
                    '"La clase SistemaReportes actúa como controlador central, desacoplando '
                    'la interfaz gráfica de la lógica de negocio."',
                    size=13,
                    color=GRIS_NIEBLA,
                    italic=True,
                    width=400,
                ),
                bgcolor="#12391f",
                border=ft.border.only(left=ft.BorderSide(3, VERDE_CLARO)),
                padding=ft.padding.symmetric(horizontal=16, vertical=14),
                border_radius=ft.border_radius.only(top_right=4, bottom_right=4),
            ),
            ft.Container(height=24),
            puntos,
        ],
        spacing=0,
    )

    return ft.Container(
        content=ft.Row(
            controls=[diagrama, texto],
            spacing=60,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor=CARBON,
        padding=ft.padding.symmetric(horizontal=60, vertical=80),
    )


def _oop_clase(header: str, body_lines: list) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(header, size=12, color=VERDE_BRILLO, weight=ft.FontWeight.BOLD),
                    bgcolor="#1c5c3066",
                    padding=ft.padding.symmetric(horizontal=10, vertical=6),
                    border_radius=ft.border_radius.only(top_left=4, top_right=4),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[ft.Text(l, size=11, color=GRIS_NIEBLA, font_family="monospace") for l in body_lines],
                        spacing=2,
                    ),
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                ),
            ],
            spacing=0,
        ),
        border=ft.border.all(1, "#2e8b4a4d"),
        border_radius=4,
        width=300,
    )


def _tech_pill(texto: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(texto, size=12, color=VERDE_CLARO),
        bgcolor="#1c5c3033",
        border=ft.border.all(1, "#2e8b4a33"),
        border_radius=100,
        padding=ft.padding.symmetric(horizontal=14, vertical=6),
    )


def seccion_cta() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("🎓 Universidad de Cundinamarca", size=13, color=VERDE_CLARO),
                ft.Container(height=16),
                ft.Text(
                    "Una solución real\npara ciudades reales.",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=BLANCO,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=16),
                ft.Text(
                    "CiudadActiva nace como proyecto universitario con visión de impacto real.\n"
                    "Un sistema que demuestra cómo la programación puede ser una herramienta\n"
                    "de transformación social.",
                    size=15,
                    color=GRIS_NIEBLA,
                    text_align=ft.TextAlign.CENTER,
                    width=560,
                ),
                ft.Container(height=36),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Ver código en GitHub →",
                            bgcolor=VERDE_VIVO,
                            color=BLANCO,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=3),
                                padding=ft.padding.symmetric(horizontal=28, vertical=18)
                            ),
                        ),
                        ft.OutlinedButton(
                            "Cómo funciona",
                            style=ft.ButtonStyle(
                                color=GRIS_NIEBLA,
                                side=ft.BorderSide(1, "#c8d9cc33"),
                                shape=ft.RoundedRectangleBorder(radius=3),
                                padding=ft.padding.symmetric(horizontal=28, vertical=18)
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor=VERDE_OSCURO,
        padding=ft.padding.symmetric(horizontal=60, vertical=100),
        border=ft.border.only(top=ft.BorderSide(1, "#4db86a1a")),
    )


def footer() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("🏙️ CiudadActiva", size=16, weight=ft.FontWeight.BOLD, color=VERDE_BRILLO),
                ft.Text(
                    "Proyecto académico — Universidad de Cundinamarca · 2026",
                    size=12, color=GRIS_NIEBLA,
                ),
                ft.Text("built with Python + Flet", size=12, color="#4db86a66"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=GRIS_OSCURO,
        padding=ft.padding.symmetric(horizontal=60, vertical=40),
        border=ft.border.only(top=ft.BorderSide(1, "#2e8b4a1a")),
    )


# ── MAIN ──────────────────────────────────────────────────
def main(page: ft.Page):
    page.title = "CiudadActiva — Sistema de Reportes Urbanos"
    page.bgcolor = CARBON
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 1280
    page.window_min_width = 900

    page.add(
        ft.Column(
            controls=[
                navbar(),
                seccion_hero(),
                seccion_problema(),
                seccion_funcionalidades(),
                seccion_como_funciona(),
                seccion_roles(),
                seccion_categorias(),
                seccion_tecnologia(),
                seccion_cta(),
                footer(),
            ],
            spacing=0,
        )
    )


ft.app(target=main)