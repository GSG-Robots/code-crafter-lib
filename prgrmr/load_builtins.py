import importlib


def load_builtin_module(subdir):
    import os

    for file in os.listdir(f"prgrmr/builtins/{subdir}"):
        if file.endswith(".py"):
            importlib.import_module(f"prgrmr.builtins.{subdir}.{file[:-3]}")


def load_builtins():
    load_builtin_module("managers")
    load_builtin_module("elements")
