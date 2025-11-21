import time

BLANK_SYMBOL = "B"


class Simulator:
    def __init__(self, config):
        self.config = config
        self.tape = {}
        self.head = 0
        self.current_state = config["q_states"]["initial"]
        self.mem_cache_value = None

    def initialize_tape(self, text):
        self.tape = {}
        for i, c in enumerate(text):
            self.tape[i] = c

    def read_tape(self):
        return self.tape.get(self.head, BLANK_SYMBOL)

    def find_transition(self):
        current_symbol = self.read_tape()

        for t in self.config["delta"]:
            p = t["params"]

            # Estado
            if p["initial_state"] != self.current_state:
                continue

            # Símbolo
            if p["tape_input"] != current_symbol:
                continue

            # Memcache
            cache_ok = (
                (self.mem_cache_value is None and p["mem_cache_value"] is None) or
                (self.mem_cache_value is not None and p["mem_cache_value"] is not None and
                 self.mem_cache_value == p["mem_cache_value"])
            )

            if not cache_ok:
                continue

            return t["output"]

        return None

    def apply_transition(self, out):
        # Cambiar estado
        self.current_state = out["final_state"]

        # Cambiar memcache
        self.mem_cache_value = out["mem_cache_value"]

        # Escribir
        tape_output = out["tape_output"] if out["tape_output"] is not None else BLANK_SYMBOL
        self.tape[self.head] = tape_output

        # Movimiento
        d = out["tape_displacement"]
        if d == "R":
            self.head += 1
        elif d == "L":
            self.head -= 1

    def get_id(self):
        min_i = min(self.tape.keys()) if self.tape else 0
        max_i = max(self.tape.keys()) if self.tape else 0

        min_i = min(min_i, self.head)
        max_i = max(max_i, self.head)

        cache = self.mem_cache_value if self.mem_cache_value is not None else BLANK_SYMBOL
        state_str = f"[{self.current_state}, {cache}]"

        result = ""
        for i in range(min_i - 1, max_i + 2):
            if i == self.head:
                result += " " + state_str + " "

            result += self.tape.get(i, BLANK_SYMBOL)
        return result

    def run(self, input_string):
        print(f"\n--- Iniciando simulación para '{input_string}' ---")

        self.initialize_tape(input_string)
        self.current_state = self.config["q_states"]["initial"]
        self.mem_cache_value = None
        self.head = 0

        max_steps = 1000

        for step in range(max_steps):
            print(self.get_id())
            time.sleep(0.05)

            trans = self.find_transition()

            if trans is None:
                if self.current_state == self.config["q_states"]["final"]:
                    print(">> Cadena ACEPTADA (estado final sin transición) <<")
                else:
                    print(">> Cadena RECHAZADA (no hay transición) <<")
                return

            self.apply_transition(trans)

            # Caso especial: estado final + quedarse
            if (
                self.current_state == self.config["q_states"]["final"]
                and trans["tape_displacement"] == "S"
            ):
                print(self.get_id())
                print(">> Cadena ACEPTADA (S en estado final) <<")
                return

        print(">> Cadena RECHAZADA (límite de pasos) <<")
