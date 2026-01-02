# ============================================================================
# TarefAuto - Módulo de Inicialização do Pacote Core
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# A pasta "core" contém o "coração" do programa - a lógica principal que faz
# a mágica acontecer. Aqui ficam os códigos responsáveis por:
# - Gravar o que você faz com mouse e teclado (recorder.py)
# - Reproduzir as ações gravadas (player.py)
# - Gerenciar os atalhos de teclado globais (hotkeys.py)
# - Definir como os eventos são estruturados (events.py)
#
# Este arquivo __init__.py facilita a importação dessas funcionalidades.
# Em vez de escrever: from src.core.recorder import Recorder
# Você pode escrever: from src.core import Recorder
#
# ============================================================================

"""
Módulo Core do TarefAuto

Este módulo contém toda a lógica principal de gravação, reprodução
e gerenciamento de hotkeys para automação de tarefas.
"""

# Importações expostas no nível do pacote para facilitar o uso
# Quando alguém fizer "from src.core import X", esses itens estarão disponíveis
from src.core.events import InputEvent, RecordingSession
from src.core.recorder import Recorder
from src.core.player import Player
from src.core.hotkeys import HotkeyManager

# __all__ define explicitamente o que é exportado quando alguém usa
# "from src.core import *" - isso é uma boa prática de segurança
__all__ = [
    "InputEvent",        # Classe que representa um único evento (clique, tecla, etc)
    "RecordingSession",  # Classe que representa uma gravação completa
    "Recorder",          # Classe responsável por gravar ações
    "Player",            # Classe responsável por reproduzir ações
    "HotkeyManager",     # Classe que gerencia atalhos de teclado globais
]
