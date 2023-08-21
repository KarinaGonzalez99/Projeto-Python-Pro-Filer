from pro_filer.actions.main_actions import show_preview  # NOQA


def test_empty_lists(capsys):
    context = {
        "all_files": [],
        "all_dirs": []
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == 'Found 0 files and 0 directories\n'


def test_multiple_files_and_directories(capsys):
    context = {
        "all_files": ["src/qwe.py", "src/utils/rty.py", "src/trybe/uio.py",
                      "src/actions/asd.py", "src/imgs/fgh.py",
                      "src/mods/jkl.py"],
        "all_dirs": ["src", "src/utils", "src/trybe", "src/actions",
                     "src/imgs", "src/mods"]
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == "Found 6 files and 6 directories\n" \
                           "First 5 files: ['src/qwe.py', " \
                           "'src/utils/rty.py'," \
                           " 'src/trybe/uio.py', 'src/actions/asd.py', " \
                           "'src/imgs/fgh.py']\n" \
                           "First 5 directories: ['src', 'src/utils', " \
                           "'src/trybe'," \
                           " 'src/actions', 'src/imgs']\n"


def test_success_case(capsys):
    context = {
        "all_files": ["src/__init__.py", "src/utils/__init__.py"],
        "all_dirs": ["src", "src/utils"]
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == "Found 2 files and 2 directories\n" \
                           "First 5 files: ['src/__init__.py', " \
                           "'src/utils/__init__.py']\n"\
                           "First 5 directories: ['src', 'src/utils']\n"
