# Este va a ser nuestra base de datos en memoria
# cada elemento de la lista es un diccionario que representa una tarea, con su título, estado de completada o no, y un ID único

db = [
    { 
        "id": 1,
        "nombre": "Maria jose",
        "apellido": "Pisetta",
        "cantidad_cursos":3
    
    }
]

def leer_texto(mensaje: str) -> str:
    while True:
        valor = input(mensaje)
        if valor.strip():
            return valor
        print("Este campo no puede estar vacío. Por favor, ingrese un valor.")

def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

def leer_texto_o_actual(mensaje: str, actual: str) -> str:
    valor = input(f"{mensaje} (actual: {actual}, Enter para conservar): ")
    return valor if valor.strip() else actual

def leer_entero_o_actual(mensaje: str, actual: int) -> int:
    while True:
        entrada = input(f"{mensaje} (actual: {actual}, Enter para conservar): ")
        if not entrada.strip():
            return actual
        try:
            return int(entrada)
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

def mostrar_menu():
    print("Bienvenido al sistema de gestión de alumnos")
    print("1. Agregar alumno")
    print("2. Mostrar alumnos")
    print("3. Modificar alumno")
    print("4. Eliminar alumno")
    print("5. Salir")

def agregar_alumno(db: list):
    nombre = leer_texto("Ingrese el nombre del alumno: ")
    apellido = leer_texto("Ingrese el apellido del alumno: ")
    cantidad_cursos = leer_entero("Ingrese la cantidad de cursos que ha tomado el alumno: ")
    
    # Generar un nuevo ID para el alumno
    # El siguiente ejemplo usa comprensión de listas para encontrar el ID máximo actual y le suma 1
    nuevo_id = max(alumno["id"] for alumno in db) + 1 if db else 1
    
    nuevo_alumno = {
        "id": nuevo_id,
        "nombre": nombre,
        "apellido": apellido,
        "cantidad_cursos": cantidad_cursos
    }
    
    # Funcion para mostrar todos los alumnos en la base de datos
def mostrar_alumnos(db: list):
    if not db:
        print("No hay alumnos registrados.")
        return
    
    print("Lista de alumnos:")
    for alumno in db:
        print(f"ID: {alumno['id']}, Nombre: {alumno['nombre']} {alumno['apellido']}, Cursos: {alumno['cantidad_cursos']}")

def eliminar_alumno(db: list):
    id_alumno = leer_entero("Ingrese el ID del alumno a eliminar: ")
    for alumno in db:
        if alumno["id"] == id_alumno:
            db.remove(alumno)
            print(f"Alumno con ID {id_alumno} eliminado.")
            return
    print(f"No se encontró un alumno con ID {id_alumno}.")

def modificar_alumno(db: list):
    id_alumno = leer_entero("Ingrese el ID del alumno que desea modificar: ")
    for alumno in db:
        if alumno["id"] == id_alumno:
            print("(Presione Enter sin escribir nada para conservar el valor actual de cada campo)")
            nombre = leer_texto_o_actual("Ingrese el nuevo nombre del alumno", alumno['nombre'])
            apellido = leer_texto_o_actual("Ingrese el nuevo apellido del alumno", alumno['apellido'])
            cantidad_cursos = leer_entero_o_actual("Ingrese la nueva cantidad de cursos", alumno['cantidad_cursos'])
            
            alumno["nombre"] = nombre
            alumno["apellido"] = apellido
            alumno["cantidad_cursos"] = cantidad_cursos
            
            print(f"Alumno con ID {id_alumno} modificado con éxito.")
            return
    print(f"No se encontró un alumno con ID {id_alumno}.")

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        agregar_alumno(db)
    elif opcion == "2":
        mostrar_alumnos(db)
    elif opcion == "3":
        modificar_alumno(db)
    elif opcion == "4":
        eliminar_alumno(db)
    elif opcion == "5":
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")    
        