# ============================================================================
# TarefAuto - Módulo de Inicialização do Pacote Utils
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# A pasta "utils" (utilitários) contém funções e classes auxiliares que
# são usadas em várias partes do programa. São ferramentas de apoio, como:
# - config.py: Salva e carrega configurações do usuário
# - platform.py: Detecta o sistema operacional e ajusta comportamentos
#
# É como uma caixa de ferramentas que os outros módulos usam quando precisam.
#
# ============================================================================

"""
Módulo de utilitários do TarefAuto.

Este pacote contém funções auxiliares e classes de suporte utilizadas
por outros módulos do sistema.

Módulos:
    config: Gerenciamento de configurações do usuário
    platform: Detecção e utilitários específicos de plataforma
"""

from src.utils.config import Config
from src.utils.platform_utils import PlatformUtils

__all__ = [
    "Config",
    "PlatformUtils",
]
