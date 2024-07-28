from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)

# Настройки Twilio
account_sid = 'AC84ef9e21ea9b9025f1ab1ad72f2deac3'
auth_token = '75e99a840f4fc4fb49871e555d42e612'
twilio_number = '+14155238886'
client = Client(account_sid, auth_token)

# Группа водителей (список номеров телефонов)
drivers_group = ['+77085420968', 'driver2_number']

# Минимальная стоимость поездки
min_cost = 1000
cost_per_km = 50

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    if 'адрес' in incoming_msg:
        # Обработка адреса
        addresses = incoming_msg.split('адрес')[1].strip().split(' до ')
        if len(addresses) == 2:
            from_address = addresses[0].strip()
            to_address = addresses[1].strip()
            distance_km = calculate_distance(from_address, to_address)
            cost = max(min_cost, distance_km * cost_per_km)
            order_message = f"Новый заказ: от {from_address} до {to_address}. Стоимость: {cost} тенге."

            # Отправка сообщения в группу водителей
            for driver in drivers_group:
                client.messages.create(
                    body=order_message,
                    from_=twilio_number,
                    to=driver
                )

            msg.body(f"Ваш заказ принят. Стоимость поездки: {cost} тенге.")
        else:
            msg.body("Пожалуйста, укажите адрес в формате: 'адрес [откуда] до [куда]'")
    else:
        msg.body("Добро пожаловать в женское такси! Пожалуйста, укажите адрес в формате: 'адрес [откуда] до [куда]'")

    return str(resp)

def calculate_distance(from_address, to_address):
    # Здесь должна быть логика для расчета расстояния между адресами
    # Для простоты, вернем фиксированное значение
    return 10

if __name__ == '__main__':
    app.run(debug=True)