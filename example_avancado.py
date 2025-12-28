# -------
# - Exemplos de Uso - VERSÃO AVANÇADA
# - Demonstração de todas as funcionalidades
# - Projeto de Algoritmos e Técnicas de Programação
# - Universidade do Minho - Engenharia Biomédica
# - 2025-11-19 by Letícia, Maria, Matilde
# -------

from sim_module_avancado import Simulacao
from analysis_avancado import AnalisadorResultados, analise_comparativa_taxa_chegada, plot_analise_comparativa


def exemplo_basico():
    """Exemplo 1: Simulacao basica"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Simulacao Basica")
    print("="*70)
    
    config = {
        'num_medicos': 3,
        'taxa_chegada': 15 / 60.0,
        'tempo_medio_consulta': 15,
        'tempo_simulacao': 480,
        'distribuicao': 'uniform',
        'usar_pessoas_reais': False,
        'usar_triagem': False,
        'tempo_max_espera': 120,
        'usar_turnos': False,
        'usar_pausas': False,
        'chegadas_nao_homogeneas': False
    }
    
    print("Executando simulacao basica...")
    sim = Simulacao(config)
    resultados = sim.simular()
    
    print(f"\nSimulacao concluida!")
    print(f"   Doentes atendidos: {resultados['doentes_atendidos']}")
    print(f"   Tempo medio de espera: {resultados['tempo_medio_espera']:.2f} min")
    print(f"   Ocupacao media dos medicos: {resultados['ocupacao_media_medicos']:.2f}%")


def exemplo_triagem():
    """Exemplo 2: Sistema de triagem"""
    print("\n" + "="*70)
    print("EXEMPLO 2: Sistema de Triagem (Prioridades)")
    print("="*70)
    
    config = {
        'num_medicos': 3,
        'taxa_chegada': 20 / 60.0,
        'tempo_medio_consulta': 15,
        'tempo_simulacao': 480,
        'distribuicao': 'uniform',
        'usar_pessoas_reais': False,
        'usar_triagem': True,
        'tempo_max_espera': 90,
        'usar_turnos': False,
        'usar_pausas': False,
        'chegadas_nao_homogeneas': False
    }
    
    print("Executando simulação com triagem...")
    sim = Simulacao(config)
    resultados = sim.simular()
    
    print(f"\nSimulacao concluida!")
    print(f"   Doentes atendidos: {resultados['doentes_atendidos']}")
    print(f"   Doentes que abandonaram: {resultados['doentes_abandonaram']}")
    print(f"   Taxa de abandono: {resultados.get('taxa_abandono', 0):.2f}%")
    
    print("\nAtendimentos por prioridade:")
    cores = {1: "VERMELHO", 2: "LARANJA", 3: "AMARELO", 4: "VERDE", 5: "AZUL"}
    for p in range(1, 6):
        atendidos = resultados['atendidos_por_prioridade'][p]
        if atendidos > 0:
            tempo_medio = resultados['tempo_medio_por_prioridade'][p]
            print(f"   {cores[p]} Prioridade {p}: {atendidos} doentes (espera: {tempo_medio:.1f}min)")


def exemplo_turnos_pausas():
    """Exemplo 3: Turnos e pausas"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Turnos e Pausas para Médicos")
    print("="*70)
    
    config = {
        'num_medicos': 4,
        'taxa_chegada': 18 / 60.0,
        'tempo_medio_consulta': 15,
        'tempo_simulacao': 960,  # 16 horas
        'distribuicao': 'uniform',
        'usar_pessoas_reais': False,
        'usar_triagem': True,
        'tempo_max_espera': 120,
        'usar_turnos': True,
        'duracao_turno': 480,  # 8 horas
        'usar_pausas': True,
        'duracao_pausa': 30,
        'intervalo_pausa': 240,
        'chegadas_nao_homogeneas': False
    }
    
    print("Executando simulação com turnos e pausas...")
    sim = Simulacao(config)
    resultados = sim.simular()
    
    print(f"\nSimulacao concluida!")
    print(f"   Doentes atendidos: {resultados['doentes_atendidos']}")
    print(f"   Ocupacao media: {resultados['ocupacao_media_medicos']:.2f}%")
    
    print("\nEstatisticas por medico:")
    for medico_id, stats in resultados['medicos_stats'].items():
        print(f"   {medico_id} ({stats['turno']}): {stats['doentes_atendidos']} doentes, {stats['ocupacao_percentual']:.1f}%")


def exemplo_chegadas_nao_homogeneas():
    """Exemplo 4: Chegadas não homogêneas"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Chegadas Não Homogêneas (Picos ao longo do dia)")
    print("="*70)
    
    config = {
        'num_medicos': 3,
        'taxa_chegada': 15 / 60.0,
        'tempo_medio_consulta': 15,
        'tempo_simulacao': 1440,  # 24 horas
        'distribuicao': 'uniform',
        'usar_pessoas_reais': False,
        'usar_triagem': True,
        'tempo_max_espera': 90,
        'usar_turnos': False,
        'usar_pausas': False,
        'chegadas_nao_homogeneas': True
    }
    
    print("Executando simulação com picos de chegada...")
    print("  Picos: 9h-11h e 14h-17h")
    print("  Vales: 12h-14h e 20h-24h")
    
    sim = Simulacao(config)
    resultados = sim.simular()
    
    print(f"\nSimulacao concluida!")
    print(f"   Doentes atendidos: {resultados['doentes_atendidos']}")
    print(f"   Fila maxima: {resultados['max_fila']} doentes")
    print(f"   Tempo medio de espera: {resultados['tempo_medio_espera']:.2f} min")


def exemplo_completo():
    """Exemplo 5: TUDO ativado"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Simulação COMPLETA (Todas as funcionalidades)")
    print("="*70)
    
    config = {
        'num_medicos': 6,
        'taxa_chegada': 25 / 60.0,
        'tempo_medio_consulta': 18,
        'tempo_simulacao': 1440,  # 24 horas
        'distribuicao': 'uniform',
        'usar_pessoas_reais': True,
        'usar_triagem': True,
        'tempo_max_espera': 90,
        'usar_turnos': True,
        'duracao_turno': 480,
        'usar_pausas': True,
        'duracao_pausa': 30,
        'intervalo_pausa': 240,
        'chegadas_nao_homogeneas': True
    }
    
    print("Executando simulacao PREMIUM com:")
    print("   Sistema de triagem")
    print("   Abandono de fila")
    print("   Turnos de medicos")
    print("   Pausas para medicos")
    print("   Chegadas nao homogeneas")
    print("   Pessoas reais")
    
    sim = Simulacao(config)
    resultados = sim.simular()
    
    analisador = AnalisadorResultados(resultados)
    print(analisador.gerar_relatorio_texto())


