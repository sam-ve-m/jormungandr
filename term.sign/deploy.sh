#!/bin/bash
fission spec init
fission env create --name term-sign-env --image nexus.sigame.com.br/fission-term-sign:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --name term-sign-fn --env term-sign-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --name term-sign-rt --method PUT --url /term/sign --function term-sign-fn --spec