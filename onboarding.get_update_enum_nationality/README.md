# Requirements

- A Kubernetes cluster running Fission
- The company's Python Docker images

# Setup

## Install Fission
See instructions in official documentation below:
> https://fission.io/docs/installation/

Or in the Confluence installation tutorial:
> https://lionx.atlassian.net/wiki/spaces/DEV/pages/336429057/Fission+-+Function+as+a+service

## Install Docker images

Run these commands in the terminal:
```bash
docker login -u [USER] -p [PASSWORD] nexus.sigame.com.br
docker pull nexus.sigame.com.br/fission-cx-env-3.8:0.0.3
docker pull nexus.sigame.com.br/fission-cx-builder-3.8:0.0.3
```

Make sure the images are installed:
```bash
docker images 
```

## Run project

Run in the project root folder:

```bash
fission spec apply
```

## Run tests

Run the `tests.sh`:

```bash
bash tests.sh
```
