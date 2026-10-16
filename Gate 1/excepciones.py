'''
EXCEPCIONES: eventos que ocurren durante la ejecución que indican que algo impide impide el programa
try: intentar, pudiera causar error
except: si sucede ese error, haz X
raise: levantar error. lanza explícitamente una excepción
finally: ejecuta SIEMPRE sin importar si hubo o no excepción. Cerrar conexiones/archivos. Liberar recursos
else: lo que se va a ejecutar si NO hubo ningún error

SINTAXIS
try:
    #Bloque de código que quiero tratar de realizar
except Error:
    #Bloque de código que quiero que se ejecute si ocurre la excepción
'''
try:
    x = 10
    y = 0
    resultado = x / y
except ZeroDivisionError: #Error que aparece al intentar dividir entre 0
    print("No puedo dividir entre cero")

try: 
    numero = int("hola") #excepcion
    print(numero)
except ValueError:
    print("Favor de dar un numeral")

texto = "Hola clase !"
num = 22
try:
    frase = texto + num
except TypeError:
    print("Tipos de datos distintos.")

try:
    frutas = ["manzanas", "platano", "sandia"]
    print(frutas[6])
except IndexError:
    print("Fruta inexistente")

try:
    estudiante = {
        "nombre": "Pedro",
        "apellido": "Páramo"
    }
    print(estudiante["email"])
except KeyError:
    print("La clave no existe")


def dividir():
    try:
        num1 = int(input("Ingresa el primer numero: "))
        num2 = int(input("Ingresa el segundo numero: "))
        resultado = num1/num2
        print(f"El resultado es: {resultado}")
    except ZeroDivisionError:
        print("La calculadora no puede dividirte entre cero")
    except ValueError:
        print("La calculadora solo permite números enteros")
    except Exception as error: #Atrapa erores de manera general, error tendrá los detalles de la excepción
        print(f"Ocurrió un error inesperado: {error}")
    finally:
        print("¡Gracias por usas la calculadora!")

#dividir()

try:
    bebidas = ["Coca-cola", "Agua saborizada", "Chocolate Caliente"]
    bebida_deseada = input("Ingresa la bebida que quieres: ")
    if bebida_deseada not in bebidas:
        raise ValueError(f"Esa bebida no está disponible") #raise -> levantando una excepción
    else:
        print(f"Tu bebida {bebida_deseada} está lista")
except ValueError as error:
    print(f"Error: {error}")