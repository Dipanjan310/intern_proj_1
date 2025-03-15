from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
import matplotlib.pyplot as plt
from qutip import *
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_circuit', methods=['POST'])
def generate_circuit():
    data = request.json
    gates = data['gates']
    
    num_qubits = max(g['qubit'] for g in gates) + 1
    qc = QubitCircuit(num_qubits) # type: ignore

    for g in gates:
        qubit = g['qubit']
        gate_type = g['gate']

        if gate_type == "H":
            qc.add_gate("SNOT", qubit)
        elif gate_type == "X":
            qc.add_gate("X", qubit)
        elif gate_type == "Y":
            qc.add_gate("Y", qubit)
        elif gate_type == "Z":
            qc.add_gate("Z", qubit)
        elif gate_type == "CNOT_C":
            control = qubit
            continue
        elif gate_type == "CNOT_T":
            target = qubit
            qc.add_gate("CNOT", control=control, target=target)
        elif gate_type == "Measure":
            qc.add_gate("MEASURE", qubit)

    fig, ax = plt.subplots(figsize=(6, 3))
    qc.plot(ax=ax)
    img_path = "static/circuit.png"
    plt.savefig(img_path)
    plt.close(fig)

    with open(img_path, "rb") as img_file:
        base64_str = base64.b64encode(img_file.read()).decode("utf-8")

    return jsonify({"image_url": f"data:image/png;base64,{base64_str}"})

if __name__ == '__main__':
    app.run(debug=True)
