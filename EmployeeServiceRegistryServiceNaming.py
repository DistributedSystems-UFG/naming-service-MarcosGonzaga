from flask import Flask, jsonify, request, abort
import requests
import atexit

app = Flask(__name__)

empDB = [
    {
        'id': '101',
        'name': 'Arício Segundo',
        'title': 'Technical Leader',
        'salary': '2000'
    },
    {
        'id': '201',
        'name': 'Geraldo Rusmão',
        'title': 'Sr Software Engineer',
        'salary': '3000'
    }
]

# Endpoint do serviço de resolução de nomes
service_registry_endpoint = 'http://52.21.65.56:5678'

# Dados de registro do serviço
registration_data = {'name': 'employee_service', 'endpoint': 'http://34.195.96.130:5678'}

# Registrar o serviço no serviço de resolução de nomes ao iniciar
response = requests.post(f'{service_registry_endpoint}/register', json=registration_data)
print(response.json())

# Função para desregistro ao encerrar o serviço
@atexit.register
def unregister_service():
    response = requests.delete(f'{service_registry_endpoint}/unregister?name={registration_data["name"]}')
    print(response.json())

def log_request_data():
    print(f"Received Request: {request.method} {request.url}")
    print(f"JSON Data: {request.json}")

@app.route('/empdb/employee', methods=['GET'])
def getAllEmp():
    log_request_data()
    return jsonify({'emps': empDB})

@app.route('/empdb/employee/<empId>', methods=['GET'])
def getEmp(empId):
    log_request_data()
    usr = [emp for emp in empDB if emp['id'] == empId]
    return jsonify({'emp': usr})

@app.route('/empdb/employee/<empId>', methods=['PUT'])
def updateEmp(empId):
    log_request_data()
    em = [emp for emp in empDB if emp['id'] == empId]

    if len(em) > 0:
        if 'name' in request.json:
            em[0]['name'] = request.json['name']

        if 'title' in request.json:
            em[0]['title'] = request.json['title']

        return jsonify(em[0])
    else:
        abort(404, description="Employee not found")

@app.route('/empdb/employee', methods=['PUT'])
def updateEmpSal():
    log_request_data()
    empId = request.json.get('empId')
    empSal = request.json.get('empSal')

    em = [emp for emp in empDB if emp['id'] == empId]

    if len(em) > 0:
        em[0]['salary'] = empSal
        return jsonify({'new_salary': em[0]['salary']})
    else:
        abort(404, description="Employee not found")

@app.route('/empdb/employee', methods=['POST'])
def createEmp():
    log_request_data()
    dat = {
        'id': request.json['id'],
        'name': request.json['name'],
        'title': request.json['title'],
        'salary': request.json['salary']
    }

    if dat['id'] is not None and dat['name'] is not None and dat['title'] is not None:
        empDB.append(dat)
        return jsonify(dat)
    else:
        abort(404, description="Employee information incomplete")

@app.route('/empdb/employee/<empId>', methods=['DELETE'])
def deleteEmp(empId):
    log_request_data()
    em = [emp for emp in empDB if emp['id'] == empId]

    if len(em) > 0:
        empDB.remove(em[0])
        return jsonify({'response': 'Success'})
    else:
        abort(404, description="Employee not found")

@app.route('/empdb/employee/average_salary', methods=['GET'])
def averageSalary():
    log_request_data()
    if len(empDB) > 0:
        total_salary = sum(float(emp['salary']) for emp in empDB)
        average_salary = total_salary / len(empDB)
        return jsonify({'average_salary': average_salary})
    else:
        abort(404, description="No employees in the database")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678)
