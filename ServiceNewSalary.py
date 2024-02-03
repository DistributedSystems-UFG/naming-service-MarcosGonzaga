from flask import Flask, jsonify, request
import requests
import atexit

app_salary = Flask(__name__)

# Endpoint do serviço de resolução de nomes
service_registry_endpoint = 'http://52.21.65.56:5678'

# Dados de registro do serviço de cálculo de salário
registration_data = {'name': 'salary_service', 'endpoint': 'http://54.221.58.118:5678'}

# Registrar o serviço de cálculo de salário no serviço de resolução de nomes ao iniciar
response = requests.post(f'{service_registry_endpoint}/register', json=registration_data)
print(response.json())

# Função para desregistro ao encerrar o serviço
@atexit.register
def unregister_service():
    response = requests.delete(f'{service_registry_endpoint}/unregister?name={registration_data["name"]}')
    print(response.json())

# Rota para calcular o novo salário
@app_salary.route('/calculate_salary', methods=['POST'])
def calculate_salary():
    data = request.get_json()
    current_salary = data.get('current_salary')
    percent_increase = data.get('percent_increase')

    if not current_salary or not percent_increase:
        return jsonify({'error': 'Invalid input'})

    new_salary = current_salary * (1 + percent_increase / 100)
    return jsonify({'new_salary': new_salary})

# Rota para simular a necessidade de migração e chamar unregister() no serviço de nomes
@app_salary.route('/migrate', methods=['POST'])
def migrate():
    data = request.get_json()
    new_endpoint = data.get('new_endpoint')

    if not new_endpoint:
        return jsonify({'error': 'New endpoint not provided'})

    # Chama unregister() no serviço de nomes antes de migrar
    unregister_service()

    # Realiza a migração (alterando o endpoint)
    registration_data['endpoint'] = new_endpoint

    # Registra novamente o serviço de cálculo de salário no serviço de nomes após a migração
    response = requests.post(f'{service_registry_endpoint}/register', json=registration_data)
    print(response.json())

    return jsonify({'message': 'Service migration completed'})

if __name__ == '__main__':
    # Registro no serviço de resolução de nomes ao iniciar
    registration_data = {'name': 'salary_service', 'endpoint': 'http://localhost:6000'}
    response = requests.post('http://localhost:5000/register', json=registration_data)
    print(response.json())
  
    app_salary.run(host='54.221.58.118', port=5678)

