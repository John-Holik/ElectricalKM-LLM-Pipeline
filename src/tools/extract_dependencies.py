#!/usr/bin/env python3
"""
Dependency Extraction Tool for ElectriAI Research

Scans all notebooks and source files to extract Python imports,
filters out standard library modules, and maps import names to pip package names.

Usage:
    python src/tools/extract_dependencies.py
"""

import ast
import json
import re
import sys
from pathlib import Path

# Standard library modules to exclude (Python 3.8+)
STDLIB_MODULES = {
    # Built-in modules
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore",
    "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect",
    "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd",
    "code", "codecs", "codeop", "collections", "colorsys", "compileall",
    "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg",
    "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime",
    "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email",
    "encodings", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass",
    "gettext", "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac",
    "html", "http", "idlelib", "imaplib", "imghdr", "imp", "importlib", "inspect",
    "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache",
    "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math",
    "mimetypes", "mmap", "modulefinder", "multiprocessing", "netrc", "nis",
    "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib",
    "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib",
    "poplib", "posix", "posixpath", "pprint", "profile", "pstats", "pty", "pwd",
    "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random", "re",
    "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets",
    "select", "selectors", "shelve", "shlex", "shutil", "signal", "site",
    "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3",
    "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile",
    "telnetlib", "tempfile", "termios", "test", "textwrap", "threading", "time",
    "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc",
    "tty", "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest",
    "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp",
    "zipfile", "zipimport", "zlib", "_thread",
    # Typing extensions that are part of typing
    "typing_extensions",
}

# Mapping from import name to pip package name
IMPORT_TO_PIP = {
    "googleapiclient": "google-api-python-client",
    "dotenv": "python-dotenv",
    "sklearn": "scikit-learn",
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "google": "google-api-python-client",  # Common case
    "youtube_transcript_api": "youtube-transcript-api",
}


def extract_imports_from_code(code: str) -> set:
    """Extract top-level module names from Python code using AST."""
    imports = set()
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Fallback to regex if AST parsing fails
        return extract_imports_regex(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Get top-level module
                top_module = alias.name.split('.')[0]
                imports.add(top_module)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                # Get top-level module
                top_module = node.module.split('.')[0]
                imports.add(top_module)
    
    return imports


def extract_imports_regex(code: str) -> set:
    """Fallback regex-based import extraction."""
    imports = set()
    
    # Match 'import X' or 'import X as Y'
    pattern1 = r'^import\s+([\w\.]+)'
    # Match 'from X import Y'
    pattern2 = r'^from\s+([\w\.]+)\s+import'
    
    for line in code.split('\n'):
        line = line.strip()
        
        match1 = re.match(pattern1, line)
        if match1:
            top_module = match1.group(1).split('.')[0]
            imports.add(top_module)
        
        match2 = re.match(pattern2, line)
        if match2:
            top_module = match2.group(1).split('.')[0]
            imports.add(top_module)
    
    return imports


def extract_imports_from_notebook(notebook_path: Path) -> dict:
    """Extract imports from a Jupyter notebook."""
    imports = set()
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  Warning: Could not parse {notebook_path}: {e}")
        return {"file": str(notebook_path), "imports": set()}
    
    cells = notebook.get('cells', [])
    for cell in cells:
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                code = ''.join(source)
            else:
                code = source
            
            cell_imports = extract_imports_from_code(code)
            imports.update(cell_imports)
    
    return {"file": str(notebook_path), "imports": imports}


def extract_imports_from_python_file(file_path: Path) -> dict:
    """Extract imports from a Python source file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"  Warning: Could not read {file_path}: {e}")
        return {"file": str(file_path), "imports": set()}
    
    imports = extract_imports_from_code(code)
    return {"file": str(file_path), "imports": imports}


def filter_third_party(imports: set) -> set:
    """Remove standard library modules from import set."""
    return {imp for imp in imports if imp not in STDLIB_MODULES}


def map_to_pip_names(imports: set) -> set:
    """Convert import names to pip package names."""
    pip_names = set()
    for imp in imports:
        pip_name = IMPORT_TO_PIP.get(imp, imp)
        pip_names.add(pip_name)
    return pip_names


def main():
    # Determine project root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent.parent  # src/tools -> src -> project_root
    
    print(f"Project root: {project_root}\n")
    
    # Find all notebooks
    notebooks_dir = project_root / "notebooks"
    notebooks = list(notebooks_dir.glob("*.ipynb"))
    
    # Find all Python files in src/
    src_dir = project_root / "src"
    python_files = list(src_dir.rglob("*.py"))
    
    all_imports = set()
    results = []
    
    # Process notebooks
    print("=" * 60)
    print("SCANNING NOTEBOOKS")
    print("=" * 60)
    for nb in sorted(notebooks):
        result = extract_imports_from_notebook(nb)
        results.append(result)
        all_imports.update(result["imports"])
        print(f"\n{nb.name}:")
        print(f"  Imports: {sorted(result['imports'])}")
    
    # Process Python files
    print("\n" + "=" * 60)
    print("SCANNING SOURCE FILES")
    print("=" * 60)
    for py_file in sorted(python_files):
        # Skip this script itself
        if py_file.name == "extract_dependencies.py":
            continue
        result = extract_imports_from_python_file(py_file)
        results.append(result)
        all_imports.update(result["imports"])
        rel_path = py_file.relative_to(project_root)
        print(f"\n{rel_path}:")
        print(f"  Imports: {sorted(result['imports'])}")
    
    # Filter and map
    print("\n" + "=" * 60)
    print("DEPENDENCY ANALYSIS")
    print("=" * 60)
    
    print(f"\nAll imports found: {sorted(all_imports)}")
    
    third_party = filter_third_party(all_imports)
    print(f"\nThird-party imports (excluding stdlib): {sorted(third_party)}")
    
    pip_packages = map_to_pip_names(third_party)
    print(f"\nPip package names: {sorted(pip_packages)}")
    
    # Output final list
    print("\n" + "=" * 60)
    print("REQUIREMENTS.TXT CONTENT")
    print("=" * 60)
    for pkg in sorted(pip_packages):
        print(pkg)
    
    return sorted(pip_packages)


if __name__ == "__main__":
    packages = main()
    sys.exit(0)
