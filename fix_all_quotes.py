#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir todas las comillas escapadas incorrectamente
"""

import os
import re

def fix_all_quotes():
    """Corrige las comillas escapadas en todos los archivos HTML"""
    
    # Obtener todos los archivos HTML
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for filename in html_files:
        print(f"🔧 Corrigiendo {filename}...")
        
        # Leer el archivo
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corregir las comillas escapadas incorrectamente
        content = content.replace("\\'", "'")
        
        # Escribir el archivo corregido
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename} corregido")

if __name__ == "__main__":
    fix_all_quotes()
    print("\n🎉 ¡Todos los archivos han sido corregidos!")

