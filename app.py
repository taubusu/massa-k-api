import serial
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешает все источники по умолчанию

def get_mass(serial_port, baudrate=4800, timeout=1, discretization=1.0):
    try:
        with serial.Serial(
            port=serial_port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        ) as ser:
            # Отправка команды 0x45
            command = bytes([0x45])
            ser.write(command)
            print(f"Отправлена команда: {command.hex()}")

            # Ждем небольшую задержку для получения ответа
            time.sleep(0.1)

            # Ожидаем 2 байта ответа
            response = ser.read(2)
            if len(response) != 2:
                print("Не получено достаточное количество байт.")
                return None
            else:
                print(f"Получен ответ: {response.hex()}")

                # Преобразуем полученные байты в целое число
                d0_d7 = response[0]
                d8_d15 = response[1]
                combined = (d8_d15 << 8) | d0_d7

                print(f"Скомбинированное значение: {combined:#06x}")

                # Извлекаем знак и массу
                sign = (combined >> 15) & 0x01
                mass_value = combined & 0x7FFF  # D14-D0

                # Применяем дискретизацию
                calculated_mass = mass_value * discretization

                # Применяем знак
                if sign == 1:
                    calculated_mass = -calculated_mass

                return calculated_mass

    except serial.SerialException as e:
        print(f"Ошибка подключения к порту: {e}")
        return None

@app.route('/mass')
def get_mass_api():
    port = request.args.get('port')
    current_mass = get_mass(port, 4800, 1, 1.0)
    if current_mass is not None:
        return jsonify({'mass': current_mass})
    else:
        return jsonify({'mass': 'Неизвестно'}), 500

if __name__ == "__main__":
    # Запуск Flask-сервера
    app.run(host='0.0.0.0', port=3333)
