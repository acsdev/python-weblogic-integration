# WebLogic Integration

#### 1. Definição

Trata-se de um programa python que tem por objetivo executar tarefas automatizadas no weblogic.

##### ​Tarefas existentes:

- Limpeza de todos os nós ( CLEAR_ALL_NODES )

#### 2. Requisito

Python 3

Biblioteca **spur** no python 3. (Utiliza a instrução **pip install spur ** para instalar esta biblioca)

WLST (Weblogic Scripting Tools)

#### 3. Configuração

Os dados de configuração dos ambientes envolvidos estão no arquivo **config.json**. 

Abaixo segue exemplo de configuração para o ambiente **RioPrevidência SIGAP DSV**.

```json
{
    "environments": [
        {
            "oracle_home" : "<DIRETÓRIO_PARA_ORACLE_HOME>",
            "name":"--",
            "ssh_host":"--",
            "ssh_usr":"--",
            "ssh_pwd":"--",
            "admin_server_name":"SERVER NAME",
            "weblogic_host":"--",
            "weblogic_port":"7001",
            "weblogic_usr":"weblogic",
            "weblogic_pwd":"welcome1",
            "weblogic_domain_dir":"/home/<user>/webLogic_domain",
            "weblogic_nodes":["node01", "node02"]
        }
    ]
}
```

***<DIRETÓRIO_PARA_ORACLE_HOME>*** é o diretório de instalação do Oracle Middleware.

#### 4. Utilização

Para utilizar de maneira interativa, basta executar a instruação sem passar parâmetros. 

Exemplo:

```shell
./main.py
```

Para utilizar sem interatividade, basta executar passando os parâmetros necessários a função desejada. Exemplo:

```shell
./main.py DSV CLEAR_ALL_NODES
```