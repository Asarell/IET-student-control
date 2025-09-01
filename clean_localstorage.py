import os

def clean_localstorage_references(filename):
    """Limpiar referencias restantes de localStorage"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Eliminar comentarios y líneas vacías de localStorage
    content = content.replace('      // Guardar en localStorage\n      \n    ', '    ')
    content = content.replace('      // Guardar en localStorage\n      ', '      ')
    
    # Eliminar referencias a localStorage.getItem
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if 'localStorage.getItem(' not in line and 'localStorage.setItem(' not in line and 'localStorage.removeItem(' not in line:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Guardar el archivo
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} limpiado")

# Limpiar los archivos que aún tienen referencias
files_to_clean = [
    'panel_astrid.html',
    'panel_patty.html', 
    'panel_jesus.html',
    'panel_erwin.html'
]

for filename in files_to_clean:
    if os.path.exists(filename):
        clean_localstorage_references(filename)

print("\n🎉 Limpieza completada!")
