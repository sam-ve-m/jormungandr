# LIGA NEST API - Template


## Description

[Nest](https://github.com/nestjs/nest) framework TypeScript starter repository.

## Installation


### create a local .env

``` text
PORT=3000
NODE_ENV=dev
MONGO_CONNECTION_URL=localhost
DB_NAME=lionx
```

```bash
$ npm install

# config
$ npm run config
```

## Running the app

```bash
# development
$ npm run start

# watch mode
$ npm run start:dev

# production mode
$ npm run start:prod
```

## Test

```bash
# unit tests
$ npm run test

# e2e tests
$ npm run test:e2e

# test coverage
$ npm run test:cov
```

## Directory structure

This application follow the following directory structure and principles:
```
root (your project root directory)
 |---> .config/        (infrastructure related files. Eg: terraform)
 |---> .github/        (github actions files)
 |---> doc/            (project additional documentation files)
 |---> db/             (database script files, case needed)
 |---> build/          (build script files eg: powershell, docker compose, bash, sh, etc)
 |---> src/            (main source files)
     |---> common      (external libraries implementations. Eg: Queues, database, caching, etc)
     |---> modules     (project source code files. Eg: domain entities, use-cases, services, etc)
     |---> nest-core   (nestjs framework related implementation files. Eg: filters, middlewares, guards, etc)
 |---> test/           (Testes unitários, testes de integração, testes funcionais, testes automatizados e etc)
```


## Support

Nest is an MIT-licensed open source project. It can grow thanks to the sponsors and support by the amazing backers. If you'd like to join them, please [read more here](https://docs.nestjs.com/support).

## Stay in touch

- Author - [Kamil Myśliwiec](https://kamilmysliwiec.com)
- Website - [https://nestjs.com](https://nestjs.com/)
- Twitter - [@nestframework](https://twitter.com/nestframework)

## License

Nest is [MIT licensed](LICENSE).
