
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

class Herramienta_Cliente:
    def __init__(self, page, volver):
        self.page = page
        self.volver = volver
        self.conn = conectar()
        self.cursor = self.conn.cursor() if self.conn else None
        self.armar_ui()
        self.mostrar_clientes()

    def armar_ui(self):
        self.page.clean()
        self.txt_dni = ft.TextField(label="DNI", width=260)
        self.txt_nombre = ft.TextField(label="Nombre", width=260)
        self.txt_apellido = ft.TextField(label="Apellido", width=260)
        self.txt_direccion = ft.TextField(label="Dirección", width=260)
        self.txt_telefono = ft.TextField(label="Teléfono", width=260)
        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=self.guardar)
        btn_limpiar = ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR, on_click=self.limpiar)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.icons.ARROW_BACK, on_click=self.volver_menu)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("DNI")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Apellido")),
                ft.DataColumn(label=ft.Text("Dirección")),
                ft.DataColumn(label=ft.Text("Teléfono")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.page.add(
            ft.Text("Clientes", size=22, weight="bold"),
            self.txt_dni,
            self.txt_nombre,
            self.txt_apellido,
            self.txt_direccion,
            self.txt_telefono,
            ft.Row([btn_guardar, btn_limpiar, btn_volver], spacing=10),
            ft.Divider(),
            self.tabla
        )
        self.page.update()

    def mostrar_clientes(self):
        self.tabla.rows.clear()
        if not self.cursor:
            self.page.update()
            return
        try:
            self.cursor.execute("SELECT DNI, Nombre, Apellido, Direccion, Telefono FROM clientes")
            for fila in self.cursor.fetchall():
                dni = fila[0]
                self.tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(dni))),
                    ft.DataCell(ft.Text(fila[1])),
                    ft.DataCell(ft.Text(fila[2])),
                    ft.DataCell(ft.Text(fila[3])),
                    ft.DataCell(ft.Text(fila[4])),
                    ft.DataCell(ft.Row([
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, id=dni: self.cargar_editar(id)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Borrar", on_click=lambda e, id=dni: self.borrar(id)),
                    ]))
                ]))
        except Exception:
            pass
        self.page.update()

    def guardar(self, e):
        dni = self.txt_dni.value.strip()
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        direccion = self.txt_direccion.value.strip()
        telefono = self.txt_telefono.value.strip()
        if dni and nombre and apellido and direccion and telefono:
            if hasattr(self, 'editando') and self.editando:
                self.cursor.execute("UPDATE clientes SET Nombre=%s, Apellido=%s, Direccion=%s, Telefono=%s WHERE DNI=%s", (nombre, apellido, direccion, telefono, self.editando))
                self.conn.commit()
                self.editando = None
            else:
                self.cursor.execute("INSERT INTO clientes (DNI, Nombre, Apellido, Direccion, Telefono) VALUES (%s, %s, %s, %s, %s)", (dni, nombre, apellido, direccion, telefono))
                self.conn.commit()
            self.limpiar()
            self.mostrar_clientes()

    def limpiar(self, e=None):
        self.txt_dni.value = ""
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_direccion.value = ""
        self.txt_telefono.value = ""
        self.editando = None
        self.page.update()

    def cargar_editar(self, dni):
        self.cursor.execute("SELECT Nombre, Apellido, Direccion, Telefono FROM clientes WHERE DNI=%s", (dni,))
        data = self.cursor.fetchone()
        if data:
            self.txt_nombre.value = data[0]
            self.txt_apellido.value = data[1]
            self.txt_direccion.value = data[2]
            self.txt_telefono.value = data[3]
            self.editando = dni
            self.page.update()

    def borrar(self, dni):
        self.cursor.execute("DELETE FROM clientes WHERE DNI=%s", (dni,))
        self.conn.commit()
        self.mostrar_clientes()

    def volver_menu(self, e):
        self.page.clean()
        self.volver(self.page)
        self.page.update()