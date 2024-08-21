fission spec init
fission env create --spec --name dash-enum-bmf-clnt-tp-env --image nexus.sigame.com.br/fission-ligadash-enum-bmf-client-type:0.1.1 newdeploy --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name dash-enum-bmf-clnt-tp-fn --env dash-enum-bmf-clnt-tp-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name dash-enum-bmf-clnt-tp-rt --method GET --url /enum/bmf-clnt-tp --function dash-enum-bmf-clnt-tp-fn
