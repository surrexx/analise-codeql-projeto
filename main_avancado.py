# -------
# - Simulacao de Clinica Medica - VERSAO PREMIUM
# - Ficheiro principal
# - Projeto de Algoritmos e Tecnicas de Programacao
# - Universidade do Minho - Engenharia Biomedica
# - 2025-11-19 by Leticia, Maria, Matilde
# -------

import sys
import os


def main():
    """Funcao principal da aplicacao"""
    print("=" * 80)
    print("SIMULACAO DE CLINICA MEDICA - VERSAO PREMIUM")
    print("=" * 80)
    print()
    print("Funcionalidades:")
    print("   - Sistema de Triagem (Prioridades)")
    print("   - Abandono por excesso de espera")
    print("   - Turnos de medicos (Dia/Noite)")
    print("   - Pausas para medicos")
    print("   - Chegadas nao homogeneas")
    print("   - Modo What-If")
    print("   - Visualizacao grafica da clinica")
    print("   - 8+ tipos de graficos diferentes")
    print()
    
    # Verificar se ficheiro pessoas.json existe
    if not os.path.exists('pessoas.json'):
        print("Aviso: ficheiro 'pessoas.json' nao encontrado")
        print("   A opcao 'Usar pessoas reais' nao estara disponivel")
        print()
    
    # Importar e executar interface
    from gui_corrigido_sem_emoji import InterfaceClinica
    
    print("Iniciando interface grafica premium...")
    print()
    interface = InterfaceClinica()
    interface.executar()
    
    print("\n" + "=" * 80)
    print("Aplicacao encerrada. Ate breve!")
    print("=" * 80)


if __name__ == '__main__':
    main()