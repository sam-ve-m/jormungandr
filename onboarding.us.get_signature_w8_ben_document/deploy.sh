fission spec init
fission env create --spec --name onb-us-sign-w8-env --image nexus.sigame.com.br/fission-onboarding-us-sign-w8-ben:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-sign-w8-fn --env onb-us-sign-w8-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-us-sign-w8-rt --method PUT --url /onboarding/update_w8_ben --function onb-us-sign-w8-fn