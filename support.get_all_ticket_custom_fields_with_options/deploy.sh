#!/bin/bash
fission spec init
fission env create --spec --name get-custom-fields-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name get-custom-fields-fn --env get-custom-fields-env --src "./func/*" --entrypoint main.get_all_ticket_custom_fields --executortype newdeploy --maxscale 1
fission route create --spec --name get-custom-fields-rt --method GET --url /support/get-custom-fields --function get-custom-fields-fn