import os
import re

# Lista de archivos a corregir
files_to_fix = [
    'alumno_pilar.html',
    'alumno_carla.html',
    'alumno_wendy.html',
    'alumno_nubia.html',
    'alumno_alberto.html',
    'alumno_miguel.html',
    'alumno_karina.html',
    'alumno_jesus_m.html',
    'alumno_laura.html',
    'alumno_michelle.html',
    'alumno_merian.html',
    'alumno_pao_rosales.html',
    'alumno_nadia.html',
    'alumno_mía.html',
    'alumno_ricardo.html',
    'alumno_rouss.html',
    'alumno_josué.html',
    'alumno_montse.html',
    'alumno_oscar.html',
    'alumno_marycarmen.html',
    'alumno_ana.html',
    'alumno_dina.html',
    'alumno_loth.html',
    'alumno_alan.html'
]

# Código a insertar después de la sección de carga de clases
reschedule_code = '''
        // Cargar reprogramación
        const rescheduleDoc = await db.collection('students').doc(studentName).collection('reschedule').doc('current').get();
        if (rescheduleDoc.exists) {
          const rescheduleData = rescheduleDoc.data().reschedule;
          const tbody = document.getElementById('rescheduleTableBody');
          tbody.innerHTML = '';

          rescheduleData.forEach(reschedule => {
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
              <td class="border border-gray-300 px-4 py-3">
                <input type="number" class="w-full border-none focus:outline-none" value="${reschedule.numeroClase}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="${reschedule.fechaClase}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="date" class="w-full border-none focus:outline-none" value="${reschedule.fechaReprogramar}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <input type="time" class="w-full border-none focus:outline-none" value="${reschedule.horarioClase}">
              </td>
              <td class="border border-gray-300 px-4 py-3">
                <select class="w-full border-none focus:outline-none bg-transparent">
                  <option value="">Seleccionar</option>
                  <option value="Asistencia" ${reschedule.asistencia === 'Asistencia' ? 'selected' : ''}>Asistencia</option>
                  <option value="Falta" ${reschedule.asistencia === 'Falta' ? 'selected' : ''}>Falta</option>
                </select>
              </td>
            `;
            tbody.appendChild(newRow);
          });
        }'''

def fix_file(filename):
    if not os.path.exists(filename):
        print(f"❌ Archivo {filename} no encontrado")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Verificar si ya tiene la lógica de reprogramación
        if '// Cargar reprogramación' in content:
            print(f"✅ {filename} ya tiene la lógica de reprogramación")
            return True
        
        # Buscar el patrón exacto donde insertar el código
        # Buscamos después de la sección de carga de clases y antes del catch
        pattern = r'(\s+});\s+}\s+} catch \(error\) {'
        
        if re.search(pattern, content):
            # Insertar el código antes del catch
            new_content = re.sub(pattern, reschedule_code + r'\1', content)
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"✅ {filename} corregido exitosamente")
            return True
        else:
            print(f"❌ No se pudo encontrar el patrón en {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error procesando {filename}: {str(e)}")
        return False

def main():
    print("🔧 Iniciando corrección de archivos de alumnos...")
    print("=" * 50)
    
    success_count = 0
    total_files = len(files_to_fix)
    
    for filename in files_to_fix:
        if fix_file(filename):
            success_count += 1
    
    print("=" * 50)
    print(f"📊 Resumen: {success_count}/{total_files} archivos corregidos exitosamente")
    
    if success_count == total_files:
        print("🎉 ¡Todos los archivos han sido corregidos!")
    else:
        print("⚠️  Algunos archivos no pudieron ser corregidos")

if __name__ == "__main__":
    main()
