import io
import os
import zipfile

from .default_preinstalls import modules
from .module_dependency import ModuleDependencyAnalyzer


def package_with_dependencies(func, extra_modules=None):
    """
    Packages the *func* module and all dependence modules on a zip.
    *func* cannot be defined at the __main__ module.
    Returns a tuple with the zip file (in memory),
    and the path to that function inside the package.
    """
    # print(func.__module__)
    if extra_modules is None:
        extra_modules = []
    function_name = func.__name__
    module_name = func.__module__

    # Get dependencies
    module_analyzer = ModuleDependencyAnalyzer()
    preinstalled_modules = [name for name, _ in modules]
    module_analyzer.ignore(preinstalled_modules)
    module_analyzer.add(module_name)
    for mod in extra_modules:
        module_analyzer.add(mod)

    mod_paths = module_analyzer.get_and_clear_paths()

    # Package it all in a zip
    file_like_object = io.BytesIO()
    with zipfile.ZipFile(file_like_object, 'w') as newzip:
        for mod in mod_paths:
            if os.path.isdir(mod):
                for root, dirs, files in os.walk(mod):
                    for file_ in files:
                        newzip.write(os.path.join(root, file_),
                                     os.path.relpath(os.path.join(root, file_),
                                                     os.path.join(mod, '..')))
            else:
                newzip.write(mod, os.path.basename(mod))
        # for mod in extra_modules:
        #     newzip.write(mod, os.path.basename(mod))
    return file_like_object, module_name + '.' + function_name
