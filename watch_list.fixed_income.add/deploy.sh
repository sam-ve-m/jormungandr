fission spec init
fission env create --spec --name wtc-list-fix-fix-add-env --image nexus.sigame.com.br/fission-wacth-list-fixed-income-add:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-fix-fix-add-fn --env wtc-list-fix-fix-add-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-fix-fix-add-rt --method POST --url /watch_list/fixed_income/add --function wtc-list-fix-fix-add-fn
