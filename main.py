import gurobipy as gurobi
import os
import json
import time
from collections import defaultdict


with open(os.path.join("dijsktra", "dijkstra_final_bases_a_eventos.json")) as file:
    diccionario = json.load(file)

start = time.time()
# Modelo
modelo = gurobi.Model()

# Parametros
q = 0.53
q_fo = 1 - q
ambulancias = 20
bases = 26
d = 1 # Por mientras usaremos peso 1 para todos los eventos
r = 2

# Conjunto J_i
J_i = defaultdict(list)
J_i_con_tiempos = defaultdict(list)
lista_bases = list()
conjunto_nodos = list()
for hora_del_dia in diccionario:
    for evento in diccionario[hora_del_dia]:
        for lista in diccionario[hora_del_dia][evento]:
            if lista[0] <= r:
                lista_bases.append(lista[2])
                J_i[hora_del_dia,evento].append(lista[2])
            else:
                break

lista_bases = list(set(lista_bases))
diccionario_nuevo = {}
for i, evento in enumerate(J_i):
    diccionario_nuevo[i] = J_i[evento]

with open("diccionario_modificado.json", "w") as file:
    json.dump(diccionario_nuevo, file)

J_i = diccionario_nuevo
I = range(len(J_i))
K = range(1,21)

# Variables
x = {}
binaria = [(i,k) for i in I for k in K]
y = modelo.addVars(binaria, vtype=gurobi.GRB.BINARY, name="y")
nro = 0
for j in lista_bases:
      x[j] = modelo.addVar(vtype=gurobi.GRB.INTEGER, name="x_{0}".format(nro))
      nro += 1
modelo.update()

# Restricciones
for i in J_i:
    modelo.addConstr(gurobi.quicksum(x[j] for j in J_i[i]) >= gurobi.quicksum(y[i, k] for k in K))

modelo.addConstr(gurobi.quicksum(x[j] for j in lista_bases) <= ambulancias)

# F.O
modelo.setObjective(gurobi.quicksum(d * (q_fo ** (k - 1)) * y[i,k] for i in I for k in K),
                    gurobi.GRB.MAXIMIZE)

# modelo.Params.OutputFlag = 0 hace que no veamos todas las iteraciones y solo muestre resultados
modelo.optimize()

end = time.time()

for variable in modelo.getVars():
    if variable.x >= 0.99:
        print((str(variable.varName) + " = " + str((round(variable.x, 2)))))

print("Tiempo ejecución del modelo: %s segundos" % round(float(end-start)))
