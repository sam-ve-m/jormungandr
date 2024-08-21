fission spec init
fission env create --spec --name onb-us-enum-exp-env --image nexus.sigame.com.br/fission-onboarding-us-enum-exp:0.1.0 --poolsize 1 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-enum-exp-fn --env onb-us-enum-exp-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-us-enum-exp-rt --method GET --url /enum/experience_time --function onb-us-enum-exp-fn
