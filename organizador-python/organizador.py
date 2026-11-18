#!/usr/bin/env python3
"""Organizador de arquivos: separa os arquivos de uma pasta em subpastas por tipo.

Exemplos:
    python organizador.py ~/Downloads --simular
    python organizador.py ~/Downloads
"""

import argparse
import shutil
from pathlib import Path

CATEGORIAS = {
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".md", ".rtf"},
    "Planilhas": {".xls", ".xlsx", ".csv", ".ods"},
    "Apresentacoes": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Audios": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Codigo": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp"},
}
OUTROS = "Outros"


def categoria_do_arquivo(caminho: Path) -> str:
    """Retorna o nome da categoria de um arquivo, com base na extensão."""
    extensao = caminho.suffix.lower()
    for nome, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return nome
    return OUTROS


def destino_sem_conflito(destino: Path) -> Path:
    """Se já existir um arquivo com o mesmo nome, acrescenta (1), (2)... ao nome."""
    if not destino.exists():
        return destino
    contador = 1
    while True:
        candidato = destino.with_name(f"{destino.stem} ({contador}){destino.suffix}")
        if not candidato.exists():
            return candidato
        contador += 1


def organizar(pasta: Path, simular: bool = False) -> list[tuple[Path, Path]]:
    """Organiza os arquivos da pasta e devolve a lista de (origem, destino).

    Só mexe nos arquivos diretamente dentro da pasta, sem entrar em subpastas.
    Arquivos ocultos (que começam com ponto) são ignorados.
    """
    if not pasta.is_dir():
        raise NotADirectoryError(f"'{pasta}' não é uma pasta válida.")

    movimentos = []
    for item in sorted(pasta.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        pasta_destino = pasta / categoria_do_arquivo(item)
        destino = destino_sem_conflito(pasta_destino / item.name)
        movimentos.append((item, destino))
        if not simular:
            pasta_destino.mkdir(exist_ok=True)
            shutil.move(str(item), str(destino))
    return movimentos


def descrever_movimentos(movimentos: list[tuple[Path, Path]], simular: bool = False) -> str:
    """Monta o texto com o resultado, usado tanto pelo terminal quanto pela janela."""
    if not movimentos:
        return "Nenhum arquivo para organizar."

    verbo = "Seria movido" if simular else "Movido"
    linhas = [
        f"{verbo}: {origem.name} -> {destino.parent.name}/{destino.name}"
        for origem, destino in movimentos
    ]
    total = len(movimentos)
    linhas.append("")
    linhas.append(f"{total} arquivo(s) {'analisado(s)' if simular else 'organizado(s)'}.")
    return "\n".join(linhas)


def main() -> None:
    parser = argparse.ArgumentParser(description="Organiza os arquivos de uma pasta por tipo.")
    parser.add_argument("pasta", type=Path, help="pasta que será organizada")
    parser.add_argument(
        "--simular", action="store_true", help="só mostra o que seria feito, sem mover nada"
    )
    args = parser.parse_args()

    try:
        movimentos = organizar(args.pasta, simular=args.simular)
    except NotADirectoryError as erro:
        parser.error(str(erro))

    print(descrever_movimentos(movimentos, simular=args.simular))


if __name__ == "__main__":
    main()
