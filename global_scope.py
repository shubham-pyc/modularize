import ast

class GlobalScope():
    # Initialize an empty scope dictionary.
    def __init__(self):
        self.scope = {}
        self.imports = set()
        self.from_import = set()

    # Construct a dictionary representing an object with a given type and empty dependencies.
    def construct_object(self, type):
        return {
            "type": type,
            "dependencies": []
        }
    
    # Add a constant to the scope.
    def add_constant(self, name):
        self.scope[name] = self.construct_object(ast.Name)
    
    # Add a function to the scope.
    def add_function(self, name):
        self.scope[name] = self.construct_object(ast.FunctionDef)
    
    # Add a class to the scope.
    def add_class(self, name):
        self.scope[name] = self.construct_object(ast.ClassDef)
    
    # Update the dependencies for a given object in the scope.
    def update_dependencie(self, name, dep):
        if name not in self.scope:
            raise KeyError("Invalid key")
        arr = self.scope[name]["dependencies"]
        if dep not in arr:
            arr.append(dep)
    
    # Check if a key is present in the scope.
    def __contains__(self, key):
        return key in self.scope
    
    # Get an object from the scope by its key.
    def get(self, key):
        return self.scope[key]
    
    # Generate import statements for the dependencies of a given node.
    def make_dependencies(self, node_name):
        imports = ""
        if node_name in self:
            for dep in self.scope[node_name]["dependencies"]:
                if self.scope[dep]["type"] == ast.Name:
                    imports += f"from .constant import {dep}\n"
                else:
                    imports += f"from .{dep} import {dep}\n"
        return imports
    
    # Generate import statements for the entire module initialization.
    def import_init(self):
        ret_value = ""
        for node in self.scope:
            if self.scope[node]["type"] == ast.Name:
                ret_value += f"from .constant import {node}\n"
            else:
                ret_value += f"from .{node} import {node}\n"
        return ret_value

    def add_import(self,value):
        if value is not None and value not in self.imports:
            self.imports.add(value)
    
    def add_from_import(self,value):
        if value is not None and value not in self.from_import:
            self.from_import.add(value)