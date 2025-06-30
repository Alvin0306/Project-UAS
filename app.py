from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__)
CORS(app)  # Mengizinkan akses dari semua domain untuk kemudahan pengujian dengan file HTML

# Simulasi database dalam bentuk list
DATABASE = [
    {"dosen_id": 1, "nama": "Dr. Alvin", "univ": "Universitas A", "jurusan": "Teknik Informatika"},
    {"dosen_id": 2, "nama": "Prof. Bella", "univ": "Universitas B", "jurusan": "Fisika"}
]

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/dosen', methods=['GET', 'POST'])
def manage_dosen():
    if request.method == 'GET':
        # Mengembalikan daftar dosen
        return jsonify(DATABASE)

    if request.method == 'POST':
        # Menambahkan dosen baru
        data = request.json
        new_id = max(d["dosen_id"] for d in DATABASE) + 1 if DATABASE else 1
        new_dosen = {
            "dosen_id": new_id,
            "nama": data["nama"],
            "univ": data["univ"],
            "jurusan": data["jurusan"]
        }
        DATABASE.append(new_dosen)
        return jsonify({"message": "Dosen added", "dosen": new_dosen}), 201

@app.route('/dosen/<int:dosen_id>', methods=['GET', 'PUT', 'DELETE'])
def modify_dosen(dosen_id):
    # Mencari dosen berdasarkan dosen_id
    dosen = next((d for d in DATABASE if d["dosen_id"] == dosen_id), None)

    if not dosen:
        return jsonify({"error": "Dosen not found"}), 404

    if request.method == 'GET':
        # Mengembalikan data dosen
        return jsonify(dosen)

    if request.method == 'PUT':
        # Memperbarui data dosen
        data = request.json
        dosen.update({
            "nama": data["nama"],
            "univ": data["univ"],
            "jurusan": data["jurusan"]
        })
        return jsonify({"message": "Dosen updated", "dosen": dosen})

    if request.method == 'DELETE':
        # Menghapus dosen dari database
        DATABASE.remove(dosen)
        return jsonify({"message": "Dosen deleted"})

if __name__ == '__main__':
    app.run(debug=True)


