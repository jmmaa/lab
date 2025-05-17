import importlib
import importlib.util
import time

value = "gg"


state = 0

while True:
    spec = importlib.util.spec_from_file_location(
        "serializer", "plugins\\serializer\\__init__.py"
    )

    if spec is None:
        raise Exception("module not found")

    else:
        if spec.loader is None:
            raise Exception("loader not found")

        else:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(module.serialize(value * state), flush=True)

            state += 1

    time.sleep(1)


# you can edit the plugins folder and see changes while you run this code
