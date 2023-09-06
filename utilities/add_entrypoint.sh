# Update djlab config based on env vars
# echo "INFO: Updating djlab config based on env vars starting with Djlab_"
CURR_CONFIG_CONTENT=$(yq eval "." "${DJLAB_CONFIG}")
for line in $(env | grep Djlab | sort); do
	KEY="$(echo $line | cut -d'=' -f1)"
	KEY="$(echo "$KEY" | sed -r 's/^([A-Z])/\L\1/g' | \
		sed -r 's/([a-z0-9_])([A-Z])/\1_\L\2/g' | sed -r 's/__/\./g')"
	VALUE="$(echo $line | cut -d'=' -f2)"
	# echo - $KEY = $VALUE
	CURR_CONFIG_CONTENT="$(echo "${CURR_CONFIG_CONTENT}" | yq eval ". | .${KEY} = \"${VALUE}\"")"
done
# echo "INFO: Updated djlab config:"
# echo "${CURR_CONFIG_CONTENT}"
echo "${CURR_CONFIG_CONTENT}" > "${DJLAB_CONFIG}"
# Run command
"$@"