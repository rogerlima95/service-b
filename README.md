
# Service-B

O `service-b` é um microserviço desenvolvido em Python que consome mensagens do RabbitMQ, processa as strings invertendo-as e salva o resultado em um arquivo no Google Cloud Storage (GCS). Cada nova mensagem lida do RabbitMQ sobrescreve o arquivo no GCS.

## Requisitos

- Python 3.7 ou superior
- RabbitMQ configurado e em execução
- Google Cloud Storage configurado com uma conta de serviço
- Kubernetes e Helm para implantação

## Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/rogerlima95/service-b
cd service-b
```

### 2. Dependências

Instale as dependências do projeto utilizando `pip`:

```bash
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente

O serviço depende de algumas variáveis de ambiente para se conectar ao RabbitMQ e ao Google Cloud Storage. As seguintes variáveis de ambiente devem ser configuradas:

- **RABBITMQ_HOST**: O endereço do servidor RabbitMQ.
- **RABBITMQ_PORT**: A porta do RabbitMQ (padrão: 5672).
- **RABBITMQ_USER**: O nome de usuário para autenticação no RabbitMQ.
- **RABBITMQ_PASSWORD**: A senha para autenticação no RabbitMQ.
- **RABBITMQ_QUEUE**: O nome da fila no RabbitMQ.
- **GCS_BUCKET**: O nome do bucket no Google Cloud Storage onde o arquivo será salvo.

### 4. Google Cloud Storage

Para o Google Cloud Storage, você precisará de um arquivo de credenciais JSON para uma conta de serviço com permissões de leitura e gravação no bucket do GCS.

1. Faça o download do arquivo JSON de credenciais do Google Cloud.
2. Crie um secret no Kubernetes para armazenar as credenciais do GCS:

```bash
kubectl create secret generic gcp-credentials-secret --from-file=credentials.json=/caminho/para/suas/credenciais/credentials.json
```

### 5. Configuração do Helm

#### 5.1 Criar o `Secret` do RabbitMQ

Antes de iniciar o Helm, crie o secret no Kubernetes para armazenar a senha do RabbitMQ:

```bash
kubectl create secret generic rabbitmq-secret --from-literal=RABBITMQ_PASSWORD=<senha_do_rabbitmq>
```

#### 5.2 Implantação com Helm

Se você já tiver o `service-b` configurado com Helm, pode instalar ou atualizar o chart da seguinte forma:

```bash
helm install service-b ./service-b
```

Ou, para atualizar:

```bash
helm upgrade service-b ./service-b
```

## Funcionamento

1. O `service-b` escuta mensagens do RabbitMQ na fila configurada.
2. Cada mensagem é processada, onde todas as strings são invertidas.
3. O resultado das strings invertidas é salvo em um arquivo no Google Cloud Storage chamado `reversed_strings.txt`.
4. O arquivo é sobrescrito cada vez que uma nova mensagem é processada.

## Kubernetes Deployment

O serviço `service-b` é implantado em Kubernetes utilizando Helm. Aqui está o resumo da configuração:

- **ConfigMap**: Armazena as configurações do RabbitMQ e o nome do bucket GCS.
- **Secret**: Usado para armazenar a senha do RabbitMQ e as credenciais do GCS.
- **Volumes**: O arquivo de credenciais do GCS é montado como volume no contêiner.

### Verificar a Implantação

Após a implantação, verifique o status dos recursos no Kubernetes:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

Verifique os logs para garantir que o `service-b` está funcionando corretamente:

```bash
kubectl logs <nome_do_pod>
```

## Como Testar

1. Envie uma mensagem para o RabbitMQ contendo um JSON com uma lista de strings.
   
   Exemplo de mensagem:

   ```json
   {
     "strings": ["hello", "world"]
   }
   ```

2. Verifique no Google Cloud Storage se o arquivo `reversed_strings.txt` foi criado e contém as strings invertidas:

   ```
   olleh
   dlrow
   ```

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias ou correções no projeto.
