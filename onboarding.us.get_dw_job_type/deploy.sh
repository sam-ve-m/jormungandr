fission spec init
fission env create --spec --name onb-us-enum-jb-tp-env --image nexus.sigame.com.br/fission-onboarding-us-enum-job-type:0.2.0-0 --poolsize 1 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-enum-jb-tp-fn --env onb-us-enum-jb-tp-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-us-enum-jb-tp-rt --method GET --url /enum/get_employ_type --function onb-us-enum-jb-tp-fn
