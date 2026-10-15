def suma(a, b): #a = 5, b = 6
    resultado = a + b
    return resultado #return: devuelve un valor de retorno




#print(suma(5, 6))


#JSON: JavaScript Object Notation
curso = {
    "nombre": "Especialización de IA",
    "horas": 180,
    "estudiantes": [
       {
        "nombre": "Juana",
        "apellido": "De Arco"
       },
       {
        "nombre": "Pedro",
        "apellido": "Páramo"
       }
    ]
}

estudiante = {
    "nombre": "Ana",
    "edad": 24,
    "curso": {
        "nombre": "Python",
        "calificacion": 92
    },
    "tareas": [
        {
            "titulo": "Variables",
            "completada": True
        },
        {
            "titulo": "Consumo de APIs",
            "completada": False
        }
    ]
}

print(estudiante["nombre"]) #El nombre de la estudiante
print(estudiante["curso"]["calificacion"]) #La calificación del curso
print(estudiante["tareas"][1]["titulo"]) #El titulo de la segunda tarea
print(estudiante["tareas"][0]["completada"]) #Si la primera tarea está completada
if estudiante["tareas"][0]["completada"]:
    print("La primera tarea esta completada")

print("La primera tarea esta completada" if estudiante["tareas"][0]["completada"] else "No esta")

#console.log(condicion ? "Si se cumple" : "No se cumple")