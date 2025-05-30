#!/usr/bin/env python3
"""
Script para identificar y corregir todos los problemas de indentación
"""
import re

def fix_indentation_problems():
    """Corregir todos los problemas de indentación en src/eda.py"""
    
    with open('src/eda.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Lista de patrones problemáticos y sus correcciones
    fixes = [
        # Corregir indentaciones incorrectas con espacios extra
        (r'^(\s{2,})(\s{2,})([^\s])', r'\1\3'),  # Reducir doble indentación
        (r'^      ([^\s])', r'    \1'),          # 6 espacios -> 4 espacios
        (r'^        ([^\s])', r'    \1'),        # 8 espacios -> 4 espacios (si es incorrecto)
    ]
    
    # Aplicar correcciones línea por línea
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        original_line = line
        
        # Casos específicos conocidos
        if line_num == 174 and line.strip().startswith('if len(cat_cols)'):
            line = '    if len(cat_cols) == 0:'
        elif '      #' in line:  # Comentarios con indentación incorrecta
            line = line.replace('      #', '    #')
        elif '      if' in line:  # If statements con indentación incorrecta
            line = line.replace('      if', '    if')
        elif '      ' in line and not line.strip().startswith('#'):
            # Corregir indentación de 6 espacios a 4
            line = line.replace('      ', '    ', 1)
        
        fixed_lines.append(line)
        
        if line != original_line:
            print(f"Línea {line_num} corregida:")
            print(f"  Antes: {repr(original_line)}")
            print(f"  Después: {repr(line)}")
    
    # Escribir el archivo corregido
    with open('src/eda.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("Correcciones de indentación aplicadas")
    
    # Verificar sintaxis
    try:
        compile('\n'.join(fixed_lines), 'src/eda.py', 'exec')
        print("✅ Sintaxis correcta después de las correcciones")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en línea {e.lineno}: {e.msg}")
        return False

if __name__ == "__main__":
    fix_indentation_problems()
