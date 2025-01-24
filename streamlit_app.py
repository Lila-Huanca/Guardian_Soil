import streamlit as st

class Producto:
    def __init__(self, nombre, categoria, precio, variacion=None):
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.variacion = variacion if variacion else {}

    def __str__(self):
        return f"{self.nombre} ({self.categoria}) - Precio: {self.precio}€"


class Carrito:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto, cantidad):
        if producto.nombre in self.productos:
            self.productos[producto.nombre]["cantidad"] += cantidad
        else:
            self.productos[producto.nombre] = {"producto": producto, "cantidad": cantidad}

    def mostrar_carrito(self):
        if not self.productos:
            st.warning("El carrito está vacío.")
        else:
            st.subheader("Productos en el carrito:")
            for nombre, datos in self.productos.items():
                producto = datos["producto"]
                cantidad = datos["cantidad"]
                st.write(f"- {producto.nombre}: {cantidad} unidades, Total: {producto.precio * cantidad:.2f}€")

    def calcular_total(self):
        return sum(datos["producto"].precio * datos["cantidad"] for datos in self.productos.values())


class Promo:
    @staticmethod
    def aplicar_descuento(carrito, porcentaje_descuento):
        total = carrito.calcular_total()
        descuento = 0
        if len(carrito.productos) > 3:
            descuento = total * (porcentaje_descuento / 100)
            total -= descuento
            st.success(f"Descuento aplicado: {descuento:.2f}€")
        return total


class Envio:
    def __init__(self):
        self.igv = 0.05

    def calcular_costo_envio(self, total, metodo_envio):
        if metodo_envio == "domicilio":
            total += total * self.igv
            st.info(f"Se ha añadido un IGV del 5%. Total final: {total:.2f}€")
        else:
            st.info("Has elegido recoger en tienda. No se aplican cargos adicionales.")
        return total


def seleccionar_producto():
    opciones = {
        "alimentos": {
            "Manzana": 1,
            "Pera": 1.5,
            "Papaya": 2
        },
        "ropa": {
            "Polos": 20,
            "Shorts": 15,
            "Pantalones": 25
        },
        "tecnologia": {
            "Teléfono": {"Samsung": 600, "Apple": 1200, "Huawei": 400},
            "Refrigeradora": 1200,
            "Computadora": 800
        }
    }

    categoria = st.selectbox("Seleccione la categoría del producto:", ["alimentos", "ropa", "tecnologia"])

    if categoria:
        producto_elegido = st.selectbox(f"¿Qué {categoria} desea comprar?", opciones[categoria].keys())

        if producto_elegido:
            if categoria == "ropa":
                talla = st.selectbox("¿Qué talla desea?", ["S", "M", "L", "XL"])
                precio_base = opciones[categoria][producto_elegido]
                precio_talla = {"S": 0, "M": 2, "L": 4, "XL": 6}
                precio_final = precio_base + precio_talla.get(talla, 0)
                return Producto(f"{producto_elegido} talla {talla.upper()}", categoria, precio_final)

            elif categoria == "tecnologia" and producto_elegido == "Teléfono":
                marca = st.selectbox("¿Qué marca prefiere?", ["Samsung", "Apple", "Huawei"])
                if marca:
                    precio = opciones[categoria][producto_elegido][marca]
                    return Producto(f"Teléfono {marca}", categoria, precio)

            else:
                return Producto(producto_elegido, categoria, opciones[categoria][producto_elegido])

    return None


def main():
    st.title("Tienda en Línea")
    st.subheader("¡Bienvenido a nuestra tienda en línea!")

    cliente_nombre = st.text_input("Ingrese su nombre:")
    if cliente_nombre:
        st.success(f"¡Hola, {cliente_nombre}!")

        carrito = Carrito()

        while True:
            st.subheader("Seleccione los productos:")
            producto_seleccionado = seleccionar_producto()
            if producto_seleccionado:
                cantidad = st.number_input(f"¿Cuántas unidades de {producto_seleccionado.nombre} desea agregar?", min_value=1, step=1)
                if st.button(f"Agregar {producto_seleccionado.nombre} al carrito"):
                    carrito.agregar_producto(producto_seleccionado, cantidad)

            if st.button("Finalizar compra"):
                break

        carrito.mostrar_carrito()

        if len(carrito.productos) > 0:
            promo = Promo()
            total_con_descuento = promo.aplicar_descuento(carrito, 10)

            envio = Envio()
            metodo_envio = st.selectbox("Seleccione el método de envío:", ["tienda", "domicilio"])
            total_final = envio.calcular_costo_envio(total_con_descuento, metodo_envio)

            metodo_pago = st.selectbox("Seleccione el método de pago:", ["Tarjeta", "Paypal", "Efectivo"])
            if st.button("Confirmar compra"):
                st.success(f"Gracias por su compra, {cliente_nombre}. Ha elegido pagar con {metodo_pago}. Total: {total_final:.2f}€.")


if __name__ == "__main__":
    main()
