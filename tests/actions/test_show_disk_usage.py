from unittest.mock import patch
import pytest
from pro_filer.actions.main_actions import show_disk_usage


@pytest.fixture
def base(tmp_path):
    arquivoone = tmp_path / "arquivoone.txt"
    arquivotwo = tmp_path / "arquivotwo.txt"
    arquivoone.write_text("example content" * 5)
    arquivotwo.write_text("different content" * 3)
    return {"all_files": [str(arquivoone), str(arquivotwo)]}


def teste1 (base, capsys):
    show_disk_usage(base)
    save = capsys.readouterr()
    ordem = save.out.strip().split("\n")
    assert len(ordem) == 3
    assert "arquivoone.txt" in ordem[0]
    assert "arquivotwo.txt" in ordem[1]
    assert "Total size:" in ordem[2]


def test_show_disk_usage_empty_base(capsys):
    base = {"all_files": []}
    show_disk_usage(base)
    save = capsys.readouterr()
    ordem = save.out.strip().split("\n")
    assert len(ordem) == 1
    assert "Total size:" in ordem[0]
    assert "0" in ordem[0]


def teste2 (base, capsys):
    show_disk_usage(base)
    save = capsys.readouterr()
    ordem = save.out.strip().split("\n")
    sizes = [
        int(line.split("(")[1].split("%")[0]) for line in ordem[:-1]
    ]
    assert sizes == sorted(sizes, reverse=True)


def teste3 (base):
    base["all_files"].append("non_existent_file.txt")
    with pytest.raises(FileNotFoundError):
        show_disk_usage(base)


def teste4 (base, capsys):
    with patch(
        "pro_filer.actions.main_actions.os.path.getsize", return_value=150
    ):
        show_disk_usage(base)
        save = capsys.readouterr()
        ordem = save.out.strip().split("\n")
        assert "Total size: 300" in ordem[-1]
