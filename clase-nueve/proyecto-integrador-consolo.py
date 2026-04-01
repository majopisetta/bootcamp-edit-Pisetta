# Este va a ser nuestra base de datos en memoria
# cada elemento de la lista es un diccionario que representa una tarea, con su título, estado de completada o no, y un ID único

db = [
    { 
        "id": 1,
        "nombre": "Maria jose,
        "apellido": "Pisetta",
        "cantidad_cursos":3
    
    }
]

def mostrar_menu():
    print("Bienvenido al sistema de gestión de alumnos")
    print("1. Agregar alumno")
    print("2. Mostrar alumnos")
    print("3. Modificar alumno")
    print("4. Eliminar alumno")
    print("5. Salir")
