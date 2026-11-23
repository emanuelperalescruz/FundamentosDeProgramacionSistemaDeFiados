
import os
import re
from datetime import datetime

# ---------- Datos en memoria (arreglos paralelos) ----------
# Fiados: la posicion i es el mismo fiado en todas las listas
codigos = []
nombres = []
productos = []
montos = []
fechas = []
fechas_pago = []
estados = []

# Stock: la posicion i es el mismo producto en las dos listas
stock_productos = []
stock_cantidades = []

MAX_FIADOS = 500

# Los archivos se guardan junto a main.py
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "fiados.txt")
ARCHIVO_STOCK = os.path.join(CARPETA, "stock.txt")


# ---------- Validaciones (barreras para datos incorrectos) ----------
def leer_opcion(mensaje, minimo, maximo):
    # Solo acepta un numero entero entre minimo y maximo
    while True:
        texto = input(mensaje).strip()
        if texto.isascii() and texto.isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print("Error: ingrese solo un numero entre", minimo, "y", maximo)


def leer_cantidad(mensaje, maximo):
    # Solo acepta un entero entre 1 y maximo
    while True:
        texto = input(mensaje).strip()
        if texto.isascii() and texto.isdigit() and 1 <= int(texto) <= maximo:
            return int(texto)
        print("Error: ingrese solo un numero entero entre 1 y", maximo)


def leer_monto(mensaje):
    # Solo acepta numeros mayores que cero, con maximo 2 decimales (9.50 o 9,50)
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        partes = texto.split(".")
        valido = False
        if texto.isascii():
            if len(partes) == 1 and partes[0].isdigit():
                valido = True
            elif len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit() and len(partes[1]) <= 2:
                valido = True
        if valido and float(texto) > 0:
            return round(float(texto), 2)
        print("Error: ingrese solo numeros mayores que cero, sin letras ni simbolos. Ejemplo: 9.50")

def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Error: responda con s o n")


def leer_codigo(mensaje):
    # Solo letras y numeros, sin espacios ni simbolos. Siempre en mayusculas
    while True:
        codigo = input(mensaje).strip().upper()
        if codigo != "" and codigo.isascii() and codigo.isalnum():
            return codigo
        print("Error: el codigo solo puede tener letras y numeros, sin espacios ni simbolos. Ejemplo: C01")


def leer_nombre(mensaje):
    # Solo letras y espacios
    while True:
        nombre = input(mensaje).strip()
        if nombre != "" and nombre.replace(" ", "").isalpha():
            return " ".join(nombre.split()).title()
        print("Error: el nombre solo puede tener letras y espacios")


def leer_producto(mensaje):
    # Solo letras, numeros y espacios
    while True:
        producto = input(mensaje).strip()
        if producto != "" and producto.replace(" ", "").isalnum():
            return " ".join(producto.split()).title()
        print("Error: el producto solo puede tener letras, numeros y espacios")


def fecha_hora_actual():
    # Fecha y hora exactas del momento del registro
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def buscar_en(lista, valor):
    # Devuelve la posicion del valor en la lista, o -1 si no existe
    for i in range(len(lista)):
        if lista[i] == valor:
            return i
    return -1

# ---------- Archivos ----------
def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for i in range(len(codigos)):
            linea = "|".join([codigos[i], nombres[i], productos[i], str(montos[i]),
                              fechas[i], fechas_pago[i], estados[i]])
            f.write(linea + "\n")


def cargar_datos():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 7:
                    try:
                        monto = float(partes[3])
                    except ValueError:
                        continue
                    codigos.append(partes[0])
                    nombres.append(partes[1])
                    productos.append(partes[2])
                    montos.append(monto)
                    fechas.append(partes[4])
                    fechas_pago.append(partes[5])
                    estados.append(partes[6])
    except FileNotFoundError:
        pass  # primera vez: todavia no existe el archivo


def guardar_stock():
    with open(ARCHIVO_STOCK, "w", encoding="utf-8") as f:
        for i in range(len(stock_productos)):
            f.write(stock_productos[i] + "|" + str(stock_cantidades[i]) + "\n")


