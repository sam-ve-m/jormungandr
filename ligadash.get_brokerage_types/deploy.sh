fission spec init
fission env create --spec --name dash-enum-broker-tp-env --image nexus.sigame.com.br/fission-ligadash-enum-brokerage-types:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name dash-enum-broker-tp-fn --env dash-enum-broker-tp-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name dash-enum-broker-tp-rt --method GET --url /enum/brokerage_type --function dash-enum-broker-tp-fn
