import sys
from pathlib import Path

import yaml

from simulador import Simulator


def discover_configs() -> dict[str, Path]:
    """Collect available YAML configs using their stem as selection key."""
    search_dirs = [Path.cwd(), Path(__file__).resolve().parent]
    configs: dict[str, Path] = {}

    for base in search_dirs:
        for path in base.glob("*.yaml"):
            if path.is_file():
                configs.setdefault(path.stem.lower(), path)

    return configs


def prompt_selection(configs: dict[str, Path]) -> Path:
    """Render a small menu so the user can choose a config interactively."""
    options = sorted(configs.items())
    print("Selecciona una configuración disponible:\n")
    for idx, (key, path) in enumerate(options, start=1):
        print(f"  {idx}. {key} -> {path.name}")

    while True:
        choice = input("\nIngresa el número o nombre: ").strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][1]
        else:
            selected = configs.get(choice)
            if selected:
                return selected
        print("Opción no válida, intenta de nuevo.")


def resolve_config_path(configs: dict[str, Path]) -> Path:
    """Resolve the configuration path from CLI argument or interactive menu."""
    if len(sys.argv) >= 2:
        key = sys.argv[1].strip().lower()
        config = configs.get(key)
        if config is None:
            print(f"La opción '{key}' no existe. Opciones válidas: {', '.join(sorted(configs))}")
            sys.exit(1)
        return config

    print("No se proporcionó opción. Mostrando menú interactivo...")
    return prompt_selection(configs)


def main():
    print("--- Iniciando Simulador de Máquina de Turing ---")

    configs = discover_configs()
    if not configs:
        print("No se encontraron archivos .yaml en el directorio actual ni en 'src/'.")
        sys.exit(1)

    config_path = resolve_config_path(configs)
    print(f"\nCargando configuración desde: '{config_path}'")

    with open(config_path, "r", encoding="utf-8") as config_file:
        mt = yaml.safe_load(config_file)

    print("\n[Configuración Cargada Exitosamente]")
    print(f"  Estado Inicial: {mt['q_states']['initial']}")
    print(f"  Estado Final:   {mt['q_states']['final']}")

    simulator = Simulator(mt)

    for s in mt["simulation_strings"]:
        simulator.run(s)

    print("\n--- Simulaciones completadas ---")


if __name__ == "__main__":
    main()
