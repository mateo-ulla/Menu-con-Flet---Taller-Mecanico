
import flet as ft
import mysql.connector

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

class Herramienta_Usuario:
    def __init__(self, page, volver):
        self.page = page
        self.volver = volver
        self.conn = conectar()
        self.cursor = self.conn.cursor() if self.conn else None
        self.armar_ui()
        self.mostrar_usuarios()

    def armar_ui(self):
        self.page.clean()
        self.txt_nombre = ft.TextField(label="Nombre", width=260)
        self.txt_apellido = ft.TextField(label="Apellido", width=260)
        self.txt_usuario = ft.TextField(label="Usuario", width=260)
        self.txt_contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=260)
        self.txt_rol = ft.TextField(label="Rol", width=260)
        btn_alta = ft.ElevatedButton("Alta", on_click=self.alta)
        btn_baja = ft.ElevatedButton("Baja", on_click=self.baja)
        btn_consulta = ft.ElevatedButton("Consulta", on_click=self.consulta)
        btn_volver = ft.ElevatedButton("Volver", on_click=self.volver_menu)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Apellido")),
                ft.DataColumn(label=ft.Text("Usuario")),
                ft.DataColumn(label=ft.Text("Contraseña")),
                ft.DataColumn(label=ft.Text("Rol")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.page.add(
            ft.Text("Usuarios", size=22, weight="bold"),
            self.txt_nombre,
            self.txt_apellido,
            self.txt_usuario,
            self.txt_contraseña,
            self.txt_rol,
            ft.Row([btn_alta, btn_baja, btn_consulta, btn_volver], spacing=10),
            ft.Divider(),
            self.tabla
        )
        self.page.update()

    def mostrar_usuarios(self):
        self.tabla.rows.clear()
        if not self.cursor:
            self.page.update()
            return
        try:
            self.cursor.execute("SELECT id_usuario, nombre, apellido, usuario, contrasena, rol FROM usuarios")
            for fila in self.cursor.fetchall():
                idu = fila[0]
                self.tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idu))),
                    ft.DataCell(ft.Text(fila[1])),
                    ft.DataCell(ft.Text(fila[2])),
                    ft.DataCell(ft.Text(fila[3])),
                    ft.DataCell(ft.Text(fila[4])),
                    ft.DataCell(ft.Text(fila[5])),
                    ft.DataCell(ft.Row([
                    ft.IconButton(content=ft.Image(src="iconos/modificar.png", width=24, height=24), tooltip="Editar", on_click=lambda e, id=idu: self.cargar_editar(id)),
                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Borrar", on_click=lambda e, id=idu: self.borrar(id)),
                    ]))
                ]))
        except Exception:
            pass
        self.page.update()

    def alta(self, e):
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        usuario = self.txt_usuario.value.strip()
        contrasena = self.txt_contraseña.value.strip()
        rol = self.txt_rol.value.strip()
        if nombre and apellido and usuario and contrasena and rol:
            self.cursor.execute("SELECT usuario FROM usuarios WHERE usuario=%s", (usuario,))
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO usuarios (nombre, apellido, usuario, contrasena, rol) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, usuario, contrasena, rol))
                self.conn.commit()
        self.limpiar()
        self.mostrar_usuarios()

    def baja(self, e):
        usuario = self.txt_usuario.value.strip()
        if usuario:
            self.cursor.execute("DELETE FROM usuarios WHERE usuario=%s", (usuario,))
            self.conn.commit()
        self.limpiar()
        self.mostrar_usuarios()

    def consulta(self, e):
        usuario = self.txt_usuario.value.strip()
        if usuario:
            self.cursor.execute("SELECT nombre, apellido, contrasena, rol FROM usuarios WHERE usuario=%s", (usuario,))
            data = self.cursor.fetchone()
            if data:
                self.txt_nombre.value = data[0]
                self.txt_apellido.value = data[1]
                self.txt_contraseña.value = data[2]
                self.txt_rol.value = data[3]
                self.page.update()

    def limpiar(self, e=None):
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_usuario.value = ""
        self.txt_contraseña.value = ""
        self.txt_rol.value = ""
        self.editando = None
        self.page.update()

    def cargar_editar(self, idu):
        self.cursor.execute("SELECT nombre, apellido, usuario, contrasena, rol FROM usuarios WHERE id_usuario=%s", (idu,))
        data = self.cursor.fetchone()
        if data:
            self.txt_nombre.value = data[0]
            self.txt_apellido.value = data[1]
            self.txt_usuario.value = data[2]
            self.txt_contraseña.value = data[3]
            self.txt_rol.value = data[4]
            self.editando = idu
            self.page.update()

    def borrar(self, idu):
        self.cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (idu,))
        self.conn.commit()
        self.mostrar_usuarios()

    def volver_menu(self, e):
        self.page.clean()
        self.volver(self.page)
        self.page.update()
