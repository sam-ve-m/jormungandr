fission spec init
fission env create --spec --name onb-us-mkt-exp-env --image nexus.sigame.com.br/fission-onboarding-us-market-expirience-ben:0.2.0-1 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-mkt-exp-fn --env onb-us-mkt-exp-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-us-mkt-exp-rt --method PUT --url /onboarding/update_experience_time --function onb-us-mkt-exp-fn