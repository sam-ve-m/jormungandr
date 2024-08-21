FROM fission/python-env-3.10
COPY ./fission.py ./server.py


RUN mkdir -p /opt/envs/etria.lionx.com.br
RUN touch /opt/envs/etria.lionx.com.br/.env


COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./func ./func
