"""Arquivo que estudantes devem editar"""


def show_deepest_file(context):
    if not context["all_files"]:
        print("No files found")
    else:
        deepest_file = max(
            context["all_files"],
            key=lambda path: path.count('/')
        )
        print(f"Deepest file: {deepest_file}")


def normalize_string(s, case_sensitive):
    return s if case_sensitive else s.lower()


def file_contains_search_term(file_name, search_term, case_sensitive):
    normalized_file_name = normalize_string(file_name, case_sensitive)
    normalized_search_term = normalize_string(search_term, case_sensitive)
    return normalized_search_term in normalized_file_name


def find_file_by_name(context, search_term, case_sensitive=True):
    if not search_term:
        return []

    found_files = []

    for path in context["all_files"]:
        file_name = path.split("/")[-1]

        if file_contains_search_term(file_name, search_term, case_sensitive):
            found_files.append(path)

    return found_files
