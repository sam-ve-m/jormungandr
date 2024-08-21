fission spec init
fission env create --spec --name asset-visual-bank-env --image nexus.sigame.com.br/fission-asset-visual-identity-bank:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name asset-visual-bank-fn --env asset-visual-bank-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name asset-visual-bank-rt --method GET --url /get_bank_logo --function asset-visual-bank-fn