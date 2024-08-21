#!/bin/bash

fission spec init
fission env create --spec --name onboarding-ouroinvest-env --image nexus.sigame.com.br/fission-async:0.1.7 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name onboarding-ouroinvest-fn --env onboarding-ouroinvest-env --src "./func/*" --entrypoint main.onboarding_ouroinvest --executortype newdeploy --maxscale 3
fission route create --spec --name onboarding-ouroinvest-rt --method POST --url /webhook/ouroinvest/onboarding --function onboarding-ouroinvest-fn