# ============================================================================
# TarefAuto - Módulo de Eventos (events.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Quando você usa o mouse ou teclado, cada ação (clicar, mover, digitar) é
# chamada de "evento". Este arquivo define como esses eventos são organizados
# e armazenados na memória do programa.
#
# Pense assim: se você está gravando um filme das suas ações no computador,
# cada "frame" do filme seria um evento. Este arquivo define o "formato"
# desses frames para que possamos salvar e reproduzir depois.
#
# EXPLICAÇÃO TÉCNICA:
# Utilizamos dataclasses do Python para criar estruturas de dados imutáveis
# e bem tipadas. Isso garante que os eventos tenham sempre os campos corretos
# e facilita a serialização para JSON (salvar em arquivo).
#
# ============================================================================

"""
Módulo de definição de eventos para o TarefAuto.

Este módulo contém as classes que representam os eventos de entrada
(mouse e teclado) capturados durante a gravação, bem como a estrutura
para armazenar uma sessão de gravação completa.

Classes:
    EventType: Enumeração dos tipos de eventos possíveis
    InputEvent: Representa um único evento de entrada
    RecordingSession: Representa uma sessão de gravação completa

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# dataclasses: Módulo que simplifica a criação de classes para armazenar dados
# @dataclass automaticamente cria __init__, __repr__, __eq__, etc.
from dataclasses import dataclass, field

# typing: Módulo para anotações de tipo, ajuda IDEs e desenvolvedores a
# entenderem que tipo de dados cada variável deve conter
from typing import Optional, List, Dict, Any, Union

# Enum: Classe base para criar enumerações (conjuntos fixos de valores)
# Por exemplo: dias da semana, tipos de eventos, etc.
from enum import Enum, auto

# json: Módulo para converter dados Python para JSON e vice-versa
# JSON é um formato de texto usado para salvar/carregar dados
import json

# time: Módulo para trabalhar com tempo (timestamps, delays, etc.)
import time

# datetime: Módulo para trabalhar com datas e horas formatadas
from datetime import datetime


# ============================================================================
# ENUMERAÇÃO DE TIPOS DE EVENTO
# ============================================================================

class EventType(Enum):
    """
    Enumeração dos tipos de eventos que podem ser capturados.
    
    EXPLICAÇÃO PARA INICIANTES:
    Uma "enumeração" (Enum) é como uma lista fixa de opções possíveis.
    Em vez de usar strings soltas como "mouse_move" ou "key_press" que
    podem ter erros de digitação, usamos esta classe para ter opções
    pré-definidas e seguras.
    
    É como ter um menu com opções numeradas - você escolhe o número,
    não precisa escrever o nome do prato e arriscar errar.
    
    EXPLICAÇÃO TÉCNICA:
    Enum garante type-safety e permite que IDEs ofereçam autocomplete.
    O método auto() gera valores únicos automaticamente para cada membro.
    
    Attributes:
        MOUSE_MOVE: Movimento do cursor do mouse
        MOUSE_CLICK: Clique de botão do mouse (esquerdo, direito, meio)
        MOUSE_SCROLL: Rolagem da roda do mouse
        KEY_PRESS: Tecla pressionada no teclado
        KEY_RELEASE: Tecla solta no teclado
    """
    
    # auto() gera um valor inteiro único automaticamente
    # Cada tipo representa uma ação diferente que o usuário pode fazer
    
    MOUSE_MOVE = auto()     # Valor: 1 - Quando o mouse se move na tela
    MOUSE_CLICK = auto()    # Valor: 2 - Quando um botão do mouse é clicado
    MOUSE_SCROLL = auto()   # Valor: 3 - Quando a rodinha do mouse gira
    KEY_PRESS = auto()      # Valor: 4 - Quando uma tecla é pressionada
    KEY_RELEASE = auto()    # Valor: 5 - Quando uma tecla é solta


# ============================================================================
# CLASSE DE EVENTO DE ENTRADA
# ============================================================================

@dataclass
class InputEvent:
    """
    Representa um único evento de entrada (mouse ou teclado).
    
    EXPLICAÇÃO PARA INICIANTES:
    Imagine que você está escrevendo um diário do que faz no computador.
    Cada entrada do diário seria algo como:
    "Às 10:30:15, eu CLIQUEI com o botão ESQUERDO na posição X=500, Y=300"
    
    Esta classe é exatamente isso - ela guarda todas as informações sobre
    UMA ação que você fez: quando foi, que tipo de ação, e os detalhes.
    
    EXPLICAÇÃO TÉCNICA:
    @dataclass é um decorador que automaticamente gera métodos especiais
    como __init__, __repr__, __eq__ baseado nos atributos definidos.
    Isso reduz código boilerplate e torna a classe mais limpa.
    
    Attributes:
        timestamp (float): Momento em que o evento ocorreu (segundos desde início)
        event_type (EventType): Tipo do evento (mouse_move, key_press, etc.)
        x (Optional[int]): Coordenada X do mouse (None para eventos de teclado)
        y (Optional[int]): Coordenada Y do mouse (None para eventos de teclado)
        button (Optional[str]): Botão do mouse clicado ('left', 'right', 'middle')
        pressed (Optional[bool]): Se o botão/tecla foi pressionado (True) ou solto (False)
        key (Optional[str]): Tecla pressionada (para eventos de teclado)
        dx (Optional[int]): Deslocamento horizontal do scroll
        dy (Optional[int]): Deslocamento vertical do scroll
    
    Example:
        >>> # Criando um evento de clique do mouse
        >>> click_event = InputEvent(
        ...     timestamp=1.5,
        ...     event_type=EventType.MOUSE_CLICK,
        ...     x=500,
        ...     y=300,
        ...     button='left',
        ...     pressed=True
        ... )
        >>> print(click_event)
        InputEvent(timestamp=1.5, event_type=<EventType.MOUSE_CLICK: 2>, ...)
    """
    
    # ========================================================================
    # ATRIBUTOS OBRIGATÓRIOS (sempre devem ser fornecidos)
    # ========================================================================
    
    # timestamp: O momento exato em que o evento aconteceu
    # É medido em segundos desde o início da gravação
    # Exemplo: 1.5 significa 1 segundo e meio após começar a gravar
    timestamp: float
    
    # event_type: Qual tipo de ação foi realizada
    # Usa a enumeração EventType definida acima
    event_type: EventType
    
    # ========================================================================
    # ATRIBUTOS OPCIONAIS (podem ser None dependendo do tipo de evento)
    # ========================================================================
    
    # Coordenadas do mouse na tela (em pixels)
    # x: posição horizontal (0 = esquerda da tela)
    # y: posição vertical (0 = topo da tela)
    # São None quando o evento é apenas de teclado
    x: Optional[int] = None  # None significa "não aplicável"
    y: Optional[int] = None
    
    # button: Qual botão do mouse foi usado
    # Valores possíveis: 'left' (esquerdo), 'right' (direito), 'middle' (meio)
    # É None para eventos que não são cliques de mouse
    button: Optional[str] = None
    
    # pressed: Indica se foi um "apertar" ou "soltar"
    # True = o botão/tecla foi pressionado
    # False = o botão/tecla foi solto
    # Importante para saber a duração de um clique ou tecla segurada
    pressed: Optional[bool] = None
    
    # key: Qual tecla do teclado foi usada
    # Pode ser uma letra ('a'), número ('1'), ou tecla especial ('space', 'enter')
    # É None para eventos de mouse
    key: Optional[str] = None
    
    # dx, dy: Deslocamento do scroll (rolagem)
    # dx: rolagem horizontal (negativo = esquerda, positivo = direita)
    # dy: rolagem vertical (negativo = para baixo, positivo = para cima)
    dx: Optional[int] = None
    dy: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o evento para um dicionário Python.
        
        EXPLICAÇÃO PARA INICIANTES:
        Um "dicionário" em Python é como uma tabela de duas colunas:
        uma coluna com nomes (chaves) e outra com valores.
        
        Exemplo: {"nome": "João", "idade": 25}
        
        Precisamos converter para dicionário porque é assim que salvamos
        os dados em arquivos JSON depois.
        
        EXPLICAÇÃO TÉCNICA:
        Este método serializa o objeto para um formato que pode ser
        facilmente convertido para JSON. O EventType é convertido para
        seu nome (string) para manter o JSON legível.
        
        Returns:
            Dict[str, Any]: Dicionário com todos os dados do evento
        
        Example:
            >>> event = InputEvent(timestamp=1.0, event_type=EventType.MOUSE_MOVE, x=100, y=200)
            >>> event.to_dict()
            {'t': 1.0, 'type': 'MOUSE_MOVE', 'x': 100, 'y': 200}
        """
        # Cria um dicionário com os campos básicos
        # Usamos nomes curtos ('t' em vez de 'timestamp') para economizar espaço
        data = {
            "t": self.timestamp,                    # 't' = timestamp (tempo)
            "type": self.event_type.name,           # 'type' = tipo do evento (como string)
        }
        
        # Adiciona campos opcionais APENAS se eles tiverem valor
        # Isso mantém o JSON limpo, sem campos desnecessários
        
        if self.x is not None:                      # Se tem coordenada X
            data["x"] = self.x
            
        if self.y is not None:                      # Se tem coordenada Y
            data["y"] = self.y
            
        if self.button is not None:                 # Se tem botão do mouse
            data["btn"] = self.button
            
        if self.pressed is not None:                # Se tem estado pressionado/solto
            data["pressed"] = self.pressed
            
        if self.key is not None:                    # Se tem tecla
            data["key"] = self.key
            
        if self.dx is not None:                     # Se tem scroll horizontal
            data["dx"] = self.dx
            
        if self.dy is not None:                     # Se tem scroll vertical
            data["dy"] = self.dy
        
        return data  # Retorna o dicionário montado

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputEvent":
        """
        Cria um InputEvent a partir de um dicionário.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este é o processo inverso do to_dict(). Quando carregamos um
        arquivo JSON, ele vem como dicionário. Este método pega esse
        dicionário e reconstrói o objeto InputEvent original.
        
        É como ter uma receita (dicionário) e usar ela para fazer o bolo
        (objeto InputEvent).
        
        EXPLICAÇÃO TÉCNICA:
        @classmethod indica que este método pertence à classe, não a uma
        instância. O primeiro parâmetro 'cls' é a própria classe.
        Isso permite criar novas instâncias de dentro de um método estático.
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados do evento
        
        Returns:
            InputEvent: Nova instância criada a partir dos dados
        
        Example:
            >>> data = {'t': 1.0, 'type': 'MOUSE_MOVE', 'x': 100, 'y': 200}
            >>> event = InputEvent.from_dict(data)
            >>> event.x
            100
        """
        # Converte a string do tipo de volta para o enum EventType
        # EventType["MOUSE_MOVE"] retorna EventType.MOUSE_MOVE
        event_type = EventType[data["type"]]
        
        # Cria e retorna uma nova instância de InputEvent
        # .get() retorna None se a chave não existir no dicionário
        return cls(
            timestamp=data["t"],                    # Pega o timestamp
            event_type=event_type,                  # Pega o tipo (já convertido)
            x=data.get("x"),                        # Pega X ou None
            y=data.get("y"),                        # Pega Y ou None
            button=data.get("btn"),                 # Pega botão ou None
            pressed=data.get("pressed"),            # Pega estado ou None
            key=data.get("key"),                    # Pega tecla ou None
            dx=data.get("dx"),                      # Pega scroll X ou None
            dy=data.get("dy"),                      # Pega scroll Y ou None
        )


