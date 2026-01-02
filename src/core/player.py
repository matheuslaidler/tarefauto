# ============================================================================
# TarefAuto - Módulo de Reprodução (player.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este módulo é responsável por "reproduzir" as ações que foram gravadas.
# Quando você grava uma sequência de cliques e movimentos do mouse, este
# código consegue executar tudo de novo automaticamente!
#
# Funciona como o "play" de um videocassete: ele lê as ações gravadas e
# faz o computador executar cada uma no tempo certo.
#
# Você pode configurar para repetir as ações várias vezes (loop), por um
# tempo determinado, ou infinitamente até você mandar parar.
#
# EXPLICAÇÃO TÉCNICA:
# Utiliza pynput.mouse.Controller e pynput.keyboard.Controller para
# simular eventos de entrada. Os eventos são reproduzidos respeitando
# os timestamps originais (delta entre eventos). Suporta diferentes
# modos de loop e possui mecanismo de parada de emergência thread-safe.
#
# ============================================================================

"""
Módulo de reprodução de eventos para o TarefAuto.

Este módulo contém a classe Player, responsável por reproduzir eventos
de mouse e teclado previamente gravados em uma RecordingSession.

Classes:
    LoopMode: Enumeração dos modos de repetição disponíveis
    Player: Gerencia a reprodução de eventos gravados

Dependencies:
    - pynput: Para simulação de eventos de mouse e teclado
    - threading: Para execução assíncrona da reprodução
    - time: Para controle de timing entre eventos

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# threading: Para executar a reprodução em uma thread separada
# Isso permite que a interface continue funcionando durante a reprodução
import threading

# time: Para controlar o tempo entre eventos e medir duração
import time

# Enum: Para criar enumeração de modos de loop
from enum import Enum, auto

# typing: Anotações de tipo
from typing import Optional, Callable, List

# pynput: Controladores para simular mouse e teclado
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode

# Importações internas
from src.core.events import InputEvent, EventType, RecordingSession


# ============================================================================
# ENUMERAÇÃO DE MODOS DE LOOP
# ============================================================================

class LoopMode(Enum):
    """
    Modos de repetição disponíveis para reprodução.
    
    EXPLICAÇÃO PARA INICIANTES:
    Quando você reproduz uma gravação, pode querer que ela:
    - Execute uma vez e pare (SINGLE)
    - Repita um número específico de vezes, como 5x (COUNT)
    - Repita por um tempo específico, como 10 minutos (DURATION)
    - Repita para sempre até você mandar parar (INFINITE)
    
    Esta enumeração define essas opções.
    
    EXPLICAÇÃO TÉCNICA:
    Enum que define os modos de loop suportados pelo Player.
    Usado em conjunto com loop_value para controlar a reprodução.
    
    Attributes:
        SINGLE: Executa apenas uma vez
        COUNT: Repete N vezes (loop_value = número de repetições)
        DURATION: Repete por N segundos (loop_value = duração em segundos)
        INFINITE: Repete indefinidamente até stop() ser chamado
    """
    SINGLE = auto()     # Executa uma única vez
    COUNT = auto()      # Executa N vezes
    DURATION = auto()   # Executa por N segundos
    INFINITE = auto()   # Executa infinitamente


# ============================================================================
# CLASSE PLAYER (REPRODUTOR)
# ============================================================================

class Player:
    """
    Classe responsável por reproduzir eventos gravados.
    
    EXPLICAÇÃO PARA INICIANTES:
    O Player é como um "robô" que executa as ações que você gravou antes.
    Ele move o mouse, clica nos botões e pressiona teclas exatamente como
    você fez durante a gravação.
    
    Você pode configurar:
    - Quantas vezes repetir (1x, 5x, 10x, infinito...)
    - Por quanto tempo ficar repetindo (30 segundos, 1 hora...)
    - Qual tecla usar para parar de emergência
    
    A reprodução roda em uma "thread" separada, então a interface do
    programa continua funcionando (você pode clicar no botão de parar).
    
    EXPLICAÇÃO TÉCNICA:
    O Player utiliza Controllers do pynput para simular eventos.
    A reprodução ocorre em uma thread separada para não bloquear a UI.
    
    Implementa parada de emergência via flag thread-safe (_stop_flag).
    Os eventos são reproduzidos respeitando os deltas de tempo originais.
    
    Attributes:
        is_playing (bool): Se está reproduzindo no momento
        loop_mode (LoopMode): Modo de repetição atual
        loop_value (float): Valor associado ao modo (contagem ou duração)
        speed_multiplier (float): Multiplicador de velocidade (1.0 = normal)
        _session (RecordingSession): Sessão sendo reproduzida
        _mouse_controller (Controller): Controlador de mouse do pynput
        _keyboard_controller (Controller): Controlador de teclado do pynput
        _playback_thread (Thread): Thread de reprodução
        _stop_flag (Event): Flag para parada de emergência
        _on_progress_callback (Callable): Callback para atualizar progresso
        _on_complete_callback (Callable): Callback quando reprodução termina
    
    Example:
        >>> player = Player()
        >>> player.set_loop_mode(LoopMode.COUNT, 3)  # Repetir 3 vezes
        >>> player.play(session)
        >>> # ... ações são reproduzidas ...
        >>> player.stop()  # Para imediatamente se necessário
    """
    
    def __init__(
        self,
        on_progress_callback: Optional[Callable[[int, int, int], None]] = None,
        on_complete_callback: Optional[Callable[[], None]] = None
    ):
        """
        Inicializa o reprodutor de eventos.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método prepara o Player para uso. Ele cria os "controladores"
        de mouse e teclado que serão usados para simular suas ações.
        
        Os callbacks são funções opcionais que você pode passar para ser
        notificado sobre o progresso da reprodução:
        - on_progress_callback: chamado durante a reprodução para mostrar progresso
        - on_complete_callback: chamado quando a reprodução termina
        
        EXPLICAÇÃO TÉCNICA:
        Construtor que inicializa os controllers do pynput e atributos
        de estado. Os callbacks permitem integração com a UI para feedback
        em tempo real.
        
        Args:
            on_progress_callback: Função(current_loop, total_loops, event_index)
                Chamada periodicamente durante a reprodução
            on_complete_callback: Função() chamada quando reprodução termina
        """
        # ====================================================================
        # CONTROLADORES DO PYNPUT
        # ====================================================================
        
        # Controller de mouse - usado para mover cursor, clicar, scroll
        self._mouse_controller = mouse.Controller()
        
        # Controller de teclado - usado para simular teclas
        self._keyboard_controller = keyboard.Controller()
        
        # ====================================================================
        # ESTADO DE REPRODUÇÃO
        # ====================================================================
        
        # Indica se estamos reproduzindo no momento
        self.is_playing = False
        
        # Modo de loop atual (padrão: executar uma vez)
        self.loop_mode = LoopMode.SINGLE
        
        # Valor do loop (número de repetições ou duração em segundos)
        self.loop_value: float = 1
        
        # Multiplicador de velocidade (1.0 = velocidade original)
        # Valores menores = mais lento, maiores = mais rápido
        self.speed_multiplier: float = 1.0
        
        # Sessão sendo reproduzida atualmente
        self._session: Optional[RecordingSession] = None
        
        # ====================================================================
        # CONTROLE DE THREAD
        # ====================================================================
        
        # Thread onde a reprodução será executada
        self._playback_thread: Optional[threading.Thread] = None
        
        # Event para sinalizar parada de emergência
        # threading.Event() é thread-safe e pode ser checado de qualquer thread
        self._stop_flag = threading.Event()
        
        # ====================================================================
        # CALLBACKS
        # ====================================================================
        
        # Função chamada para atualizar progresso
        # Recebe: (loop_atual, total_loops, evento_atual)
        self._on_progress_callback = on_progress_callback
        
        # Função chamada quando a reprodução termina (normal ou forçada)
        self._on_complete_callback = on_complete_callback
        
        # ====================================================================
        # ESTATÍSTICAS
        # ====================================================================
        
        # Contador de loops completados
        self._loops_completed = 0
        
        # Contador de eventos reproduzidos
        self._events_played = 0
        
        # Loop atual (para UI)
        self._current_loop = 0
        
        # Tempo de início da reprodução
        self._start_time: float = 0

    def set_loop_mode(self, mode: LoopMode, value: float = 1) -> None:
        """
        Define o modo de repetição da reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Use este método para configurar quantas vezes a gravação será
        executada:
        
        - SINGLE: Uma vez só
        - COUNT: X vezes (você define o número)
        - DURATION: Por X segundos/minutos (você define o tempo)
        - INFINITE: Para sempre até você parar
        
        Exemplos:
            player.set_loop_mode(LoopMode.COUNT, 5)      # Repete 5 vezes
            player.set_loop_mode(LoopMode.DURATION, 60)  # Repete por 60 segundos
            player.set_loop_mode(LoopMode.INFINITE)      # Repete para sempre
        
        EXPLICAÇÃO TÉCNICA:
        Configura os atributos loop_mode e loop_value que controlam
        o comportamento do loop na thread de reprodução.
        
        Args:
            mode (LoopMode): O modo de repetição desejado
            value (float): Valor associado (contagem ou segundos). Default: 1
        """
        self.loop_mode = mode
        self.loop_value = value

    def set_speed(self, multiplier: float) -> None:
        """
        Define a velocidade de reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Você pode fazer a reprodução ser mais rápida ou mais lenta:
        
        - 1.0 = velocidade normal (como você gravou)
        - 2.0 = 2x mais rápido
        - 0.5 = 2x mais lento
        
        ATENÇÃO: Velocidades muito altas podem causar problemas, pois
        alguns programas não conseguem acompanhar cliques muito rápidos.
        
        EXPLICAÇÃO TÉCNICA:
        O multiplicador é aplicado ao delay entre eventos durante a
        reprodução. Valores < 1 aumentam o delay, > 1 diminuem.
        
        Args:
            multiplier (float): Multiplicador de velocidade (0.1 a 10.0 recomendado)
        """
        # Garante que o multiplicador está em uma faixa razoável
        self.speed_multiplier = max(0.1, min(10.0, multiplier))

    def _execute_event(self, event: InputEvent) -> None:
        """
        Executa um único evento (move mouse, clica, pressiona tecla, etc.).
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função recebe um evento e faz ele acontecer de verdade no
        seu computador. Se o evento for "mover mouse para (100, 200)",
        ela move o mouse para lá. Se for "clicar com botão esquerdo",
        ela clica.
        
        EXPLICAÇÃO TÉCNICA:
        Despacha o evento para o método de execução apropriado baseado
        no EventType. Usa os Controllers do pynput para simular.
        
        Args:
            event (InputEvent): O evento a ser executado
        """
        # Escolhe a ação baseado no tipo de evento
        event_type = event.event_type
        
        if event_type == EventType.MOUSE_MOVE:
            # Move o cursor do mouse para a posição especificada
            self._mouse_controller.position = (event.x, event.y)
        
        elif event_type == EventType.MOUSE_CLICK:
            # Clique de mouse
            # Primeiro, precisamos converter o nome do botão para o enum Button
            button = self._get_mouse_button(event.button)
            
            # Move para a posição do clique (importante!)
            self._mouse_controller.position = (event.x, event.y)
            
            # Executa press ou release dependendo do estado
            if event.pressed:
                self._mouse_controller.press(button)    # Pressiona o botão
            else:
                self._mouse_controller.release(button)  # Solta o botão
        
        elif event_type == EventType.MOUSE_SCROLL:
            # Rolagem do mouse
            # Move para a posição primeiro
            self._mouse_controller.position = (event.x, event.y)
            # Executa o scroll
            self._mouse_controller.scroll(event.dx, event.dy)
        
        elif event_type == EventType.KEY_PRESS:
            # Tecla pressionada
            key = self._get_keyboard_key(event.key)
            self._keyboard_controller.press(key)
        
        elif event_type == EventType.KEY_RELEASE:
            # Tecla solta
            key = self._get_keyboard_key(event.key)
            self._keyboard_controller.release(key)

    def _get_mouse_button(self, button_name: str) -> Button:
        """
        Converte nome de botão para enum Button do pynput.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando salvamos a gravação, guardamos o nome do botão como texto
        ('left', 'right', 'middle'). Mas para clicar, precisamos usar
        o formato que o pynput entende. Esta função faz essa conversão.
        
        EXPLICAÇÃO TÉCNICA:
        Mapeia strings para enum mouse.Button. Usa dicionário para
        lookup O(1) e retorna left como fallback.
        
        Args:
            button_name (str): Nome do botão ('left', 'right', 'middle')
        
        Returns:
            Button: Enum correspondente do pynput
        """
        # Mapa de nomes para enums
        button_map = {
            'left': Button.left,        # Botão esquerdo
            'right': Button.right,      # Botão direito
            'middle': Button.middle,    # Botão do meio (rodinha)
        }
        
        # Retorna o botão correspondente, ou esquerdo como padrão
        return button_map.get(button_name.lower(), Button.left)

    def _get_keyboard_key(self, key_str: str):
        """
        Converte string de tecla para formato do pynput.
        
        EXPLICAÇÃO PARA INICIANTES:
        Similar ao botão do mouse, precisamos converter o nome da tecla
        (que salvamos como texto) de volta para o formato que o pynput
        precisa para pressionar essa tecla.
        
        Teclas especiais como 'space', 'enter', 'ctrl' são convertidas
        para seus códigos especiais. Teclas normais (letras, números)
        são usadas diretamente.
        
        EXPLICAÇÃO TÉCNICA:
        Tenta encontrar a tecla no enum keyboard.Key (teclas especiais).
        Se não encontrar, assume que é um caractere e cria KeyCode.
        
        Args:
            key_str (str): Nome ou caractere da tecla
        
        Returns:
            Key ou KeyCode: Objeto apropriado para o pynput
        """
        # Primeiro, tenta encontrar como tecla especial
        # Teclas especiais: space, enter, tab, shift, ctrl, alt, etc.
        try:
            # Key[key_str] busca a tecla pelo nome no enum
            return Key[key_str]
        except (KeyError, AttributeError):
            pass
        
        # Também tenta com letras minúsculas
        try:
            return Key[key_str.lower()]
        except (KeyError, AttributeError):
            pass
        
        # Se não é tecla especial, é um caractere normal
        # Retorna como KeyCode se for um único caractere
        if len(key_str) == 1:
            return KeyCode.from_char(key_str)
        
        # Último recurso: tenta como KeyCode mesmo assim
        return KeyCode.from_char(key_str[0]) if key_str else Key.space

    def _playback_loop(self) -> None:
        """
        Loop principal de reprodução (executado em thread separada).
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta é a função que realmente faz a "mágica" da reprodução.
        Ela roda em uma thread separada e:
        
        1. Pega cada evento da gravação na ordem
        2. Espera o tempo certo (como na gravação original)
        3. Executa o evento (move mouse, clica, digita)
        4. Repete se configurado para fazer loop
        
        A cada momento, ela verifica se você mandou parar (stop_flag).
        
        EXPLICAÇÃO TÉCNICA:
        Implementa a lógica de reprodução com suporte a diferentes
        modos de loop. Respeita os timestamps originais para timing
        preciso. Verifica stop_flag regularmente para responsividade.
        
        Esta função não deve ser chamada diretamente - use play().
        """
        # Verifica se há eventos para reproduzir
        if not self._session or not self._session.events:
            print("Nenhum evento para reproduzir!")
            self.is_playing = False
            if self._on_complete_callback:
                self._on_complete_callback()
            return
        
        # Lista de eventos a reproduzir
        events = self._session.events
        
        # ====================================================================
        # CONFIGURAÇÃO DO LOOP
        # ====================================================================
        
        # Determina quantos loops fazer baseado no modo
        max_loops = float('inf')  # Padrão: infinito
        
        if self.loop_mode == LoopMode.SINGLE:
            max_loops = 1
        elif self.loop_mode == LoopMode.COUNT:
            max_loops = int(self.loop_value)
        elif self.loop_mode == LoopMode.DURATION:
            # Para DURATION, usamos um timer em vez de contador de loops
            max_loops = float('inf')
        elif self.loop_mode == LoopMode.INFINITE:
            max_loops = float('inf')
        
        # Timestamp de início (para modo DURATION e get_elapsed_time)
        start_time = time.time()
        self._start_time = start_time
        
        # Contadores
        self._loops_completed = 0
        self._events_played = 0
        self._current_loop = 1
        
        # ====================================================================
        # LOOP DE REPRODUÇÃO
        # ====================================================================
        
        current_loop = 0  # Contador de loops atual
        
        while current_loop < max_loops:
            # Atualiza loop atual para UI
            self._current_loop = current_loop + 1
            
            # Verifica se devemos parar (flag de emergência)
            if self._stop_flag.is_set():
                break
            
            # Verifica tempo para modo DURATION
            if self.loop_mode == LoopMode.DURATION:
                elapsed = time.time() - start_time
                if elapsed >= self.loop_value:
                    break
            
            # ================================================================
            # REPRODUZ TODOS OS EVENTOS DA GRAVAÇÃO
            # ================================================================
            
            # Timestamp do evento anterior (para calcular delay)
            prev_timestamp = 0.0
            
            for i, event in enumerate(events):
                # Verifica stop flag antes de cada evento
                if self._stop_flag.is_set():
                    break
                
                # Verifica tempo para modo DURATION
                if self.loop_mode == LoopMode.DURATION:
                    elapsed = time.time() - start_time
                    if elapsed >= self.loop_value:
                        break
                
                # Calcula o delay até este evento
                # É a diferença de tempo entre este evento e o anterior
                delay = event.timestamp - prev_timestamp
                
                # Aplica o multiplicador de velocidade
                # Dividimos porque queremos: velocidade maior = delay menor
                if self.speed_multiplier > 0:
                    delay = delay / self.speed_multiplier
                
                # Espera o tempo necessário
                # Usamos um loop com pequenos sleeps para checar stop_flag
                if delay > 0:
                    sleep_start = time.time()
                    while time.time() - sleep_start < delay:
                        # Verifica stop_flag a cada 10ms
                        if self._stop_flag.is_set():
                            break
                        # Dorme no máximo 10ms por vez
                        remaining = delay - (time.time() - sleep_start)
                        time.sleep(min(0.01, max(0, remaining)))
                    
                    # Se foi interrompido durante o delay
                    if self._stop_flag.is_set():
                        break
                
                # Executa o evento
                try:
                    self._execute_event(event)
                    self._events_played += 1
                except Exception as e:
                    print(f"Erro ao executar evento: {e}")
                
                # Atualiza timestamp anterior
                prev_timestamp = event.timestamp
                
                # Notifica progresso se callback configurado
                if self._on_progress_callback:
                    total_loops = int(max_loops) if max_loops != float('inf') else -1
                    self._on_progress_callback(current_loop + 1, total_loops, i + 1)
            
            # Incrementa contador de loops (se não foi interrompido)
            if not self._stop_flag.is_set():
                current_loop += 1
                self._loops_completed = current_loop
        
        # ====================================================================
        # FINALIZAÇÃO
        # ====================================================================
        
        self.is_playing = False
        
        # Notifica que terminou
        if self._on_complete_callback:
            self._on_complete_callback()
        
        print(f"Reprodução concluída: {self._loops_completed} loops, {self._events_played} eventos")

    def play(self, session: RecordingSession) -> bool:
        """
        Inicia a reprodução de uma sessão gravada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este é o método que você chama para começar a reprodução. Passe
        a sessão que você quer reproduzir e o Player vai executar todos
        os eventos gravados.
        
        A reprodução acontece em segundo plano (em uma thread), então
        você pode continuar usando o programa normalmente (como clicar
        no botão de parar).
        
        EXPLICAÇÃO TÉCNICA:
        Cria e inicia uma thread para executar _playback_loop().
        Thread daemon=True garante que a thread morre se o programa
        for fechado inesperadamente.
        
        Args:
            session (RecordingSession): A sessão a ser reproduzida
        
        Returns:
            bool: True se a reprodução iniciou, False se já estava rodando
        """
        # Não permite iniciar se já está reproduzindo
        if self.is_playing:
            print("Reprodução já em andamento!")
            return False
        
        # Valida a sessão
        if not session or not session.events:
            print("Sessão vazia ou inválida!")
            return False
        
        # Armazena a sessão
        self._session = session
        
        # Reseta a flag de parada
        self._stop_flag.clear()
        
        # Atualiza estado
        self.is_playing = True
        
        # Cria e inicia a thread de reprodução
        self._playback_thread = threading.Thread(
            target=self._playback_loop,  # Função a executar
            name="TarefAuto-Playback",    # Nome para debug
            daemon=True                   # Morre com o programa principal
        )
        self._playback_thread.start()
        
        print(f"Reprodução iniciada: {len(session.events)} eventos")
        return True

    def stop(self) -> None:
        """
        Para a reprodução imediatamente (parada de emergência).
        
        EXPLICAÇÃO PARA INICIANTES:
        Chame este método quando quiser parar a reprodução antes que
        ela termine naturalmente. É como apertar o botão de "stop"
        de um player de música.
        
        A parada não é instantânea - pode levar até ~10ms para a
        reprodução realmente parar (por segurança).
        
        EXPLICAÇÃO TÉCNICA:
        Define a flag de parada que é verificada regularmente no
        _playback_loop(). A thread termina de forma limpa no próximo
        ciclo de verificação.
        
        Returns:
            None
        """
        if not self.is_playing:
            return
        
        # Seta a flag de parada
        self._stop_flag.set()
        
        # Espera a thread terminar (com timeout)
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)  # Espera até 1 segundo
        
        self.is_playing = False
        print("Reprodução interrompida pelo usuário")

    def get_stats(self) -> dict:
        """
        Retorna estatísticas da reprodução atual/última.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método te diz informações sobre a reprodução:
        - Quantos loops foram completados
        - Quantos eventos foram executados
        - Se está reproduzindo agora
        
        EXPLICAÇÃO TÉCNICA:
        Retorna um dicionário com métricas de estado e progresso.
        
        Returns:
            dict: Dicionário com estatísticas da reprodução
        """
        return {
            "is_playing": self.is_playing,
            "loops_completed": self._loops_completed,
            "events_played": self._events_played,
            "loop_mode": self.loop_mode.name,
            "loop_value": self.loop_value,
            "speed": self.speed_multiplier,
        }

    def get_current_loop(self) -> int:
        """
        Retorna o número do loop atual.
        
        Returns:
            int: Número do loop atual (começa em 1)
        """
        return self._current_loop

    def get_elapsed_time(self) -> float:
        """
        Retorna o tempo decorrido desde o início da reprodução.
        
        Returns:
            float: Tempo em segundos
        """
        if self._start_time > 0 and self.is_playing:
            return time.time() - self._start_time
        return 0.0


# ============================================================================
# BLOCO DE TESTE
# ============================================================================

if __name__ == "__main__":
    # Este bloco só executa quando você roda: python player.py
    
    print("=== Teste do módulo player.py ===")
    print("Este teste vai mover o mouse em um padrão quadrado.")
    print("Prepare-se! Começando em 3 segundos...")
    time.sleep(3)
    
    # Cria uma sessão de teste com movimentos em quadrado
    session = RecordingSession(name="Teste de Player")
    
    # Adiciona eventos de movimento em forma de quadrado
    # Cada lado do quadrado leva 0.5 segundos
    positions = [
        (100, 100),   # Canto superior esquerdo
        (300, 100),   # Canto superior direito
        (300, 300),   # Canto inferior direito
        (100, 300),   # Canto inferior esquerdo
        (100, 100),   # Volta ao início
    ]
    
    for i, (x, y) in enumerate(positions):
        event = InputEvent(
            timestamp=i * 0.5,  # 0.5 segundos entre cada posição
            event_type=EventType.MOUSE_MOVE,
            x=x,
            y=y
        )
        session.add_event(event)
    
    # Cria o player
    player = Player()
    
    # Configura para executar 2 vezes
    player.set_loop_mode(LoopMode.COUNT, 2)
    
    # Inicia a reprodução
    player.play(session)
    
    # Espera terminar
    while player.is_playing:
        time.sleep(0.1)
    
    # Mostra estatísticas
    stats = player.get_stats()
    print(f"\nEstatísticas finais:")
    print(f"  Loops completados: {stats['loops_completed']}")
    print(f"  Eventos executados: {stats['events_played']}")
    
    print("\n=== Teste concluído! ===")
