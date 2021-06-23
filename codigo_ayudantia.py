# Esto estaba en la clase auto
def generar_tiempo_abandono_taller(self, tiempo_actual):
    self.tiempo_abandono_taller = tiempo_actual + timedelta(minutes=int(uniform(10, 15)))

def generar_tiempo_total_sistema(self, tiempo_actual):
    self.tiempo_total_sistema = tiempo_actual - self.tiempo_llegada
    print(self.tiempo_total_sistema)


# Clase principal que contiene el motor de la simulación
class Taller:
    def __init__(self, tiempo_simulacion, tasa_llegada, capacidad):
        # usamos datetime para manejar temporalidad
        date = datetime(2019, 8, 1)
        newdate = date.replace(hour=9)

        # seteamos variables de tiempo
        self.tiempo_actual = newdate
        self.tiempo_maximo = newdate + timedelta(hours=tiempo_simulacion)

        # seteamos inputs de distribuciones y estructuras de la simulación
        self.tasa_llegada = tasa_llegada
        self.estacion = {"E1": None}
        self.proximo_auto_llega = self.tiempo_actual + timedelta(
            minutes=int(expovariate(1 / tasa_llegada)))
        self.capacidad_cola = capacidad
        self.cola = deque()

        # las variables para el cálculo de estadísticas se dejan en el constructor
        self.cantidad_autos = 0  # son los autos que llegan
        self.cantidad_autos_perdidos = 0
        self.abandonos = 0

        # manejamos una lista con todos los tiempos de abandono que se generan
        self.tiempos_abandono_taller = [[self.tiempo_actual.replace(year=3000), None]]

    # usamos properties para trabajar con mayor comodidad el atributo del proximo auto que termina de ser atendido
    @property
    def proximo_auto_termina(self):
        # Esta la próxima persona que terminará de ser atendida con su tiempo asociado
        x, y = self.tiempos_abandono_taller[0]
        return x, y

    @property
    def proximo_evento(self):
        tiempos = [self.proximo_auto_llega,
                   self.proximo_auto_termina[0]]
        tiempo_prox_evento = min(tiempos)

        if tiempo_prox_evento >= self.tiempo_maximo:
            return "fin"
        eventos = ["llegada_auto", "abandono_taller"]
        return eventos[tiempos.index(tiempo_prox_evento)]

    # funcion que define la llegada de autos al taller
    def llegar_auto(self):
        time.sleep(0.4)
        self.tiempo_actual = self.proximo_auto_llega
        self.proximo_auto_llega = self.tiempo_actual + timedelta(
            minutes=int(expovariate(1 / self.tasa_llegada)))
        auto = Auto(self.tiempo_actual)
        print("\r\r\033[91m[LLEGADA]\033[0m ha llegado un auto id: {} {}".format(auto._id,
                                                                                 self.tiempo_actual))

        if len(self.cola) == self.capacidad_cola:
            print("[COLA LLENA!!!] Se ha llenado la cola de espera para el taller")
            self.cantidad_autos += 1
            self.cantidad_autos_perdidos += 1
        elif self.estacion["E1"] == None:
            # self.tiempo_sistema_vacio += (self.tiempo_actual - self.ultimo_tiempo_actual_vacio)
            self.estacion["E1"] = auto
            self.estacion["E1"].estacion = "E1"
            self.estacion["E1"].generar_tiempo_abandono_taller(self.tiempo_actual)
            self.tiempos_abandono_taller.append((auto.tiempo_abandono_taller, auto))
            self.tiempos_abandono_taller.sort(
                key=lambda z: datetime.strftime(z[0], "%Y-%m-%d-%H-%M"))
            print(
                "\r\r\033[92m[INGRESO ESTACION]\033[0m ha ingresado un auto a E1 id: {} {}".format(
                    self.estacion["E1"]._id, self.tiempo_actual))
            self.cantidad_autos += 1
        else:
            self.cola.append(auto)
        # print(self.estacion["E1"])

    # funcion que defin la salida de autos del taller
    def abandono_taller(self):
        time.sleep(0.4)
        # print("quien va a abandonar "+ str(self.proximo_auto_termina[1]))
        self.tiempo_actual, auto_sale = self.proximo_auto_termina
        # print("quien va a abandonar " + str(auto_sale))
        if len(self.cola) > 0:  # A tiene prioridad sobre B
            # Si hay, la proxima persona pasa
            print('[RETIRA] Se ha desocupado la Estacion, abandona el auto id {} {}'.
                  format(auto_sale, self.tiempo_actual))
            prox_auto = self.cola.popleft()
            # print(prox_auto)
            prox_auto.estacion = auto_sale.estacion
            self.auto_pasa_a_ser_atendido(prox_auto, auto_sale.estacion)
        else:
            print("[RETIRA] La estacion termina de atender al auto id: {}, esta desocupado pero "
                  "no hay autos en cola {}".format(auto_sale._id, self.tiempo_actual))
            self.estacion[auto_sale.estacion] = None

        self.tiempos_abandono_taller.pop(0)
        self.abandonos += 1

    # funcion que apoya el ingreso de autos
    def auto_pasa_a_ser_atendido(self, auto, e):
        time.sleep(0.4)
        self.estacion[e] = auto
        self.estacion[e].generar_tiempo_abandono_taller(self.tiempo_actual)
        self.tiempos_abandono_taller.append((self.estacion[e].tiempo_abandono_taller, auto))
        self.tiempos_abandono_taller.sort(key=lambda z: datetime.strftime(z[0], "%Y-%m-%d-%H-%M"))
        print("\r\r\033[92m[INGRESO ESTACION]\033[0m ha ingresado un auto a E1 id: {0} {1}".format(
            auto, self.tiempo_actual))
        self.cantidad_autos += 1

    # motor de la simulacion
    def run(self):
        while self.tiempo_actual < self.tiempo_maximo:
            evento = self.proximo_evento
            # print("en el modulo hay {}".format(self.modulo_atencion))
            if evento == "fin":
                self.tiempo_actual = self.tiempo_maximo
                break
            elif evento == "llegada_auto":
                self.llegar_auto()
            elif evento == "abandono_taller":
                self.abandono_taller()

    def show(self):
        print("La cantidad de autos que llegaron al taller {}".format(self.cantidad_autos))
        print("La cantidad de autos que se aburrieron de esperar {}".format(
            self.cantidad_autos_perdidos))
        print("La cantidad de autos que abandondan el taller {}".format(self.abandonos))

