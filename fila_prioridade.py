import pandas as pd
import heapq
from pathlib import Path


def processar_fila(dados):
    fila = []

    for sequencia, (_, paciente) in enumerate(dados.iterrows()):
        prioridade = int(paciente["Prioridade_RETTS"])
        horario = str(paciente["Hora_Chegada"])

        heapq.heappush(
            fila,
            (prioridade, horario, sequencia, paciente.to_dict())
        )

    pacientes_ordenados = []

    while fila:
        prioridade, horario, sequencia, paciente = heapq.heappop(fila)
        pacientes_ordenados.append(paciente)

    return pd.DataFrame(pacientes_ordenados)


if __name__ == "__main__":
    caminho = Path(__file__).parent / "dados" / "pacientes_triagem.csv"

    dados = pd.read_csv(caminho, encoding="utf-8-sig")

    resultado = processar_fila(dados)

    print("\n===== FILA DE ATENDIMENTO RETTS =====\n")

    for _, paciente in resultado.iterrows():
        print(
            f"Paciente: {paciente['Nome']} | "
            f"Prioridade: {paciente['Prioridade_RETTS']} | "
            f"Horário: {paciente['Hora_Chegada']} | "
            f"Classe: {paciente['Classe_RETTS']}"
        )