fission spec init
fission env create --spec --name onb-us-enum-jb-stat-env --image nexus.sigame.com.br/fission-onboarding-us-enum-job-status:0.2.0-0 --poolsize 1 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-enum-jb-stat-fn --env onb-us-enum-jb-stat-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-us-enum-jb-stat-rt --method GET --url /enum/employ_status_us --function onb-us-enum-jb-stat-fn
