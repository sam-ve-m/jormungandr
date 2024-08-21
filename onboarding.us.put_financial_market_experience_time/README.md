## ONBOARDING US UPDATE FINANCIAL MARKET EXPERIENCE TIME
#### _FISSION PARA ATUALIZAÇÃO DOS DADOS DE TEMPO DE EXPERIÊNCIA EM MERCADO FINANCEIRO
___
### Esse projeto refere-se a rota do Sphinx:

```
UserService.update_time_experience_us
```
&nbsp; 
### 1.1. `update_market_experience_time`
&nbsp; 
#### MODELO DE REQUISIÇÃO:

```http://127.0.0.1:9000/update-market-experience-time```

&nbsp; 
##### BODY REQUEST
```
{
    "time_experience": "10"
}
```
&nbsp;

#### MODELO DE RESPOSTA:

```
{
    "result": true,
    "message": "The Time Experience of Financial Market Was Updated Successfully",
    "success": true,
    "code": 200
}

```
&nbsp;
#### RODAR SCRIPT DE TESTS:

- No mesmo nível da pasta root, rodar o seguinte comando no terminal: `bash tests.sh`

&nbsp;