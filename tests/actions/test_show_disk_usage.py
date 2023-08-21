from unittest.mock import patch
import pytest
from pro_filer.actions.main_actions import show_disk_usage

@pytest.fixture
def context(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("example content" * 5)
    file2 = tmp_path / "file2.txt"
    file2.write_text("different content" * 3)
    return {"all_files": [str(file1), str(file2)]}

def test_show_disk_usage_all_in_one(context, capsys):
    show_disk_usage(context)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert len(output_lines) == 3
    assert "file1.txt" in output_lines[0]
    assert "file2.txt" in output_lines[1]
    assert "Total size:" in output_lines[2]

    context["all_files"] = []
    show_disk_usage(context)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert len(output_lines) == 1
    assert "Total size:" in output_lines[0]
    assert "0" in output_lines[0]

    show_disk_usage(context)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    sizes = [
        int(line.split("(")[1].split("%")[0]) for line in output_lines[:-1]
    ]

    assert sizes == sorted(sizes, reverse=True)

    context["all_files"].append("non_existent_file.txt")

    with pytest.raises(FileNotFoundError):
        show_disk_usage(context)

    with patch(
        "pro_filer.actions.main_actions.os.path.getsize", return_value=150
    ):
        show_disk_usage(context)
        captured = capsys.readouterr()
        output_lines = captured.out.strip().split("\n")

        assert "Total size: 300" in output_lines[-1]
