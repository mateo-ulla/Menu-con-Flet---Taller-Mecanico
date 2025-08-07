
import flet as ft
import mysql.connector
from cliente import Herramienta_Cliente
from proveedor import Herramienta_Proveedor
from repuesto import Herramienta_Repuesto
from empleado import Herramienta_Empleado
from usuario import Herramienta_Usuario

def conectar():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='mateo',
            password='1234',
            database='taller_mecanico',
        )
        if conn.is_connected():
            return conn
    except Exception:
        return None

def menu_principal(page: ft.Page):
    page.window.maximized = True
    page.title = "Taller Mecánico"
    iconos = {
        "cliente": ft.Image(src="iconos/Cliente.png", width=32, height=32),
        "proveedor": ft.Image(src="iconos/proveedor.png", width=32, height=32),
        "repuesto": ft.Image(src="iconos/caja-de-cambios.png", width=32, height=32),
        "empleado": ft.Image(src="iconos/Empleado.png", width=32, height=32),
        "usuario": ft.Image(src="iconos/usuarios.png", width=32, height=32),
        "ficha": ft.Image(src="iconos/auto.png", width=32, height=32),
        "presupuesto": ft.Image(src="iconos/Presupuesto.png", width=32, height=32)
    }
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Image(src="iconos/bandeja-de-entrada.png", width=24, height=24)),
            ft.PopupMenuItem(text="Pegar", icon=ft.Image(src="iconos/papel.png", width=24, height=24)),
            ft.PopupMenuItem(text="Salir", icon=ft.Image(src="iconos/nota-adhesiva.png", width=24, height=24), on_click=lambda e: page.window_close()),
        ],
        content=ft.Row([ft.Image(src="iconos/carpeta.png", width=24, height=24), ft.Text("Archivo")]), tooltip="Archivo"
    )
    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Row([iconos["cliente"], ft.Text("Cliente")]), on_click=lambda e: Herramienta_Cliente(page, menu_principal), tooltip="Gestión de clientes"),
            ft.PopupMenuItem(content=ft.Row([iconos["proveedor"], ft.Text("Proveedor")]), on_click=lambda e: Herramienta_Proveedor(page, menu_principal), tooltip="Gestión de proveedores"),
            ft.PopupMenuItem(content=ft.Row([iconos["repuesto"], ft.Text("Producto")]), on_click=lambda e: Herramienta_Repuesto(page, menu_principal), tooltip="Gestión de repuestos"),
            ft.PopupMenuItem(content=ft.Row([iconos["empleado"], ft.Text("Empleado")]), on_click=lambda e: Herramienta_Empleado(page, menu_principal), tooltip="Gestión de empleados"),
            ft.PopupMenuItem(content=ft.Row([iconos["usuario"], ft.Text("Usuario")]), on_click=lambda e: Herramienta_Usuario(page, menu_principal), tooltip="Gestión de usuarios"),
        ],
        content=ft.Row([ft.Image(src="iconos/gestion-de-proyectos.png", width=24, height=24), ft.Text("Herramientas")]), tooltip="Herramientas"
    )
    administracion_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Row([iconos["ficha"], ft.Text("Ficha del Vehículo")]), tooltip="Ficha técnica"),
            ft.PopupMenuItem(content=ft.Row([iconos["presupuesto"], ft.Text("Presupuesto")]), tooltip="Presupuestos"),
        ],
        content=ft.Row([ft.Image(src="iconos/Ficha.png", width=24, height=24), ft.Text("Administración")]), tooltip="Administración"
    )
    barra_menu = ft.Row([
        archivo_menu,
        herramientas_menu,
        administracion_menu
    ], alignment=ft.MainAxisAlignment.START, spacing=20)
    acceso_rapido = ft.Row([
        ft.IconButton(content=iconos["cliente"], tooltip="Clientes", on_click=lambda e: Herramienta_Cliente(page, menu_principal)),
        ft.IconButton(content=iconos["proveedor"], tooltip="Proveedores", on_click=lambda e: Herramienta_Proveedor(page, menu_principal)),
        ft.IconButton(content=iconos["repuesto"], tooltip="Repuestos", on_click=lambda e: Herramienta_Repuesto(page, menu_principal)),
        ft.IconButton(content=iconos["empleado"], tooltip="Empleados", on_click=lambda e: Herramienta_Empleado(page, menu_principal)),
        ft.IconButton(content=iconos["usuario"], tooltip="Usuarios", on_click=lambda e: Herramienta_Usuario(page, menu_principal)),
    ], alignment=ft.MainAxisAlignment.START, spacing=16)
    page.clean()
    page.add(
        ft.Container(
            content=ft.Column([
                barra_menu,
                ft.Divider(),
                acceso_rapido
            ], alignment=ft.MainAxisAlignment.START),
            padding=20
        )
    )

def main(page: ft.Page):
    menu_principal(page)

ft.app(target=main)
