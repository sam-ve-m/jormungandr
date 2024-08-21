fission spec init
fission env create --spec --name term-get-order-tkn-env --image nexus.sigame.com.br/fission-term-get-order-token:0.1.0-3 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name term-get-order-tkn-fn --env term-get-order-tkn-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name term-get-order-tkn-rt --method POST --url /order/generate_token --function term-get-order-tkn-fn