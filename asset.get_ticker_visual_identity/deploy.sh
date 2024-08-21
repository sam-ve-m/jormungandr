#!/bin/bash
fission spec init
fission env create --spec --name get-ticker-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name ticker-visual-fn --env get-ticker-env --src "./func/*" --entrypoint main.get_ticker_visual_identity --executortype newdeploy --maxscale 1
fission route create --name get-ticker-visual-identity --spec --method GET --url /get_ticker_visual_identity --function ticker-visual-fn