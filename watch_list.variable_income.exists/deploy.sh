fission spec init
fission env create --spec --name wtc-list-var-exists-env --image nexus.sigame.com.br/fission-wacth-list-variable-income-exists:0.2.0-0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-var-exists-fn --env wtc-list-var-exists-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-var-exists-rt --method GET --url /watch_list/variable_income/exists --function wtc-list-var-exists-fn
