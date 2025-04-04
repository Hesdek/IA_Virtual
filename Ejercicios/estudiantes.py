def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Agregar nuevo estudiante")
    print("2. Calcular promedio de calificaciones")
    print("3. Mostrar estudiantes con promedio mayor a X")
    print("4. Buscar estudiantes por nombre")
    print("5. Salir")
    return input("Seleccione una opción: ")

def agregar_estudiante(estudiantes):
    nombre = input("Nombre del estudiante: ")
    edad = int(input("Edad del estudiante: "))
    calificaciones = []
    
    while True:
        calif = input("Ingrese calificación (o 'fin' para terminar): ")
        if calif.lower() == 'fin':
            break
        try:
            calificaciones.append(float(calif))
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    estudiantes.append({
        'nombre': nombre,
        'edad': edad,
        'calificaciones': calificaciones
    })
    print(f"Estudiante {nombre} agregado correctamente.")

def calcular_promedio(calificaciones):
    if not calificaciones:
        return 0
    return sum(calificaciones) / len(calificaciones)

def mostrar_promedios(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
        
    print("\nPromedios de calificaciones:")
    for est in estudiantes:
        promedio = calcular_promedio(est['calificaciones'])
        print(f"{est['nombre']}: {promedio:.2f}")

def filtrar_por_promedio(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
        
    try:
        minimo = float(input("Ingrese el promedio mínimo: "))
        print(f"\nEstudiantes con promedio mayor a {minimo}:")
        
        encontrados = False
        for est in estudiantes:
            promedio = calcular_promedio(est['calificaciones'])
            if promedio > minimo:
                print(f"{est['nombre']} - Edad: {est['edad']} - Promedio: {promedio:.2f}")
                encontrados = True
        
        if not encontrados:
            print("No se encontraron estudiantes con ese promedio.")
    except ValueError:
        print("Por favor ingrese un número válido.")

def buscar_por_nombre(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
        
    busqueda = input("Ingrese nombre o parte del nombre a buscar: ").lower()
    encontrados = [est for est in estudiantes if busqueda in est['nombre'].lower()]
    
    if encontrados:
        print("\nEstudiantes encontrados:")
        for est in encontrados:
            promedio = calcular_promedio(est['calificaciones'])
            print(f"Nombre: {est['nombre']} - Edad: {est['edad']} - Promedio: {promedio:.2f}")
    else:
        print("No se encontraron estudiantes con ese nombre.")

def main():
    estudiantes = []
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            agregar_estudiante(estudiantes)
        elif opcion == "2":
            mostrar_promedios(estudiantes)
        elif opcion == "3":
            filtrar_por_promedio(estudiantes)
        elif opcion == "4":
            buscar_por_nombre(estudiantes)
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor seleccione 1-5.")

if __name__ == "__main__":
    main()