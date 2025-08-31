#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir las comillas faltantes en los botones de navegación
"""

import os
import re

def fix_button_quotes():
    """Corrige las comillas faltantes en los botones de navegación"""
    
    # Obtener todos los archivos de paneles de profesores
    panel_files = [f for f in os.listdir('.') if f.startswith('panel_') and f.endswith('.html')]
    
    for filename in panel_files:
        print(f"🔧 Corrigiendo {filename}...")
        
        # Leer el archivo
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corregir los botones que no tienen comillas
        # Buscar patrones como: onclick="goToStudent(alumno_xxx.html)"
        # Y reemplazarlos con: onclick="goToStudent('alumno_xxx.html')"
        pattern = r'onclick="goToStudent\(([^)]+\.html)\)"'
        replacement = r'onclick="goToStudent(\'\1\')"'
        
        content = re.sub(pattern, replacement, content)
        
        # Escribir el archivo corregido
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename} corregido")

if __name__ == "__main__":
    fix_button_quotes()
    print("\n🎉 ¡Todos los botones han sido corregidos!")

