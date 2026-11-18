# Organizador de Arquivos (Python)

Separa os arquivos de uma pasta em subpastas por tipo (Imagens, Documentos, Planilhas, Vídeos, etc.). Tem duas formas de uso: uma janela simples e um comando de terminal. Usa apenas a biblioteca padrão do Python, sem dependências.

## Como usar

Requer Python 3.9 ou superior.

### Com janela

```bash
python app.py
```

Clique em **Escolher pasta...**, use **Simular** para ver o que vai acontecer e depois **Organizar** para mover de verdade.

> A janela usa o `tkinter`, que já vem com o Python no Windows e no Mac. No Linux pode ser preciso instalar: `sudo apt install python3-tk`.

### Pelo terminal

```bash
# Veja o que seria feito, sem mover nada
python organizador.py ~/Downloads --simular

# Organize de verdade
python organizador.py ~/Downloads
```

## Comportamento

- Mexe só nos arquivos diretamente dentro da pasta, sem entrar em subpastas.
- Ignora arquivos ocultos (que começam com ponto).
- Nunca sobrescreve: se já existir `foto.png` no destino, o novo vira `foto (1).png`.
- Extensões desconhecidas vão para a pasta `Outros`.

## Testes

```bash
python -m unittest -v
```

## Ideias para evoluir

- Permitir categorias personalizadas por arquivo de configuração (JSON).
- Opção de desfazer a última organização.
- Organizar também por data de modificação.
