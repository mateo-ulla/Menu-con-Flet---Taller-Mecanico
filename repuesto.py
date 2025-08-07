
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

class Herramienta_Repuesto:
    def __init__(self, page, volver):
        self.page = page
        self.volver = volver
        self.conn = conectar()
        self.cursor = self.conn.cursor() if self.conn else None
        self.armar_ui()
        self.mostrar_repuestos()

    def armar_ui(self):
        self.page.clean()
        self.txt_nombre = ft.TextField(label="Nombre", width=260)
        self.txt_precio = ft.TextField(label="Precio", width=260)
        self.txt_fabricante = ft.TextField(label="Fabricante", width=260)
        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=self.guardar)
        btn_limpiar = ft.ElevatedButton("Limpiar", icon=ft.icons.CLEAR, on_click=self.limpiar)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.icons.ARROW_BACK, on_click=self.volver_menu)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Precio")),
                ft.DataColumn(label=ft.Text("Fabricante")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.page.add(
            ft.Text("Repuestos", size=22, weight="bold"),
            self.txt_nombre,
            self.txt_precio,
            self.txt_fabricante,
            ft.Row([btn_guardar, btn_limpiar, btn_volver], spacing=10),
            ft.Divider(),
            self.tabla
        )
        self.page.update()

    def mostrar_repuestos(self):
        self.tabla.rows.clear()
        if not self.cursor:
            self.page.update()
            return
        try:
            self.cursor.execute("SELECT id, nombre, precio, fabricante FROM repuestos")
            for fila in self.cursor.fetchall():
                idr = fila[0]
                self.tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idr))),
                    ft.DataCell(ft.Text(fila[1])),
                    ft.DataCell(ft.Text(str(fila[2]))),
                    ft.DataCell(ft.Text(fila[3])),
                    ft.DataCell(ft.Row([
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, id=idr: self.cargar_editar(id)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Borrar", on_click=lambda e, id=idr: self.borrar(id)),
                    ]))
                ]))
        except Exception:
            pass
        self.page.update()

    def guardar(self, e):
        nombre = self.txt_nombre.value.strip()
        precio = self.txt_precio.value.strip()
        fabricante = self.txt_fabricante.value.strip()
        if nombre and precio and fabricante:
            if hasattr(self, 'editando') and self.editando:
                self.cursor.execute("UPDATE repuestos SET nombre=%s, precio=%s, fabricante=%s WHERE id=%s", (nombre, precio, fabricante, self.editando))
                self.conn.commit()
                self.editando = None
            else:
                self.cursor.execute("INSERT INTO repuestos (nombre, precio, fabricante) VALUES (%s, %s, %s)", (nombre, precio, fabricante))
                self.conn.commit()
            self.limpiar()
            self.mostrar_repuestos()

    def limpiar(self, e=None):
        self.txt_nombre.value = ""
        self.txt_precio.value = ""
        self.txt_fabricante.value = ""
        self.editando = None
        self.page.update()

    def cargar_editar(self, idr):
        self.cursor.execute("SELECT nombre, precio, fabricante FROM repuestos WHERE id=%s", (idr,))
        data = self.cursor.fetchone()
        if data:
            self.txt_nombre.value = data[0]
            self.txt_precio.value = str(data[1])
            self.txt_fabricante.value = data[2]
            self.editando = idr
            self.page.update()

    def borrar(self, idr):
        self.cursor.execute("DELETE FROM repuestos WHERE id=%s", (idr,))
        self.conn.commit()
        self.mostrar_repuestos()

    def volver_menu(self, e):
        self.page.clean()
        self.volver(self.page)
        self.page.update()
