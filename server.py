#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor simple para manejar la creación dinámica de archivos HTML
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Importar las funciones del generador
from generate_all_files import create_student_page

@app.route('/create-student-file', methods=['POST'])
def create_student_file():
    """Endpoint para crear archivo HTML de un nuevo alumno"""
    try:
        data = request.get_json()
        student_name = data.get('studentName')
        professor_name = data.get('professorName')
        
        if not student_name or not professor_name:
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        # Crear el HTML del alumno
        student_html = create_student_page(student_name, professor_name)
        
        # Generar el nombre del archivo
        filename = f"alumno_{student_name.lower().replace(' ', '_')}.html"
        
        # Guardar el archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(student_html)
        
        return jsonify({
            'success': True,
            'message': f'Archivo {filename} creado exitosamente',
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud del servidor"""
    return jsonify({'status': 'ok', 'message': 'Servidor funcionando correctamente'})

if __name__ == '__main__':
    print("🚀 Iniciando servidor para creación dinámica de archivos...")
    print("📡 Servidor disponible en: http://localhost:5000")
    print("🔗 Endpoint de creación: POST /create-student-file")
    app.run(host='0.0.0.0', port=5000, debug=True)

