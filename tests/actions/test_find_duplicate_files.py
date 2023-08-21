from pro_filer.actions.main_actions import find_duplicate_files  # NOQA
import pytest
from pro_filer.actions.main_actions import find_duplicate_files

@pytest.fixture
def base(tmp_path):
    arquivoone = tmp_path / "arquivoone.txt"
    arquivotwo = tmp_path / "arquivotwo.txt"
    arquivothree = tmp_path / "arquivothree.txt"
    arquivoone.write_text("test content" * 1)
    arquivotwo.write_text("test content" * 1)
    arquivothree.write_text("different content")

    return {"all_files":
     [str(arquivoone), 
     str(arquivotwo), 
     str(arquivothree)]}


def teste1(base):
    arquivos_duplicados = find_duplicate_files(base)
    assert len(arquivos_duplicados) == 1
    assert len(arquivos_duplicados[0]) == 2


def teste2(base):
    base["all_files"] = [] 
    arquivos_duplicados = find_duplicate_files(base)
    assert len(arquivos_duplicados) == 0


def teste3(base):
    conteudo_arquivo = "same content" * 10
    for arquivo in base["all_files"]:
        with open(arquivo, "w") as arquivo_aberto:
            arquivo_aberto.write(conteudo_arquivo)
    arquivos_duplicados = find_duplicate_files(base)
    numero_de_combinacoes = len(base["all_files"]) * (len(base["all_files"]) - 1) // 2
    assert len(arquivos_duplicados) == numero_de_combinacoes


def test_4 (base):
    base["all_files"].append("arquivo_nao_existente.txt")
    with pytest.raises(ValueError, match="All files must exist"):
        find_duplicate_files(base)