def cargar_stock():
    try:
        with open(ARCHIVO_STOCK, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 2 and partes[1].isdigit():
                    stock_productos.append(partes[0])
                    stock_cantidades.append(int(partes[1]))
    except FileNotFoundError:
        pass


# ---------- Menu ----------
def mostrar_menu():
    print("======================================")
    print("       SISTEMA DE REGISTRO DE FIADOS")
    print("======================================")
    print("1. Registrar fiado")
    print("2. Buscar cliente por codigo")
    print("3. Listar clientes pendientes")
    print("4. Ordenar clientes por deuda")
    print("5. Registrar pago")
    print("6. Anadir stock")
    print("7. Ver stock")
    print("8. Salir")


# ---------- Stock ----------
def buscar_producto(nombre):
    # Devuelve la posicion del producto en el stock, o -1 si no existe
    for i in range(len(stock_productos)):
        if stock_productos[i].lower() == nombre.lower():
            return i
    return -1


def anadir_stock():
    print("----- ANADIR STOCK -----")
    producto = leer_producto("Ingrese el nombre del producto: ")
    cantidad = leer_cantidad("Ingrese la cantidad a agregar: ", 100000)

    pos = buscar_producto(producto)
    if pos == -1:
        stock_productos.append(producto)
        stock_cantidades.append(cantidad)
        print("Producto nuevo agregado:", producto)
        print("Stock actual:", cantidad)
    else:
        stock_cantidades[pos] = stock_cantidades[pos] + cantidad
        print("Stock actualizado:", stock_productos[pos])
        print("Stock actual:", stock_cantidades[pos])

    guardar_stock()


def ver_stock():
    print("----- STOCK DE LA TIENDA -----")

    if len(stock_productos) == 0:
        print("No hay productos en stock")
        return

    for i in range(len(stock_productos)):
        if stock_cantidades[i] > 0:
            print(str(i + 1) + ".", stock_productos[i], "- cantidad:", stock_cantidades[i])
        else:
            print(str(i + 1) + ".", stock_productos[i], "- AGOTADO")


def hay_stock_disponible():
    for i in range(len(stock_cantidades)):
        if stock_cantidades[i] > 0:
            return True
    return False


# ---------- Fiados ----------
def registrar_fiado():
    print("----- REGISTRAR FIADO -----")

    if len(codigos) >= MAX_FIADOS:
        print("No se pueden registrar mas de", MAX_FIADOS, "fiados")
        return

    if not hay_stock_disponible():
        print("No hay productos disponibles en el stock.")
        print("Primero use la opcion 6 (Anadir stock)")
        return

    codigo = leer_codigo("Ingrese el codigo del cliente: ")

    # Si el cliente ya existe, se usa su nombre registrado (evita nombres distintos)
    pos = buscar_en(codigos, codigo)
    if pos != -1:
        nombre = nombres[pos]
        print("Cliente ya registrado:", nombre)
    else:
        nombre = leer_nombre("Ingrese el nombre del cliente: ")

    if not leer_si_no("El cliente es confiable? (s/n): "):
        print("No se registro el fiado porque el cliente no fue considerado confiable")
        return

    # Elegir los productos del stock (todavia no se descuenta nada)
    elegidos = []      # posicion del producto en el stock
    cantidades = []    # cantidad que se llevo
    seguir = True
    while seguir:
        disponibles = []   # posiciones del stock que todavia tienen unidades libres
        libres = []        # unidades libres de cada una
        print("Productos disponibles:")
        for i in range(len(stock_productos)):
            reservado = 0
            for k in range(len(elegidos)):
                if elegidos[k] == i:
                    reservado = reservado + cantidades[k]
            libre = stock_cantidades[i] - reservado
            if libre > 0:
                disponibles.append(i)
                libres.append(libre)
                print(str(len(disponibles)) + ".", stock_productos[i], "- disponible:", libre)

        if len(disponibles) == 0:
            print("Ya no quedan mas productos disponibles")
            break

        eleccion = leer_opcion("Elija el producto (numero): ", 1, len(disponibles))
        maximo = libres[eleccion - 1]
        cantidad = leer_cantidad("Cantidad (1 a " + str(maximo) + "): ", maximo)

        elegidos.append(disponibles[eleccion - 1])
        cantidades.append(cantidad)

        seguir = leer_si_no("Agregar otro producto? (s/n): ")

    monto = leer_monto("Ingrese el monto del fiado (S/): ")

    # Todo validado: recien ahora se descuenta el stock y se guarda el fiado
    texto_productos = ""
    for k in range(len(elegidos)):
        stock_cantidades[elegidos[k]] = stock_cantidades[elegidos[k]] - cantidades[k]
        if texto_productos != "":
            texto_productos = texto_productos + ", "
        texto_productos = texto_productos + str(cantidades[k]) + " x " + stock_productos[elegidos[k]]

    fecha = fecha_hora_actual()

    codigos.append(codigo)
    nombres.append(nombre)
    productos.append(texto_productos)
    montos.append(monto)
    fechas.append(fecha)
    fechas_pago.append("Sin pagos")
    estados.append("Pendiente")

    print("Fiado registrado correctamente")
    print("Codigo:", codigo)
    print("Cliente:", nombre)
    print("Productos:", texto_productos)
    print("Monto:", monto)
    print("Fecha y hora:", fecha)
    print("Estado: Pendiente")

    guardar_datos()
    guardar_stock()


def buscar_cliente():
    print("----- BUSCAR CLIENTE -----")

    if len(codigos) == 0:
        print("No hay clientes registrados")
        return

    codigo = leer_codigo("Ingrese el codigo del cliente: ")
    encontrado = False
    deuda_total = 0

    for i in range(len(codigos)):
        if codigos[i] == codigo:
            encontrado = True
            print("----------------------------------")
            print("Cliente:", nombres[i])
            print("Codigo:", codigos[i])
            print("Productos:", productos[i])
            print("Fecha del fiado:", fechas[i])
            print("Deuda de este fiado:", montos[i])
            print("Estado:", estados[i])
            print("Fecha del ultimo pago:", fechas_pago[i])

            if estados[i] == "Pendiente":
                deuda_total = deuda_total + montos[i]

    if encontrado:
        print("==================================")
        print("DEUDA TOTAL PENDIENTE:", round(deuda_total, 2))
    else:
        print("Cliente no encontrado")


def listar_pendientes():
    print("----- CLIENTES PENDIENTES -----")

    if len(codigos) == 0:
        print("No hay clientes registrados")
        return

    encontrado = False

    for i in range(len(codigos)):
        if estados[i] == "Pendiente" and montos[i] > 0:
            encontrado = True
            print("----------------------------------")
            print("Codigo:", codigos[i])
            print("Cliente:", nombres[i])
            print("Productos:", productos[i])
            print("Deuda:", montos[i])
            print("Fecha del fiado:", fechas[i])

    if not encontrado:
        print("No hay deudas pendientes")


def ordenar_por_deuda():
    print("----- ORDENAR POR DEUDA TOTAL -----")

    if len(codigos) == 0:
        print("No hay clientes registrados")
        return

    # 1. Clientes unicos (sin repetir codigos)
    codigos_u = []
    nombres_u = []
    for i in range(len(codigos)):
        if codigos[i] not in codigos_u:
            codigos_u.append(codigos[i])
            nombres_u.append(nombres[i])

    # 2. Deuda pendiente de cada cliente
    deudas_u = []
    for c in codigos_u:
        deuda = 0
        for j in range(len(codigos)):
            if codigos[j] == c and estados[j] == "Pendiente":
                deuda = deuda + montos[j]
        deudas_u.append(round(deuda, 2))

    # 3. Ordenar de mayor a menor (burbuja)
    n = len(codigos_u)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if deudas_u[j] < deudas_u[j + 1]:
                deudas_u[j], deudas_u[j + 1] = deudas_u[j + 1], deudas_u[j]
                codigos_u[j], codigos_u[j + 1] = codigos_u[j + 1], codigos_u[j]
                nombres_u[j], nombres_u[j + 1] = nombres_u[j + 1], nombres_u[j]

    # 4. Mostrar
    print("Clientes ordenados de mayor a menor deuda:")
    for i in range(n):
        print("----------------------------------")
        print("Codigo:", codigos_u[i])
        print("Cliente:", nombres_u[i])
        print("Deuda total pendiente:", deudas_u[i])


def registrar_pago():
    print("----- REGISTRAR PAGO -----")

    if len(codigos) == 0:
        print("No hay clientes registrados")
        return

    codigo = leer_codigo("Ingrese el codigo del cliente: ")
    encontrado = False
    deuda_total = 0

    for i in range(len(codigos)):
        if codigos[i] == codigo:
            encontrado = True
            if estados[i] == "Pendiente":
                deuda_total = deuda_total + montos[i]
    deuda_total = round(deuda_total, 2)

    if not encontrado:
        print("Cliente no encontrado")
        return

    if deuda_total == 0:
        print("El cliente no tiene deudas pendientes")
        return

    print("Deuda total pendiente:", deuda_total)
    pago = leer_monto("Ingrese el monto del pago (S/): ")

    if pago > deuda_total:
        print("El pago no puede superar la deuda total")
        return

    fecha_pago = fecha_hora_actual()

    # El pago se descuenta de los fiados pendientes, en orden
    restante = pago
    for i in range(len(codigos)):
        if codigos[i] == codigo and estados[i] == "Pendiente" and restante > 0:
            if restante >= montos[i]:
                restante = round(restante - montos[i], 2)
                montos[i] = 0
                estados[i] = "Pagado"
                fechas_pago[i] = fecha_pago
            else:
                montos[i] = round(montos[i] - restante, 2)
                restante = 0
                fechas_pago[i] = fecha_pago

    # Deuda que le queda
    deuda_total = 0
    for i in range(len(codigos)):
        if codigos[i] == codigo and estados[i] == "Pendiente":
            deuda_total = deuda_total + montos[i]
    deuda_total = round(deuda_total, 2)

    print("Pago registrado correctamente")
    print("Monto abonado:", pago)
    print("Fecha y hora del pago:", fecha_pago)
    print("Deuda restante:", deuda_total)

    if deuda_total == 0:
        print("Todas las deudas del cliente estan pagadas")
    else:
        print("El cliente aun tiene deudas pendientes")

    guardar_datos()


# ---------- Programa principal ----------
def main():
    cargar_datos()
    cargar_stock()
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = leer_opcion("Seleccione una opcion del 1 al 8: ", 1, 8)

        if opcion == 1:
            registrar_fiado()
        elif opcion == 2:
            buscar_cliente()
        elif opcion == 3:
            listar_pendientes()
        elif opcion == 4:
            ordenar_por_deuda()
        elif opcion == 5:
            registrar_pago()
        elif opcion == 6:
            anadir_stock()
        elif opcion == 7:
            ver_stock()
        elif opcion == 8:
            print("Programa finalizado")
        print()


main()
