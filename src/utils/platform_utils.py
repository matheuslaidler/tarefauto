# ============================================================================
# TarefAuto - Utilitários de Plataforma (platform_utils.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este módulo ajuda o programa a funcionar em diferentes sistemas operacionais
# (Windows, Linux, macOS). Cada sistema tem suas particularidades, e este
# código detecta em qual sistema você está e ajusta comportamentos conforme
# necessário.
#
# Por exemplo: abrir uma pasta no Windows usa "explorer", no Linux usa
# "xdg-open", e no macOS usa "open". Este módulo sabe qual usar!
#
# EXPLICAÇÃO TÉCNICA:
# Fornece abstrações para operações específicas de sistema operacional,
# detecção de ambiente (X11/Wayland no Linux), e verificação de requisitos.
#
# ============================================================================

"""
Utilitários específicos de plataforma para o TarefAuto.

Este módulo fornece funções auxiliares para detectar e trabalhar com
diferentes sistemas operacionais de forma transparente.

Classes:
    PlatformUtils: Utilitários estáticos para operações de plataforma

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# sys: Informações sobre o sistema Python e plataforma
import sys

# os: Operações do sistema operacional
import os

# subprocess: Para executar comandos externos
import subprocess

# platform: Informações detalhadas sobre a plataforma
import platform

# typing: Anotações de tipo
from typing import Optional, Tuple, Dict


# ============================================================================
# CLASSE PLATFORM UTILS
# ============================================================================

class PlatformUtils:
    """
    Utilitários estáticos para operações específicas de plataforma.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta classe contém várias funções úteis que funcionam em qualquer
    sistema operacional. Por exemplo:
    - Descobrir qual sistema você está usando
    - Abrir pastas no explorador de arquivos
    - Verificar se o ambiente está configurado corretamente
    
    Todas as funções são "estáticas" (@staticmethod), o que significa
    que você não precisa criar um objeto para usá-las:
        PlatformUtils.get_os_name()  # Funciona diretamente!
    
    EXPLICAÇÃO TÉCNICA:
    Classe utilitária com métodos estáticos que abstraem diferenças entre
    sistemas operacionais. Evita lógica condicional espalhada pelo código.
    
    Example:
        >>> PlatformUtils.get_os_name()
        'Windows'
        >>> PlatformUtils.is_windows()
        True
        >>> PlatformUtils.open_folder("C:/Users")
    """
    
    @staticmethod
    def get_os_name() -> str:
        """
        Retorna o nome do sistema operacional.
        
        EXPLICAÇÃO PARA INICIANTES:
        Diz qual sistema operacional você está usando:
        - "Windows" para Windows
        - "Linux" para Linux (Ubuntu, Fedora, etc.)
        - "macOS" para Mac
        
        EXPLICAÇÃO TÉCNICA:
        Mapeia sys.platform para nome legível.
        
        Returns:
            str: Nome do sistema operacional ("Windows", "Linux", "macOS", "Unknown")
        """
        # sys.platform retorna strings como 'win32', 'linux', 'darwin'
        if sys.platform == "win32":
            return "Windows"
        elif sys.platform == "darwin":
            return "macOS"
        elif sys.platform.startswith("linux"):
            return "Linux"
        else:
            return "Unknown"

    @staticmethod
    def is_windows() -> bool:
        """
        Verifica se está rodando no Windows.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna True se você está no Windows, False caso contrário.
        
        EXPLICAÇÃO TÉCNICA:
        Verifica sys.platform para 'win32'.
        
        Returns:
            bool: True se Windows, False caso contrário
        """
        return sys.platform == "win32"

    @staticmethod
    def is_linux() -> bool:
        """
        Verifica se está rodando no Linux.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna True se você está no Linux, False caso contrário.
        
        Returns:
            bool: True se Linux, False caso contrário
        """
        return sys.platform.startswith("linux")

    @staticmethod
    def is_macos() -> bool:
        """
        Verifica se está rodando no macOS.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna True se você está no Mac, False caso contrário.
        
        Returns:
            bool: True se macOS, False caso contrário
        """
        return sys.platform == "darwin"

    @staticmethod
    def get_display_server() -> Optional[str]:
        """
        Detecta o servidor de display no Linux (X11 ou Wayland).
        
        EXPLICAÇÃO PARA INICIANTES:
        No Linux, existem dois sistemas que controlam a interface gráfica:
        - X11: O mais antigo e mais compatível (recomendado para TarefAuto)
        - Wayland: O mais novo, mas pynput não funciona bem com ele
        
        Esta função descobre qual você está usando. Se não for Linux,
        retorna None (não aplicável).
        
        EXPLICAÇÃO TÉCNICA:
        Verifica as variáveis de ambiente XDG_SESSION_TYPE e WAYLAND_DISPLAY
        para determinar o servidor de display em uso.
        
        Returns:
            Optional[str]: "X11", "Wayland", ou None se não for Linux
        """
        if not PlatformUtils.is_linux():
            return None
        
        # Verifica a variável de ambiente XDG_SESSION_TYPE
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        
        if session_type == "x11":
            return "X11"
        elif session_type == "wayland":
            return "Wayland"
        
        # Fallback: verifica se WAYLAND_DISPLAY está definido
        if os.environ.get("WAYLAND_DISPLAY"):
            return "Wayland"
        
        # Fallback: assume X11 se DISPLAY estiver definido
        if os.environ.get("DISPLAY"):
            return "X11"
        
        return None

    @staticmethod
    def is_wayland() -> bool:
        """
        Verifica se está usando Wayland (Linux).
        
        EXPLICAÇÃO PARA INICIANTES:
        Wayland é um sistema mais novo no Linux que ainda não funciona
        bem com o pynput. Esta função verifica se você está usando
        Wayland para podermos avisar que pode haver problemas.
        
        EXPLICAÇÃO TÉCNICA:
        Usa get_display_server() para verificar se é Wayland.
        
        Returns:
            bool: True se estiver usando Wayland
        """
        return PlatformUtils.get_display_server() == "Wayland"

    @staticmethod
    def check_requirements() -> Dict[str, bool]:
        """
        Verifica se os requisitos do sistema estão presentes.
        
        EXPLICAÇÃO PARA INICIANTES:
        Verifica se seu sistema tem tudo necessário para rodar o TarefAuto.
        Retorna um dicionário dizendo o que está OK e o que não está.
        
        EXPLICAÇÃO TÉCNICA:
        Verifica:
        - Versão do Python (3.8+)
        - Bibliotecas necessárias (pynput, customtkinter)
        - Servidor de display no Linux
        
        Returns:
            Dict[str, bool]: Dicionário com status de cada requisito
        """
        requirements = {}
        
        # Verifica versão do Python
        # Precisamos de Python 3.8 ou superior
        python_version = sys.version_info
        requirements["python_3.8+"] = python_version >= (3, 8)
        
        # Verifica pynput
        try:
            import pynput
            requirements["pynput"] = True
        except ImportError:
            requirements["pynput"] = False
        
        # Verifica customtkinter
        try:
            import customtkinter
            requirements["customtkinter"] = True
        except ImportError:
            requirements["customtkinter"] = False
        
        # Verifica Pillow
        try:
            from PIL import Image
            requirements["pillow"] = True
        except ImportError:
            requirements["pillow"] = False
        
        # Verifica servidor de display no Linux
        if PlatformUtils.is_linux():
            display_server = PlatformUtils.get_display_server()
            requirements["linux_x11"] = display_server == "X11"
            requirements["linux_wayland_warning"] = display_server == "Wayland"
        
        return requirements

    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """
        Obtém informações detalhadas sobre o sistema.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna várias informações sobre seu computador e sistema.
        Útil para diagnósticos e relatórios de bugs.
        
        EXPLICAÇÃO TÉCNICA:
        Coleta informações usando os módulos platform e sys.
        
        Returns:
            Dict[str, str]: Dicionário com informações do sistema
        """
        info = {
            "os_name": PlatformUtils.get_os_name(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
        }
        
        # Adiciona info específica de Linux
        if PlatformUtils.is_linux():
            info["display_server"] = PlatformUtils.get_display_server() or "Unknown"
            
            # Tenta obter nome da distribuição
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            info["linux_distro"] = line.split("=")[1].strip().strip('"')
                            break
            except Exception:
                pass
        
        return info

    @staticmethod
    def get_platform_info() -> Dict[str, str]:
        """
        Obtém informações da plataforma para exibição na interface.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna informações simplificadas sobre o sistema para mostrar
        na tela de configurações. Similar a get_system_info mas mais
        amigável para exibição.
        
        EXPLICAÇÃO TÉCNICA:
        Coleta informações resumidas do sistema para display na UI.
        
        Returns:
            Dict[str, str]: Dicionário com informações da plataforma
        """
        info = {
            "sistema_operacional": PlatformUtils.get_os_name(),
            "versao_so": platform.release(),
            "arquitetura": platform.machine(),
            "python": platform.python_version(),
        }
        
        # Adiciona info específica de Linux
        if PlatformUtils.is_linux():
            display_server = PlatformUtils.get_display_server()
            info["servidor_display"] = display_server or "Desconhecido"
            info["wayland_detected"] = display_server == "Wayland"
        
        return info

    @staticmethod
    def open_folder(path: str) -> bool:
        """
        Abre uma pasta no explorador de arquivos do sistema.
        
        EXPLICAÇÃO PARA INICIANTES:
        Abre uma pasta no programa que mostra arquivos e pastas:
        - Windows: Explorador de Arquivos
        - Linux: Nautilus, Dolphin, ou outro
        - Mac: Finder
        
        EXPLICAÇÃO TÉCNICA:
        Usa o comando apropriado do sistema para abrir o gerenciador
        de arquivos. Executa de forma não-bloqueante.
        
        Args:
            path (str): Caminho da pasta a ser aberta
        
        Returns:
            bool: True se abriu com sucesso
        """
        try:
            if PlatformUtils.is_windows():
                # Windows: usa o comando 'explorer'
                subprocess.Popen(["explorer", path])
            elif PlatformUtils.is_macos():
                # macOS: usa o comando 'open'
                subprocess.Popen(["open", path])
            else:
                # Linux: usa xdg-open (funciona na maioria das distros)
                subprocess.Popen(["xdg-open", path])
            
            return True
            
        except Exception as e:
            print(f"Erro ao abrir pasta: {e}")
            return False

    @staticmethod
    def open_url(url: str) -> bool:
        """
        Abre uma URL no navegador padrão.
        
        EXPLICAÇÃO PARA INICIANTES:
        Abre um site no seu navegador de internet preferido.
        
        EXPLICAÇÃO TÉCNICA:
        Usa o módulo webbrowser para abrir URLs de forma cross-platform.
        
        Args:
            url (str): URL a ser aberta
        
        Returns:
            bool: True se abriu com sucesso
        """
        try:
            import webbrowser
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Erro ao abrir URL: {e}")
            return False

    @staticmethod
    def get_keyboard_layout() -> str:
        """
        Tenta detectar o layout do teclado.
        
        EXPLICAÇÃO PARA INICIANTES:
        Diferentes países usam diferentes layouts de teclado (QWERTY,
        AZERTY, ABNT2, etc.). Esta função tenta descobrir qual você usa.
        
        NOTA: A detecção nem sempre é precisa em todos os sistemas.
        
        EXPLICAÇÃO TÉCNICA:
        Usa APIs específicas do sistema para detectar o layout.
        Fallback para "Unknown" se não conseguir detectar.
        
        Returns:
            str: Nome do layout ou "Unknown"
        """
        try:
            if PlatformUtils.is_windows():
                # Windows: usa a API de sistema
                import ctypes
                
                # GetKeyboardLayout retorna o ID do layout
                user32 = ctypes.windll.user32
                layout_id = user32.GetKeyboardLayout(0)
                
                # O ID é um valor hexadecimal, convertemos para string
                # Os primeiros bytes indicam o idioma
                lang_id = layout_id & 0xFFFF
                
                # Mapa básico de IDs para nomes (simplificado)
                layout_map = {
                    0x0409: "US English (QWERTY)",
                    0x0416: "Brazilian Portuguese (ABNT2)",
                    0x0809: "UK English",
                    0x040C: "French (AZERTY)",
                    0x0407: "German (QWERTZ)",
                    0x0410: "Italian",
                    0x0C0A: "Spanish",
                    0x0816: "Portuguese",
                }
                
                return layout_map.get(lang_id, f"Unknown (0x{lang_id:04X})")
            
            elif PlatformUtils.is_linux():
                # Linux: usa setxkbmap para obter info
                result = subprocess.run(
                    ["setxkbmap", "-query"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.startswith("layout:"):
                            return line.split(":")[1].strip()
                
            return "Unknown"
            
        except Exception:
            return "Unknown"

    @staticmethod
    def get_warnings() -> list:
        """
        Retorna lista de avisos sobre a plataforma atual.
        
        EXPLICAÇÃO PARA INICIANTES:
        Verifica se há problemas conhecidos com seu sistema e retorna
        uma lista de avisos para você ficar ciente.
        
        EXPLICAÇÃO TÉCNICA:
        Coleta avisos baseados em verificações de plataforma.
        
        Returns:
            list: Lista de strings com avisos
        """
        warnings = []
        
        # Aviso de Wayland
        if PlatformUtils.is_wayland():
            warnings.append(
                "⚠️ Wayland detectado: O TarefAuto funciona melhor com X11. "
                "A captura de mouse/teclado pode não funcionar corretamente em Wayland. "
                "Considere usar uma sessão X11 ou Xwayland."
            )
        
        # Verifica requisitos
        reqs = PlatformUtils.check_requirements()
        
        if not reqs.get("pynput", False):
            warnings.append(
                "⚠️ pynput não encontrado: Instale com 'pip install pynput'"
            )
        
        if not reqs.get("customtkinter", False):
            warnings.append(
                "⚠️ customtkinter não encontrado: Instale com 'pip install customtkinter'"
            )
        
        if not reqs.get("python_3.8+", True):
            warnings.append(
                "⚠️ Python 3.8 ou superior é necessário"
            )
        
        return warnings


# ============================================================================
# BLOCO DE TESTE
# ============================================================================

if __name__ == "__main__":
    print("=== Teste do módulo platform_utils.py ===")
    print()
    
    # Informações básicas
    print("Informações do Sistema:")
    print(f"  Sistema Operacional: {PlatformUtils.get_os_name()}")
    print(f"  É Windows: {PlatformUtils.is_windows()}")
    print(f"  É Linux: {PlatformUtils.is_linux()}")
    print(f"  É macOS: {PlatformUtils.is_macos()}")
    
    if PlatformUtils.is_linux():
        print(f"  Servidor de Display: {PlatformUtils.get_display_server()}")
        print(f"  É Wayland: {PlatformUtils.is_wayland()}")
    
    print()
    
    # Informações detalhadas
    print("Informações Detalhadas:")
    info = PlatformUtils.get_system_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print()
    
    # Verificação de requisitos
    print("Verificação de Requisitos:")
    reqs = PlatformUtils.check_requirements()
    for req, status in reqs.items():
        icon = "✓" if status else "✗"
        print(f"  {icon} {req}")
    
    print()
    
    # Layout do teclado
    print(f"Layout do Teclado: {PlatformUtils.get_keyboard_layout()}")
    
    print()
    
    # Avisos
    warnings = PlatformUtils.get_warnings()
    if warnings:
        print("Avisos:")
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("Nenhum aviso!")
    
    print()
    print("=== Teste concluído! ===")
