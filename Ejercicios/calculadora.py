def suma(a, b):
    resultado = a + b
    return resultado

def resta(a, b):
    resultado = a - b
    return resultado

def multiplicar(a, b):
    resultado = a * b
    return resultado

def dividir(a, b):
    if b != 0:
        resultado = a / b
        return resultado
    else:
        return "Error: División por cero no permitida."
    
def menu():
    while True:
        print("operaciones matemáticas:")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Salir")
        
        opcion = input("Digite la opción que desea realizar: ")

        if opcion in ["1", "2", "3", "4"]:
            try:
                a = float(input("Ingrese el primer número: "))
                b = float(input("Ingrese el segundo número: "))
            except ValueError:
                print("Error: Ingrese solo números.")
                continue

            if opcion == "1":
                resultado = suma(a, b)
                print(f"Resultado de la suma: {resultado}")
            elif opcion == "2":
                resultado = resta(a, b)
                print(f"Resultado de la resta: {resultado}")
            elif opcion == "3":
                resultado = multiplicar(a, b)
                print(f"Resultado de la multiplicación: {resultado}")
            elif opcion == "4":
                resultado = dividir(a, b)
                print(f"Resultado de la división: {resultado}")
        elif opcion == "5":
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú
menu()