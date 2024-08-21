fission spec init
fission env create --spec --name wtc-list-fix-exists-env --image nexus.sigame.com.br/fission-wacth-list-fixed-income-exists:0.1.0-0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-fix-exists-fn --env wtc-list-fix-exists-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-fix-exists-rt --method GET --url /watch_list/fixed_income/exists --function wtc-list-fix-exists-fn
