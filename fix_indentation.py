#!/usr/bin/env python3
"""
Script para corregir problemas de indentación en app.py
"""

def fix_indentation_issues():
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Corregir líneas específicas conocidas con problemas
        if line_num == 235:  # with col1:
            fixed_lines.append("    with col1:\n")
        elif line_num == 370:  # if can_train:
            fixed_lines.append("        if can_train:\n")
        elif line_num == 485:  # numeric_vars = ...
            fixed_lines.append("        numeric_vars = [v for v in variables if pd.api.types.is_numeric_dtype(df[v])]\n")
        elif line_num == 490:  # if can_segment:
            fixed_lines.append("        if can_segment:\n")
        elif line_num == 495:  # if st.button(
            fixed_lines.append("            if st.button(\"🚀 Ejecutar segmentación\", type=\"primary\", key=\"execute_segmentation_btn\"):\n")
        else:
            # Para otras líneas, mantener el contenido original
            fixed_lines.append(line)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Problemas de indentación corregidos")

if __name__ == "__main__":
    fix_indentation_issues()
