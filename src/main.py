import yaml
import sys
from simulador import Simulator

def main():
    print("--- Iniciando Simulador de Máquina de Turing ---")

    # Leer archivo desde argumentos
    if len(sys.argv) < 2:
        config_file = "reconocedora.yaml"
        print("Advertencia: No se especificó archivo. Usando 'reconocedora.yaml'")
        print("Uso: python main.py <archivo.yaml>")
    else:
        config_file = sys.argv[1]

    print(f"\nCargando configuración desde: '{config_file}'")

    # Cargar YAML
    with open(config_file, "r") as f:
        mt = yaml.safe_load(f)

    print("\n[Configuración Cargada Exitosamente]")
    print(f"  Estado Inicial: {mt['q_states']['initial']}")
    print(f"  Estado Final:   {mt['q_states']['final']}")

    # Crear simulador
    simulator = Simulator(mt)

    # Ejecutar simulación para cada cadena
    for s in mt["simulation_strings"]:
        simulator.run(s)

    print("\n--- Simulaciones completadas ---")


main()
