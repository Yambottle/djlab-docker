Documentation for the DataJoint's DJLab Image
#############################################

| A docker image optimized for running a `JupyterLab <https://jupyterlab.readthedocs.io/en/stable/>`_ environment with `DataJoint Python <https://github.com/datajoint/datajoint-python>`_.
| For more details, have a look at `prebuilt images <https://hub.docker.com/r/datajoint/djlab>`_, `source <https://github.com/datajoint/djlab-docker>`_, and `documentation <https://datajoint.github.io/djlab-docker>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Launch Locally
**************

Debian
======
.. code-block:: shell

   docker-compose -f dist/debian/docker-compose.yaml --env-file config/.env up --build

Alpine
======
.. code-block:: shell

   docker-compose -f dist/alpine/docker-compose.yaml --env-file config/.env up --build

Features
********

- Adds a JupyterLab environment.
- Includes Jupyter Lab debugger (py3.8+).
- Defaults Markdown rendering to ``preview`` within JupyterLab.
- Adds ``djlab`` magic: a mechanism for configuring and modifying Jupyter features w/o JupyterLab service interruption.
- Adds ``jupyter-collaboration`` extension: a mechanism for sharing notebooks and collaborating with others in real-time.
- Applies image compression.

Usage Notes
***********

- ``djlab`` can be accessed in a notebook via magic e.g. ``%djlab [args*]`` or programatically.
- To show the current config use: ``%djlab``.
- To access a specific config use: ``%djlab [djlab config index]`` e.g. ``%djlab djlab.jupyter_server.save_output``.
- To set a specific config use: ``%djlab [djlab config index] [value]`` e.g. ``%djlab djlab.jupyter_server.save_output TRUE``.
- ``djlab`` magic supports the following configuration:

  - ``djlab.jupyter_server.display_filepath`` - (string, default: ``'NULL'``, env_var: ``Djlab_JupyterServer_DisplayFilepath``) Absolute filepath of file to show immediately after login.
  - ``djlab.jupyter_server.password`` - (string, default: ``'datajoint'``, env_var: ``Djlab_JupyterServer_Password``) Password to allow JupyterLab login.
  - ``djlab.jupyter_server.save_output`` - (string, default: ``'FALSE'``, env_var: ``Djlab_JupyterServer_SaveOutput``) Determine if output should be saved when saving noteboook.

- To access ``djlab`` magic programatically, you may call into like so: ``print(__import__('djlab').get_djlab_config('djlab.jupyter_server'))``.

Testing
*******

To rebuild and run tests locally, execute the following statements:

.. code-block:: shell

   set -a  # automatically export sourced variables
   . config/.env  # source config for build and tests
   docker buildx bake -f dist/${DISTRO}/docker-compose.yaml --set *.platform=${PLATFORM} --set *.context=. --load  # build image
   tests/main.sh  # run tests
   set +a  # disable auto-export behavior for sourced variables

Base Image
**********

Build is a child of `datajoint/djbase <https://datajoint.github.io/djbase-docker/>`_.