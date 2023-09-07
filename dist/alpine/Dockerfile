ARG BASE_IMAGE_HASH
ARG PY_VER
FROM datajoint/djbase:py${PY_VER}-alpine-${BASE_IMAGE_HASH} as jup_build

LABEL maintainerName="Raphael Guzman" \
	maintainerEmail="raphael@datajoint.com" \
	maintainerCompany="DataJoint"
ENV DJLAB_CONFIG /tmp/djlab_config.yaml
COPY --chown=anaconda:anaconda ./dist/alpine/apk_requirements.txt \
    ./config/pip_requirements.txt ./config/djlab_config.yaml /tmp/
COPY --chown=anaconda:anaconda ./utilities/djlab.py ./utilities/setup.py /main/
RUN \
	umask u+rwx,g+rwx,o-rwx && \
	chmod u=rw,g=rw,o=r /tmp/djlab_config.yaml && \
	# Install jupyter
	/entrypoint.sh echo "Requirements updated..." && \
	rm $APK_REQUIREMENTS && \
	rm $PIP_REQUIREMENTS && \
	# Install djlab magic
	pip install --no-cache-dir /main && \
	# Install jupyter widgets
	conda install -y -n base -c conda-forge jupyterlab_widgets ipywidgets "nodejs>=18" && \
	# Add markdown preview as default
	DOC_MANGER_CONFIG=$(jq -r \
		'.properties.defaultViewers.default = {"markdown":"Markdown Preview"}' \
		$(echo "/opt/conda/share/jupyter/lab/schemas/@jupyterlab/docmanager-extension\
			/plugin.json" | tr -d '\n' | tr -d '\t')) && \
	echo "$DOC_MANGER_CONFIG" > \
		$(echo "/opt/conda/share/jupyter/lab/schemas/@jupyterlab/docmanager-extension\
			/plugin.json" | tr -d '\n' | tr -d '\t') && \
	chmod u+rwx,g+rwx,o-rwx \
		$(echo "/opt/conda/share/jupyter/lab/schemas/@jupyterlab/docmanager-extension\
			/plugin.json" | tr -d '\n' | tr -d '\t') && \
	# Clean up
	find /opt/conda/conda-meta -user anaconda -exec chmod u+rwx,g+rwx,o-rwx "{}" \; && \
	rm -r /main/* && \
	conda clean -ya
COPY --chown=anaconda:anaconda ./config/jupyter_server_config.py /etc/jupyter/
COPY --chown=anaconda:anaconda ./config/ipython_config.py /etc/ipython/
# Add add_entrypoint.sh to /entrypoint.sh
COPY ./utilities/add_entrypoint.sh /tmp/add_entrypoint.sh
USER root:anaconda
RUN \
	# Install yq
	wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq && \
  chmod +x /usr/bin/yq && \
	# Add add_entrypoint.sh to /entrypoint.sh
	(cat /entrypoint.sh | \
		tr '\n' '\r' | \
		sed "s~# Run command\r\"\$@\"~~g" | \
		tr '\r' '\n' && \
		cat /tmp/add_entrypoint.sh) > /tmp/entrypoint.sh && \
	mv /tmp/entrypoint.sh /entrypoint.sh && \
	chmod +x /entrypoint.sh && \
	rm /tmp/add_entrypoint.sh
USER anaconda:anaconda
# Add landing page
ENV HOME /home/anaconda
COPY --chown=anaconda:anaconda ./config/README.md /home/anaconda/


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
