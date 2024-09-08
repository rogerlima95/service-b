import pika
import json
import os
from google.cloud import storage

# Configurações do RabbitMQ
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.getenv('RABBITMQ_PORT', '5672')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'queue')
rabbitmq_user = os.getenv('RABBITMQ_USER', 'user')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'senhaSegura')

# Configuração do Google Cloud Storage
bucket_name = os.getenv('GCS_BUCKET_NAME', 'meu-bucket-2021')

def save_to_gcs(reversed_strings):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('reversed_strings.txt')

    blob.upload_from_string('\n'.join(reversed_strings))

    print("Arquivo salvo no Google Cloud Storage com sucesso.")

def callback(ch, method, properties, body):
    print("Mensagem recebida do RabbitMQ")
    strings = json.loads(body)

    # Inverter as strings
    reversed_strings = [s[::-1] for s in strings]

    # Salvar as strings invertidas no GCS
    save_to_gcs(reversed_strings)

    # Confirma o processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=int(rabbitmq_port), credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback)

    print("Aguardando mensagens do RabbitMQ. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer()