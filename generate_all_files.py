#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador simplificado de archivos para It's English Time
Incluye nueva tabla de horarios, botones de guardar y Firebase
"""

import os

# Configuración de profesores y sus alumnos
PROFESORES = {
    'ale': ['Pao Rosales', 'Nadia', 'Mía', 'Ricardo', 'Rouss', 'Aimee', 'Josué', 'Montse', 'Oscar', 'Marycarmen', 'Ana', 'Dina', 'Loth', 'Alan', 'Hanny'],
    'jesus': ['Pilar', 'Carla', 'Wendy', 'Pablo', 'Angel'],
    'astrid': ['Manuel', 'Yessenia', 'Ximena'],
    'patty': ['Alberto', 'Miguel', 'Karina'],
    'blanca': ['Paola Marín', 'Laura', 'Michelle', 'Merian', 'Miguel Santillán', 'Miguel Gonzáles'],
    'erwin': ['Daniel', 'Alfredo', 'Lily']
}

def create_professor_panel(professor_name, students):
    """Crea un panel simple para un profesor"""
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Panel {professor_name.title()} - It's English Time</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://kit.fontawesome.com/a2f1a4d5e1.js" crossorigin="anonymous"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen p-6">
  <div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-blue-800 mb-2">👩‍🏫 Panel de {professor_name.title()}</h1>
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
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">📚 Mis Alumnos</h2>
        <button onclick="showAddStudentModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-all">
          <i class="fas fa-plus mr-2"></i>Agregar Alumno
        </button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4" id="studentsGrid">'''
    
    colors = ['from-pink-500 to-rose-500', 'from-blue-500 to-indigo-500', 'from-purple-500 to-violet-500', 
              'from-green-500 to-emerald-500', 'from-yellow-500 to-orange-500', 'from-red-500 to-pink-500']
    
    for i, student in enumerate(students):
        color = colors[i % len(colors)]
        filename = f"alumno_{student.lower().replace(' ', '_')}.html"
        
        button_html = f'''
        <button onclick="goToStudent('{filename}')" class="bg-gradient-to-r {color} text-white p-4 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
          <div class="text-center">
            <i class="fas fa-user-graduate text-2xl mb-2"></i>
            <p class="font-semibold">{student}</p>
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

  <!-- Modal para agregar alumno -->
  <div id="addStudentModal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
    <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-2xl font-bold text-gray-800">👨‍🎓 Agregar Nuevo Alumno</h3>
        <button onclick="hideAddStudentModal()" class="text-gray-500 hover:text-gray-700 text-2xl">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <form id="addStudentForm" onsubmit="addNewStudent(event)">
        <div class="mb-6">
          <label for="studentName" class="block text-sm font-medium text-gray-700 mb-2">
            Nombre del Alumno
          </label>
          <input 
            type="text" 
            id="studentName" 
            name="studentName" 
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            placeholder="Ej: Juan Pérez"
          >
        </div>
        
        <div class="flex gap-3">
          <button 
            type="submit" 
            class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg transition-all font-semibold"
          >
            <i class="fas fa-save mr-2"></i>Guardar
          </button>
          <button 
            type="button" 
            onclick="hideAddStudentModal()"
            class="flex-1 bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg transition-all font-semibold"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Firebase SDK -->
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js"></script>

  <script>
    // Configuración Firebase
    const firebaseConfig = {{
      apiKey: "AIzaSyAbS_UCnlfw3P2loqpTl6Oh8A2Xswz3rPY",
      authDomain: "iet-student-control.firebaseapp.com",
      projectId: "iet-student-control",
      storageBucket: "iet-student-control.firebasestorage.app",
      messagingSenderId: "635566809825",
      appId: "1:635566809825:web:696842a0cb60356ed10da0"
    }};

    // Inicializar Firebase
    firebase.initializeApp(firebaseConfig);
    const db = firebase.firestore();
    const professorName = '{professor_name}';

    function goToStudent(studentPage) {{
      window.location.href = studentPage;
    }}
    
    function goToClasses() {{
      window.open('https://meet.google.com/abc-defg-hij', '_blank');
    }}
    
    function goToHome() {{
      window.location.href = 'home.html';
    }}
    
    function logout() {{
      window.location.href = 'index.html';
    }}

    // Funciones para el modal
    function showAddStudentModal() {{
      document.getElementById('addStudentModal').classList.remove('hidden');
      document.getElementById('studentName').focus();
    }}

    function hideAddStudentModal() {{
      document.getElementById('addStudentModal').classList.add('hidden');
      document.getElementById('addStudentForm').reset();
    }}

    // Función para agregar nuevo alumno
    async function addNewStudent(event) {{
      event.preventDefault();
      
      const studentName = document.getElementById('studentName').value.trim();
      if (!studentName) {{
        alert('Por favor ingresa el nombre del alumno');
        return;
      }}

      try {{
        // Mostrar loading
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Guardando...';
        submitBtn.disabled = true;

        // Obtener lista actual de alumnos
        const professorRef = db.collection('professors').doc(professorName);
        const professorDoc = await professorRef.get();
        
        let currentStudents = [];
        if (professorDoc.exists) {{
          currentStudents = professorDoc.data().students || [];
        }}

        // Verificar si el alumno ya existe
        if (currentStudents.includes(studentName)) {{
          alert('Este alumno ya existe en la lista');
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
          return;
        }}

        // Agregar nuevo alumno
        currentStudents.push(studentName);
        
        // Guardar en Firebase
        await professorRef.set({{
          students: currentStudents,
          lastUpdated: firebase.firestore.FieldValue.serverTimestamp()
        }}, {{ merge: true }});

        // Actualizar la interfaz
        await loadStudentsFromFirebase();

        // Cerrar modal y mostrar notificación
        hideAddStudentModal();
        showNotification('Alumno agregado exitosamente', 'success');

      }} catch (error) {{
        console.error('Error al agregar alumno:', error);
        showNotification('Error al agregar alumno', 'error');
        
        // Restaurar botón
        const submitBtn = event.target.querySelector('button[type="submit"]');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }}
    }}

    // Función para cargar alumnos desde Firebase
    async function loadStudentsFromFirebase() {{
      try {{
        const professorRef = db.collection('professors').doc(professorName);
        const professorDoc = await professorRef.get();
        
        if (professorDoc.exists) {{
          const students = professorDoc.data().students || [];
          renderStudents(students);
        }}
      }} catch (error) {{
        console.error('Error al cargar alumnos:', error);
      }}
    }}

    // Función para renderizar alumnos
    function renderStudents(students) {{
      const grid = document.getElementById('studentsGrid');
      const colors = ['from-pink-500 to-rose-500', 'from-blue-500 to-indigo-500', 'from-purple-500 to-violet-500', 
                     'from-green-500 to-emerald-500', 'from-yellow-500 to-orange-500', 'from-red-500 to-pink-500'];
      
      grid.innerHTML = '';
      
      students.forEach((student, index) => {{
        const color = colors[index % colors.length];
        const filename = `alumno_${{student.toLowerCase().replace(/ /g, '_')}}.html`;
        
        const buttonHtml = `
          <button onclick="goToStudent('${{filename}}')" class="bg-gradient-to-r ${{color}} text-white p-4 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
            <div class="text-center">
              <i class="fas fa-user-graduate text-2xl mb-2"></i>
              <p class="font-semibold">${{student}}</p>
            </div>
          </button>
        `;
        
        grid.innerHTML += buttonHtml;
      }});
    }}

    // Función para mostrar notificaciones
    function showNotification(message, type) {{
      const notification = document.createElement('div');
      const bgColor = type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white';
      notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all ${{bgColor}}`;
      notification.textContent = message;
      
      document.body.appendChild(notification);
      
      setTimeout(() => {{
        notification.remove();
      }}, 3000);
    }}

    // Cargar alumnos al iniciar la página
    document.addEventListener('DOMContentLoaded', function() {{
      // Inicializar con alumnos existentes si no hay datos en Firebase
      initializeStudentsIfNeeded();
      loadStudentsFromFirebase();
    }});

    // Función para inicializar alumnos si es necesario
    async function initializeStudentsIfNeeded() {{
      try {{
        const professorRef = db.collection('professors').doc(professorName);
        const professorDoc = await professorRef.get();
        
        if (!professorDoc.exists) {{
          // Si no existe el documento del profesor, crear con alumnos iniciales
          const initialStudents = {students};
          await professorRef.set({{
            students: initialStudents,
            lastUpdated: firebase.firestore.FieldValue.serverTimestamp()
          }});
        }}
      }} catch (error) {{
        console.error('Error al inicializar alumnos:', error);
      }}
    }}
  </script>
</body>
</html>'''
    
    return html

def create_student_page(student_name, professor_name):
    """Crea una página completa para un alumno con todas las funcionalidades"""
    
    # Determinar el color del gradiente basado en el profesor
    professor_colors = {
        'ale': 'from-pink-50 to-rose-100',
        'jesus': 'from-blue-50 to-indigo-100', 
        'patty': 'from-purple-50 to-violet-100',
        'astrid': 'from-green-50 to-emerald-100',
        'blanca': 'from-yellow-50 to-orange-100',
        'erwin': 'from-red-50 to-pink-100'
    }
    
    bg_color = professor_colors.get(professor_name.lower(), 'from-pink-50 to-rose-100')
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{student_name} - It's English Time</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://kit.fontawesome.com/a2f1a4d5e1.js" crossorigin="anonymous"></script>
</head>
<body class="bg-gradient-to-br {bg_color} min-h-screen p-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-4xl font-bold text-pink-800 mb-2">👩‍🎓 {student_name}</h1>
        <p class="text-gray-600">Alumno de {professor_name.title()} - Control de Pagos y Asistencias</p>
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

    <!-- Nueva tabla de horarios -->
    <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">🕐 Horarios de Clase</h2>
        <div class="flex gap-2">
          <button onclick="addScheduleRow()" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-all">
            <i class="fas fa-plus mr-2"></i>Agregar Fila
          </button>
          <button onclick="saveScheduleData()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
            <i class="fas fa-save mr-2"></i>Guardar
          </button>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table id="scheduleTable" class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Hora Central México</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Hora de la Clase</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Días de Clase</th>
            </tr>
          </thead>
          <tbody id="scheduleTableBody">
            <tr>
              <td class="border border-gray-300 px-4 py-3">
                <input type="time" class="w-full border-none focus:outline-none" value="15:00">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="time" class="w-full border-none focus:outline-none" value="15:00">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="Lunes, Miércoles, Viernes" placeholder="Ej: Lunes, Miércoles, Viernes">
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">💰 Control de Pagos</h2>
        <div class="flex gap-2">
          <button onclick="addPaymentRow()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
            <i class="fas fa-plus mr-2"></i>Agregar Fila
          </button>
          <button onclick="savePaymentData()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
            <i class="fas fa-save mr-2"></i>Guardar
          </button>
        </div>
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
                <input type="number" class="w-full border-none focus:outline-none payment-amount" value="2000" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="2024-12-01">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="1000" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="500" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 restante">
                $500.00
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">📚 Seguimiento de Clases</h2>
        <div class="flex gap-2">
          <button onclick="addClassRow()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-all">
            <i class="fas fa-plus mr-2"></i>Agregar Fila
          </button>
          <button onclick="saveClassData()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-all">
            <i class="fas fa-save mr-2"></i>Guardar
          </button>
        </div>
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
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Clases Restantes</th>
              <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Observaciones</th>
            </tr>
          </thead>
          <tbody id="classTableBody">
            <tr>
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="Diciembre 2024">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none classes-programmed" value="8" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none class-input" value="7" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none class-input" value="1" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none class-input" value="1" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 classes-remaining">
                0
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <textarea class="w-full border-none focus:outline-none resize-none" rows="2" maxlength="300" placeholder="Máximo 300 caracteres">Falta por enfermedad, reprogramar para la siguiente semana</textarea>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Firebase SDK -->
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js"></script>

  <script>
    // Configuración Firebase
    const firebaseConfig = {{
      apiKey: "AIzaSyAbS_UCnlfw3P2loqpTl6Oh8A2Xswz3rPY",
      authDomain: "iet-student-control.firebaseapp.com",
      projectId: "iet-student-control",
      storageBucket: "iet-student-control.firebasestorage.app",
      messagingSenderId: "635566809825",
      appId: "1:635566809825:web:696842a0cb60356ed10da0"
    }};

    // Inicializar Firebase
    firebase.initializeApp(firebaseConfig);
    const db = firebase.firestore();
    const studentName = '{student_name}';

    function goToClasses() {{
      window.open('https://meet.google.com/abc-defg-hij', '_blank');
    }}
    
    function goToPanel() {{
      window.location.href = 'panel_{professor_name.lower()}.html';
    }}

    // Función para agregar fila a la tabla de horarios
    function addScheduleRow() {{
      const tbody = document.getElementById('scheduleTableBody');
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td class="border border-gray-300 px-4 py-3">
          <input type="time" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="time" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="text" class="w-full border-none focus:outline-none" placeholder="Ej: Lunes, Miércoles, Viernes">
        </td>
      `;
      tbody.appendChild(newRow);
    }}

    // Función para guardar datos de horarios
    async function saveScheduleData() {{
      try {{
        const tbody = document.getElementById('scheduleTableBody');
        const rows = tbody.querySelectorAll('tr');
        const scheduleData = [];

        rows.forEach(row => {{
          const inputs = row.querySelectorAll('input');
          scheduleData.push({{
            horaCentral: inputs[0].value,
            horaClase: inputs[1].value,
            diasClase: inputs[2].value
          }});
        }});

        await db.collection('students').doc(studentName).collection('schedules').doc('current').set({{
          schedules: scheduleData,
          lastUpdated: firebase.firestore.FieldValue.serverTimestamp()
        }});

        showNotification('Horarios guardados exitosamente', 'success');
      }} catch (error) {{
        console.error('Error al guardar horarios:', error);
        showNotification('Error al guardar horarios', 'error');
      }}
    }}

    // Función para guardar datos de pagos
    async function savePaymentData() {{
      try {{
        const tbody = document.getElementById('paymentTableBody');
        const rows = tbody.querySelectorAll('tr');
        const paymentData = [];

        rows.forEach(row => {{
          const inputs = row.querySelectorAll('input');
          const restante = row.querySelector('.restante').textContent;
          paymentData.push({{
            fechaUltimaClase: inputs[0].value,
            fechaProximoPago: inputs[1].value,
            totalClases: inputs[2].value,
            mes: inputs[3].value,
            totalPagar: inputs[4].value,
            fechaPago: inputs[5].value,
            abono1: inputs[6].value,
            abono2: inputs[7].value,
            abono3: inputs[8].value,
            restante: restante
          }});
        }});

        await db.collection('students').doc(studentName).collection('payments').doc('current').set({{
          payments: paymentData,
          lastUpdated: firebase.firestore.FieldValue.serverTimestamp()
        }});

        showNotification('Datos de pagos guardados exitosamente', 'success');
      }} catch (error) {{
        console.error('Error al guardar pagos:', error);
        showNotification('Error al guardar pagos', 'error');
      }}
    }}

    // Función para guardar datos de clases
    async function saveClassData() {{
      try {{
        const tbody = document.getElementById('classTableBody');
        const rows = tbody.querySelectorAll('tr');
        const classData = [];

        rows.forEach(row => {{
          const inputs = row.querySelectorAll('input');
          const textarea = row.querySelector('textarea');
          const restante = row.querySelector('.classes-remaining').textContent;
          classData.push({{
            mesAnio: inputs[0].value,
            totalClasesProgramadas: inputs[1].value,
            totalAsistencias: inputs[2].value,
            totalFaltas: inputs[3].value,
            clasesReprogramar: inputs[4].value,
            clasesRestantes: restante,
            observaciones: textarea.value
          }});
        }});

        await db.collection('students').doc(studentName).collection('classes').doc('current').set({{
          classes: classData,
          lastUpdated: firebase.firestore.FieldValue.serverTimestamp()
        }});

        showNotification('Datos de clases guardados exitosamente', 'success');
      }} catch (error) {{
        console.error('Error al guardar clases:', error);
        showNotification('Error al guardar clases', 'error');
      }}
    }}

    // Función para mostrar notificaciones
    function showNotification(message, type) {{
      const notification = document.createElement('div');
      const bgColor = type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white';
      notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all ${{bgColor}}`;
      notification.textContent = message;
      
      document.body.appendChild(notification);
      
      setTimeout(() => {{
        notification.remove();
      }}, 3000);
    }}

    // Función para cargar datos guardados
    async function loadSavedData() {{
      try {{
        // Cargar horarios
        const scheduleDoc = await db.collection('students').doc(studentName).collection('schedules').doc('current').get();
        if (scheduleDoc.exists) {{
          const scheduleData = scheduleDoc.data().schedules;
          const tbody = document.getElementById('scheduleTableBody');
          tbody.innerHTML = '';
          
          scheduleData.forEach(schedule => {{
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
              <td class="border border-gray-300 px-4 py-3">
                <input type="time" class="w-full border-none focus:outline-none" value="${{schedule.horaCentral}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="time" class="w-full border-none focus:outline-none" value="${{schedule.horaClase}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="${{schedule.diasClase}}">
              </td>
            `;
            tbody.appendChild(newRow);
          }});
        }}

        // Cargar pagos
        const paymentDoc = await db.collection('students').doc(studentName).collection('payments').doc('current').get();
        if (paymentDoc.exists) {{
          const paymentData = paymentDoc.data().payments;
          const tbody = document.getElementById('paymentTableBody');
          tbody.innerHTML = '';
          
          paymentData.forEach(payment => {{
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="${{payment.fechaUltimaClase}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="${{payment.fechaProximoPago}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="${{payment.totalClases}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="${{payment.mes}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none payment-amount" value="${{payment.totalPagar}}" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="${{payment.fechaPago}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="${{payment.abono1}}" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="${{payment.abono2}}" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none abono" value="${{payment.abono3}}" step="0.01" onchange="calculatePaymentRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 restante">
                ${{payment.restante}}
              </td>
            `;
            tbody.appendChild(newRow);
          }});
        }}

        // Cargar clases
        const classDoc = await db.collection('students').doc(studentName).collection('classes').doc('current').get();
        if (classDoc.exists) {{
          const classData = classDoc.data().classes;
          const tbody = document.getElementById('classTableBody');
          tbody.innerHTML = '';
          
          classData.forEach(classItem => {{
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
              <td class="border border-gray-300 px-4 py-3">
                <input type="text" class="w-full border-none focus:outline-none" value="${{classItem.mesAnio}}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none classes-programmed" value="${{classItem.totalClasesProgramadas}}" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none class-input" value="${{classItem.totalAsistencias}}" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none class-input" value="${{classItem.totalFaltas}}" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none class-input" value="${{classItem.clasesReprogramar}}" onchange="calculateClassRemaining(this)">
              </td>
              <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 classes-remaining">
                ${{classItem.clasesRestantes}}
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <textarea class="w-full border-none focus:outline-none resize-none" rows="2" maxlength="300" placeholder="Máximo 300 caracteres">${{classItem.observaciones}}</textarea>
              </td>
            `;
            tbody.appendChild(newRow);
          }});
        }}
      }} catch (error) {{
        console.error('Error al cargar datos:', error);
      }}
    }}
    
    // Función para calcular el restante en la tabla de pagos
    function calculatePaymentRemaining(input) {{
      const row = input.closest('tr');
      const totalPagar = parseFloat(row.querySelector('.payment-amount').value) || 0;
      const abono1 = parseFloat(row.querySelectorAll('.abono')[0].value) || 0;
      const abono2 = parseFloat(row.querySelectorAll('.abono')[1].value) || 0;
      const abono3 = parseFloat(row.querySelectorAll('.abono')[2].value) || 0;
      
      const restante = totalPagar - abono1 - abono2 - abono3;
      row.querySelector('.restante').textContent = '$' + restante.toFixed(2);
      
      // Cambiar color según el restante
      const restanteElement = row.querySelector('.restante');
      if (restante > 0) {{
        restanteElement.className = 'border border-gray-300 px-4 py-3 font-semibold text-red-600 restante';
      }} else if (restante === 0) {{
        restanteElement.className = 'border border-gray-300 px-4 py-3 font-semibold text-green-600 restante';
      }} else {{
        restanteElement.className = 'border border-gray-300 px-4 py-3 font-semibold text-blue-600 restante';
      }}
    }}
    
    // Función para calcular el restante en la tabla de clases
    function calculateClassRemaining(input) {{
      const row = input.closest('tr');
      const programadas = parseFloat(row.querySelector('.classes-programmed').value) || 0;
      const asistencias = parseFloat(row.querySelectorAll('.class-input')[0].value) || 0;
      const faltas = parseFloat(row.querySelectorAll('.class-input')[1].value) || 0;
      const reprogramar = parseFloat(row.querySelectorAll('.class-input')[2].value) || 0;
      
      const totalUsado = asistencias + faltas + reprogramar;
      const restante = programadas - totalUsado;
      
      // Actualizar el campo de clases restantes
      const restanteElement = row.querySelector('.classes-remaining');
      restanteElement.textContent = restante;
      
      // Cambiar color según el restante
      if (restante > 0) {{
        restanteElement.className = 'border border-gray-300 px-4 py-3 font-semibold text-blue-600 classes-remaining';
      }} else if (restante === 0) {{
        restanteElement.className = 'border border-gray-300 px-4 py-3 font-semibold text-green-600 classes-remaining';
      }} else {{
        restanteElement.className = 'border border-gray-300 px-4 py-3 font-semibold text-red-600 classes-remaining';
      }}
    }}
    
    function addPaymentRow() {{
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
          <input type="number" class="w-full border-none focus:outline-none payment-amount" value="0" step="0.01" onchange="calculatePaymentRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="date" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01" onchange="calculatePaymentRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01" onchange="calculatePaymentRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none abono" value="0" step="0.01" onchange="calculatePaymentRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 restante">
          $0.00
        </td>
      `;
      tbody.appendChild(newRow);
    }}
    
    function addClassRow() {{
      const tbody = document.getElementById('classTableBody');
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td class="border border-gray-300 px-4 py-3">
          <input type="text" class="w-full border-none focus:outline-none">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none classes-programmed" value="0" onchange="calculateClassRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none class-input" value="0" onchange="calculateClassRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none class-input" value="0" onchange="calculateClassRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <input type="number" class="w-full border-none focus:outline-none class-input" value="0" onchange="calculateClassRemaining(this)">
        </td>
        <td class="border border-gray-300 px-4 py-3 font-semibold text-green-600 classes-remaining">
          0
        </td>
        <td class="border border-gray-300 px-4 py-3">
          <textarea class="w-full border-none focus:outline-none resize-none" rows="2" maxlength="300" placeholder="Máximo 300 caracteres"></textarea>
        </td>
      `;
      tbody.appendChild(newRow);
    }}
    
    // Inicializar cálculos al cargar la página
    document.addEventListener('DOMContentLoaded', function() {{
      // Cargar datos guardados
      loadSavedData();
      
      // Calcular restante en tabla de pagos
      const paymentRows = document.querySelectorAll('#paymentTableBody tr');
      paymentRows.forEach(row => {{
        calculatePaymentRemaining(row.querySelector('.payment-amount'));
      }});
      
      // Calcular restante en tabla de clases
      const classRows = document.querySelectorAll('#classTableBody tr');
      classRows.forEach(row => {{
        calculateClassRemaining(row.querySelector('.classes-programmed'));
      }});
    }});
  </script>
</body>
</html>'''
    
    return html

def main():
    """Función principal que genera todos los archivos"""
    
    print("🚀 Generando archivos para It's English Time...")
    
    # Crear archivos de panel para cada profesor
    for professor, students in PROFESORES.items():
        panel_html = create_professor_panel(professor, students)
        filename = f"panel_{professor}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(panel_html)
        print(f"✅ Panel creado: {filename}")
    
    # Crear archivos de alumno para cada estudiante
    for professor, students in PROFESORES.items():
        for student in students:
            student_html = create_student_page(student, professor)
            filename = f"alumno_{student.lower().replace(' ', '_')}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(student_html)
            print(f"✅ Alumno creado: {filename}")
    
    print("\n🎉 ¡Todos los archivos han sido generados exitosamente!")
    print(f"📊 Total de archivos creados: {len(PROFESORES) + sum(len(students) for students in PROFESORES.values())}")

if __name__ == "__main__":
    main()
