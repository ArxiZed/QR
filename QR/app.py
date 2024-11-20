from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Глобальные данные
queue = []  # Очередь пациентов
current_patient = None  # Текущий пациент

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/take_queue", methods=["POST"])
def take_queue():
    global queue
    patient_number = len(queue) + 1
    queue.append(patient_number)
    # Уведомить всех клиентов об обновлении очереди
    socketio.emit("update_queue", {"queue": queue, "current": current_patient})
    return jsonify({"number": patient_number})

@socketio.on("get_queue")
def get_queue():
    emit("update_queue", {"queue": queue, "current": current_patient})

@app.route("/next_patient", methods=["POST"])
def next_patient():
    global queue, current_patient
    if queue:
        current_patient = queue.pop(0)
        # Уведомить всех клиентов об обновлении очереди
        socketio.emit("update_queue", {"queue": queue, "current": current_patient})
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/accept_patient", methods=["POST"])
def accept_patient():
    global current_patient
    if current_patient:
        # Уведомить всех клиентов об обновлении очереди
        socketio.emit("update_queue", {"queue": queue, "current": current_patient})
        return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    socketio.run(app, debug=True)
