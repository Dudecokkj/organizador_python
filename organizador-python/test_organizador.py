import tempfile
import unittest
from pathlib import Path

from organizador import (
    categoria_do_arquivo,
    descrever_movimentos,
    destino_sem_conflito,
    organizar,
)


class TestCategoria(unittest.TestCase):
    def test_extensoes_conhecidas(self):
        self.assertEqual(categoria_do_arquivo(Path("foto.JPG")), "Imagens")
        self.assertEqual(categoria_do_arquivo(Path("relatorio.pdf")), "Documentos")
        self.assertEqual(categoria_do_arquivo(Path("script.py")), "Codigo")

    def test_extensao_desconhecida_vai_para_outros(self):
        self.assertEqual(categoria_do_arquivo(Path("arquivo.xyz")), "Outros")
        self.assertEqual(categoria_do_arquivo(Path("semextensao")), "Outros")


class TestOrganizar(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.pasta = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_move_arquivos_para_subpastas(self):
        (self.pasta / "foto.png").write_text("x")
        (self.pasta / "nota.txt").write_text("x")
        organizar(self.pasta)
        self.assertTrue((self.pasta / "Imagens" / "foto.png").exists())
        self.assertTrue((self.pasta / "Documentos" / "nota.txt").exists())

    def test_simular_nao_move_nada(self):
        (self.pasta / "foto.png").write_text("x")
        movimentos = organizar(self.pasta, simular=True)
        self.assertEqual(len(movimentos), 1)
        self.assertTrue((self.pasta / "foto.png").exists())
        self.assertFalse((self.pasta / "Imagens").exists())

    def test_nao_sobrescreve_arquivo_existente(self):
        (self.pasta / "Imagens").mkdir()
        (self.pasta / "Imagens" / "foto.png").write_text("antigo")
        (self.pasta / "foto.png").write_text("novo")
        organizar(self.pasta)
        self.assertEqual((self.pasta / "Imagens" / "foto.png").read_text(), "antigo")
        self.assertEqual((self.pasta / "Imagens" / "foto (1).png").read_text(), "novo")

    def test_ignora_ocultos_e_subpastas(self):
        (self.pasta / ".segredo.txt").write_text("x")
        (self.pasta / "subpasta").mkdir()
        self.assertEqual(organizar(self.pasta), [])
        self.assertTrue((self.pasta / ".segredo.txt").exists())

    def test_pasta_invalida(self):
        with self.assertRaises(NotADirectoryError):
            organizar(self.pasta / "nao-existe")


class TestDescricao(unittest.TestCase):
    def test_sem_movimentos(self):
        self.assertEqual(descrever_movimentos([]), "Nenhum arquivo para organizar.")

    def test_texto_da_simulacao_e_da_organizacao(self):
        movimentos = [(Path("/x/foto.png"), Path("/x/Imagens/foto.png"))]
        simulado = descrever_movimentos(movimentos, simular=True)
        real = descrever_movimentos(movimentos, simular=False)
        self.assertIn("Seria movido: foto.png -> Imagens/foto.png", simulado)
        self.assertIn("1 arquivo(s) analisado(s).", simulado)
        self.assertIn("Movido: foto.png -> Imagens/foto.png", real)
        self.assertIn("1 arquivo(s) organizado(s).", real)


class TestDestino(unittest.TestCase):
    def test_gera_nome_unico(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "a.txt"
            base.write_text("x")
            (Path(tmp) / "a (1).txt").write_text("x")
            self.assertEqual(destino_sem_conflito(base).name, "a (2).txt")


if __name__ == "__main__":
    unittest.main()
