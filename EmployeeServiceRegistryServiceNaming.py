from flask import Flask, jsonify, request, abort
import requests

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

@app.route('/empdb/employee', methods=['GET'])
def getAllEmp():
    return jsonify({'emps': empDB})

@app.route('/empdb/employee/<empId>', methods=['GET'])
def getEmp(empId):
    usr = [emp for emp in empDB if emp['id'] == empId]
    return jsonify({'emp': usr})

@app.route('/empdb/employee/<empId>', methods=['PUT'])
def updateEmp(empId):
    em = [emp for emp in empDB if emp['id'] == empId]

    if len(em) > 0:
        if 'name' in request.json:
            em[0]['name'] = request.json['name']

        if 'title' in request.json:
            em[0]['title'] = request.json['title']

        return jsonify(em[0])
    else:
        abort(404, description="Employee not found")

@app.route('/empdb/employee/<empId>/<empSal>', methods=['PUT'])
def updateEmpSal(empId, empSal):
    em = [emp for emp in empDB if emp['id'] == empId]

    if len(em) > 0:
        em[0]['salary'] = empSal
        return jsonify(em[0])
    else:
        abort(404, description="Employee not found")

@app.route('/empdb/employee', methods=['POST'])
def createEmp():
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
    em = [emp for emp in empDB if emp['id'] == empId]

    if len(em) > 0:
        empDB.remove(em[0])
        return jsonify({'response': 'Success'})
    else:
        abort(404, description="Employee not found")

@app.route('/empdb/employee/average_salary', methods=['GET'])
def averageSalary():
    if len(empDB) > 0:
        total_salary = sum(float(emp['salary']) for emp in empDB)
        average_salary = total_salary / len(empDB)
        return jsonify({'average_salary': average_salary})
    else:
        abort(404, description="No employees in the database")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678)
