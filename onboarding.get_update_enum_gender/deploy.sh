fission spec init
fission env create --spec --name onb-br-enum-gender-env --image nexus.sigame.com.br/fission-onboarding-br-enum-gender:0.2.0-0 --poolsize 1 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-enum-gender-fn --env onb-br-enum-gender-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-enum-gender-rt --method GET --url /enum/gender --function onb-br-enum-gender-fn
