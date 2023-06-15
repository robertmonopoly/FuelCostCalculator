#!/bin/sh

log () {
    type="$1"; shift
    printf '%s [%s] [Entrypoint]: %s\n' "$(date -Iseconds)" "$type" "$*"
}

log Note "Entrypoint script for Fuel calculator started"

if [ ! -d "/srv/fuel/instance" ]; then
    log Note "Creating data directory"
    mkdir -p "/srv/fuel/instance"
fi

owner=$(stat -c "%U %G" /srv/fuel/instance)
if [ "$owner" != "fuel fuel" ]; then
    log Note "Changing ownership of data directory"
    chown -R fuel:fuel /srv/fuel/instance
fi

log Note "Startup tasks finished, starting server"

cd /srv/fuel || exit
exec runuser -u  fuel "$@"

exit $?
