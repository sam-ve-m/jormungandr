fission spec init
fission env create --spec --name sup-tckt-snapshot-env --image nexus.sigame.com.br/fission-support-ticket-snapshot:0.1.0-1 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name sup-tckt-snapshot-fn --env sup-tckt-snapshot-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name sup-tckt-snapshot-rt --method GET --url /support/get-user-snapshot --function sup-tckt-snapshot-fn