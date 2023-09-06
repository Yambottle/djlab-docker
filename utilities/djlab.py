from IPython.core.magic import line_magic, Magics, magics_class
import yaml
import os
from functools import reduce


def get_djlab_config(key):
    with open(os.getenv("DJLAB_CONFIG"), "r") as f:
        config = yaml.safe_load(f)
        return reduce(dict.__getitem__, key.split("."), config)


def set_djlab_config(key, value):
    try:
        os.system(
            "yq eval -i '. | .{key} = {value}' {config_path}".format(
                key=key, value=value, config_path=os.getenv("DJLAB_CONFIG")
            )
        )
    except SystemExit:
        pass


@magics_class
class DjlabConfig(Magics):
    @line_magic
    def djlab(self, line):
        args = line.split()
        if len(args) == 0:
            print(get_djlab_config(""))
        elif len(args) == 1:
            print(get_djlab_config(args[0]))
        elif len(args) == 2:
            set_djlab_config(args[0], args[1])


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(DjlabConfig)
