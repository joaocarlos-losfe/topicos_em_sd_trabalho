import pika
import sys
import os
import json
import requests
from datetime import datetime
import uuid
import pymongo

def insert_on_database(data: dict):
    client = pymongo.MongoClient()
    db = client["weather"]
    
    result = db["weather"].insert_one({
        **data
    })

    print("inserted data on database")
    print(result)

def get_api_data(api_url:str):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    
    return None

def getTemperature(cep:str):
    api_url_cep = f"https://brasilapi.com.br/api/cep/v2/{cep}"
    
    city_data = get_api_data(api_url_cep)
    
    if city_data:
        
        city = city_data["city"].lower()
        state = city_data["state"]
        street = city_data["street"]
        api_url_weather = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d1af9eb638a7a24e06f0889f9e2c6a0d&lang=pt_br&units=metric"
        
        weather_result = get_api_data(api_url_weather)

        if weather_result:
            temperature = weather_result["main"]["temp"]
            return {
                "_id": uuid.uuid4().hex,
                "data": str(datetime.now()),
                "temperatura": f"{temperature}°", 
                "cidade": city,
                "estado": state,
                "rua": street
            }
        else:
            print('a API não encontrou a cidade')
    else:
        print("CEP invalido")
    
    
    return None

def callback(ch, method, properties, body):
    print("[x] Mensagem recebida ✅\nProcessando...")
    cep = str(body.decode("UTF-8")).removeprefix("\"").removesuffix("\"")
    print(cep)
    weather = getTemperature(cep)

    if weather:
        insert_on_database(weather)
        print(weather)

    print(' [*] Aguardando menssagens. CTRL+C para sair')

    
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

    print(' [*] Aguardando menssagens. CTRL+C para sair')

    channel.start_consuming()

if __name__ == '__main__':
    try:

        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

"""
ceps: ["95020-360", "64602-990", "01153-000"]
"""