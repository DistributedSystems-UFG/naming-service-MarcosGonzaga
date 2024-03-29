import requests
from urllib.parse import urljoin

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

        old_salary = calculate_data.get('current_salary')
        print(f'Salário antigo do funcionário: {old_salary}')

        new_salary = response.json().get('new_salary')
        print(f'Novo salário calculado: {new_salary}')

        # Consulta o serviço de nomes para obter o endpoint do serviço "employee"
        lookup_data = {'name': 'employee_service'}
        response = requests.get(urljoin(service_registry_endpoint, '/lookup'), params=lookup_data)
        response.raise_for_status()

        employee_service_endpoint = response.json().get('endpoint')

        if employee_service_endpoint:
            # Atualiza o valor do salário do colaborador de id 201 no serviço "employee"
            update_salary_endpoint = urljoin(f'{employee_service_endpoint}', '/empdb/employee')
            update_data = {'empId': 201, 'empSal': new_salary}
            response = requests.put(update_salary_endpoint, json=update_data)
            response.raise_for_status()

            updated_salary = response.json().get('new_salary')
            print(f'Novo valor do salário do funcionário (ID 201): {updated_salary}')

        else:
            print('Endpoint do serviço "employee" não encontrado no serviço de nomes.')

    else:
        print('Endpoint do serviço de cálculo de salário não encontrado no serviço de nomes.')

except requests.exceptions.RequestException as e:
    print(f"Erro na solicitação: {e}")