def exemplo_graficos_completo():
    """Exemplo 6: Gerar todos os gráficos"""
    print("\n" + "="*70)
    print("EXEMPLO 6: Gerar Todos os Gráficos Premium")
    print("="*70)
    
    config = {
        'num_medicos': 4,
        'taxa_chegada': 20 / 60.0,
        'tempo_medio_consulta': 15,
        'tempo_simulacao': 480,
        'distribuicao': 'uniform',
        'usar_pessoas_reais': False,
        'usar_triagem': True,
        'tempo_max_espera': 90,
        'usar_turnos': True,
        'duracao_turno': 240,
        'usar_pausas': True,
        'duracao_pausa': 30,
        'intervalo_pausa': 180,
        'chegadas_nao_homogeneas': True
    }
    
    print("Executando simulação...")
    sim = Simulacao(config)
    resultados = sim.simular()
    
    print("\nGerando todos os 8 graficos premium...")
    analisador = AnalisadorResultados(resultados)
    analisador.plot_todos_graficos()


def exemplo_analise_comparativa():
    """Exemplo 7: Análise comparativa"""
    print("\n" + "="*70)
    print("EXEMPLO 7: Análise Comparativa de Taxas")
    print("="*70)
    
    config_base = {
        'num_medicos': 3,
        'taxa_chegada': 10 / 60.0,
        'tempo_medio_consulta': 15,
        'tempo_simulacao': 480,
        'distribuicao': 'uniform',
        'usar_pessoas_reais': False,
        'usar_triagem': True,
        'tempo_max_espera': 90,
        'usar_turnos': False,
        'usar_pausas': False,
        'chegadas_nao_homogeneas': False
    }
    
    print("Testando taxas de 10 a 35 doentes/hora...")
    taxas = [10, 15, 20, 25, 30, 35]
    
    def progresso(p):
        print(f"  Progresso: {p}%")
    
    resultados_comp = analise_comparativa_taxa_chegada(
        config_base, taxas, callback_progresso=progresso
    )
    
    print("\nAnalise concluida!")
    print("\nResultados:")
    print("-" * 80)
    print(f"{'Taxa':>6} | {'Espera':>8} | {'Fila':>8} | {'Ocupacao':>10} | {'Abandono':>9}")
    print("-" * 80)
    
    for i, taxa in enumerate(resultados_comp['taxas']):
        espera = resultados_comp['tempo_medio_espera'][i]
        fila = resultados_comp['tamanho_medio_fila'][i]
        ocupacao = resultados_comp['ocupacao_medicos'][i]
        abandono = resultados_comp['taxa_abandono'][i]
        print(f"{taxa:>6.0f} | {espera:>6.2f}m | {fila:>8.2f} | {ocupacao:>8.2f}% | {abandono:>7.2f}%")
    
    print("\nGerando gráfico comparativo...")
    plot_analise_comparativa(resultados_comp)


def menu_principal():
    """Menu interativo"""
    print("\n" + "="*70)
    print("EXEMPLOS DE USO - VERSAO PREMIUM")
    print("="*70)
    print("\nEscolha um exemplo:")
    print("1. Simulacao Basica")
    print("2. Sistema de Triagem (Prioridades)")
    print("3. Turnos e Pausas para Medicos")
    print("4. Chegadas Nao Homogeneas")
    print("5. Simulacao COMPLETA (Tudo ativado)")
    print("6. Gerar Todos os Graficos Premium")
    print("7. Analise Comparativa")
    print("8. Executar TODOS os Exemplos")
    print("0. Sair")
    
    running = True
    while running:
        escolha = input("\nEscolha (0-8): ").strip()
        
        if escolha == '1':
            exemplo_basico()
        elif escolha == '2':
            exemplo_triagem()
        elif escolha == '3':
            exemplo_turnos_pausas()
        elif escolha == '4':
            exemplo_chegadas_nao_homogeneas()
        elif escolha == '5':
            exemplo_completo()
        elif escolha == '6':
            exemplo_graficos_completo()
        elif escolha == '7':
            exemplo_analise_comparativa()
        elif escolha == '8':
            exemplo_basico()
            exemplo_triagem()
            exemplo_turnos_pausas()
            exemplo_chegadas_nao_homogeneas()
            exemplo_completo()
            exemplo_graficos_completo()
            exemplo_analise_comparativa()
        elif escolha == '0':
            print("\nAte breve!")
            running = False
        else:
            print("\nOpcao invalida! Tente novamente.")
        
        if running:
            input("\nPressione Enter para continuar...")


if __name__ == '__main__':
    menu_principal()