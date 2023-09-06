# Configuration file for jupyter server.
import hashlib
import random
from os import getenv, getuid
from pwd import getpwall
from traitlets.config import Config
from djlab import get_djlab_config

user = [u for u in getpwall() if u.pw_uid == getuid()][0]
c = Config() if "c" not in locals() else c


def passwd(passphrase: str):
    salt_len = 12
    h = hashlib.new("sha256")
    salt = ("%0" + str(salt_len) + "x") % random.getrandbits(4 * salt_len)
    h.update(passphrase.encode("utf-8") + salt.encode("ascii"))
    return ":".join(("sha256", salt, h.hexdigest()))


# The password to use i.e. "datajoint".
c.PasswordIdentityProvider.hashed_password = passwd(
    get_djlab_config("djlab.jupyter_server.password")
)

# Allow root access.
c.ServerApp.allow_root = False

# IP to serve on.
c.ServerApp.ip = "0.0.0.0"

# Port to serve on.
c.ServerApp.port = 8888

# Directory to use on new terminal sessions i.e. user's home
c.ServerApp.root_dir = user.pw_dir

# Shell to use for terminal sessions
c.ServerApp.terminado_settings = {"shell_command": [user.pw_shell]}

# Root for the file navigation tree menu
c.FileContentsManager.root_dir = "/home"

# Default browser url to redirect user after login
# Note: you may also use a query param to modify tree navigation on left
# e.g. localhost:8888/lab/workspaces/main/tree/dja/hi.md?file-browser-path=/dja
c.LabApp.default_url = (
    "/lab"
    if get_djlab_config("djlab.jupyter_server.display_filepath") == "NULL"
    else "/lab/tree{}".format(
        get_djlab_config("djlab.jupyter_server.display_filepath").replace(
            c.FileContentsManager.root_dir, ""
        )
    )
)


def scrub_output_pre_save(model, **kwargs):
    """scrub output before saving notebooks"""
    if not get_djlab_config("djlab.jupyter_server.save_output").upper() == "TRUE":
        # only run on notebooks
        if model["type"] != "notebook":
            return
        # only run on nbformat v4
        if model["content"]["nbformat"] != 4:
            return

        model["content"]["metadata"].pop("signature", None)
        for cell in model["content"]["cells"]:
            if cell["cell_type"] != "code":
                continue
            cell["outputs"] = []
            cell["execution_count"] = None
    else:
        return


# Allow user to specify if output should be included in save or not
c.FileContentsManager.pre_save_hook = scrub_output_pre_save

# add shortcut to move cell up/down
