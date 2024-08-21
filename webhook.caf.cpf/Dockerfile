FROM fission/python-env-3.10
COPY ./fission.py ./server.py


RUN mkdir -p /opt/envs/etria.lionx.com.br
RUN touch /opt/envs/etria.lionx.com.br/.env

RUN mkdir -p /opt/envs/persephone.client.python.lionx.com.br
RUN touch /opt/envs/persephone.client.python.lionx.com.br/.env

RUN mkdir -p /opt/envs/iara.client.python.lionx.com.br
RUN touch /opt/envs/iara.client.python.lionx.com.br/.env

RUN mkdir -p /app
RUN touch /app/.env


COPY ./requirements.txt ./requirements.txt

ENV PIP_CONFIG_FILE=/root/.config/pip/pip.conf
RUN --mount=type=secret,id=pipconfig,target=/root/.config/pip/pip.conf \
pip install -r requirements.txt

COPY ./func ./func

COPY ./.build/entrypoint.sh /opt/app/entrypoint.sh
RUN chmod +x /opt/app/entrypoint.sh

ENTRYPOINT ["/opt/app/entrypoint.sh"]
