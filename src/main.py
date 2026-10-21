# Sistema de registro de fiados - Bodega
# Avance: opciones 1, 2, 3 y 6

# Arreglos paralelos: la posicion i es el mismo fiado en todas las listas
codigos = []
nombres = []
productos = []
montos = []
fechas = []
fechas_pago = []
estados = []

MAX_FIADOS = 10


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
        print("No se pueden registrar mas de 10 fiados")
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

def main():
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
        elif opcion == 4 or opcion == 5:
            print("Opcion en construccion")
        elif opcion == 6:
            print("Programa finalizado")
        else:
            print("Opcion invalida")
        print()


main()