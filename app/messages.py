import boto3
import json
import os
from app.database import get_db
from app.models import ClienteModel

sqs = boto3.client('sqs', region_name=os.environ.get("REGION"), aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

fila_payment_status = sqs.get_queue_url(QueueName='payment-status-topic')['QueueUrl']

def processar_mensagens_entrada():
    while True:
        response = sqs.receive_message(
            QueueUrl = fila_payment_status,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                corpo_mensagem = json.loads(message['Body'])
                status = corpo_mensagem['status']
                db = next(get_db())
                cliente = db.query(ClienteModel).filter(ClienteModel._id == corpo_mensagem['customerId']).first()
                
                if(status == "PAYMENT_ACCEPT" or status == "PAYMENT_ACCEPTED"):
                    print(f"{cliente.nome}, o pagamento do pedido '{corpo_mensagem['orderIdentifier']}' foi recebido e a cozinha irá preparar seu pedido.")
                if(status == "PAYMENT_REJECTED" or status == "PAYMENT_REJECT" ):
                    print(f"{cliente.nome}, o pagamento do pedido '{corpo_mensagem['orderIdentifier']}' foi rejeitado. Entre em contato com a operadora do seu cartão e tente novamente.")

                sqs.delete_message(
                    QueueUrl=fila_payment_status,
                    ReceiptHandle=message['ReceiptHandle']
                )
                