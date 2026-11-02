import os

# Sistema de registro de fiados - Bodega

# Arreglos paralelos: la posicion i es el mismo fiado en todas las listas
codigos = []
nombres = []
productos = []
montos = []
fechas = []
fechas_pago = []
estados = []

MAX_FIADOS = 67
ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fiados.txt")


def mostrar_menu():
    print("======================================")
    print("       SISTEMA DE REGISTRO DE FIADOS")
    print("======================================")
    print("1. Registrar fiado")
    print("2. Buscar cliente por codigo")
    print("3. Listar clientes pendientes")
    print("4. Ordenar clientes por deuda")
    print("5. Registrar pago")
    print("6. Salir")

def registrar_fiado():
    print("----- REGISTRAR FIADO -----")

    if len(codigos) >= MAX_FIADOS:
        print("No se pueden registrar mas de", MAX_FIADOS, "fiados")
        return

    codigo = input("Ingrese el codigo del cliente: ")
    nombre = input("Ingrese el nombre del cliente: ")
    producto = input("Ingrese los productos: ")
    fecha = input("Ingrese la fecha del fiado (dd/mm/aaaa): ")
    confiable = input("El cliente es confiable? (s/n): ").lower()

    if confiable != "s" and confiable != "si":
        print("No se registro el fiado porque el cliente no fue considerado confiable")
        return

    monto = float(input("Ingrese el monto del fiado: "))

    if monto <= 0:
        print("Error: el monto debe ser mayor que cero")
        return

    # Todo bien validado xd: se guarda en las 7 listas a la vez
    codigos.append(codigo)
    nombres.append(nombre)
    productos.append(producto)
    montos.append(monto)
    fechas.append(fecha)
    fechas_pago.append("Sin pagos")
    estados.append("Pendiente")

    print("Fiado registrado correctamente")
    print("Codigo:", codigo)
    print("Cliente:", nombre)
    print("Monto:", monto)
    print("Estado: Pendiente")

    guardar_datos()

def buscar_cliente():
    print("----- BUSCAR CLIENTE -----")

    if len(codigos) == 0:
        print("No hay clientes registrados")
        return

    codigo = input("Ingrese el codigo del cliente: ")
    encontrado = False
    deuda_total = 0

    for i in range(len(codigos)):
        if codigos[i] == codigo:
            encontrado = True
            print("----------------------------------")
            print("Cliente:", nombres[i])
            print("Codigo:", codigos[i])
            print("Producto:", productos[i])
            print("Fecha del fiado:", fechas[i])
            print("Deuda de este fiado:", montos[i])
            print("Estado:", estados[i])
            print("Fecha del ultimo pago:", fechas_pago[i])

            if estados[i] == "Pendiente":
                deuda_total = deuda_total + montos[i]

    if encontrado:
        print("==================================")
        print("DEUDA TOTAL PENDIENTE:", deuda_total)
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
            print("Producto:", productos[i])
            print("Deuda:", montos[i])
            print("Fecha del fiado:", fechas[i])

    if not encontrado:
        print("No hay deudas pendientes")

def ordenar_por_deuda():
    print("----- ORDENAR POR DEUDA TOTAL -----")

    if len(codigos) == 0:
        print("No hay clientes registrados")
        return

    codigos_u = []
    nombres_u = []
    for i in range(len(codigos)):
        if codigos[i] not in codigos_u:
            codigos_u.append(codigos[i])
            nombres_u.append(nombres[i])

    deudas_u = []
    for c in codigos_u:
        deuda = 0
        for j in range(len(codigos)):
            if codigos[j] == c and estados[j] == "Pendiente":
                deuda = deuda + montos[j]
        deudas_u.append(round(deuda, 2))

    n = len(codigos_u)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if deudas_u[j] < deudas_u[j + 1]:
                deudas_u[j], deudas_u[j + 1] = deudas_u[j + 1], deudas_u[j]
                codigos_u[j], codigos_u[j + 1] = codigos_u[j + 1], codigos_u[j]
                nombres_u[j], nombres_u[j + 1] = nombres_u[j + 1], nombres_u[j]

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

    codigo = input("Ingrese el codigo del cliente: ")
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
    pago = float(input("Ingrese el monto del pago: "))

    if pago <= 0:
        print("El pago debe ser mayor que cero")
        return

    if pago > deuda_total:
        print("El pago no puede superar la deuda total")
        return

    fecha_pago = input("Ingrese la fecha del pago (dd/mm/aaaa): ")

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

    deuda_total = 0
    for i in range(len(codigos)):
        if codigos[i] == codigo and estados[i] == "Pendiente":
            deuda_total = deuda_total + montos[i]
    deuda_total = round(deuda_total, 2)

    print("Pago registrado correctamente")
    print("Monto abonado:", pago)
    print("Deuda restante:", deuda_total)

    if deuda_total == 0:
        print("Todas las deudas del cliente estan pagadas")
    else:
        print("El cliente aun tiene deudas pendientes")

    guardar_datos()

def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for i in range(len(codigos)):
            linea = (codigos[i] + "|" + nombres[i] + "|" + productos[i] + "|" +
                     str(montos[i]) + "|" + fechas[i] + "|" +
                     fechas_pago[i] + "|" + estados[i])
            f.write(linea + "\n")


def cargar_datos():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 7:
                    codigos.append(partes[0])
                    nombres.append(partes[1])
                    productos.append(partes[2])
                    montos.append(float(partes[3]))
                    fechas.append(partes[4])
                    fechas_pago.append(partes[5])
                    estados.append(partes[6])
    except FileNotFoundError:
        pass  # primera vez: todavia no existe el archivo

def main():
    cargar_datos()
    opcion = 0
    while opcion != 6:
        mostrar_menu()
        opcion = int(input("Seleccione una opcion del 1 al 6: "))

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
            print("Programa finalizado")
        else:
            print("Opcion invalida")
        print()


main()