#!/usr/bin/env bash

POSTGRES_USER="user"
POSTGRES_DB="gallery"

#===============================================================================

log()  { echo -e "\x1b[1m[\x1b[93mLOG\x1b[0m\x1b[1m]\x1b[0m ${@}";  }
info() { echo -e "\x1b[1m[\x1b[92mINFO\x1b[0m\x1b[1m]\x1b[0m ${@}"; }
warn() { echo -e "\x1b[1m[\x1b[91mWARN\x1b[0m\x1b[1m]\x1b[0m ${@}"; }

install_pip_deps(){
    log "Installing project dependencies ..."
    python3 -m pip install -r requirements.txt 1>/dev/null
    info "Done !"
}

prepare_db(){
    log "Configuring container db"
    POSTGRES_PASSWORD="$(cat /dev/urandom | base64 | head -n3 | tr -d "\n" | sed 's!+!!g' | sed 's!/!!g' | cut -b -20)"
    cp 'docker/prod/env/db.prod.env.sample'                                  'docker/prod/env/db.prod.env'
    sed -i "s/POSTGRES_USER=.*/POSTGRES_USER=${POSTGRES_USER}/g"             'docker/prod/env/db.prod.env'
    echo " + POSTGRES_USER     = ${POSTGRES_USER}"
    sed -i "s/POSTGRES_DB=.*/POSTGRES_DB=${POSTGRES_DB}/g"                   'docker/prod/env/db.prod.env'
    echo " + POSTGRES_DB       = ${POSTGRES_DB}"
    sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=${POSTGRES_PASSWORD}/g" 'docker/prod/env/db.prod.env'
    echo " + POSTGRES_PASSWORD = ${POSTGRES_PASSWORD}"
    info "Done."
}

prepare_django(){
    local PAGETITLE=""
    local SECRET_KEY="$(cat /dev/urandom | base64 | head -n5 | tr -d "\n" | sed 's!+!!g' | sed 's!/!!g' | cut -b -64)"
    log "Configuring container django"
    cp 'docker/prod/env/django.prod.env.sample' 'docker/prod/env/django.prod.env'
    sed -i "s/SQL_ENGINE=.*/SQL_ENGINE=django.db.backends.postgresql/g" 'docker/prod/env/django.prod.env'
    sed -i "s/SQL_DATABASE=.*/SQL_DATABASE=${POSTGRES_DB}/g"            'docker/prod/env/django.prod.env'
    sed -i "s/SQL_USER=.*/SQL_USER=${POSTGRES_USER}/g"                  'docker/prod/env/django.prod.env'
    sed -i "s/SQL_PASSWORD=.*/SQL_PASSWORD=${POSTGRES_PASSWORD}/g"      'docker/prod/env/django.prod.env'
    sed -i "s/SQL_HOST=.*/SQL_HOST=db/g"                                'docker/prod/env/django.prod.env'
    sed -i "s/SQL_PORT=.*/SQL_PORT=5432/g"                              'docker/prod/env/django.prod.env'
    sed -i "s/DATABASE=.*/DATABASE=postgres/g"                          'docker/prod/env/django.prod.env'
    sed -i "s/DEBUG=.*/DEBUG=0/g"                                       'docker/prod/env/django.prod.env'
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/g"                 'docker/prod/env/django.prod.env'
    sed -i "s/PAGETITLE=.*/PAGETITLE=${PAGETITLE}/g"                    'docker/prod/env/django.prod.env'
    info "Done."
}

prepare_gunicorn(){
    log "Configuring container gunicorn"
    cp 'docker/prod/env/gunicorn.prod.env.sample' 'docker/prod/env/gunicorn.prod.env'
    sed -i "s/ACCESS_LOG=.*/ACCESS_LOG=gunicorn-access.log/g" 'docker/prod/env/gunicorn.prod.env'
    sed -i "s/ERROR_LOG=.*/ERROR_LOG=gunicorn-error.log/g"    'docker/prod/env/gunicorn.prod.env'
    info "Done."
}

build(){
    if [[ -f "./docker/prod/docker-compose.prod.yml" ]]; then
        docker-compose -f ./docker/prod/docker-compose.prod.yml up -d --build 1>/dev/null
    fi
}

#===============================================================================

install_pip_deps
#
prepare_db
prepare_django
prepare_gunicorn
#
build
