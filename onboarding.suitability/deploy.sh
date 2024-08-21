fission spec init
fission env create --spec --name onb-br-suitability-env --image nexus.sigame.com.br/fission-onboarding-br-suitability::0.2.0-0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-suitability-fn --env onb-br-suitability-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-suitability-rt --method POST --url /onboarding/set_suitability --function onb-br-suitability-fn
