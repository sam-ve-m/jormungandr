# `/get_ticker_visual_identity`
> _Endpoint para a pegar as imagens utilizadas na visualização do ticker (logo, banner e thumbnail)_

## Requisição

#### **Modelo de Requisição:**

**Rota HTTP:** `http:{host}/get_ticker_visual_identity`

**Corpo da requisição:**
```json
{
    "symbol": "Ticker refente as imagens.",
    "region": "Região do ticker. ('br' ou 'us')",
    "type": "Tipo de imagem que está buscando. ('logo', 'banner' ou 'thumbnail')"
}
```

## Resposta

#### **Modelo de Resposta:**

```json
{
    "result": "Imagem requisitada.",
    "message": "Mensagem com algum detalhamento da situação.",
    "success": "Sucesso da requisição. (true ou false)",
    "code": "Código de status."
}
```
**Códigos de Status disponíveis:**

- **SUCCESS:**

  Código: 0


- **INVALID_PARAMS:**

  Código: 10


- **DATA_NOT_FOUND:**

  Código: 99


- **INTERNAL_SERVER_ERROR:**

  Código: 100


## Exemplo

#### Requisição:
```json
{
    "symbol": "PETR",
    "region": "br",
    "type": "logo"
}
```

#### Resposta:
```json
{
    "result": null,
    "message": "No images found.",
    "success": true,
    "code": 99
}
```