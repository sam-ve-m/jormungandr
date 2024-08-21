#!/bin/bash

fission spec init
fission env create --spec --name payment-order-ouroinvest-env --image nexus.sigame.com.br/fission-async:0.1.7 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name payment-order-ouroinvest-fn --env payment-order-ouroinvest-env --src "./func/*" --entrypoint main.payment_order_ouroinvest --executortype newdeploy --maxscale 3
fission route create --spec --name payment-order-ouroinvest-rt --method POST --url /webhook/ouroinvest/payment_order --function payment-order-ouroinvest-fn