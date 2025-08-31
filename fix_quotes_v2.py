#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para corregir las comillas en los archivos de paneles de profesores
"""

import os
import re

def fix_professor_panels():
    """Corrige las comillas en todos los archivos de paneles de profesores"""
    
    professor_files = [
        'panel_ale.html',
        'panel_jesus.html', 
        'panel_patty.html',
        'panel_astrid.html',
        'panel_blanca.html',
        'panel_erwin.html'
    ]
    
    for filename in professor_files:
        if os.path.exists(filename):
            print(f"🔧 Corrigiendo {filename}...")
            
            # Leer el archivo
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Corregir las comillas escapadas
            content = content.replace("\\'", "'")
            
            # Corregir las comillas en los onclick
            # Buscar patrones como: onclick="goToStudent(alumno_xxx.html)"
            # Y reemplazarlos con: onclick="goToStudent('alumno_xxx.html')"
            pattern = r'onclick="goToStudent\(([^)]+\.html)\)"'
            replacement = r'onclick="goToStudent(\'\1\')"'
            
            content = re.sub(pattern, replacement, content)
            
            # Escribir el archivo corregido
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filename} corregido")
        else:
            print(f"❌ {filename} no encontrado")

if __name__ == "__main__":
    fix_professor_panels()
    print("\n🎉 ¡Todos los archivos han sido corregidos!")

