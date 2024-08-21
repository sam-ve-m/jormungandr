fission spec init
fission env create --spec --name acc-address-by-cep-env --image nexus.sigame.com.br/fission-account-address-by-cep:0.1.0-3 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name acc-address-by-cep-fn --env acc-address-by-cep-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name acc-address-by-cep-rt --method GET --url /account/address --function acc-address-by-cep-fn