ARG BASE_IMAGE_HASH
ARG PY_VER
FROM datajoint/djbase:py${PY_VER}-alpine-${BASE_IMAGE_HASH} as jup_build

LABEL maintainerName="Datajoint DevOps" \
	maintainerEmail="devops@datajoint.com" \
	maintainerCompany="DataJoint"
## Copy os, conda, and pip requirements
COPY --chown=anaconda:anaconda \
	./dist/alpine/apk_requirements.txt \
	./config/pip_requirements.txt \
	./config/conda_requirements.txt \
	/tmp/
## Install os, conda, and pip dependencies by /entrypoint.sh
## For more details check: https://github.com/datajoint/miniconda3-docker/tree/master/utilities
## shell_intercept.sh and start_up.go
RUN \
	umask u+rwx,g+rwx,o-rwx && \
	/entrypoint.sh echo "Requirements updated..." && \
	rm $APK_REQUIREMENTS && \
	rm $PIP_REQUIREMENTS && \
	rm $CONDA_REQUIREMENTS && \
	# Clean up installation cache
	find /opt/conda/conda-meta -user anaconda -exec chmod u+rwx,g+rwx,o-rwx "{}" \; && \
	conda clean -ya

ENV HOME /home/anaconda
## Copy jupyter config files that already customized to take configs from env
COPY --chown=anaconda:anaconda \
	./config/jupyter_server_config.py \
	./config/jupyter_lab_config.py \
	$HOME/.jupyter/
COPY --chown=anaconda:anaconda ./config/ipython_config.py $HOME/.ipython/
## Unconfigurable jupyterlab:DocManagerExtension
## Set markdown preview as default
RUN	DOC_MANGER_CONFIG=$(jq -r \
		'.properties.defaultViewers.default = {"markdown":"Markdown Preview"}' \
		$(echo "/opt/conda/share/jupyter/lab/schemas/@jupyterlab/docmanager-extension\
			/plugin.json" | tr -d '\n' | tr -d '\t')) && \
	echo "$DOC_MANGER_CONFIG" > \
		$(echo "/opt/conda/share/jupyter/lab/schemas/@jupyterlab/docmanager-extension\
			/plugin.json" | tr -d '\n' | tr -d '\t') && \
	chmod u+rwx,g+rwx,o-rwx \
		$(echo "/opt/conda/share/jupyter/lab/schemas/@jupyterlab/docmanager-extension\
			/plugin.json" | tr -d '\n' | tr -d '\t')
## Add repo README as a landing page
## Will be specified in env: JUPYTER_LAB_DEFAULT_URL=/home/anacoda/README.md
COPY --chown=anaconda:anaconda ./config/README.md $HOME

## Change ownership for later customized env: HOST_ID mostly for mounting local files to debug
## Docker COPY will set uid:gid to anaconda(3000):anaconda since default uid set to 3000 in datajoint/miniconda3-docker
RUN \
	chmod -R 775 $HOME/.jupyter && \
	chmod -R 775 $HOME/.ipython 


# Squashed Final Image
FROM scratch
COPY --from=jup_build / /
LABEL maintainerName="Raphael Guzman" \
	maintainerEmail="raphael@datajoint.com" \
	maintainerCompany="DataJoint"
USER anaconda:anaconda
ENV ENV "/home/anaconda/.ashrc"
# Add conda to path here for use in downstream dockerfiles
ENV PATH /opt/conda/bin:$PATH
ENV HOME /home/anaconda
ENV LANG C.UTF-8
ENV APK_REQUIREMENTS /tmp/apk_requirements.txt
ENV PIP_REQUIREMENTS /tmp/pip_requirements.txt
ENV CONDA_REQUIREMENTS /tmp/conda_requirements.txt
ENV DJLAB_CONFIG /tmp/djlab_config.yaml
ENTRYPOINT ["/entrypoint.sh"]
WORKDIR /home/anaconda
VOLUME /tmp/.X11-unix
EXPOSE 8888
CMD ["jupyter", "lab"]
