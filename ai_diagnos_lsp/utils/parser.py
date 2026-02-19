#!/usr/bin/env python

from pathlib import Path
import ast
from typing import Literal, Any
from pygls.workspace import TextDocument
from importlib import util
import os
import logging
import subprocess
import json

ROOT_MARKERS = {"setup.py", "pyproject.toml", "setup.cfg"}

LOG = True if os.getenv('AI_DIAGNOS_LOG') is not None else False

ParserPluginsDict = dict[str, str]


def plugin_loader(plugin_path: Path,
                  scope: list[str],
                  solid_str_file_content: str,
                  file_path: Path
                  ) -> list[Path] | None:
    
    json_payload = {
            "project_scope": scope,
            "file_content": solid_str_file_content.splitlines(),
            "solid_file_content": solid_str_file_content,
            "file_path": file_path.as_posix()
            }
    json_payload = json.dumps(json_payload)

    try:
        result_strings = subprocess.run(plugin_path.as_posix(), 
                       input=json_payload,
                       capture_output=True,
                       text=True
                       )

        result_strings = json.loads(result_strings.stdout)
    except Exception as e:
        if LOG:
            logging.error(f"subprocess running or reading its stdout into json failed with error {e}")
        return None
    
    result_Path_objects: list[Path] = []

    for i in result_strings:
        result_Path_objects.append(Path(i))

    return result_Path_objects



def find_project_root(path: Path) -> Path:
    """Walk up directories until a project root marker is found."""
    if path.is_dir():
        if any((path / marker).exists() for marker in ROOT_MARKERS):
            return path
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

def resolve_absolute_import(absolute_import_statement: str, root_project: str) -> Path | None:
    """
    This function resolves the absolute import statement by walking down each of its steps until a file is found. 
    """
    current_step = Path(root_project)

    steps = absolute_import_statement.split('.')

    if (current_step / steps[0]).exists():
        pass
    
    else:
        if (current_step / 'src' / steps[0]).exists():
            current_step = current_step / 'src'
        else:
            return None

    for step in steps:
        current_step_try = current_step / step

        if current_step_try.exists() and current_step_try.is_dir():
            current_step = current_step_try
            continue

        if not current_step_try.exists():

            if (current_step / f"{step}.py").exists():
                 return current_step / f"{step}.py"

    if current_step.is_dir():
        current_step_try = current_step / '__init__.py'

        if current_step_try.is_file():
            return current_step_try

    return None



def resolve_relative_import(info: dict[Literal['name', 'level', 'module'], Any], analysed_file: str) -> Path | None:
    """
    Resolves relative imports by incremental path traversal
    """

    current_step = Path(analysed_file)

    if not current_step.exists():
        return None
    
    level: int = info['level']
    name: str = info['name']
    module: str | None = info['module']


    for _ in range(level):
        current_step = current_step.parent
    

    if module is None:
        module_parts = []

    else:
        module_parts = module.split('.')
    
    for step in module_parts:
        current_step_try = current_step / step

        if current_step_try.is_dir():
            current_step = current_step_try

        elif current_step_try.is_file():
            return current_step_try

        elif not current_step_try.exists():
            current_step_try = current_step / f"{step}.py"

            if current_step_try.is_file():
                return current_step_try

            else:
                return None 

    current_step_try = current_step / name

    if current_step_try.is_dir():
        current_step_try = current_step / '__init__.py'

        if current_step_try.is_file():
            return current_step_try

    elif current_step_try.is_file():
        return current_step_try

    elif not current_step_try.exists():
        current_step_try = current_step / f"{name}.py"
        if current_step_try.is_file():
            return current_step_try
        elif current_step_try.is_dir():
            current_step_try = current_step_try / '__init__.py'   # IDK WHY I DID THIS LOL, but it doesnt hurt to try one last time, you know ?
            if current_step_try.is_file():
                return current_step_try

    return None


def resolve_import(import_statement: str | dict[Literal['name', 'level', 'module'], Any], currently_analysed_file_path: Path) -> Path | None:
    root = find_project_root(
            currently_analysed_file_path.resolve().absolute()
            ).as_posix()
    if isinstance(import_statement, str):
        result = resolve_absolute_import(import_statement, root)
    else:
        if import_statement['level'] == 0:
            result = resolve_absolute_import(f"{import_statement['module']}.{import_statement['name']}", 
                                            root
                                             )
        else:
            result = resolve_relative_import(import_statement, currently_analysed_file_path.as_posix())

    return result


