#!/bin/sh
docker build -t webhook.caf.cpf --secret id=pipconfig,src=$HOME/.pip.conf .
