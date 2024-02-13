import example_cy
import example_py
import time

x=100000000
#Ejecucion con cython
inicio=time.time()
example_cy.test(x)
final=time.time()
tiempo=final-inicio
print("tiempo cython")
print(tiempo)

#Ejecucion con cython
inicio=time.time()
example_py.test(x)
final=time.time()
tiempo=final-inicio
print("tiempo python")
print(tiempo)
