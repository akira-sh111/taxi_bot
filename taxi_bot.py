from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC84ef9e21ea9b9025f1ab1ad72f2deac3'
auth_token = '75e99a840f4fc4fb49871e555d42e612'
client = Client(account_sid, auth_token)

# WhatsApp group ID for drivers
drivers_group_id = 'whatsapp:B6PiB1rXn39KttBjant8I7'

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    response = MessagingResponse()
    msg = response.message()

    if 'привет' in incoming_msg:
        msg.body('Здравствуйте! Пожалуйста, укажите адрес откуда и куда вы хотите поехать.')
    elif 'адрес' in incoming_msg:
        # Extract addresses and calculate cost
        addresses = incoming_msg.replace('адрес', '').strip().split(' до ')
        if len(addresses) == 2:
            from_address, to_address = addresses
            distance_km = calculate_distance(from_address, to_address)
            cost = max(1000, distance_km * 50)
            order_message = f'Новый заказ: {from_address} до {to_address}. Стоимость: {cost} тенге.'
            send_to_drivers(order_message, from_number)
            msg.body(f'Ваш заказ принят. Стоимость поездки: {cost} тенге.')
        else:
            msg.body('Пожалуйста, укажите адрес в формате: "адрес [откуда] до [куда]".')
    else:
        msg.body('Извините, я не понимаю ваш запрос. Пожалуйста, укажите адрес откуда и куда вы хотите поехать.')

    return str(response)

def calculate_distance(from_address, to_address):
    # Здесь должна быть логика для расчета расстояния между адресами
    # Для простоты вернем фиксированное значение
    return 10

def send_to_drivers(message, client_number):
    client.messages.create(
        body=message,
        from_='whatsapp:+14155238886', # Twilio WhatsApp number
        to=drivers_group_id
    )

if __name__ == '__main__':
    app.run(debug=True)
