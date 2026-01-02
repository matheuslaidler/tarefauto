# ============================================================================
# TarefAuto - Módulo de Inicialização do Pacote src
# ============================================================================
# 
# EXPLICAÇÃO PARA INICIANTES:
# Este arquivo __init__.py é especial em Python. Ele transforma uma pasta
# comum em um "pacote Python" - uma coleção organizada de módulos (arquivos .py).
# Quando você vê uma pasta com __init__.py dentro, significa que você pode
# importar código dessa pasta como se fosse uma biblioteca.
#
# Por exemplo, graças a este arquivo, podemos fazer:
#   from src.core import Recorder
#   from src.gui import MainWindow
#
# Mesmo que este arquivo esteja vazio, ele é essencial para que Python
# reconheça a pasta como um pacote importável.
#
# ============================================================================
# 
# EXPLICAÇÃO TÉCNICA:
# O __init__.py serve como ponto de entrada do pacote. Quando alguém importa
# o pacote, este arquivo é executado primeiro. Podemos usar isso para:
# 1. Expor classes/funções importantes no nível do pacote
# 2. Inicializar configurações do pacote
# 3. Definir __all__ para controlar o que é exportado com "from pkg import *"
#
# ============================================================================

"""
TarefAuto - Ferramenta de Automação de Tarefas

Este é o pacote principal do TarefAuto, uma aplicação para gravação e
reprodução de ações de mouse e teclado para automação de tarefas repetitivas.

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler
Repositório: https://github.com/matheuslaidler/tarefauto
"""

# Informações do pacote - usadas para identificar a versão e autor
__version__ = "1.0.0"  # Versão atual do software (Major.Minor.Patch)
__author__ = "Matheus Laidler"  # Autor do projeto
__github__ = "https://github.com/matheuslaidler"  # Perfil do GitHub
__repo__ = "https://github.com/matheuslaidler/tarefauto"  # Repositório do projeto
