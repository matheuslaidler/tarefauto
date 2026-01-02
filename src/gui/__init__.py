# ============================================================================
# TarefAuto - Módulo de Inicialização do Pacote GUI
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# A pasta "gui" contém todo o código da interface gráfica do programa -
# os botões, janelas, abas e tudo que você vê e clica na tela.
#
# Organizamos em vários arquivos:
# - theme.py: Define as cores e estilos (a "cara" do programa)
# - main_window.py: A janela principal que contém tudo
# - recording_tab.py: Aba para configurar e iniciar gravações
# - playback_tab.py: Aba para configurar e iniciar reproduções
# - settings_tab.py: Aba para configurar atalhos e outras opções
#
# ============================================================================

"""
Módulo de Interface Gráfica do TarefAuto.

Este pacote contém todos os componentes da interface gráfica do usuário,
construída com CustomTkinter para uma aparência moderna e suporte a temas.

Módulos:
    theme: Definição de cores, fontes e estilos
    main_window: Janela principal da aplicação
    recording_tab: Aba de controle de gravação
    playback_tab: Aba de controle de reprodução
    settings_tab: Aba de configurações gerais
"""

from src.gui.theme import TarefAutoTheme
from src.gui.main_window import MainWindow
from src.gui.recording_tab import RecordingTab
from src.gui.playback_tab import PlaybackTab
from src.gui.settings_tab import SettingsTab

__all__ = [
    "TarefAutoTheme",
    "MainWindow",
    "RecordingTab",
    "PlaybackTab",
    "SettingsTab",
]
