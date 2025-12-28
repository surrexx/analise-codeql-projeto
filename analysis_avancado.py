# -------
# - Módulo de Análise Avançado
# - Gráficos premium + Visualização da clínica
# - Projeto de Algoritmos e Técnicas de Programação
# - Universidade do Minho - Engenharia Biomédica
# - 2025-11-19 by Letícia, Maria, Matilde
# -------

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List
from sim_module_avancado import Simulacao, NOMES_PRIORIDADE


class AnalisadorResultados:
    """Classe para análise avançada e visualização de resultados"""
    
    def __init__(self, resultados: Dict):
        """Inicializa o analisador"""
        self.resultados = resultados
    
    def gerar_relatorio_texto(self) -> str:
        """Gera relatório completo com todas as estatísticas"""
        r = "\n" + "="*70 + "\n"
        r += "📊 RELATÓRIO COMPLETO DA SIMULAÇÃO\n"
        r += "="*70 + "\n\n"
        
        r += "🏥 ESTATÍSTICAS GERAIS:\n"
        r += f"  ✅ Doentes atendidos: {self.resultados['doentes_atendidos']}\n"
        r += f"  ❌ Doentes que abandonaram: {self.resultados['doentes_abandonaram']}\n"
        r += f"  📉 Taxa de abandono: {self.resultados.get('taxa_abandono', 0):.2f}%\n"
        r += f"  ⏱️  Tempo médio de espera: {self.resultados['tempo_medio_espera']:.2f} min\n"
        r += f"  🩺 Tempo médio de consulta: {self.resultados['tempo_medio_consulta']:.2f} min\n"
        r += f"  🏥 Tempo médio na clínica: {self.resultados['tempo_medio_clinica']:.2f} min\n"
        r += f"  👥 Tamanho médio da fila: {self.resultados['tamanho_medio_fila']:.2f}\n"
        r += f"  📈 Tamanho máximo da fila: {self.resultados['max_fila']}\n"
        r += f"  👨‍⚕️ Ocupação média dos médicos: {self.resultados['ocupacao_media_medicos']:.2f}%\n"
        
        # Estatísticas por prioridade
        if 'atendidos_por_prioridade' in self.resultados:
            r += "\n" + "-"*70 + "\n"
            r += "🚦 ESTATÍSTICAS POR PRIORIDADE (TRIAGEM):\n"
            r += "-"*70 + "\n"
            
            cores = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "🔵"}
            
            for prioridade in range(1, 6):
                atendidos = self.resultados['atendidos_por_prioridade'][prioridade]
                abandonos = self.resultados['abandonos_por_prioridade'][prioridade]
                tempo_medio = self.resultados['tempo_medio_por_prioridade'].get(prioridade, 0)
                
                if atendidos > 0 or abandonos > 0:
                    r += f"\n{cores[prioridade]} {NOMES_PRIORIDADE[prioridade]}:\n"
                    r += f"  Atendidos: {atendidos}\n"
                    r += f"  Abandonos: {abandonos}\n"
                    r += f"  Tempo médio espera: {tempo_medio:.2f} min\n"
        
        # Estatísticas dos médicos
        r += "\n" + "-"*70 + "\n"
        r += "👨‍⚕️ ESTATÍSTICAS POR MÉDICO:\n"
        r += "-"*70 + "\n"
        
        for medico_id, stats in self.resultados['medicos_stats'].items():
            r += f"\n{medico_id} ({stats.get('turno', 'N/A')}):\n"
            r += f"  Doentes atendidos: {stats['doentes_atendidos']}\n"
            r += f"  Tempo ocupado: {stats['tempo_ocupado']:.2f} min\n"
            r += f"  Ocupação: {stats['ocupacao_percentual']:.2f}%\n"
        
        r += "\n" + "="*70 + "\n"
        return r
    
    def plot_evolucao_fila(self, salvar=False, filename='grafico_fila.png'):
        """Gráfico da evolução da fila"""
        if not self.resultados['historico_fila']:
            print("Sem dados de fila")
            return
        
        tempos = [t for t, _ in self.resultados['historico_fila']]
        tamanhos = [tam for _, tam in self.resultados['historico_fila']]
        
        plt.figure(figsize=(14, 6))
        plt.plot(tempos, tamanhos, linewidth=2, color='#2E86AB', alpha=0.8)
        plt.fill_between(tempos, tamanhos, alpha=0.3, color='#2E86AB')
        plt.xlabel('Tempo (minutos)', fontsize=13, fontweight='bold')
        plt.ylabel('Tamanho da Fila', fontsize=13, fontweight='bold')
        plt.title('Evolucao do Tamanho da Fila de Espera', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_ocupacao_medicos(self, salvar=False, filename='grafico_ocupacao.png'):
        """Gráfico da ocupação dos médicos"""
        if not self.resultados['historico_ocupacao']:
            print("Sem dados de ocupação")
            return
        
        tempos = [t for t, _ in self.resultados['historico_ocupacao']]
        ocupacao = [ocu for _, ocu in self.resultados['historico_ocupacao']]
        
        plt.figure(figsize=(14, 6))
        plt.plot(tempos, ocupacao, linewidth=2, color='#A23B72', alpha=0.8)
        plt.fill_between(tempos, ocupacao, alpha=0.3, color='#A23B72')
        plt.axhline(y=90, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Limite Crítico (90%)')
        plt.xlabel('Tempo (minutos)', fontsize=13, fontweight='bold')
        plt.ylabel('Ocupacao (%)', fontsize=13, fontweight='bold')
        plt.title('Evolucao da Ocupacao dos Medicos', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.ylim(0, 105)
        plt.legend(fontsize=11)
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_distribuicao_tempos_espera(self, salvar=False, filename='grafico_espera.png'):
        """Histograma dos tempos de espera"""
        if not self.resultados['tempos_espera_individuais']:
            print("Sem dados de tempo de espera")
            return
        
        tempos = self.resultados['tempos_espera_individuais']
        
        plt.figure(figsize=(14, 6))
        plt.hist(tempos, bins=40, color='#F18F01', alpha=0.7, edgecolor='black', linewidth=1.2)
        plt.xlabel('Tempo de Espera (minutos)', fontsize=13, fontweight='bold')
        plt.ylabel('Frequencia', fontsize=13, fontweight='bold')
        plt.title('Distribuicao dos Tempos de Espera', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        media = np.mean(tempos)
        mediana = np.median(tempos)
        plt.axvline(media, color='red', linestyle='--', linewidth=2.5, label=f'Média: {media:.2f} min')
        plt.axvline(mediana, color='green', linestyle='--', linewidth=2.5, label=f'Mediana: {mediana:.2f} min')
        plt.legend(fontsize=12)
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_estatisticas_medicos(self, salvar=False, filename='grafico_medicos.png'):
        """Gráfico de estatísticas dos médicos"""
        if not self.resultados['medicos_stats']:
            print("Sem dados de médicos")
            return
        
        medicos = list(self.resultados['medicos_stats'].keys())
        doentes = [stats['doentes_atendidos'] for stats in self.resultados['medicos_stats'].values()]
        ocupacao = [stats['ocupacao_percentual'] for stats in self.resultados['medicos_stats'].values()]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Gráfico 1: Doentes
        colors1 = plt.cm.viridis(np.linspace(0, 0.8, len(medicos)))
        ax1.bar(medicos, doentes, color=colors1, alpha=0.85, edgecolor='black', linewidth=1.2)
        ax1.set_xlabel('Medico', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Doentes Atendidos', fontsize=12, fontweight='bold')
        ax1.set_title('Doentes Atendidos por Medico', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Grafico 2: Ocupacao
        colors2 = ['#06A77D' if o < 80 else '#F18F01' if o < 90 else '#D62828' for o in ocupacao]
        ax2.bar(medicos, ocupacao, color=colors2, alpha=0.85, edgecolor='black', linewidth=1.2)
        ax2.axhline(y=80, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='Alerta (80%)')
        ax2.axhline(y=90, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Critico (90%)')
        ax2.set_xlabel('Medico', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Ocupacao (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Ocupacao dos Medicos', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax2.set_ylim(0, 105)
        ax2.legend(fontsize=10)
        
        plt.tight_layout()
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_taxa_abandono(self, salvar=False, filename='grafico_abandono.png'):
        """NOVO: Gráfico de taxa de abandono"""
        total_atendidos = self.resultados['doentes_atendidos']
        total_abandonos = self.resultados['doentes_abandonaram']
        
        if total_atendidos == 0 and total_abandonos == 0:
            print("Sem dados suficientes")
            return
        
        plt.figure(figsize=(10, 8))
        
        labels = ['Atendidos', 'Abandonaram']
        valores = [total_atendidos, total_abandonos]
        cores = ['#06A77D', '#D62828']
        explode = (0, 0.1)
        
        plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90,
                colors=cores, explode=explode, shadow=True, textprops={'fontsize': 14, 'fontweight': 'bold'})
        plt.title('Taxa de Abandono vs Atendimento', fontsize=16, fontweight='bold')
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_espera_por_prioridade(self, salvar=False, filename='grafico_prioridade.png'):
        """NOVO: Gráfico de espera por prioridade"""
        tempos_por_prioridade = self.resultados.get('tempo_medio_por_prioridade', {})
        
        if not tempos_por_prioridade:
            print("Sem dados de triagem")
            return
        
        prioridades = list(range(1, 6))
        tempos = [tempos_por_prioridade.get(p, 0) for p in prioridades]
        labels = ['Vermelho', 'Laranja', 'Amarelo', 'Verde', 'Azul']
        cores = ['#D62828', '#F18F01', '#F4D03F', '#06A77D', '#2E86AB']
        
        plt.figure(figsize=(12, 7))
        bars = plt.bar(labels, tempos, color=cores, alpha=0.85, edgecolor='black', linewidth=1.5)
        plt.xlabel('Prioridade (Triagem)', fontsize=13, fontweight='bold')
        plt.ylabel('Tempo Medio de Espera (min)', fontsize=13, fontweight='bold')
        plt.title('Tempo de Espera Medio por Prioridade', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}min', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_percentagem_urgentes(self, salvar=False, filename='grafico_urgentes.png'):
        """NOVO: Gráfico de % urgentes atendidos"""
        atendidos = self.resultados.get('atendidos_por_prioridade', {})
        abandonos = self.resultados.get('abandonos_por_prioridade', {})
        
        if not atendidos:
            print("Sem dados de triagem")
            return
        
        labels = ['Vermelho', 'Laranja', 'Amarelo', 'Verde', 'Azul']
        cores = ['#D62828', '#F18F01', '#F4D03F', '#06A77D', '#2E86AB']
        
        percentagens = []
        for p in range(1, 6):
            total = atendidos[p] + abandonos[p]
            if total > 0:
                perc = (atendidos[p] / total) * 100
                percentagens.append(perc)
            else:
                percentagens.append(0)
        
        plt.figure(figsize=(12, 7))
        bars = plt.bar(labels, percentagens, color=cores, alpha=0.85, edgecolor='black', linewidth=1.5)
        plt.axhline(y=90, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Meta (90%)')
        plt.xlabel('Prioridade', fontsize=13, fontweight='bold')
        plt.ylabel('% Atendidos', fontsize=13, fontweight='bold')
        plt.title('Percentagem de Doentes Atendidos por Prioridade', fontsize=16, fontweight='bold')
        plt.ylim(0, 105)
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        plt.legend(fontsize=11)
        
        # Adicionar valores
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_visualizacao_clinica(self, salvar=False, filename='visualizacao_clinica.png'):
        """NOVO: Visualização gráfica da clínica"""
        num_medicos = len(self.resultados['medicos_stats'])
        max_fila = self.resultados['max_fila']
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Titulo
        ax.text(5, 9.5, 'VISUALIZACAO DA CLINICA', 
                fontsize=20, fontweight='bold', ha='center', 
                bbox=dict(boxstyle='round', facecolor='#06A77D', alpha=0.3))
        
        # Recepcao
        recepcao = patches.Rectangle((0.5, 7), 2, 1.5, linewidth=3, 
                                     edgecolor='#2E86AB', facecolor='#E3F2FD')
        ax.add_patch(recepcao)
        ax.text(1.5, 7.75, 'RECEPCAO', fontsize=12, fontweight='bold', ha='center')
        
        # Fila de espera
        fila_y = 6
        ax.text(0.5, fila_y + 0.5, 'FILA DE ESPERA', fontsize=11, fontweight='bold')
        pessoas_na_fila = min(max_fila, 20)
        for i in range(pessoas_na_fila):
            x = 0.5 + (i % 10) * 0.3
            y = fila_y - (i // 10) * 0.3
            ax.plot(x, y, 'o', markersize=8, color='blue')
        
        # Consultorios
        consultorios_y = 4
        ax.text(5, consultorios_y + 1.2, 'CONSULTORIOS', 
                fontsize=12, fontweight='bold', ha='center')
        
        for i in range(min(num_medicos, 6)):
            x = 1 + (i % 3) * 2.5
            y = consultorios_y - (i // 3) * 2
            
            # Consultório
            consultorio = patches.Rectangle((x, y), 1.8, 1.5, linewidth=2, 
                                           edgecolor='black', facecolor='#FFF9C4')
            ax.add_patch(consultorio)
            
            # Medico
            ax.plot(x + 0.5, y + 1, 'D', markersize=15, color='green')
            ax.text(x + 0.9, y + 0.5, f'M{i}', fontsize=10, fontweight='bold')
            
            # Status
            stats = self.resultados['medicos_stats'][f'm{i}']
            ocupacao = stats['ocupacao_percentual']
            cor = '#06A77D' if ocupacao < 80 else '#F18F01' if ocupacao < 90 else '#D62828'
            ax.text(x + 0.9, y + 0.2, f'{ocupacao:.0f}%', fontsize=9, 
                   color=cor, fontweight='bold')
        
        # Legenda
        ax.text(7.5, 1.5, 'LEGENDA:', fontsize=11, fontweight='bold')
        ax.text(7.5, 1.2, '<80% - Normal', fontsize=9, color='#06A77D')
        ax.text(7.5, 0.9, '80-90% - Alerta', fontsize=9, color='#F18F01')
        ax.text(7.5, 0.6, '>90% - Critico', fontsize=9, color='#D62828')
        
        # Estatisticas
        ax.text(0.5, 0.8, f'Atendidos: {self.resultados["doentes_atendidos"]}', 
                fontsize=10, fontweight='bold')
        ax.text(0.5, 0.5, f'Abandonos: {self.resultados["doentes_abandonaram"]}', 
                fontsize=10, fontweight='bold')
        
        if salvar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_todos_graficos(self):
        """Gera TODOS os graficos"""
        print("\nGerando todos os graficos...\n")
        self.plot_evolucao_fila()
        self.plot_ocupacao_medicos()
        self.plot_distribuicao_tempos_espera()
        self.plot_estatisticas_medicos()
        self.plot_taxa_abandono()
        self.plot_espera_por_prioridade()
        self.plot_percentagem_urgentes()
        self.plot_visualizacao_clinica()
        print("Todos os graficos gerados com sucesso!")


def analise_comparativa_taxa_chegada(config_base: Dict, taxas: List[float], callback_progresso=None) -> Dict:
    """Análise comparativa variando taxa de chegada"""
    resultados_comp = {
        'taxas': [],
        'tempo_medio_espera': [],
        'tamanho_medio_fila': [],
        'tamanho_max_fila': [],
        'ocupacao_medicos': [],
        'taxa_abandono': []
    }
    
    total = len(taxas)
    
    for i, taxa in enumerate(taxas):
        config = config_base.copy()
        config['taxa_chegada'] = taxa / 60.0
        
        sim = Simulacao(config)
        resultados = sim.simular()
        
        resultados_comp['taxas'].append(taxa)
        resultados_comp['tempo_medio_espera'].append(resultados['tempo_medio_espera'])
        resultados_comp['tamanho_medio_fila'].append(resultados['tamanho_medio_fila'])
        resultados_comp['tamanho_max_fila'].append(resultados['max_fila'])
        resultados_comp['ocupacao_medicos'].append(resultados['ocupacao_media_medicos'])
        resultados_comp['taxa_abandono'].append(resultados.get('taxa_abandono', 0))
        
        if callback_progresso:
            progresso = int(((i + 1) / total) * 100)
            callback_progresso(progresso)
    
    return resultados_comp


def plot_analise_comparativa(resultados: Dict, salvar=False, filename='grafico_comparativo.png'):
    """Gráfico comparativo completo"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    taxas = resultados['taxas']
    
    # Gráfico 1
    ax1.plot(taxas, resultados['tempo_medio_espera'], marker='o', linewidth=2.5, 
            color='#2E86AB', markersize=8)
    ax1.set_xlabel('Taxa de Chegada (doentes/hora)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Tempo Medio de Espera (min)', fontsize=11, fontweight='bold')
    ax1.set_title('Tempo de Espera vs Taxa de Chegada', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Grafico 2
    ax2.plot(taxas, resultados['tamanho_medio_fila'], marker='s', linewidth=2.5, 
            color='#F18F01', markersize=8)
    ax2.set_xlabel('Taxa de Chegada (doentes/hora)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Tamanho Medio da Fila', fontsize=11, fontweight='bold')
    ax2.set_title('Tamanho Medio da Fila vs Taxa de Chegada', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Grafico 3
    ax3.plot(taxas, resultados['ocupacao_medicos'], marker='d', linewidth=2.5, 
            color='#A23B72', markersize=8)
    ax3.axhline(y=90, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Critico')
    ax3.set_xlabel('Taxa de Chegada (doentes/hora)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Ocupacao dos Medicos (%)', fontsize=11, fontweight='bold')
    ax3.set_title('Ocupacao dos Medicos vs Taxa de Chegada', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.set_ylim(0, 105)
    ax3.legend()
    
    # Grafico 4 - NOVO: Taxa de abandono
    ax4.plot(taxas, resultados['taxa_abandono'], marker='^', linewidth=2.5, 
            color='#D62828', markersize=8)
    ax4.set_xlabel('Taxa de Chegada (doentes/hora)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Taxa de Abandono (%)', fontsize=11, fontweight='bold')
    ax4.set_title('Taxa de Abandono vs Taxa de Chegada', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    plt.close()