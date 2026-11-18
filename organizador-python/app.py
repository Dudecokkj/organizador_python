#!/usr/bin/env python3
"""Versão com janela do Organizador de Arquivos.

Abra com:  python app.py
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from organizador import descrever_movimentos, organizar


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Organizador de Arquivos")
        self.geometry("620x440")
        self.minsize(480, 340)

        self.pasta = tk.StringVar(value="Nenhuma pasta escolhida")
        self._montar_tela()

    def _montar_tela(self) -> None:
        corpo = ttk.Frame(self, padding=12)
        corpo.pack(fill="both", expand=True)

        # Linha da pasta
        linha_pasta = ttk.Frame(corpo)
        linha_pasta.pack(fill="x")
        ttk.Button(linha_pasta, text="Escolher pasta...", command=self.escolher_pasta).pack(
            side="left"
        )
        ttk.Label(linha_pasta, textvariable=self.pasta).pack(side="left", padx=10)

        # Botões de ação
        linha_botoes = ttk.Frame(corpo)
        linha_botoes.pack(fill="x", pady=10)
        self.botao_simular = ttk.Button(
            linha_botoes, text="Simular (não move nada)", command=self.simular, state="disabled"
        )
        self.botao_simular.pack(side="left")
        self.botao_organizar = ttk.Button(
            linha_botoes, text="Organizar", command=self.organizar_de_verdade, state="disabled"
        )
        self.botao_organizar.pack(side="left", padx=8)

        # Área de resultado
        self.saida = scrolledtext.ScrolledText(corpo, state="disabled", wrap="word", height=14)
        self.saida.pack(fill="both", expand=True)

        self.status = ttk.Label(corpo, text="Escolha uma pasta para começar.")
        self.status.pack(anchor="w", pady=(8, 0))

    def escolher_pasta(self) -> None:
        escolhida = filedialog.askdirectory(title="Escolha a pasta para organizar")
        if not escolhida:
            return
        self.pasta.set(escolhida)
        self.botao_simular.config(state="normal")
        self.botao_organizar.config(state="normal")
        self.status.config(text="Dica: use Simular primeiro para ver o que vai acontecer.")
        self._mostrar("")

    def _mostrar(self, texto: str) -> None:
        self.saida.config(state="normal")
        self.saida.delete("1.0", "end")
        self.saida.insert("end", texto)
        self.saida.config(state="disabled")

    def _executar(self, simular: bool) -> None:
        pasta = Path(self.pasta.get())
        try:
            movimentos = organizar(pasta, simular=simular)
        except (NotADirectoryError, OSError) as erro:
            messagebox.showerror("Erro", str(erro))
            return
        self._mostrar(descrever_movimentos(movimentos, simular=simular))
        self.status.config(text="Simulação concluída." if simular else "Organização concluída.")

    def simular(self) -> None:
        self._executar(simular=True)

    def organizar_de_verdade(self) -> None:
        confirmou = messagebox.askyesno(
            "Confirmar",
            f"Mover os arquivos de:\n{self.pasta.get()}\n\npara subpastas por tipo?",
        )
        if confirmou:
            self._executar(simular=False)


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
