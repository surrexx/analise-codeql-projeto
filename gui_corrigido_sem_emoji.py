# -------
# - Interface Grafica Avancada da Simulacao
# - GUI com PySimpleGUI + Funcionalidades Premium
# - Projeto de Algoritmos e Tecnicas de Programacao
# - Universidade do Minho - Engenharia Biomedica
# - 2025-11-19 by Leticia, Maria, Matilde
# -------

import PySimpleGUI as sg
from sim_module_avancado import Simulacao
from analysis_avancado import AnalisadorResultados, analise_comparativa_taxa_chegada, plot_analise_comparativa


class InterfaceClinica:
    """Interface grafica avancada para a simulacao da clinica"""
    
    def __init__(self):
        """Inicializa a interface"""
        sg.theme('DarkBlue3')
        self.resultados = None
        self.window = None
        self.config_base = None
    
    def criar_layout(self):
        """Cria o layout da interface com todas as funcionalidades"""
        
        # Coluna 1: PARAMETROS BASICOS
        col_parametros_basicos = [
            [sg.Text('Configuracao Basica', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Text('Numero de medicos:', size=(22, 1)), 
             sg.Spin([i for i in range(1, 21)], initial_value=3, key='-MEDICOS-', size=(8, 1))],
            [sg.Text('Taxa de chegada (doentes/h):', size=(22, 1)), 
             sg.Spin([i for i in range(5, 51)], initial_value=15, key='-TAXA-', size=(8, 1))],
            [sg.Text('Tempo medio consulta (min):', size=(22, 1)), 
             sg.Spin([i for i in range(5, 61)], initial_value=15, key='-TEMPO_CONSULTA-', size=(8, 1))],
            [sg.Text('Tempo de simulacao (min):', size=(22, 1)), 
             sg.Spin([i for i in range(60, 1441, 60)], initial_value=480, key='-TEMPO_SIM-', size=(8, 1))],
            [sg.Text('Distribuicao:', size=(22, 1)), 
             sg.Combo(['exponential', 'normal', 'uniform'], default_value='uniform', key='-DIST-', size=(10, 1))],
            [sg.Checkbox('Usar pessoas reais', key='-PESSOAS-', default=False)],
        ]
        
        # Coluna 2: FUNCIONALIDADES AVANCADAS
        col_funcionalidades = [
            [sg.Text('Funcionalidades Avancadas', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Checkbox('Sistema de Triagem (Prioridades)', key='-TRIAGEM-', default=True)],
            [sg.Text('  Tempo max. espera (min):', size=(22, 1)), 
             sg.Spin([i for i in range(30, 181, 10)], initial_value=90, key='-TEMPO_MAX_ESPERA-', size=(8, 1))],
            [sg.Checkbox('Turnos de Medicos (Dia/Noite)', key='-TURNOS-', default=False)],
            [sg.Text('  Duracao turno (min):', size=(22, 1)), 
             sg.Spin([i for i in range(120, 481, 60)], initial_value=240, key='-DURACAO_TURNO-', size=(8, 1))],
            [sg.Checkbox('Pausas para Medicos', key='-PAUSAS-', default=True)],
            [sg.Text('  Duracao pausa (min):', size=(22, 1)), 
             sg.Spin([i for i in range(15, 61, 5)], initial_value=30, key='-DURACAO_PAUSA-', size=(8, 1))],
            [sg.Text('  Intervalo entre pausas (min):', size=(22, 1)), 
             sg.Spin([i for i in range(120, 301, 30)], initial_value=180, key='-INTERVALO_PAUSA-', size=(8, 1))],
            [sg.Checkbox('Chegadas Nao Homogeneas', key='-NAO_HOMOGENEAS-', default=True)],
        ]
        
        # Coluna 3: MODO WHAT-IF
        col_whatif = [
            [sg.Text('Modo What-If', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Button('E se contratar +1 medico?', size=(25, 1), button_color=('white', '#2E86AB'))],
            [sg.Button('E se contratar +2 medicos?', size=(25, 1), button_color=('white', '#2E86AB'))],
            [sg.Button('E se consultas forem +5min?', size=(25, 1), button_color=('white', '#F18F01'))],
            [sg.Button('E se consultas forem -5min?', size=(25, 1), button_color=('white', '#06A77D'))],
            [sg.Button('E se taxa de chegada +50%?', size=(25, 1), button_color=('white', '#D62828'))],
            [sg.Button('E se taxa de chegada -50%?', size=(25, 1), button_color=('white', '#06A77D'))],
            [sg.Button('Comparar Cenarios', size=(25, 2), button_color=('white', '#A23B72'))],
        ]
        
        # Area de resultados
        col_resultados = [
            [sg.Text('Resultados da Simulacao', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Multiline(size=(70, 25), key='-OUTPUT-', disabled=True, autoscroll=True, 
                         font=('Courier', 9))],
            [sg.ProgressBar(100, orientation='h', size=(60, 20), key='-PROGRESSO-', 
                           bar_color=('#06A77D', '#E0E0E0'))],
        ]
        
        # Botoes de controle e graficos
        col_controle = [
            [sg.Text('Controles', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Button('Executar Simulacao', size=(20, 2), 
                      button_color=('white', '#06A77D'), font=('Arial', 10, 'bold'))],
            [sg.Button('Analise Comparativa', size=(20, 1), button_color=('white', '#F18F01'))],
            [sg.HorizontalSeparator()],
            [sg.Text('Graficos Basicos', font=('Arial', 11, 'bold'))],
            [sg.Button('Evolucao da Fila', size=(20, 1))],
            [sg.Button('Ocupacao dos Medicos', size=(20, 1))],
            [sg.Button('Tempos de Espera', size=(20, 1))],
            [sg.Button('Estatisticas Medicos', size=(20, 1))],
            [sg.HorizontalSeparator()],
            [sg.Text('Graficos Avancados', font=('Arial', 11, 'bold'))],
            [sg.Button('Taxa Abandono vs Chegada', size=(20, 1), button_color=('white', '#D62828'))],
            [sg.Button('Espera por Prioridade', size=(20, 1), button_color=('white', '#F18F01'))],
            [sg.Button('% Urgentes Atendidos', size=(20, 1), button_color=('white', '#2E86AB'))],
            [sg.Button('Visualizacao da Clinica', size=(20, 1), button_color=('white', '#A23B72'))],
            [sg.HorizontalSeparator()],
            [sg.Button('Todos os Graficos', size=(20, 1), button_color=('white', '#06A77D'))],
            [sg.Button('Sair', size=(20, 2), button_color=('white', '#D62828'))],
        ]
        
        # Layout principal
        layout = [
            [sg.Text('SIMULACAO DE CLINICA MEDICA - VERSAO PREMIUM', 
                    font=('Arial', 20, 'bold'), justification='center', expand_x=True, 
                    text_color='#06A77D')],
            [sg.Text('Sistema Avancado com Triagem, Turnos, Pausas e Analise What-If', 
                    font=('Arial', 11), justification='center', expand_x=True)],
            [sg.HorizontalSeparator()],
            [
                sg.Column(col_parametros_basicos, vertical_alignment='top'),
                sg.VerticalSeparator(),
                sg.Column(col_funcionalidades, vertical_alignment='top'),
                sg.VerticalSeparator(),
                sg.Column(col_whatif, vertical_alignment='top'),
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Column(col_resultados, vertical_alignment='top'),
                sg.VerticalSeparator(),
                sg.Column(col_controle, vertical_alignment='top'),
            ]
        ]
        
        return layout
    
    def obter_config(self, values):
        """Obtem configuracao dos campos da interface"""
        config = {
            'num_medicos': int(values['-MEDICOS-']),
            'taxa_chegada': float(values['-TAXA-']) / 60.0,
            'tempo_medio_consulta': int(values['-TEMPO_CONSULTA-']),
            'tempo_simulacao': int(values['-TEMPO_SIM-']),
            'distribuicao': values['-DIST-'],
            'usar_pessoas_reais': values['-PESSOAS-'],
            'usar_triagem': values['-TRIAGEM-'],
            'tempo_max_espera': int(values['-TEMPO_MAX_ESPERA-']),
            'usar_turnos': values['-TURNOS-'],
            'duracao_turno': int(values['-DURACAO_TURNO-']),
            'usar_pausas': values['-PAUSAS-'],
            'duracao_pausa': int(values['-DURACAO_PAUSA-']),
            'intervalo_pausa': int(values['-INTERVALO_PAUSA-']),
            'chegadas_nao_homogeneas': values['-NAO_HOMOGENEAS-']
        }
        return config
    
    def atualizar_output(self, texto):
        """Atualiza o campo de output"""
        if self.window:
            self.window['-OUTPUT-'].update(texto)
    
    def adicionar_output(self, texto):
        """Adiciona texto ao output sem apagar"""
        if self.window:
            atual = self.window['-OUTPUT-'].get()
            self.window['-OUTPUT-'].update(atual + texto)
    
    def atualizar_progresso(self, valor):
        """Atualiza a barra de progresso"""
        if self.window:
            self.window['-PROGRESSO-'].update(valor)
    
    def executar_simulacao(self, values):
        """Executa uma simulacao com os parametros configurados"""
        self.atualizar_output("Iniciando simulacao...\n\n")
        self.atualizar_progresso(0)
        
        config = self.obter_config(values)
        self.config_base = config.copy()
        
        self.adicionar_output("CONFIGURACAO:\n")
        self.adicionar_output(f"  Medicos: {config['num_medicos']}\n")
        self.adicionar_output(f"  Taxa chegada: {config['taxa_chegada']*60:.1f} doentes/hora\n")
        self.adicionar_output(f"  Tempo consulta: {config['tempo_medio_consulta']} min\n")
        self.adicionar_output(f"  Distribuicao: {config['distribuicao']}\n")
        self.adicionar_output(f"  Triagem: {'Sim' if config['usar_triagem'] else 'Nao'}\n")
        self.adicionar_output(f"  Turnos: {'Sim' if config['usar_turnos'] else 'Nao'}\n")
        self.adicionar_output(f"  Pausas: {'Sim' if config['usar_pausas'] else 'Nao'}\n")
        self.adicionar_output(f"  Chegadas nao homogeneas: {'Sim' if config['chegadas_nao_homogeneas'] else 'Nao'}\n")
        self.adicionar_output("\n")
        
        def callback_progresso(p):
            self.atualizar_progresso(p)
            self.window.refresh()
        
        sim = Simulacao(config)
        self.resultados = sim.simular(callback_progresso=callback_progresso)
        
        analisador = AnalisadorResultados(self.resultados)
        relatorio = analisador.gerar_relatorio_texto()
        self.adicionar_output(relatorio)
        self.atualizar_progresso(100)
    
    def executar_whatif(self, tipo, values):
        """Executa cenario What-If"""
        if not self.config_base:
            sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            return
        
        config = self.config_base.copy()
        
        if tipo == 'medico+1':
            config['num_medicos'] += 1
            titulo = f"WHAT-IF: +1 Medico ({config['num_medicos']} medicos)"
        elif tipo == 'medico+2':
            config['num_medicos'] += 2
            titulo = f"WHAT-IF: +2 Medicos ({config['num_medicos']} medicos)"
        elif tipo == 'consulta+5':
            config['tempo_medio_consulta'] += 5
            titulo = f"WHAT-IF: Consultas +5min ({config['tempo_medio_consulta']}min)"
        elif tipo == 'consulta-5':
            config['tempo_medio_consulta'] = max(5, config['tempo_medio_consulta'] - 5)
            titulo = f"WHAT-IF: Consultas -5min ({config['tempo_medio_consulta']}min)"
        elif tipo == 'taxa+50':
            config['taxa_chegada'] *= 1.5
            titulo = f"WHAT-IF: Taxa +50% ({config['taxa_chegada']*60:.1f} doentes/h)"
        elif tipo == 'taxa-50':
            config['taxa_chegada'] *= 0.5
            titulo = f"WHAT-IF: Taxa -50% ({config['taxa_chegada']*60:.1f} doentes/h)"
        
        self.atualizar_output(f"\n{'='*60}\n{titulo}\n{'='*60}\n\n")
        
        def callback_progresso(p):
            self.atualizar_progresso(p)
            self.window.refresh()
        
        sim = Simulacao(config)
        resultados = sim.simular(callback_progresso=callback_progresso)
        
        analisador = AnalisadorResultados(resultados)
        relatorio = analisador.gerar_relatorio_texto()
        self.adicionar_output(relatorio)
    
    def executar(self):
        """Executa o loop principal da interface"""
        layout = self.criar_layout()
        self.window = sg.Window('Simulacao de Clinica Medica - Versao Premium', 
                               layout, finalize=True, resizable=True, size=(1400, 900))
        
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED or event == 'Sair':
                break
            
            elif event == 'Executar Simulacao':
                self.executar_simulacao(values)
            
            elif event == 'E se contratar +1 medico?':
                self.executar_whatif('medico+1', values)
            
            elif event == 'E se contratar +2 medicos?':
                self.executar_whatif('medico+2', values)
            
            elif event == 'E se consultas forem +5min?':
                self.executar_whatif('consulta+5', values)
            
            elif event == 'E se consultas forem -5min?':
                self.executar_whatif('consulta-5', values)
            
            elif event == 'E se taxa de chegada +50%?':
                self.executar_whatif('taxa+50', values)
            
            elif event == 'E se taxa de chegada -50%?':
                self.executar_whatif('taxa-50', values)
            
            elif event == 'Evolucao da Fila':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_evolucao_fila()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Ocupacao dos Medicos':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_ocupacao_medicos()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Tempos de Espera':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_distribuicao_tempos_espera()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Estatisticas Medicos':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_estatisticas_medicos()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Taxa Abandono vs Chegada':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_taxa_abandono()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Espera por Prioridade':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_espera_por_prioridade()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == '% Urgentes Atendidos':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_percentagem_urgentes()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Visualizacao da Clinica':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_visualizacao_clinica()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
            
            elif event == 'Todos os Graficos':
                if self.resultados:
                    analisador = AnalisadorResultados(self.resultados)
                    analisador.plot_todos_graficos()
                else:
                    sg.popup('Execute uma simulacao primeiro!', title='Aviso')
        
        self.window.close()