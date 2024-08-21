## ONBOARDING US TO GET EMPLOY POSITIONS
#### _FISSION PARA LISTAR OS CARGOS DISPONÍVEIS NA DRIVE WEALTH
___
### Esse projeto refere-se a rota do Sphinx:

```
SinaCorTypes.get_employ_position
```
&nbsp; 
### 1.1. `get_employ_position`
&nbsp; 
#### MODELO DE REQUISIÇÃO:

```http://127.0.0.1:9000/get-employ-positions```

&nbsp; 
##### BODY REQUEST
```
NADA É REQUERIDO
```
&nbsp;

#### MODELO DE RESPOSTA:

```
{
    "result": [
        {
            "code": "ACCOUNTANT",
            "description": "ACCOUNTANT"
        },
        {
            "code": "ACTUARY",
            "description": "ACTUARY"
        }
    ],
    "message": "SUCCESS",
    "success": true,
    "code": 0
}

```
&nbsp;
#### RODAR SCRIPT DE TESTS:

- No mesmo nível da pasta root, rodar o seguinte comando no terminal: `bash tests.sh`

&nbsp;