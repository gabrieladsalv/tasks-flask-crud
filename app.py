from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, name=data['name'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({'message': 'New task created', 'task': new_task.to_dic()})


@app.route('/tasks', methods=['GET'])
def list_tasks():
    task_list = [task.to_dic() for task in tasks]
    output = {
        'tasks': task_list,
        'total_tasks': len(task_list)
    }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dic())
    return jsonify({'message': 'Task not found'}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    for task in tasks:
        if task.id == id:
            task.name = data.get('name', task.name)
            task.description = data.get('description', task.description)
            task.completed = data.get('completed', task.completed)
            return jsonify({'message': 'Task updated', 'task': task.to_dic()})
    return jsonify({'message': 'Task not found'}), 404


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
