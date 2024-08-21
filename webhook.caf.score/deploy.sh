fission spec init
fission env create --spec --name wbh-caf-score-env --image nexus.sigame.com.br/fission-webhook-caf-score:0.1.0-0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wbh-caf-score-fn --env wbh-caf-score-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name wbh-caf-score-rt --method POST --url /webhook/caf/score_validation --function wbh-caf-score-fn
