import re
from pathlib import Path

ARQUIVO = Path(__file__).parent / "entrada.txt"

# Ordem: padrões mais específicos primeiro
PADROES = [  
    ("CNPJ", r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"),
    ("CPF", r"\d{3}\.\d{3}\.\d{3}-\d{2}"),
    ("RG", r"\d{1,2}\.\d{3}\.\d{3}-[\dXx]"),
    ("EMAIL", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    ("URL", r"https?://[^\s]+\.com(?:\.br)?(?:/[^\s]*)?"),
    ("MOEDA", r"R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?"),
    ("TELEFONE", r"(?:\(?\d{2}\)|\d{2})\s(?:9\d{4}|\d{4})-\d{4}"),
    ("CEP", r"\d{5}-\d{3}"),
    ("PLACA", r"[A-Z]{3}-?\d{4}|[A-Z]{3}\d[A-Z]\d{2}"),
    ("DATA", r"\d{2}/\d{2}/\d{4}"),
    ("HORA", r"\b\d{2}:\d{2}(?::\d{2})?\b"),
    ("PORCENTAGEM", r"\b\d+(?:,\d+)?%"),
]


def encontrar_na_linha(linha: str) -> list[tuple[str, str]]:
    candidatos = []
    for prioridade, (nome, padrao) in enumerate(PADROES):
        for match in re.finditer(padrao, linha):
            candidatos.append((match.start(), match.end(), prioridade, nome, match.group()))

    candidatos.sort(key=lambda x: (x[0], -(x[1] - x[0]), x[2]))

    resultados = []
    ocupado_ate = -1
    for inicio, fim, _, nome, valor in candidatos:
        if inicio < ocupado_ate:
            continue
        resultados.append((nome, valor))
        ocupado_ate = fim
    return resultados


def analisar_arquivo(caminho: Path) -> None:
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    achou_algo = False
    for num, linha in enumerate(linhas, start=1):
        for nome, valor in encontrar_na_linha(linha):
            print(f"Linha {num}: {nome} - {valor}")
            achou_algo = True

    if not achou_algo:
        print("Nenhum padrão encontrado.")


if __name__ == "__main__":
    if not ARQUIVO.exists():
        print(f"Arquivo não encontrado: {ARQUIVO}")
    else:
        print(f"Analisando: {ARQUIVO.name}\n")
        analisar_arquivo(ARQUIVO)
