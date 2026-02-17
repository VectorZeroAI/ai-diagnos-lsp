from pathlib import Path
import ast
from typing import Literal, Any
from pygls.workspace import TextDocument
from importlib import util

ROOT_MARKERS = {"setup.py", "pyproject.toml", "setup.cfg"}

def find_project_root(path: Path) -> Path:
    """Walk up directories until a project root marker is found."""
    for parent in path.parents:
        if any((parent / marker).exists() for marker in ROOT_MARKERS):
            return parent
    raise RuntimeError("No project root found. ")

def path_to_dotted(path: Path) -> str:
    """Convert a file path to a dotted module name."""
    path = path.resolve()
    root = find_project_root(path)

    if (root / 'src').exists():   
        result = ".".join(path.relative_to((root / 'src')).with_suffix("").parts)
    else:
        result = ".".join(path.relative_to(root).with_suffix("").parts)
    return result

def parse_source(source: str) -> tuple[list[str], list[dict[Literal["name", "level", "module"], Any]]]:
    """ Parse python source code and extract import statements from it """
    tree = ast.parse(source)
    imports: list[str] = []
    from_imports: list[dict[Literal["name", "level", "module"], Any]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
            continue
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                from_imports.append({
                    "name": alias.name,
                    "level": node.level,
                    "module": node.module
                    })
            continue

    return (imports, from_imports)

def parse_file(file: TextDocument | Path, scope: list[str]) -> list[Path]:
    
    result: list[Path] = []

    if isinstance(file, TextDocument):
        source = file.source
        path_of_the_analysed_file: Path = Path(file.path)
    else:
        source = file.read_text()
        path_of_the_analysed_file: Path = file.absolute().resolve()

    imports_lists_tuple = parse_source(source)

    for i in imports_lists_tuple[0]:
        spec = util.find_spec(i)
        if spec and spec.origin:
            resulting_file_path = Path(spec.origin)
            if any(Path(s) in resulting_file_path.parents for s in scope):
                result.append(resulting_file_path)
            else:
                continue

    for i in imports_lists_tuple[1]:
        if i['level'] > 0:
            # relative import
            dots = '.' * i['level']
            absolute_import_statement = util.resolve_name(f"{dots}{i.get('module') + '.' if i.get('module') is not None else ""}{i['name']}", # pyright: ignore
                                                          f"{path_to_dotted(path_of_the_analysed_file)}"
                                                          )
        else:
            absolute_import_statement = f"{i.get('module') + '.' if i.get('module') is not None else ''}{i['name']}" # pyright: ignore

        spec = util.find_spec(absolute_import_statement)
        if spec and spec.origin:
            resulting_file_path = Path(spec.origin)
            if any(Path(s) in resulting_file_path.parents for s in scope):
                result.append(resulting_file_path)
            else:
                continue

    return result
    

def recursive_resolve_imports(file: TextDocument | Path,
                              scope: list[str],
                              analysis_max_depth: int | None = None,
                              max_string_size_char: int | None = None
                              ) -> str | None:
    """ 
    This function recursivly resolves imports inside for ether analysis_max_depth or until the end. 

    Architecture: 
        there are 3 lists: 
            unified list of all imports (All the relevant files, limited by scope)
            prev_iteration_result (the results of each iteration for the next iteration to work with)
            intermidiate_iteration_results (where each iteration appends its results to, during the iteration through 
                                            prev_iteration_result, before overwriting prev_iteration_results with intermidiate iterattion result 
                                            at the end of an iteration, and overwriting the intermidiate iteration results with an empty list. 
                                            )

        After the import resolution is finished, this function then reads the contents of every of those files, and puts it into a giant string
        wich is basically the context blob for the AI to work with
    """

    result_str: str = ""

    visited_files: set[Path] = set()

    unified_list_of_all_the_imports: list[Path] = []
    
    prev_iteration_result: list[Path] = parse_file(file, scope)
    intermediate_iteration_results: list[Path] = []

    if analysis_max_depth is not None:

        for _ in range(analysis_max_depth):

            for i in prev_iteration_result:
                if i in visited_files:
                    continue
                else:
                    visited_files.add(i)

                iteration_result = parse_file(i, scope)

                if len(iteration_result) > 0:

                    for j in iteration_result:

                        unified_list_of_all_the_imports.append(j)
                        intermediate_iteration_results.append(j)
                            
            prev_iteration_result = intermediate_iteration_results
            intermediate_iteration_results = []

    else:
        _flag_complete = False
        
        while not _flag_complete:
            
            for i in prev_iteration_result:
                if i in visited_files:
                    continue
                else:
                    visited_files.add(i)

                iteration_result = parse_file(i, scope)

                if len(iteration_result) > 0:

                    for i in iteration_result:

                        unified_list_of_all_the_imports.append(i)
                        intermediate_iteration_results.append(i)
                            
            if len(intermediate_iteration_results) > 0:
                prev_iteration_result = intermediate_iteration_results
                intermediate_iteration_results = []
            else:
                _flag_complete = True
                        
    
    for i in unified_list_of_all_the_imports:
        result_str = result_str + f"@{i.resolve().absolute().as_uri()}: \n"
        result_str = result_str + f"{i.read_text()} \n\n"

    if max_string_size_char is not None:
        if len(result_str) > max_string_size_char:
            return None
            # TODO : Add some behaviour to here
        
    return result_str
















# def parse_line(line: str, scope: list[str]) -> Path | None:
#     line = line.strip()
#     if "#" in line:
#         if line.startswith("#"):
#             return
# 
#         line = line.split("#")[0]
#     
#     tokens = line.split(" ")
# 
#     if tokens[0] not in ("from", "import"):
#         return
# 
#     if tokens[0] == "from":
#         import_path = tokens[1].split(".")
# 
#         if tokens [2] != "import":
#             return
#         
#         if len(tokens) == 4:
#             import_items = tokens[3]
#         else:
#             import_items: list[str] | str = []
#             for i in tokens:
#                 if tokens.index(i) < 3:
#                     continue
#                 uncrammed_token = i.split(",")
#                 for j in uncrammed_token:
#                     j = j.strip()
#                     import_items.append(j)
#                 
# 
#     if tokens[0] == "import":
#         if "," in tokens[1]:
#             for i in tokens:
#                 if tokens.index(i) == 0:
#                     continue
#                 actual_tokens = i.split(",")
#                 for i in actual_tokens:
#                     uncrammed_token = i.split(".")
#                     for i in uncrammed_token:
#                         import_path = ""
#                         if uncrammed_token.index(i) != len(uncrammed_token):
#                             if i == "":
#                                 import_path = import_path + "."
#                                 continue
#                             import_path = import_path + "." + i
#                         else:
#                             import_items = i
#             
#         else:
#             if len(tokens) > 2:
#                 for i in tokens:
#                     if tokens.index(i) == 0:
#                         continue
#                     uncrammed_token = i.rstrip(",").split(".")
#                     import_path = ""
#                     for i in uncrammed_token:
#                         if uncrammed_token.index(i) != len(uncrammed_token):
#                             if i == "":
#                                 import_path = import_path + "."
#                                 continue
#                             import_path = import_path + "." + i
#                         else:
#                             import_items = i
#                             
#             else:
#                 uncrammed_token = tokens[1].split(".")
#                 if len(uncrammed_token) == 0:
#                     import_path = ""
#                     import_items = uncrammed_token
#                 else:
#                     import_path = ""
#                     for i in uncrammed_token:
#                         if uncrammed_token.index(i) != len(uncrammed_token):
#                             if i == "":
#                                 import_path = import_path + "."
#                                 continue
#                             import_path = import_path + "." + i
#                         else:
#                             import_items = i
# 