def parse_file(file: TextDocument | Path, scope: list[str], plugins: ParserPluginsDict | None) -> list[Path]:
    """
    Parses the file, with ether built in parser or with a plugin parser. 

    Checks the file type by checking file extension. 
    """
    
    result: list[Path] = []

    if isinstance(file, TextDocument):
        source = file.source
        path_of_the_analysed_file: Path = Path(file.path)
        file_type: str = path_of_the_analysed_file.suffix
    else:
        source = file.read_text()
        path_of_the_analysed_file: Path = file.absolute().resolve()
        file_type: str = path_of_the_analysed_file.suffix

    if file_type == '.py':
        imports_lists_tuple = parse_source(source)

        for i in imports_lists_tuple[0]:
            try:
                spec = util.find_spec(i)
                if spec and spec.origin:
                    resulting_file_path = Path(spec.origin)
                    if any(Path(s) in resulting_file_path.parents for s in scope):
                        result.append(resulting_file_path)
                    else:
                        continue
            except Exception as e:
                if LOG: 
                    logging.info(f"error ecountered by the parser (upper) : {e}")
                tmp = resolve_import(i, path_of_the_analysed_file)
                if tmp is not None:
                    result.append(tmp)
                else:
                    if LOG:
                        logging.info("My directory traversal based resolver failed as well. ")

        for i in imports_lists_tuple[1]:
            try:
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
            except Exception as e:
                if LOG: 
                    logging.info(f"attribute error encoutered by parser: {e}")
                tmp = resolve_import(i, path_of_the_analysed_file)
                if tmp is not None: 
                    result.append(tmp)



    else:
        if plugins is not None:
            plug_in_found = plugins.get(file_type)
            if plug_in_found is not None:
                result_pre = plugin_loader(Path(plug_in_found),
                                       scope=scope,
                                       solid_str_file_content=source,
                                       file_path=path_of_the_analysed_file
                                       )
                if result_pre is not None:
                    result = result_pre
                else:
                    result = []

    return result
    

def get_cross_file_context(file: TextDocument | Path,
                          scope: list[str],
                          analysis_max_depth: int | None = None,
                          max_string_size_char: int | None = None,
                          plugins: ParserPluginsDict | None = None
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

    unified_list_of_all_the_imports: set[Path] = set()

    prev_iteration_result: list[Path] = parse_file(file, scope, plugins)

    if isinstance(file, TextDocument):
        visited_files.add(Path(file.path))
    else:
        visited_files.add(file)

    for i in prev_iteration_result:
        unified_list_of_all_the_imports.add(i)

    intermediate_iteration_results: list[Path] = []

    if analysis_max_depth is not None:

        for _ in range(analysis_max_depth):

            for i in prev_iteration_result:
                if i in visited_files:
                    continue
                else:
                    visited_files.add(i)

                iteration_result = parse_file(i, scope, plugins)

                if len(iteration_result) > 0:

                    for j in iteration_result:

                        unified_list_of_all_the_imports.add(j)
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

                iteration_result = parse_file(i, scope, plugins)

                if len(iteration_result) > 0:

                    for i in iteration_result:

                        unified_list_of_all_the_imports.add(i)
                        intermediate_iteration_results.append(i)
                            
            if len(intermediate_iteration_results) > 0:
                prev_iteration_result = intermediate_iteration_results
                intermediate_iteration_results = []
            else:
                _flag_complete = True
                        
    
    for i in unified_list_of_all_the_imports:
        try:
            result_str_new = result_str + f"@{i.resolve().absolute().as_uri()}: \n"
            result_str_new = result_str_new + f"{i.read_text()} \n\n"
            if max_string_size_char is not None:
                if len(result_str_new) > max_string_size_char:
                    return result_str
                else:
                    result_str = result_str_new
            else:
                result_str = result_str_new
        except Exception as e:
            if LOG:
                logging.error(f"Expetion in parser during final results reading {e}")

    return result_str


