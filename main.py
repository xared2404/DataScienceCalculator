from modulos.aritmetica import raiz_cuadrada

def menu():
    while True:
        print("\n=== Calculadora Matemática ===")
        print("Aritmética")
        print("1.- Calcular la raiz cuadrada")
        print("Salir: Ctrl + D")
        
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            valor = float(input("Ingresa el valor al que quieres calcular la raiz: "))
            print(f"La raiz cuadrada de {valor} es {raiz_cuadrada(valor)}")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
