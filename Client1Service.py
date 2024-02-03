import requests
from urllib.parse import urljoin
from requests.exceptions import RequestException

# Endpoint do serviço de resolução de nomes
service_registry_endpoint = 'http://52.21.65.56:5678'

try:
    # Consulta o serviço de nomes para obter o endpoint do serviço de cálculo de novo salário
    lookup_data = {'name': 'salary_service'}
    response = requests.get(urljoin(service_registry_endpoint, '/lookup'), params=lookup_data)
    response.raise_for_status()

    salary_service_endpoint = response.json().get('endpoint')

    if salary_service_endpoint:
        # Faz uma requisição ao serviço de cálculo de novo salário
        calculate_salary_endpoint = urljoin(f'{salary_service_endpoint}', '/calculate_salary')
        calculate_data = {'current_salary': 3000, 'percent_increase': 15}
        response = requests.post(calculate_salary_endpoint, json=calculate_data)
        response.raise_for_status()

        new_salary = response.json().get('new_salary')
        print(f'Novo salário calculado: {new_salary}')

        # Consulta o serviço de nomes para obter o endpoint do serviço "employee"
        lookup_data = {'name': 'employee_service'}
        response = requests.get(urljoin(service_registry_endpoint, '/lookup'), params=lookup_data)
        response.raise_for_status()

        employee_service_endpoint = response.json().get('endpoint')

        if employee_service_endpoint:
            # Atualiza o valor do salário do colaborador de id 201 no serviço "employee"
            update_salary_endpoint = urljoin(f'{employee_service_endpoint}', '/empdb/employee/201')
            update_data = {'salary': new_salary}
            response = requests.put(update_salary_endpoint, json=update_data)
            response.raise_for_status()

            print(f'Resposta do serviço de atualização de salário: {response.json()}')

        else:
            print('Endpoint do serviço "employee" não encontrado no serviço de nomes.')

    else:
        print('Endpoint do serviço de cálculo de salário não encontrado no serviço de nomes.')

except RequestException as e:
    print(f"Erro na solicitação: {e}")
