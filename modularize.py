import os
import ast
from functools import lru_cache
import argparse
from global_scope import GlobalScope
from utils import make_from_import_statement, make_import_statement

# This class represents the global scope of your module, keeping track of constants, functions, and classes.


# Create an instance of the GlobalScope class to keep track of module-wide information.
global_scope = GlobalScope()

# This class is used to traverse the AST and update the dependencies in the global scope.
class Something(ast.NodeVisitor):
    def __init__(self, root_node):
        super(Something, self).__init__()
        self.root_name = root_node

    # Visit a Name node and update dependencies if needed.
    def visit_Name(self, node):
        if node.id in global_scope:
            if not (node.id == self.root_name):
                global_scope.update_dependencie(self.root_name, node.id)
        self.generic_visit(node)

# This function extracts imports from a given node.
def extract_imports(node):
    tree = ast.parse(node)
    visitor = Something(node.name)
    visitor.visit(tree)

# This function creates import statements for the entire module.
@lru_cache(None)
def make_global_import():
    retValue = ""
    for im in global_scope.imports:
        retValue += f"import {im}\n"
    for im in global_scope.from_import:
        retValue += f"from {im}\n"
    return retValue

# Lists to store functions, classes, constants, and imports parsed from the source code.
functions = []
classes = []
constants = []
imports = set()

# Scan a file's AST and populate the lists with appropriate information.
def scan_file(code):
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
            global_scope.add_function(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node)
            global_scope.add_class(node.name)
        elif isinstance(node, ast.Assign):
            constants.append(node)
            for c in node.targets:
                global_scope.add_constant(c.id)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                value = make_import_statement(alias)
                global_scope.add_import(value)

        elif isinstance(node, ast.ImportFrom):
            full_import = make_from_import_statement(node)
            global_scope.add_from_import(full_import)

# Create Python files for functions, classes, and constants.
def create_file(arr, module_name):
    global_imports = make_global_import()
    for chunk in arr:
        chunk_code = ast.unparse(chunk)
        extract_imports(chunk)
        imports = global_scope.make_dependencies(chunk.name)
        chunk_code = global_imports + imports + "\n\n\n\n" + chunk_code
        chunk_name = chunk.name
        with open(os.path.join(module_name, f"{chunk_name}.py"), "w") as file:
            file.write(chunk_code)

# Create a separate constant file.
def make_constant_file(module_name):
    pp = ""
    for constant in constants:
        con_code = ast.unparse(constant)
        pp += con_code + "\n"
    if len(constants):
        with open(os.path.join(module_name, f"constant.py"), "w") as file:
            file.write(pp)

# Create the __init__.py file for the module.
def make_init(module_name):
    with open(os.path.join(module_name, "__init__.py"), "w") as file:
        imports = global_scope.import_init()
        file.write(imports)

# Main function that orchestrates the process of creating the module.
def main():
    # parser = argparse.ArgumentParser(description="Create a modular Python module based on functions, classes, and constants.")
    # parser.add_argument("input_file", help="Path to the source Python file to be modularized.")
    # args = parser.parse_args()

    # file_path = args.input_file
    file_path = "validate.py"
    module_name = file_path[:-3]  # Remove the .py extension




    with open(file_path, "r") as file:
        source_code = file.read()

    os.makedirs(module_name, exist_ok=True)
    scan_file(source_code)
    create_file(functions, module_name)
    create_file(classes, module_name)
    make_constant_file(module_name)
    make_init(module_name)

# Entry point of the script.
if __name__ == "__main__":
    main()

# Print a message to indicate successful module creation.
print("Module creation complete.")
