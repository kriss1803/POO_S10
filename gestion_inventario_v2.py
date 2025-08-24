import os

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio:.2f}"

    # Convertir a línea para archivo
    def to_line(self):
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}\n"

    # Crear objeto desde línea de archivo
    @staticmethod
    def from_line(line):
        parts = line.strip().split(',')
        if len(parts) != 4:
            return None
        try:
            return Producto(int(parts[0]), parts[1], int(parts[2]), float(parts[3]))
        except ValueError:
            return None


class Inventario:
    FILE_NAME = "inventario.txt"

    def __init__(self):
        self.productos = []
        self.cargar_desde_archivo()

    # --- Manejo de Archivos ---
    def guardar_archivo(self):
        try:
            with open(self.FILE_NAME, "w") as f:
                for p in self.productos:
                    f.write(p.to_line())
            print("Inventario guardado correctamente en archivo.")
        except PermissionError:
            print("Error: No se puede escribir en el archivo. Verifique permisos.")

    def cargar_desde_archivo(self):
        if not os.path.exists(self.FILE_NAME):
            print("No se encontró inventario existente. Se creará uno nuevo al agregar productos.")
            return
        try:
            with open(self.FILE_NAME, "r") as f:
                for line in f:
                    producto = Producto.from_line(line)
                    if producto:
                        self.productos.append(producto)
            print(f"Inventario cargado correctamente desde '{self.FILE_NAME}'.")
        except FileNotFoundError:
            print("Archivo de inventario no encontrado. Se creará al guardar productos.")
        except PermissionError:
            print("Error: No se puede leer el archivo de inventario. Verifique permisos.")

    # --- Operaciones de Inventario ---
    def agregar_producto(self, producto):
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("Error: Ya existe un producto con ese ID.")
                return
        self.productos.append(producto)
        self.guardar_archivo()
        print("Producto agregado con éxito.")

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                self.guardar_archivo()
                print("Producto eliminado con éxito.")
                return
        print("No se encontró el producto.")

    def actualizar_producto(self, id_producto, nombre=None, cantidad=None, precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nombre is not None:
                    p.set_nombre(nombre)
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                self.guardar_archivo()
                print("Producto actualizado con éxito.")
                return
        print("No se encontró el producto.")

    def buscar_por_nombre(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("\nProductos encontrados:")
            for p in resultados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\nInventario actual:")
            for p in sorted(self.productos, key=lambda x: x.get_id()):
                print(p)


# --- Menú interactivo ---
def menu():
    inventario = Inventario()
    while True:
        print("\nSistema de Gestión de Inventario")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = int(input("ID del producto: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inventario.agregar_producto(Producto(id_producto, nombre, cantidad, precio))
                inventario.mostrar_productos()
            except ValueError:
                print("Datos inválidos, inténtelo de nuevo.")

        elif opcion == "2":
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                inventario.eliminar_producto(id_producto)
                inventario.mostrar_productos()
            except ValueError:
                print("ID inválido.")

        elif opcion == "3":
            try:
                id_producto = int(input("ID del producto a actualizar: "))
                nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
                cantidad = input("Nueva cantidad (dejar vacío para no cambiar): ")
                precio = input("Nuevo precio (dejar vacío para no cambiar): ")
                inventario.actualizar_producto(
                    id_producto,
                    nombre=nombre if nombre else None,
                    cantidad=int(cantidad) if cantidad else None,
                    precio=float(precio) if precio else None
                )
                inventario.mostrar_productos()
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "4":
            nombre = input("Nombre del producto: ")
            inventario.buscar_por_nombre(nombre)

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
