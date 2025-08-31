#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador final de archivos para It's English Time
"""

import os

# Configuración de profesores y sus alumnos
PROFESORES = {
    'ale': ['Aimee', 'Alberto', 'Carla', 'Daniel', 'Laura', 'Miguel'],
    'jesus': ['Ana Elisa', 'Bere', 'Hanny', 'Josué', 'Mary Alegría', 'Mary Carmen'],
    'patty': ['Paola Marín', 'Paola Rosales', 'Pilar', 'Ricardo', 'Rouss', 'Sandy'],
    'astrid': ['Dina', 'Ilce', 'Loth', 'Merian', 'Michelle', 'Wendy'],
    'blanca': ['Aleca Macaro', 'Angela', 'Miguel Ángel', 'Miguel Santillán', 'Moni', 'Montse'],
    'erwin': ['Angel', 'Kari', 'Manuel', 'Miguel', 'Nadia', 'Ximena', 'Yessenia']
}

def create_professor_panel(professor_name, students):
    """Crea un panel simple para un profesor"""
    
    html = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Panel ''' + professor_name.title() + ''' - It's English Time</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://kit.fontawesome.com/a2f1a4d5e1.js" crossorigin="anonymous"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen p-6">
  <div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-blue-800 mb-2">👩‍🏫 Panel de ''' + professor_name.title() + '''</h1>
        <p class="text-gray-600">Gestiona tus alumnos y accede a las clases</p>
      </div>
      <div class="flex gap-4">
        <button onclick="goToClasses()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-lg transition-all font-semibold">
          <i class="fas fa-video mr-2"></i>CLASES
        </button>
        <button onclick="goToHome()" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-3 rounded-xl shadow-lg transition-all">
          <i class="fas fa-home mr-2"></i>Inicio
        </button>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">📚 Mis Alumnos</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">'''
    
    colors = ['from-pink-500 to-rose-500', 'from-blue-500 to-indigo-500', 'from-purple-500 to-violet-500', 
              'from-green-500 to-emerald-500', 'from-yellow-500 to-orange-500', 'from-red-500 to-pink-500']
    
    for i, student in enumerate(students):
        color = colors[i % len(colors)]
        filename = "alumno_" + student.lower().replace(' ', '_') + ".html"
        
        # Usar comillas dobles para el JavaScript
        button_html = '''
        <button onclick="goToStudent(''' + filename + ''')" class="bg-gradient-to-r ''' + color + ''' text-white p-4 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
          <div class="text-center">
            <i class="fas fa-user-graduate text-2xl mb-2"></i>
            <p class="font-semibold">''' + student + '''</p>
          </div>
        </button>'''
        
        html += button_html
    
    html += '''
      </div>
    </div>

    <div class="text-center">
      <button onclick="logout()" class="text-sm text-red-600 underline hover:text-red-800">
        <i class="fas fa-sign-out-alt mr-1"></i> Cerrar sesión
      </button>
    </div>
  </div>

  <script>
    function goToStudent(studentPage) {
      window.location.href = studentPage;
    }
    
    function goToClasses() {
      window.open('https://meet.google.com/abc-defg-hij', '_blank');
    }
    
    function goToHome() {
      window.location.href = 'home.html';
    }
    
    function logout() {
      window.location.href = 'index.html';
    }
  </script>
</body>
</html>'''
    
    return html

def create_student_page(student_name, professor_name):
    """Crea una página simple para un alumno"""
    
    html = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>''' + student_name + ''' - It's English Time</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://kit.fontawesome.com/a2f1a4d5e1.js" crossorigin="anonymous"></script>
</head>
<body class="bg-gradient-to-br from-pink-50 to-rose-100 min-h-screen p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-pink-800 mb-2">👩‍🎓 ''' + student_name + '''</h1>
        <p class="text-gray-600">Alumno de ''' + professor_name.title() + ''' - Control de Pagos y Asistencias</p>
      </div>
      <div class="flex gap-4">
        <button onclick="goToClasses()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-lg transition-all font-semibold">
          <i class="fas fa-video mr-2"></i>CLASES
        </button>
        <button onclick="goToPanel()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-xl shadow-lg transition-all">
          <i class="fas fa-arrow-left mr-2"></i>Volver
        </button>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">💰 Control de Pagos</h2>
        <button onclick="addPaymentRow()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
          <i class="fas fa-plus mr-2"></i>Agregar Fila
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table id="paymentTable" class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Fecha Última Clase</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Fecha Próximo Pago</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Total Clases</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Mes</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Total a Pagar</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Fecha de Pago</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Abono 1</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Abono 2</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Abono 3</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Restante</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Acciones</th>
            </tr>
          </thead>
          <tbody id="paymentTableBody">
            <tr>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="2024-12-15">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="2025-01-15">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="8">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="Diciembre 2024">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none payment-amount" value="2000" step="0.01">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="2024-12-01">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="1000" step="0.01">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="500" step="0.01">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01">
              </td>
              <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 restante">
                $500.00
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <button onclick="deleteRow(this)" class="text-red-600 hover:text-red-800">
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">📚 Seguimiento de Clases</h2>
        <button onclick="addClassRow()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-all">
          <i class="fas fa-plus mr-2"></i>Agregar Fila
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table id="classTable" class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Mes y Año</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Total Clases Programadas</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Total Asistencias</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Total Faltas</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Clases para Reprogramar</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Observaciones</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Acciones</th>
            </tr>
          </thead>
          <tbody id="classTableBody">
            <tr>
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="Diciembre 2024">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="8">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="7">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="1">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="1">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <textarea class="w-full border-none focus:outline-none resize-none" rows="2" maxlength="300" placeholder="Máximo 300 caracteres">Falta por enfermedad, reprogramar para la siguiente semana</textarea>
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <button onclick="deleteRow(this)" class="text-red-600 hover:text-red-800">
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    function goToClasses() {
      window.open('https://meet.google.com/abc-defg-hij', '_blank');
    }
    
    function goToPanel() {
      window.location.href = 'panel_''' + professor_name + '''.html';
    }
    
    function addPaymentRow() {
      const tbody = document.getElementById('paymentTableBody');
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td class="border border-gray-300 px-4 py-3">
          <input type="date" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="date" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none" value="0">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="text" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none payment-amount" value="0" step="0.01">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="date" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01">
        </td>
        <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 restante">
          $0.00
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <button onclick="deleteRow(this)" class="text-red-600 hover:text-red-800">
            <i class="fas fa-trash"></i>
          </button>
        </td>
      `;
      tbody.appendChild(newRow);
    }
    
    function addClassRow() {
      const tbody = document.getElementById('classTableBody');
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td class="border border-gray-300 px-4 py-3">
          <input type="text" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none" value="0">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none" value="0">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none" value="0">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none" value="0">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <textarea class="w-full border-none focus:outline-none resize-none" rows="2" maxlength="300" placeholder="Máximo 300 caracteres"></textarea>
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <button onclick="deleteRow(this)" class="text-red-600 hover:text-red-800">
            <i class="fas fa-trash"></i>
          </button>
        </td>
      `;
      tbody.appendChild(newRow);
    }
    
    function deleteRow(button) {
      button.closest('tr').remove();
    }
  </script>
</body>
</html>'''
    
    return html

def main():
    """Función principal"""
    print("🚀 Generando archivos para It's English Time...")
    
    # Generar paneles de profesores
    for professor_name, students in PROFESORES.items():
        print("📝 Generando panel de " + professor_name.title() + "...")
        
        html_content = create_professor_panel(professor_name, students)
        filename = "panel_" + professor_name + ".html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Panel de " + professor_name.title() + " creado: " + filename)
    
    # Generar páginas de alumnos
    for professor_name, students in PROFESORES.items():
        for student_name in students:
            print("📝 Generando página de " + student_name + "...")
            
            html_content = create_student_page(student_name, professor_name)
            filename = "alumno_" + student_name.lower().replace(' ', '_') + ".html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print("✅ Página de " + student_name + " creada: " + filename)
    
    print("\n🎉 ¡Todos los archivos han sido generados exitosamente!")
    print("📊 Resumen:")
    print("   - " + str(len(PROFESORES)) + " paneles de profesores")
    
    total_students = sum(len(students) for students in PROFESORES.values())
    print("   - " + str(total_students) + " páginas de alumnos")
    print("   - Total: " + str(len(PROFESORES) + total_students) + " archivos HTML")

if __name__ == "__main__":
    main()

