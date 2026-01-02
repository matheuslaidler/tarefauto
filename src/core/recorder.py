# ============================================================================
# TarefAuto - Módulo de Gravação (recorder.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este é o módulo responsável por "gravar" tudo o que você faz com o mouse
# e teclado. Quando você clica em "Iniciar Gravação", este código começa a
# observar cada movimento do mouse, cada clique e cada tecla que você aperta.
#
# Funciona como um gravador de áudio, mas para suas ações no computador.
# Ele anota o tempo exato de cada ação para poder reproduzir depois na
# mesma velocidade que você fez.
#
# EXPLICAÇÃO TÉCNICA:
# Utiliza a biblioteca pynput para criar listeners de mouse e teclado que
# rodam em threads separadas. Os eventos são capturados via callbacks e
# armazenados em uma RecordingSession com timestamps relativos ao início
# da gravação.
#
# ============================================================================

"""
Módulo de gravação de eventos para o TarefAuto.

Este módulo contém a classe Recorder, responsável por capturar eventos
de mouse e teclado em tempo real e armazená-los em uma RecordingSession.

Classes:
    Recorder: Gerencia a gravação de eventos de entrada

Dependencies:
    - pynput: Para captura de eventos de mouse e teclado
    - threading: Para execução assíncrona dos listeners

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# threading: Módulo para trabalhar com múltiplas "linhas de execução"
# Permite que o programa faça várias coisas ao mesmo tempo
import threading

# time: Módulo para trabalhar com tempo (medição, delays)
import time

# typing: Anotações de tipo para melhor documentação do código
from typing import Optional, Callable, List

# pynput: Biblioteca principal para captura de mouse e teclado
# Importamos os módulos de mouse e keyboard separadamente
from pynput import mouse, keyboard

# Importações internas do nosso projeto
# Usamos as classes que definimos em events.py
from src.core.events import InputEvent, EventType, RecordingSession


# ============================================================================
# CLASSE RECORDER (GRAVADOR)
# ============================================================================

class Recorder:
    """
    Classe responsável por gravar eventos de mouse e teclado.
    
    EXPLICAÇÃO PARA INICIANTES:
    O Recorder é como um "observador" que fica de olho em tudo que você faz
    com o mouse e teclado. Quando você inicia a gravação:
    
    1. Ele começa a observar seus movimentos
    2. Cada ação (mover, clicar, digitar) é anotada com o tempo exato
    3. Quando você para a gravação, ele te dá a lista de tudo que fez
    
    Você pode escolher gravar apenas mouse, apenas teclado, ou os dois juntos.
    
    EXPLICAÇÃO TÉCNICA:
    O Recorder utiliza pynput.mouse.Listener e pynput.keyboard.Listener
    para capturar eventos de forma não-bloqueante em threads separadas.
    
    Os listeners usam o padrão callback: cada vez que um evento ocorre,
    uma função é chamada automaticamente. Esses callbacks registram os
    eventos na session com timestamps relativos.
    
    Attributes:
        session (RecordingSession): Sessão atual contendo os eventos gravados
        record_mouse (bool): Se deve gravar eventos de mouse
        record_keyboard (bool): Se deve gravar eventos de teclado
        is_recording (bool): Estado atual da gravação
        _start_time (float): Timestamp do início da gravação
        _mouse_listener (Listener): Listener do pynput para mouse
        _keyboard_listener (Listener): Listener do pynput para teclado
        _on_event_callback (Callable): Callback opcional para notificar eventos
    
    Example:
        >>> recorder = Recorder(record_mouse=True, record_keyboard=True)
        >>> recorder.start()
        >>> # ... usuário faz ações ...
        >>> session = recorder.stop()
        >>> print(f"Gravados {len(session.events)} eventos")
    """
    
    def __init__(
        self,
        record_mouse: bool = True,
        record_keyboard: bool = True,
        on_event_callback: Optional[Callable[[InputEvent], None]] = None
    ):
        """
        Inicializa o gravador com as configurações desejadas.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método é chamado automaticamente quando você cria um novo
        Recorder. Aqui definimos as configurações iniciais:
        - Queremos gravar o mouse? Sim ou não?
        - Queremos gravar o teclado? Sim ou não?
        - Queremos ser notificados quando algo acontecer? (opcional)
        
        EXPLICAÇÃO TÉCNICA:
        Construtor que inicializa os atributos da instância. O parâmetro
        on_event_callback permite injetar uma função que será chamada
        cada vez que um evento for capturado (útil para atualizar a UI).
        
        Args:
            record_mouse (bool): Se True, grava eventos de mouse. Default: True
            record_keyboard (bool): Se True, grava eventos de teclado. Default: True
            on_event_callback (Callable, optional): Função chamada para cada evento.
                Recebe um InputEvent como parâmetro. Default: None
        """
        # ====================================================================
        # CONFIGURAÇÕES DE GRAVAÇÃO
        # ====================================================================
        
        # Armazena se devemos gravar mouse e/ou teclado
        self.record_mouse = record_mouse          # Gravar mouse?
        self.record_keyboard = record_keyboard    # Gravar teclado?
        
        # ====================================================================
        # ESTADO INTERNO
        # ====================================================================
        
        # Indica se estamos gravando no momento
        # False = parado, True = gravando
        self.is_recording = False
        
        # Sessão que armazenará os eventos gravados
        # Inicialmente é uma sessão vazia
        self.session = RecordingSession(
            record_mouse=record_mouse,
            record_keyboard=record_keyboard
        )
        
        # Timestamp do momento em que a gravação iniciou
        # Usado para calcular o tempo relativo de cada evento
        self._start_time: float = 0.0
        
        # ====================================================================
        # LISTENERS DO PYNPUT
        # ====================================================================
        
        # Listener para eventos de mouse (movimento, clique, scroll)
        # Inicialmente None - será criado quando a gravação iniciar
        self._mouse_listener: Optional[mouse.Listener] = None
        
        # Listener para eventos de teclado (tecla pressionada/solta)
        self._keyboard_listener: Optional[keyboard.Listener] = None
        
        # ====================================================================
        # CALLBACK OPCIONAL
        # ====================================================================
        
        # Função que será chamada quando um evento for capturado
        # Útil para atualizar a interface gráfica em tempo real
        self._on_event_callback = on_event_callback
        
        # ====================================================================
        # CONTROLE DE THREAD-SAFETY
        # ====================================================================
        
        # Lock para garantir que apenas uma thread acesse os dados por vez
        # Evita problemas quando mouse e teclado capturam eventos simultaneamente
        self._lock = threading.Lock()

    def _get_relative_time(self) -> float:
        """
        Calcula o tempo decorrido desde o início da gravação.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando gravamos uma ação, precisamos saber "quantos segundos depois
        do início" ela aconteceu. Esta função calcula isso.
        
        Exemplo:
        - Gravação iniciou às 10:00:00
        - Você clicou às 10:00:02
        - Esta função retorna: 2.0 (dois segundos depois)
        
        EXPLICAÇÃO TÉCNICA:
        Calcula a diferença entre o timestamp atual (time.time()) e o
        timestamp de início armazenado em _start_time. Retorna em segundos
        como float para precisão de milissegundos.
        
        Returns:
            float: Tempo em segundos desde o início da gravação
        """
        # time.time() retorna o timestamp atual em segundos
        # Subtraímos o timestamp de início para obter o tempo relativo
        return time.time() - self._start_time

    def _add_event(self, event: InputEvent) -> None:
        """
        Adiciona um evento à sessão de forma thread-safe.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando capturamos um evento (clique, tecla, etc.), usamos esta
        função para adicioná-lo à nossa lista de eventos gravados.
        
        O "thread-safe" significa que é seguro chamar esta função de
        múltiplos lugares ao mesmo tempo (mouse e teclado podem capturar
        eventos simultaneamente) sem causar problemas.
        
        EXPLICAÇÃO TÉCNICA:
        Usa um Lock para garantir exclusão mútua ao acessar a session.
        Também chama o callback de notificação, se configurado.
        
        Args:
            event (InputEvent): O evento a ser adicionado
        """
        # with self._lock: adquire o lock antes de executar o bloco
        # Isso garante que apenas uma thread por vez adicione eventos
        with self._lock:
            # Adiciona o evento à sessão
            self.session.add_event(event)
        
        # Se há um callback configurado, notifica sobre o novo evento
        # Isso é útil para atualizar a UI em tempo real
        if self._on_event_callback:
            self._on_event_callback(event)

    # ========================================================================
    # CALLBACKS DO MOUSE
    # ========================================================================
    
    def _on_mouse_move(self, x: int, y: int) -> None:
        """
        Callback chamado quando o mouse se move.
        
        EXPLICAÇÃO PARA INICIANTES:
        Toda vez que você move o mouse, o pynput chama esta função
        automaticamente, informando para onde o mouse foi (posição x, y).
        
        A posição (x, y) funciona assim:
        - x é a distância em pixels a partir da borda esquerda da tela
        - y é a distância em pixels a partir do topo da tela
        
        Exemplo: (100, 200) significa 100 pixels à direita e 200 abaixo
        
        EXPLICAÇÃO TÉCNICA:
        Callback registrado no mouse.Listener. Cria um InputEvent do tipo
        MOUSE_MOVE com as coordenadas atuais e adiciona à sessão.
        
        Args:
            x (int): Coordenada X (horizontal) do cursor em pixels
            y (int): Coordenada Y (vertical) do cursor em pixels
        """
        # Só processa se estamos gravando E se devemos gravar mouse
        if not self.is_recording or not self.record_mouse:
            return  # Sai sem fazer nada
        
        # Cria o evento de movimento
        event = InputEvent(
            timestamp=self._get_relative_time(),    # Quando aconteceu
            event_type=EventType.MOUSE_MOVE,        # Tipo: movimento de mouse
            x=int(x),                               # Posição X (convertido para int)
            y=int(y)                                # Posição Y (convertido para int)
        )
        
        # Adiciona à sessão de forma segura
        self._add_event(event)

    def _on_mouse_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        """
        Callback chamado quando um botão do mouse é clicado ou solto.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você clica com o mouse (ou solta o botão), esta função é
        chamada. Ela recebe:
        - Onde você clicou (x, y)
        - Qual botão (esquerdo, direito, meio)
        - Se foi um "apertar" ou "soltar" o botão
        
        Precisamos saber se foi apertar ou soltar para poder reproduzir
        cliques longos (segurar o botão) corretamente.
        
        EXPLICAÇÃO TÉCNICA:
        Callback do mouse.Listener para eventos de clique. O parâmetro
        button é um enum mouse.Button que convertemos para string legível.
        
        Args:
            x (int): Coordenada X do clique
            y (int): Coordenada Y do clique
            button (mouse.Button): Qual botão foi clicado (Button.left, etc.)
            pressed (bool): True se pressionado, False se solto
        """
        if not self.is_recording or not self.record_mouse:
            return
        
        # Converte o enum Button para string legível
        # button.name retorna 'left', 'right', ou 'middle'
        button_name = button.name if hasattr(button, 'name') else str(button)
        
        event = InputEvent(
            timestamp=self._get_relative_time(),
            event_type=EventType.MOUSE_CLICK,
            x=int(x),
            y=int(y),
            button=button_name,                     # Nome do botão
            pressed=pressed                         # Pressionado ou solto?
        )
        
        self._add_event(event)

    def _on_mouse_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """
        Callback chamado quando a rodinha do mouse é usada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você usa a rodinha do mouse para rolar uma página:
        - dy positivo = rolou para cima
        - dy negativo = rolou para baixo
        - dx é para rolagem horizontal (mais raro)
        
        Também registramos onde o mouse estava quando você rolou.
        
        EXPLICAÇÃO TÉCNICA:
        Callback para eventos de scroll. dx e dy indicam a direção e
        "intensidade" da rolagem. Valores típicos são +1/-1 ou múltiplos.
        
        Args:
            x (int): Coordenada X do cursor durante o scroll
            y (int): Coordenada Y do cursor durante o scroll
            dx (int): Deslocamento horizontal (scroll horizontal)
            dy (int): Deslocamento vertical (scroll vertical)
        """
        if not self.is_recording or not self.record_mouse:
            return
        
        event = InputEvent(
            timestamp=self._get_relative_time(),
            event_type=EventType.MOUSE_SCROLL,
            x=int(x),
            y=int(y),
            dx=int(dx),                             # Scroll horizontal
            dy=int(dy)                              # Scroll vertical
        )
        
        self._add_event(event)

    # ========================================================================
    # CALLBACKS DO TECLADO
    # ========================================================================
    
    def _get_key_string(self, key) -> str:
        """
        Converte uma tecla do pynput para string legível.
        
        EXPLICAÇÃO PARA INICIANTES:
        O pynput representa teclas de formas diferentes:
        - Letras e números: keyboard.KeyCode(char='a')
        - Teclas especiais: keyboard.Key.space, keyboard.Key.enter
        
        Esta função converte qualquer formato para uma string simples
        que podemos salvar e usar depois.
        
        EXPLICAÇÃO TÉCNICA:
        Trata os dois tipos principais de tecla do pynput:
        - KeyCode: teclas com caractere (letras, números, símbolos)
        - Key: teclas especiais (space, enter, ctrl, etc.)
        
        Args:
            key: Objeto tecla do pynput (KeyCode ou Key)
        
        Returns:
            str: Representação string da tecla
        """
        # Tenta diferentes formas de obter o valor da tecla
        try:
            # Se é uma tecla com caractere (letra, número)
            # keyboard.KeyCode tem o atributo 'char'
            if hasattr(key, 'char') and key.char is not None:
                return key.char  # Retorna o caractere ('a', '1', etc.)
            
            # Se é uma tecla especial (space, enter, ctrl, etc.)
            # keyboard.Key tem o atributo 'name'
            elif hasattr(key, 'name'):
                return key.name  # Retorna o nome ('space', 'enter', etc.)
            
            # Caso genérico - converte para string
            else:
                return str(key)
                
        except Exception:
            # Se algo der errado, retorna a representação string padrão
            return str(key)

    def _on_key_press(self, key) -> None:
        """
        Callback chamado quando uma tecla é pressionada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Toda vez que você aperta uma tecla no teclado, esta função é
        chamada. Ela anota qual tecla você apertou e quando.
        
        Note que "pressionar" é diferente de "soltar" - se você segura
        uma tecla, primeiro é chamado o press, e só quando solta é
        chamado o release.
        
        EXPLICAÇÃO TÉCNICA:
        Callback do keyboard.Listener para eventos key_press.
        A tecla é convertida para string usando _get_key_string().
        
        Args:
            key: Objeto tecla do pynput (KeyCode ou Key)
        """
        if not self.is_recording or not self.record_keyboard:
            return
        
        # Converte a tecla para string
        key_str = self._get_key_string(key)
        
        event = InputEvent(
            timestamp=self._get_relative_time(),
            event_type=EventType.KEY_PRESS,
            key=key_str,                            # Qual tecla
            pressed=True                            # Foi pressionada (não solta)
        )
        
        self._add_event(event)

    def _on_key_release(self, key) -> None:
        """
        Callback chamado quando uma tecla é solta.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você solta uma tecla que estava pressionada, esta função
        é chamada. Isso é importante para saber quanto tempo uma tecla
        ficou pressionada (como ao segurar Shift).
        
        EXPLICAÇÃO TÉCNICA:
        Callback do keyboard.Listener para eventos key_release.
        
        Args:
            key: Objeto tecla do pynput (KeyCode ou Key)
        """
        if not self.is_recording or not self.record_keyboard:
            return
        
        key_str = self._get_key_string(key)
        
        event = InputEvent(
            timestamp=self._get_relative_time(),
            event_type=EventType.KEY_RELEASE,
            key=key_str,
            pressed=False                           # Foi solta (não pressionada)
        )
        
        self._add_event(event)

    # ========================================================================
    # CONTROLE DE GRAVAÇÃO
    # ========================================================================

    def start(self) -> None:
        """
        Inicia a gravação de eventos.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este é o método que você chama para começar a gravar. A partir
        deste momento, tudo o que você fizer com mouse e teclado será
        capturado até você chamar stop().
        
        Você pode chamar start() várias vezes, mas se já estiver gravando,
        nada acontece (não vai reiniciar nem perder dados).
        
        EXPLICAÇÃO TÉCNICA:
        1. Verifica se já está gravando (evita duplicação)
        2. Cria uma nova RecordingSession
        3. Registra o timestamp de início
        4. Cria e inicia os listeners de mouse e teclado
        
        Os listeners rodam em threads separadas e chamam os callbacks
        automaticamente quando eventos ocorrem.
        
        Returns:
            None
        """
        # Se já está gravando, não faz nada
        if self.is_recording:
            print("Gravação já está em andamento!")
            return
        
        # Cria uma nova sessão para esta gravação
        self.session = RecordingSession(
            record_mouse=self.record_mouse,
            record_keyboard=self.record_keyboard
        )
        
        # Marca o momento de início (usado para calcular tempos relativos)
        self._start_time = time.time()
        
        # Atualiza o estado
        self.is_recording = True
        
        # --------------------------------------------------------------------
        # CRIAÇÃO DOS LISTENERS
        # --------------------------------------------------------------------
        
        # Cria e inicia o listener de mouse (se configurado para gravar)
        if self.record_mouse:
            self._mouse_listener = mouse.Listener(
                on_move=self._on_mouse_move,        # Callback para movimento
                on_click=self._on_mouse_click,      # Callback para clique
                on_scroll=self._on_mouse_scroll     # Callback para scroll
            )
            self._mouse_listener.start()  # Inicia a thread do listener
        
        # Cria e inicia o listener de teclado (se configurado para gravar)
        if self.record_keyboard:
            self._keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press,        # Callback para tecla pressionada
                on_release=self._on_key_release     # Callback para tecla solta
            )
            self._keyboard_listener.start()  # Inicia a thread do listener
        
        print("Gravação iniciada!")

    def stop(self) -> RecordingSession:
        """
        Para a gravação e retorna a sessão com os eventos capturados.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você chama este método, a gravação para imediatamente.
        Ele retorna um objeto RecordingSession contendo todos os eventos
        que foram capturados desde o início.
        
        Você pode então salvar essa sessão em um arquivo ou usá-la
        diretamente para reprodução.
        
        EXPLICAÇÃO TÉCNICA:
        1. Verifica se está gravando
        2. Para os listeners (os listeners do pynput não podem ser
           reiniciados, então são destruídos)
        3. Atualiza o estado
        4. Retorna a sessão com todos os eventos
        
        Returns:
            RecordingSession: Sessão contendo todos os eventos gravados
        """
        # Se não está gravando, retorna a sessão atual (possivelmente vazia)
        if not self.is_recording:
            print("Nenhuma gravação em andamento!")
            return self.session
        
        # Atualiza o estado primeiro
        self.is_recording = False
        
        # --------------------------------------------------------------------
        # PARANDO OS LISTENERS
        # --------------------------------------------------------------------
        
        # Para o listener de mouse
        if self._mouse_listener is not None:
            self._mouse_listener.stop()     # Para a thread
            self._mouse_listener = None     # Libera a referência
        
        # Para o listener de teclado
        if self._keyboard_listener is not None:
            self._keyboard_listener.stop()
            self._keyboard_listener = None
        
        # Mostra estatísticas da gravação
        num_events = len(self.session.events)
        duration = self.session.get_duration()
        print(f"Gravação parada! {num_events} eventos em {duration:.2f} segundos")
        
        # Retorna a sessão completa
        return self.session

    def update_settings(self, record_mouse: bool, record_keyboard: bool) -> None:
        """
        Atualiza as configurações de gravação.
        
        EXPLICAÇÃO PARA INICIANTES:
        Use este método para mudar o que será gravado ANTES de iniciar
        uma gravação. Por exemplo, se você só quer gravar cliques de
        mouse sem o teclado.
        
        Se você chamar durante uma gravação, as mudanças só terão efeito
        na próxima gravação.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza os flags de configuração. Não afeta gravação em andamento
        pois os listeners já foram criados com as configurações anteriores.
        
        Args:
            record_mouse (bool): Se deve gravar eventos de mouse
            record_keyboard (bool): Se deve gravar eventos de teclado
        """
        self.record_mouse = record_mouse
        self.record_keyboard = record_keyboard

    def get_event_count(self) -> int:
        """
        Retorna o número de eventos gravados até o momento.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método é útil para mostrar na interface quantos eventos
        já foram capturados. Um "contador" de ações, basicamente.
        
        EXPLICAÇÃO TÉCNICA:
        Acessa a lista de eventos da sessão de forma thread-safe.
        
        Returns:
            int: Número de eventos na sessão atual
        """
        with self._lock:
            return len(self.session.events)


# ============================================================================
# BLOCO DE TESTE
# ============================================================================

if __name__ == "__main__":
    # Este bloco só executa quando você roda: python recorder.py
    
    print("=== Teste do módulo recorder.py ===")
    print("Este é um teste interativo. Mova o mouse e pressione teclas.")
    print("A gravação durará 5 segundos...")
    print()
    
    # Cria o recorder com ambos mouse e teclado habilitados
    recorder = Recorder(record_mouse=True, record_keyboard=True)
    
    # Inicia a gravação
    recorder.start()
    
    # Espera 5 segundos
    time.sleep(5)
    
    # Para a gravação
    session = recorder.stop()
    
    # Mostra os resultados
    print(f"\nEventos capturados: {len(session.events)}")
    print(f"Duração: {session.get_duration():.2f} segundos")
    
    # Mostra os primeiros 10 eventos como exemplo
    print("\nPrimeiros 10 eventos:")
    for i, event in enumerate(session.events[:10]):
        print(f"  {i+1}. [{event.timestamp:.3f}s] {event.event_type.name}", end="")
        if event.x is not None:
            print(f" @ ({event.x}, {event.y})", end="")
        if event.key is not None:
            print(f" key='{event.key}'", end="")
        if event.button is not None:
            print(f" button={event.button}", end="")
        print()
    
    print("\n=== Teste concluído! ===")
