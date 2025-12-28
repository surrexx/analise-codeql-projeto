# -------
# - Módulo de simulação da Clínica Médica - VERSÃO AVANÇADA
# - Simulação de eventos discretos com funcionalidades avançadas
# - Projeto de Algoritmos e Técnicas de Programação
# - Universidade do Minho - Engenharia Biomédica
# - 2025-11-19 by Letícia, Maria, Matilde
# -------

import numpy as np
import json
from typing import Dict, List, Tuple, Optional

# Constantes para prioridades (Triagem)
PRIORIDADE_VERMELHO = 1  # Emergência
PRIORIDADE_LARANJA = 2   # Muito urgente
PRIORIDADE_AMARELO = 3   # Urgente
PRIORIDADE_VERDE = 4     # Pouco urgente
PRIORIDADE_AZUL = 5      # Não urgente

NOMES_PRIORIDADE = {
    1: "Vermelho (Emergência)",
    2: "Laranja (Muito Urgente)",
    3: "Amarelo (Urgente)",
    4: "Verde (Pouco Urgente)",
    5: "Azul (Não Urgente)"
}

class Simulacao:
    """Classe principal para a simulação da clínica médica com funcionalidades avançadas"""
    
    def __init__(self, config: Dict):
        """
        Inicializa a simulação com os parâmetros configurados
        
        Args:
            config: Dicionário com parâmetros da simulação
        """
        self.num_medicos = config.get('num_medicos', 3)
        self.taxa_chegada = config.get('taxa_chegada', 10 / 60.0)
        self.tempo_medio_consulta = config.get('tempo_medio_consulta', 15)
        self.tempo_simulacao = config.get('tempo_simulacao', 480)
        self.distribuicao = config.get('distribuicao', 'exponential')
        self.usar_pessoas_reais = config.get('usar_pessoas_reais', False)
        
        # NOVAS FUNCIONALIDADES
        self.usar_triagem = config.get('usar_triagem', False)
        self.tempo_max_espera = config.get('tempo_max_espera', 120)  # Tempo para abandonar (min)
        self.usar_turnos = config.get('usar_turnos', False)
        self.duracao_turno = config.get('duracao_turno', 240)  # 4 horas por turno
        self.usar_pausas = config.get('usar_pausas', False)
        self.duracao_pausa = config.get('duracao_pausa', 30)  # 30 min de pausa
        self.intervalo_pausa = config.get('intervalo_pausa', 180)  # Pausa a cada 3h
        self.chegadas_nao_homogeneas = config.get('chegadas_nao_homogeneas', False)
        
        # Carregar dados de pessoas
        self.pessoas = []
        if self.usar_pessoas_reais:
            self.carregar_pessoas()
        
        # Estruturas de dados para resultados
        self.resultados = {
            'doentes_atendidos': 0,
            'doentes_abandonaram': 0,
            'tempo_total_espera': 0.0,
            'tempo_total_consulta': 0.0,
            'tempo_total_clinica': 0.0,
            'max_fila': 0,
            'historico_fila': [],
            'historico_ocupacao': [],
            'tempos_espera_individuais': [],
            'tempos_consulta_individuais': [],
            'tempos_clinica_individuais': [],
            'medicos_stats': {},
            # Estatísticas de triagem
            'atendidos_por_prioridade': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'abandonos_por_prioridade': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'espera_por_prioridade': {1: [], 2: [], 3: [], 4: [], 5: []},
            'taxa_abandono_vs_taxa_chegada': []
        }
        
    def carregar_pessoas(self):
        """Carrega o dataset de pessoas do ficheiro JSON"""
        ficheiro = open('pessoas.json', 'r', encoding='utf-8')
        conteudo = ficheiro.read()
        ficheiro.close()
        
        if conteudo:
            self.pessoas = json.loads(conteudo)
        else:
            print("Aviso: ficheiro pessoas.json vazio. Usando IDs genéricos.")
            self.usar_pessoas_reais = False
    
    def gera_prioridade(self) -> int:
        """Gera prioridade aleatória com distribuição realista"""
        # Distribuição realista de urgências
        prob = np.random.random()
        if prob < 0.05:  # 5% emergências
            return PRIORIDADE_VERMELHO
        elif prob < 0.15:  # 10% muito urgente
            return PRIORIDADE_LARANJA
        elif prob < 0.35:  # 20% urgente
            return PRIORIDADE_AMARELO
        elif prob < 0.70:  # 35% pouco urgente
            return PRIORIDADE_VERDE
        else:  # 30% não urgente
            return PRIORIDADE_AZUL
    
    def gera_intervalo_chegada(self, tempo_atual: float) -> float:
        """Gera intervalo entre chegadas (pode ser não homogênea)"""
        if self.chegadas_nao_homogeneas:
            # Taxa varia ao longo do dia
            hora_do_dia = (tempo_atual % 1440) / 60  # Converter para horas (0-24)
            
            # Picos: 9h-11h e 14h-17h
            if 9 <= hora_do_dia < 11 or 14 <= hora_do_dia < 17:
                taxa = self.taxa_chegada * 1.5  # 50% mais doentes
            elif 12 <= hora_do_dia < 14 or 20 <= hora_do_dia < 24:
                taxa = self.taxa_chegada * 0.5  # 50% menos doentes
            else:
                taxa = self.taxa_chegada
            
            return np.random.exponential(1 / taxa)
        else:
            return np.random.exponential(1 / self.taxa_chegada)
    
    def gera_tempo_consulta(self, prioridade: int = None) -> float:
        """Gera tempo de consulta (urgências tendem a ser mais rápidas)"""
        tempo_base = self.tempo_medio_consulta
        
        # Urgências são mais rápidas
        if prioridade and prioridade <= 2:
            tempo_base = tempo_base * 0.7
        
        if self.distribuicao == "exponential":
            return np.random.exponential(tempo_base)
        elif self.distribuicao == "normal":
            return max(5, np.random.normal(tempo_base, tempo_base * 0.3))
        elif self.distribuicao == "uniform":
            # Valores mais realistas: min=5min, max=30min
            return np.random.uniform(max(5, tempo_base * 0.4), tempo_base * 1.6)
        else:
            return tempo_base
    
    def procura_medico_livre(self, medicos: List, tempo_atual: float) -> Optional[Dict]:
        """Procura médico disponível (considerando turnos e pausas)"""
        medico_encontrado = None
        i = 0
        
        while i < len(medicos) and medico_encontrado is None:
            medico = medicos[i]
            
            # Verificar se médico está no turno correto
            if self.usar_turnos:
                turno_atual = int(tempo_atual / self.duracao_turno) % 2
                turno_medico = i % 2  # Médicos pares turno 0, ímpares turno 1
                if turno_atual != turno_medico:
                    i += 1
                    continue  # Médico não está de turno
            
            # Verificar se está em pausa
            if medico.get('em_pausa', False):
                if tempo_atual >= medico.get('fim_pausa', 0):
                    medico['em_pausa'] = False
                else:
                    i += 1
                    continue  # Ainda em pausa
            
            # Verificar se precisa de pausa
            if self.usar_pausas and not medico['ocupado']:
                tempo_trabalho = tempo_atual - medico.get('ultimo_inicio_pausa', 0)
                if tempo_trabalho >= self.intervalo_pausa:
                    medico['em_pausa'] = True
                    medico['fim_pausa'] = tempo_atual + self.duracao_pausa
                    medico['ultimo_inicio_pausa'] = tempo_atual
                    i += 1
                    continue
            
            # Médico disponível
            if not medico['ocupado']:
                medico_encontrado = medico
            
            i += 1
        
        return medico_encontrado
    
    def inserir_na_fila_por_prioridade(self, fila: List, doente_info: Dict):
        """Insere doente na fila mantendo ordem de prioridade"""
        if not self.usar_triagem:
            fila.append(doente_info)
            return
        
        # Inserir mantendo ordem de prioridade
        prioridade_nova = doente_info['prioridade']
        i = 0
        inserido = False
        
        while i < len(fila) and not inserido:
            if fila[i]['prioridade'] > prioridade_nova:
                fila.insert(i, doente_info)
                inserido = True
            i += 1
        
        if not inserido:
            fila.append(doente_info)
    
    def simular(self, callback_progresso=None) -> Dict:
        """
        Executa a simulação completa com todas as funcionalidades
        
        Args:
            callback_progresso: Função para reportar progresso
            
        Returns:
            Dicionário com todos os resultados
        """
        tempo_atual = 0.0
        contador_doentes = 0
        queue_eventos = []
        fila_espera = []
        
        # Inicializar médicos
        medicos = []
        for i in range(self.num_medicos):
            medicos.append({
                'id': f'm{i}',
                'ocupado': False,
                'doente_atual': None,
                'tempo_ocupado': 0.0,
                'inicio_consulta': 0.0,
                'doentes_atendidos': 0,
                'em_pausa': False,
                'fim_pausa': 0.0,
                'ultimo_inicio_pausa': 0.0
            })
            self.resultados['medicos_stats'][f'm{i}'] = {
                'tempo_ocupado': 0.0,
                'doentes_atendidos': 0,
                'ocupacao_percentual': 0.0,
                'turno': 'Dia' if i % 2 == 0 else 'Noite'
            }
        
        # Dicionário de informações dos doentes
        info_doentes = {}
        
        # Gerar chegadas de doentes
        tempo_chegada = self.gera_intervalo_chegada(0)
        while tempo_chegada < self.tempo_simulacao:
            if self.usar_pessoas_reais and self.pessoas:
                pessoa = self.pessoas[contador_doentes % len(self.pessoas)]
                doente_id = pessoa['id']
                info_doentes[doente_id] = pessoa.copy()
            else:
                doente_id = f'd{contador_doentes}'
                info_doentes[doente_id] = {'id': doente_id}
            
            # Atribuir prioridade
            if self.usar_triagem:
                info_doentes[doente_id]['prioridade'] = self.gera_prioridade()
            else:
                info_doentes[doente_id]['prioridade'] = PRIORIDADE_VERDE
            
            contador_doentes += 1
            queue_eventos.append((tempo_chegada, 'CHEGADA', doente_id))
            tempo_chegada += self.gera_intervalo_chegada(tempo_chegada)
        
        # Ordenar eventos
        queue_eventos.sort(key=lambda x: x[0])
        
        total_eventos = len(queue_eventos)
        eventos_processados = 0
        
        # Processar eventos
        while queue_eventos:
            evento = queue_eventos.pop(0)
            tempo_atual, tipo_evento, doente_id = evento
            eventos_processados += 1
            
            if callback_progresso and eventos_processados % 10 == 0:
                progresso = int((eventos_processados / max(total_eventos, 1)) * 100)
                callback_progresso(progresso)
            
            # Verificar abandonos
            fila_atualizada = []
            for doente_info in fila_espera:
                tempo_espera = tempo_atual - doente_info['tempo_chegada']
                if tempo_espera > self.tempo_max_espera:
                    # Doente abandona
                    self.resultados['doentes_abandonaram'] += 1
                    prioridade = doente_info['prioridade']
                    self.resultados['abandonos_por_prioridade'][prioridade] += 1
                else:
                    fila_atualizada.append(doente_info)
            fila_espera = fila_atualizada
            
            # Registrar histórico
            self.resultados['historico_fila'].append((tempo_atual, len(fila_espera)))
            medicos_ocupados = sum(1 for m in medicos if m['ocupado'])
            ocupacao = (medicos_ocupados / self.num_medicos) * 100
            self.resultados['historico_ocupacao'].append((tempo_atual, ocupacao))
            
            if tipo_evento == 'CHEGADA':
                info_doentes[doente_id]['tempo_chegada'] = tempo_atual
                medico_livre = self.procura_medico_livre(medicos, tempo_atual)
                
                if medico_livre:
                    # Atendimento imediato
                    medico_livre['ocupado'] = True
                    medico_livre['doente_atual'] = doente_id
                    medico_livre['inicio_consulta'] = tempo_atual
                    
                    prioridade = info_doentes[doente_id]['prioridade']
                    tempo_consulta = self.gera_tempo_consulta(prioridade)
                    
                    info_doentes[doente_id]['tempo_espera'] = 0.0
                    info_doentes[doente_id]['tempo_inicio_consulta'] = tempo_atual
                    info_doentes[doente_id]['tempo_consulta'] = tempo_consulta
                    
                    queue_eventos.append((tempo_atual + tempo_consulta, 'SAIDA', doente_id))
                    queue_eventos.sort(key=lambda x: x[0])
                else:
                    # Entra na fila por prioridade
                    doente_info = {
                        'id': doente_id,
                        'tempo_chegada': tempo_atual,
                        'prioridade': info_doentes[doente_id]['prioridade']
                    }
                    self.inserir_na_fila_por_prioridade(fila_espera, doente_info)
                    self.resultados['max_fila'] = max(self.resultados['max_fila'], len(fila_espera))
            
            elif tipo_evento == 'SAIDA':
                # Encontrar médico
                medico = None
                i = 0
                while i < len(medicos) and medico is None:
                    if medicos[i]['doente_atual'] == doente_id:
                        medico = medicos[i]
                    i += 1
                
                if medico:
                    tempo_consulta_real = tempo_atual - medico['inicio_consulta']
                    medico['tempo_ocupado'] += tempo_consulta_real
                    medico['doentes_atendidos'] += 1
                    medico['ocupado'] = False
                    medico['doente_atual'] = None
                    
                    # Registrar estatísticas
                    tempo_chegada = info_doentes[doente_id]['tempo_chegada']
                    tempo_espera = info_doentes[doente_id].get('tempo_espera', 0.0)
                    tempo_consulta = info_doentes[doente_id]['tempo_consulta']
                    tempo_total = tempo_atual - tempo_chegada
                    prioridade = info_doentes[doente_id]['prioridade']
                    
                    self.resultados['doentes_atendidos'] += 1
                    self.resultados['tempo_total_espera'] += tempo_espera
                    self.resultados['tempo_total_consulta'] += tempo_consulta
                    self.resultados['tempo_total_clinica'] += tempo_total
                    
                    self.resultados['tempos_espera_individuais'].append(tempo_espera)
                    self.resultados['tempos_consulta_individuais'].append(tempo_consulta)
                    self.resultados['tempos_clinica_individuais'].append(tempo_total)
                    
                    self.resultados['atendidos_por_prioridade'][prioridade] += 1
                    self.resultados['espera_por_prioridade'][prioridade].append(tempo_espera)
                    
                    # Atender próximo da fila
                    if fila_espera:
                        proximo_info = fila_espera.pop(0)
                        proximo_doente = proximo_info['id']
                        
                        medico['ocupado'] = True
                        medico['doente_atual'] = proximo_doente
                        medico['inicio_consulta'] = tempo_atual
                        
                        prioridade_prox = info_doentes[proximo_doente]['prioridade']
                        tempo_consulta = self.gera_tempo_consulta(prioridade_prox)
                        tempo_espera = tempo_atual - info_doentes[proximo_doente]['tempo_chegada']
                        
                        info_doentes[proximo_doente]['tempo_espera'] = tempo_espera
                        info_doentes[proximo_doente]['tempo_inicio_consulta'] = tempo_atual
                        info_doentes[proximo_doente]['tempo_consulta'] = tempo_consulta
                        
                        queue_eventos.append((tempo_atual + tempo_consulta, 'SAIDA', proximo_doente))
                        queue_eventos.sort(key=lambda x: x[0])
        
        self._calcular_estatisticas_finais(medicos)
        
        if callback_progresso:
            callback_progresso(100)
        
        return self.resultados
    
    def _calcular_estatisticas_finais(self, medicos: List):
        """Calcula estatísticas finais"""
        n = self.resultados['doentes_atendidos']
        
        if n > 0:
            self.resultados['tempo_medio_espera'] = self.resultados['tempo_total_espera'] / n
            self.resultados['tempo_medio_consulta'] = self.resultados['tempo_total_consulta'] / n
            self.resultados['tempo_medio_clinica'] = self.resultados['tempo_total_clinica'] / n
        else:
            self.resultados['tempo_medio_espera'] = 0.0
            self.resultados['tempo_medio_consulta'] = 0.0
            self.resultados['tempo_medio_clinica'] = 0.0
        
        # Taxa de abandono
        total_doentes = n + self.resultados['doentes_abandonaram']
        if total_doentes > 0:
            self.resultados['taxa_abandono'] = (self.resultados['doentes_abandonaram'] / total_doentes) * 100
        else:
            self.resultados['taxa_abandono'] = 0.0
        
        # Estatísticas da fila
        if self.resultados['historico_fila']:
            tamanhos = [tam for _, tam in self.resultados['historico_fila']]
            self.resultados['tamanho_medio_fila'] = np.mean(tamanhos)
        else:
            self.resultados['tamanho_medio_fila'] = 0.0
        
        # Estatísticas dos médicos
        for medico in medicos:
            tempo_ocupado_real = min(medico['tempo_ocupado'], self.tempo_simulacao)
            ocupacao_percentual = (tempo_ocupado_real / self.tempo_simulacao) * 100
            
            self.resultados['medicos_stats'][medico['id']]['tempo_ocupado'] = tempo_ocupado_real
            self.resultados['medicos_stats'][medico['id']]['doentes_atendidos'] = medico['doentes_atendidos']
            self.resultados['medicos_stats'][medico['id']]['ocupacao_percentual'] = min(ocupacao_percentual, 100.0)
        
        # Ocupação média
        ocupacoes = [stats['ocupacao_percentual'] for stats in self.resultados['medicos_stats'].values()]
        self.resultados['ocupacao_media_medicos'] = np.mean(ocupacoes) if ocupacoes else 0.0
        
        # Tempos médios por prioridade
        self.resultados['tempo_medio_por_prioridade'] = {}
        for prioridade in range(1, 6):
            tempos = self.resultados['espera_por_prioridade'][prioridade]
            if tempos:
                self.resultados['tempo_medio_por_prioridade'][prioridade] = np.mean(tempos)
            else:
                self.resultados['tempo_medio_por_prioridade'][prioridade] = 0.0