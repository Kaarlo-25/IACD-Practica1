""""""

try:
    if int("f").is_integer():
        print("Es posible")
except ValueError:
    print("No es")