# ============================================================================
# CLASSE DE SESSÃO DE GRAVAÇÃO
# ============================================================================

@dataclass
class RecordingSession:
    """
    Representa uma sessão completa de gravação.
    
    EXPLICAÇÃO PARA INICIANTES:
    Se cada InputEvent é uma "foto" de uma ação, então RecordingSession
    é o "álbum de fotos" completo. Ela guarda todas as ações que você
    gravou, junto com informações extras como:
    - Quando a gravação foi feita
    - Quais configurações foram usadas (gravar mouse? teclado? ambos?)
    - A lista de todos os eventos na ordem que aconteceram
    
    Quando você salva ou carrega uma gravação, está salvando/carregando
    um objeto RecordingSession.
    
    EXPLICAÇÃO TÉCNICA:
    Esta classe agrega múltiplos InputEvents e metadados da gravação.
    Implementa métodos para serialização/deserialização JSON completa,
    permitindo persistência e compartilhamento de gravações.
    
    Attributes:
        events (List[InputEvent]): Lista ordenada de eventos gravados
        created_at (str): Data/hora de criação no formato ISO 8601
        record_mouse (bool): Se movimentos/cliques de mouse foram gravados
        record_keyboard (bool): Se teclas do teclado foram gravadas
        version (str): Versão do formato de arquivo para compatibilidade
        name (str): Nome amigável para identificar a gravação
        description (str): Descrição opcional do que a gravação faz
    
    Example:
        >>> session = RecordingSession(
        ...     name="Preencher formulário",
        ...     description="Automatiza o preenchimento do formulário X"
        ... )
        >>> session.add_event(InputEvent(...))
        >>> session.save("minha_gravacao.json")
    """
    
    # ========================================================================
    # ATRIBUTOS COM VALORES PADRÃO
    # ========================================================================
    
    # Lista de eventos gravados - começa vazia
    # field(default_factory=list) cria uma nova lista para cada instância
    # (se usássemos events=[], todas as instâncias compartilhariam a mesma lista!)
    events: List[InputEvent] = field(default_factory=list)
    
    # Data e hora de criação - preenchido automaticamente
    # datetime.now().isoformat() gera algo como "2026-01-02T10:30:00"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Configurações de gravação - por padrão, grava tudo
    record_mouse: bool = True       # Gravar ações do mouse?
    record_keyboard: bool = True    # Gravar ações do teclado?
    
    # Metadados da gravação
    version: str = "1.0.0"          # Versão do formato (para compatibilidade futura)
    name: str = "Gravação sem nome" # Nome amigável da gravação
    description: str = ""           # Descrição do que a gravação faz

    def add_event(self, event: InputEvent) -> None:
        """
        Adiciona um novo evento à lista de eventos gravados.
        
        EXPLICAÇÃO PARA INICIANTES:
        Conforme você usa o mouse e teclado durante a gravação, cada ação
        é transformada em um InputEvent e adicionada à lista usando este
        método. É como adicionar uma nova foto ao álbum.
        
        EXPLICAÇÃO TÉCNICA:
        Método simples que encapsula a adição de eventos, permitindo
        futuras validações ou processamentos antes da inserção.
        
        Args:
            event (InputEvent): O evento a ser adicionado
        
        Returns:
            None: Este método não retorna nada, apenas modifica a lista
        """
        self.events.append(event)  # append adiciona ao final da lista

    def clear_events(self) -> None:
        """
        Remove todos os eventos gravados.
        
        EXPLICAÇÃO PARA INICIANTES:
        Se você quer começar uma nova gravação do zero, este método
        "limpa o álbum" removendo todas as fotos anteriores.
        
        EXPLICAÇÃO TÉCNICA:
        Limpa a lista de eventos para permitir reutilização da sessão
        sem criar uma nova instância.
        
        Returns:
            None
        """
        self.events.clear()  # clear() remove todos os itens da lista

    def get_duration(self) -> float:
        """
        Calcula a duração total da gravação em segundos.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método olha para o último evento gravado e diz quanto tempo
        durou toda a gravação. Se o último evento foi aos 30 segundos,
        então a gravação tem 30 segundos de duração.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna o timestamp do último evento, que representa a duração
        total desde o início da gravação (timestamp=0).
        
        Returns:
            float: Duração em segundos, ou 0.0 se não houver eventos
        """
        # Se não há eventos, duração é zero
        if not self.events:  # Lista vazia é "falsy" em Python
            return 0.0
        
        # Retorna o timestamp do último evento da lista
        return self.events[-1].timestamp  # [-1] acessa o último elemento

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a sessão completa para um dicionário.
        
        EXPLICAÇÃO PARA INICIANTES:
        Assim como InputEvent tem seu to_dict(), a sessão também precisa
        ser convertida para dicionário para poder ser salva em arquivo.
        Este método converte TUDO: as configurações E todos os eventos.
        
        EXPLICAÇÃO TÉCNICA:
        Serializa recursivamente a sessão e todos os eventos contidos
        para um formato compatível com JSON.
        
        Returns:
            Dict[str, Any]: Dicionário com todos os dados da sessão
        """
        return {
            "version": self.version,                                    # Versão do formato
            "name": self.name,                                          # Nome da gravação
            "description": self.description,                            # Descrição
            "created_at": self.created_at,                              # Data de criação
            "settings": {                                               # Configurações usadas
                "record_mouse": self.record_mouse,                      # Gravou mouse?
                "record_keyboard": self.record_keyboard,                # Gravou teclado?
            },
            "events": [event.to_dict() for event in self.events],       # Lista de eventos (convertidos)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordingSession":
        """
        Cria uma RecordingSession a partir de um dicionário.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você carrega um arquivo de gravação, ele vem como dicionário.
        Este método reconstrói toda a sessão (com todos os eventos) a
        partir desses dados.
        
        EXPLICAÇÃO TÉCNICA:
        Deserializa recursivamente os dados JSON de volta para objetos
        Python, recriando todos os InputEvents contidos.
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados da sessão
        
        Returns:
            RecordingSession: Nova instância com todos os dados carregados
        """
        # Extrai as configurações do dicionário
        settings = data.get("settings", {})  # Pega settings ou dict vazio
        
        # Converte cada dicionário de evento de volta para InputEvent
        events = [InputEvent.from_dict(e) for e in data.get("events", [])]
        
        # Cria e retorna a sessão reconstruída
        return cls(
            version=data.get("version", "1.0.0"),
            name=data.get("name", "Gravação sem nome"),
            description=data.get("description", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            record_mouse=settings.get("record_mouse", True),
            record_keyboard=settings.get("record_keyboard", True),
            events=events,
        )

    def save(self, filepath: str) -> bool:
        """
        Salva a sessão de gravação em um arquivo JSON.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método pega toda a gravação e salva em um arquivo no seu
        computador. O arquivo fica em formato JSON, que é basicamente
        texto organizado que pode ser aberto em qualquer editor.
        
        Você escolhe onde salvar passando o caminho do arquivo.
        Exemplo: "C:/Minhas Gravações/formulario.json"
        
        EXPLICAÇÃO TÉCNICA:
        Serializa a sessão para JSON e escreve no sistema de arquivos.
        Usa indentação para legibilidade e ensure_ascii=False para
        suportar caracteres Unicode (acentos, emojis, etc.).
        
        Args:
            filepath (str): Caminho completo onde o arquivo será salvo
        
        Returns:
            bool: True se salvou com sucesso, False se houve erro
        
        Raises:
            Não levanta exceções - erros são capturados e retorna False
        """
        try:
            # Abre o arquivo para escrita ('w' = write)
            # encoding='utf-8' garante suporte a caracteres especiais
            with open(filepath, 'w', encoding='utf-8') as f:
                # json.dump converte o dicionário para JSON e escreve no arquivo
                json.dump(
                    self.to_dict(),     # O que salvar (nossa sessão como dict)
                    f,                  # Onde salvar (o arquivo aberto)
                    indent=2,           # Indentação de 2 espaços (fica bonito)
                    ensure_ascii=False  # Permite acentos e caracteres especiais
                )
            return True  # Sucesso!
            
        except Exception as e:
            # Se algo der errado (permissão, disco cheio, etc.)
            print(f"Erro ao salvar gravação: {e}")  # Mostra o erro no console
            return False  # Indica que falhou

    @classmethod
    def load(cls, filepath: str) -> Optional["RecordingSession"]:
        """
        Carrega uma sessão de gravação de um arquivo JSON.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método faz o oposto do save() - ele lê um arquivo de
        gravação que foi salvo anteriormente e reconstrói toda a
        sessão na memória para poder ser reproduzida.
        
        É como abrir um álbum de fotos que estava guardado.
        
        EXPLICAÇÃO TÉCNICA:
        Lê o arquivo JSON e deserializa de volta para objetos Python.
        Retorna None em caso de erro para permitir tratamento pelo chamador.
        
        Args:
            filepath (str): Caminho do arquivo a ser carregado
        
        Returns:
            Optional[RecordingSession]: A sessão carregada, ou None se falhar
        """
        try:
            # Abre o arquivo para leitura ('r' = read)
            with open(filepath, 'r', encoding='utf-8') as f:
                # json.load lê o JSON e converte para dicionário Python
                data = json.load(f)
            
            # Usa from_dict para criar a sessão a partir dos dados
            return cls.from_dict(data)
            
        except Exception as e:
            # Se algo der errado (arquivo não existe, JSON inválido, etc.)
            print(f"Erro ao carregar gravação: {e}")
            return None  # Retorna None para indicar falha


# ============================================================================
# BLOCO DE TESTE - Executado apenas quando este arquivo é rodado diretamente
# ============================================================================

if __name__ == "__main__":
    # Este bloco só executa se você rodar: python events.py
    # Não executa quando o módulo é importado por outro arquivo
    
    print("=== Teste do módulo events.py ===\n")
    
    # Criando alguns eventos de teste
    event1 = InputEvent(
        timestamp=0.0,
        event_type=EventType.MOUSE_MOVE,
        x=100,
        y=200
    )
    print(f"Evento 1 (movimento): {event1}")
    
    event2 = InputEvent(
        timestamp=0.5,
        event_type=EventType.MOUSE_CLICK,
        x=100,
        y=200,
        button='left',
        pressed=True
    )
    print(f"Evento 2 (clique): {event2}")
    
    event3 = InputEvent(
        timestamp=1.0,
        event_type=EventType.KEY_PRESS,
        key='a',
        pressed=True
    )
    print(f"Evento 3 (tecla): {event3}")
    
    # Criando uma sessão de gravação
    session = RecordingSession(
        name="Teste de Gravação",
        description="Uma gravação de exemplo para teste"
    )
    
    # Adicionando os eventos
    session.add_event(event1)
    session.add_event(event2)
    session.add_event(event3)
    
    print(f"\nSessão criada: {session.name}")
    print(f"Eventos gravados: {len(session.events)}")
    print(f"Duração: {session.get_duration()} segundos")
    
    # Testando conversão para dict
    session_dict = session.to_dict()
    print(f"\nJSON da sessão:")
    print(json.dumps(session_dict, indent=2))
    
    print("\n=== Testes concluídos com sucesso! ===")
