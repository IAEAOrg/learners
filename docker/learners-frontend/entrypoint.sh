#!/bin/sh

# Check if the variable doesn't start with "http" or "/"
if [ "${LEARNERS_BASE_URL#"http"}" = "$LEARNERS_BASE_URL" ] && [ "${LEARNERS_BASE_URL#"/"}" = "$LEARNERS_BASE_URL" ]; then
    LEARNERS_BASE_URL="/$LEARNERS_BASE_URL"
fi

# Ensure the variable does not end with "/"
if [ "${LEARNERS_BASE_URL%"${LEARNERS_BASE_URL##*[!/]}"}" = "/" ]; then
    LEARNERS_BASE_URL="${LEARNERS_BASE_URL%/}"
fi

# Check if the variable would result in "/"
if [ "$LEARNERS_BASE_URL" = "/" ]; then
    LEARNERS_BASE_URL=""
fi

echo "LEARNERS_BASE_URL = $LEARNERS_BASE_URL"

if [ "$LEARNERS_ENABLE_NGINX_SUBSTITUTION" -eq 1 ]; then
    # Substitute environment variables in the NGINX configuration file
    envsubst '$LEARNERS_BASE_URL' < /etc/nginx/template/nginx.conf.template > /etc/nginx/conf.d/default.conf
else
    mv /etc/nginx/template/nginx.conf.template /etc/nginx/conf.d/default.conf
fi

# Start NGINX
nginx -g "daemon off;"
