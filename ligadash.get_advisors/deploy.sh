fission spec init
fission env create --spec --name dash-enum-advisor-env --image nexus.sigame.com.br/fission-ligadash-enum-advisor:0.1.1 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name dash-enum-advisor-fn --env dash-enum-advisor-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name dash-enum-advisor-rt --method GET --url /enum/advisor --function dash-enum-advisor-fn
