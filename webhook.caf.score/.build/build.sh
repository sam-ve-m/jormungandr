#!/bin/sh
docker build -t webhook.caf.score --secret id=pipconfig,src=$HOME/.pip.conf .
