import os
import importlib.util
from . import parser

macro_packages = {}
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def load_all_packages(package_dir="packages"):

    for filename in os.listdir(package_dir):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        module_name = filename[:-3]
        file_path = os.path.join(package_dir, filename)

        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Look for a package registry dictionary.
        if hasattr(module, "package_registry"):
            reg = module.package_registry
            namespace = reg["namespace"]

            if namespace in macro_packages:
                print(f"{RED}[Package Import Failure] Duplicate namespace '{namespace}' found in {filename}{RESET}")
                exit(1)
        
            macro_packages[namespace] = reg
            parser.register_package_macros(namespace, reg)

        else:
            print(f"{YELLOW}[Faulty Package Warning] Skipping '{filename}': Package Registry could not be found.{RESET}")

def get_all_macro_registries():
    return macro_packages