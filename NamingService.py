from flask import Flask, jsonify, request, abort

app_registry = Flask(__name__)
service_registry = {}

@app_registry.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    service_name = data.get('name')
    service_endpoint = data.get('endpoint')

    if not service_name or not service_endpoint:
        abort(400, description="Invalid registration data")

    service_registry[service_name] = service_name
    service_registry[service_endpoint] = service_endpoint
    print(f'Register request received - Service: {service_name}, Endpoint: {service_endpoint}')
    return jsonify({'message': f'Service {service_name} registered successfully'})

@app_registry.route('/lookup', methods=['GET'])
def lookup():
    service_name = request.args.get('name')

    if not service_name or service_name not in service_registry:
        abort(404, description="Service not found")

    service_endpoint = service_registry[service_name]
    print(f'Lookup request received - Service: {service_name}, Endpoint: {service_endpoint}')
    return jsonify({'endpoint': service_endpoint})

@app_registry.route('/unregister', methods=['DELETE'])
def unregister():
    service_name = request.args.get('name')

    if not service_name or service_name not in service_registry:
        abort(404, description="Service not found")

    del service_registry[service_name]
    print(f'Unregister request received - Service: {service_name}')
    return jsonify({'message': f'Service {service_name} unregistered successfully'})

if __name__ == '__main__':
    app_registry.run(host='0.0.0.0', port=5678)
