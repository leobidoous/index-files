from requests import get


def integration_viacep(cep):
    resp = get("https://viacep.com.br/ws/%s/json/" % cep)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'Error': True}