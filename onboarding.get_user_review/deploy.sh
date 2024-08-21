#!/bin/bash
fission spec init
fission env create --spec --name get-user-review-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name get-user-review-fn --env get-user-review-env --src "./func/*" --entrypoint main.user_data_review --executortype newdeploy --maxscale 1
fission route create --spec --name get-user-review-rt --method GET --url /onboarding/get_user_review --function get-user-review-fn
