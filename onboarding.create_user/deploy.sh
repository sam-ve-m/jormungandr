fission spec init
fission env create --spec --name onb-br-create-env --image nexus.sigame.com.br/fission-onboarding-br-create:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-create-fn --env onb-br-create-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-create-rt --method POST --url /onboarding/create_user --function onb-br-create-fn
