import requests

# Endpoint do serviço de resolução de nomes
service_registry_endpoint = 'http://localhost:5000'

# Consulta o serviço de nomes para obter o endpoint do serviço "employee"
lookup_data = {'name': 'employee_service'}
response = requests.post(f'{service_registry_endpoint}/lookup', json=lookup_data)
employee_service_endpoint = response.json().get('endpoint')

if employee_service_endpoint:
    # Endpoint do serviço "employee"
    create_emp_endpoint = f'{employee_service_endpoint}/empdb/employee'

    # Dados para o novo funcionário
    new_employee_data = {
        'id': '301',
        'name': 'Novo Funcionário',
        'title': 'Cargo Novo',
        'salary': 2500
    }

    # Chama o método createEmp() no serviço "employee"
    response = requests.post(create_emp_endpoint, json=new_employee_data)

    # Exibe a resposta do serviço
    print(f'Resposta do serviço de cadastro de funcionário: {response.json()}')

else:
    print('Endpoint do serviço "employee" não encontrado no serviço de nomes.')
