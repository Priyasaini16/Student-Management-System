from flask import Flask, request, jsonify
from db import db, cursor

app = Flask(__name__)

print("students API loaded")

students = []

@app.route('/')
def home():
    return "Hello, Backend Started!"

@app.route('/students', methods=['GET'])
def get_students():
    try:
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()

        students = []
        for row in result:
            students.append({
                "id": row[0],
                "name": row[1],
                "age": row[2]
            })

        return jsonify(students)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        age = data.get('age')

        if not name or name.strip() == "":
            return jsonify({"error": "Name is required"}), 400

        if not isinstance(age, int):
            return jsonify({"error": "Age must be a number"}), 400

        query = "INSERT INTO students (name, age) VALUES (?, ?)"
        cursor.execute(query, (name, age))
        db.commit()

        return jsonify({"message": "Student added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        age = data.get('age')

        if not name or name.strip() == "":
            return jsonify({"error": "Name is required"}), 400

        if not isinstance(age, int):
            return jsonify({"error": "Age must be a number"}), 400

        query = "UPDATE students SET name=?, age=? WHERE id=?"
        cursor.execute(query, (name, age, id))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student updated successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        query = "DELETE FROM students WHERE id=?"
        cursor.execute(query, (id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student deleted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
