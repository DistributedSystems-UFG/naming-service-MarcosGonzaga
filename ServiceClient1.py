import requests

# Endpoint do serviço de resolução de nomes
service_registry_endpoint = 'http://52.21.65.56:5678'

# Consulta o serviço de nomes para obter o endpoint do serviço de cálculo de novo salário
lookup_data = {'name': 'salary_service'}
response = requests.get(f'{service_registry_endpoint}/lookup', params=lookup_data)
salary_service_endpoint = response.json().get('endpoint')


if salary_service_endpoint:
    # Faz uma requisição ao serviço de cálculo de novo salário
    calculate_salary_endpoint = f'http://{salary_service_endpoint}/calculate_salary'
    calculate_data = {'current_salary': 3000, 'percent_increase': 15}
    response = requests.post(calculate_salary_endpoint, json=calculate_data)

    if response.status_code == 200:
        new_salary = response.json().get('new_salary')
        print(f'Novo salário calculado: {new_salary}')

        # Consulta o serviço de nomes para obter o endpoint do serviço "employee"
        lookup_data = {'name': 'employee_service'}
        response = requests.post(f'http://{service_registry_endpoint}/lookup', json=lookup_data)

        if response.status_code == 200:
            employee_service_endpoint = response.json().get('endpoint')

            if employee_service_endpoint:
                # Atualiza o valor do salário do colaborador de id 201 no serviço "employee"
                update_salary_endpoint = f'http://{employee_service_endpoint}/empdb/employee/201'
                update_data = {'salary': new_salary}
                response = requests.put(update_salary_endpoint, json=update_data)

                if response.status_code == 200:
                    print(f'Resposta do serviço de atualização de salário: {response.json()}')
                else:
                    print(f"Erro na atualização de salário: {response.status_code} - {response.text}")

            else:
                print('Endpoint do serviço "employee" não encontrado no serviço de nomes.')

        else:
            print(f"Erro ao obter endpoint do serviço 'employee': {response.status_code} - {response.text}")

    else:
        print(f"Erro no serviço de cálculo de salário: {response.status_code} - {response.text}")

else:
    print('Endpoint do serviço de cálculo de salário não encontrado no serviço de nomes.')
