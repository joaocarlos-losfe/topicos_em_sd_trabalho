from typing import Union
from fastapi import FastAPI
import pika
import json
import uvicorn

def send_to_queen(cep: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(cep))
    print(f" [x] Sent body >> {cep}")

    connection.close()

app = FastAPI()

@app.post("/{cep}", tags=["Producer"])
def send(cep: str):
    send_to_queen(cep)
    return {"enviado 🚀": cep}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")


"""
ceps: ["95020-360", "64602-990", "01153 000"]
"""