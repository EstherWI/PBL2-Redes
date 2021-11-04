# PBL2-Redes - Computação em Névoa
## Pré-requisitos

Para rodar a aplicação web, você vai precisar ter instalado:
[Python 3.5 ou superior](https://www.python.org/downloads/) - 


```bash
# Clone este repositório
$ git clone https://github.com/EstherWI/PBL-Redes-Front.git
# Instale as dependências
$ pip install -r requirements.txt
```

## Para executar a aplicação

### Executar a FOG 
$ python fog.py

### Rodar o Publisher dos pacientes
$ python publisher.py

### Abrir tela do médico
$ python medico.py

### Variáveis de ambiente

Criar arquivo *.env* na pasta raiz do diretório e setar as configurações.

Ex env1:

FOG="FOG1"
A=0
B=100
cliente_local=600
cliente_publico=601

Ex env2:

FOG="FOG2"
A = 200
B = 300
cliente_local = 602
cliente_publico = 603

Observação: Caso queira rodar mais uma fog em local diferente, basta seguir os exemplos acima,
diferenciando os nomes das fogs, o intevalo A e B e os clientes.

## O deploy da API foi feito no Heroku: https://connect-covid.herokuapp.com

```
