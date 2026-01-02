# ============================================================================
# TarefAuto - Ponto de Entrada Principal (main.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este é o arquivo que você executa para iniciar o programa TarefAuto!
# 
# Para executar, abra um terminal/cmd na pasta do projeto e digite:
#   python main.py
#
# Ou, se você criou um executável com PyInstaller, simplesmente clique
# duas vezes no arquivo .exe.
#
# Este arquivo faz as seguintes coisas:
# 1. Verifica se você tem Python na versão correta (3.8+)
# 2. Verifica se todas as bibliotecas necessárias estão instaladas
# 3. Mostra mensagens úteis se algo estiver faltando
# 4. Inicia a interface gráfica do programa
#
# EXPLICAÇÃO TÉCNICA:
# Entry point da aplicação. Realiza verificações de ambiente antes de
# iniciar a GUI. Usa importação lazy para otimizar tempo de startup
# e verificar dependências apenas quando necessário.
#
# ============================================================================

"""
Ponto de entrada do TarefAuto.

Este é o arquivo principal que deve ser executado para iniciar
o aplicativo TarefAuto.

Uso:
    python main.py

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES DE SISTEMA (sempre disponíveis)
# ============================================================================

import sys         # Acesso a funcionalidades do sistema Python
import os          # Operações do sistema operacional
import platform    # Informações da plataforma (Windows, Linux, etc)


# ============================================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================================

# Versão mínima do Python requerida
MIN_PYTHON_VERSION = (3, 8)

# Nome do aplicativo (usado em mensagens)
APP_NAME = "TarefAuto"


# ============================================================================
# FUNÇÕES DE VERIFICAÇÃO
# ============================================================================

def check_python_version() -> bool:
    """
    Verifica se a versão do Python é compatível.
    
    EXPLICAÇÃO PARA INICIANTES:
    O TarefAuto precisa do Python 3.8 ou superior para funcionar.
    Esta função verifica se você tem a versão correta instalada.
    
    Se você ver um erro de versão, baixe o Python mais recente em:
    https://www.python.org/downloads/
    
    EXPLICAÇÃO TÉCNICA:
    Compara sys.version_info com MIN_PYTHON_VERSION usando
    comparação de tuplas.
    
    Returns:
        bool: True se versão é compatível, False caso contrário
    """
    # sys.version_info é uma tupla: (major, minor, micro, ...)
    # Exemplo: Python 3.10.5 = (3, 10, 5, ...)
    
    current_version = sys.version_info[:2]  # Pega apenas (major, minor)
    
    if current_version < MIN_PYTHON_VERSION:
        # Versão incompatível - mostra erro e instruções
        print("=" * 60)
        print(f"ERRO: Versão do Python incompatível!")
        print("=" * 60)
        print(f"")
        print(f"Versão atual:   Python {current_version[0]}.{current_version[1]}")
        print(f"Versão mínima:  Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}")
        print(f"")
        print(f"Por favor, atualize seu Python:")
        print(f"https://www.python.org/downloads/")
        print("=" * 60)
        return False
    
    return True


def check_dependencies() -> bool:
    """
    Verifica se todas as dependências estão instaladas.
    
    EXPLICAÇÃO PARA INICIANTES:
    O TarefAuto usa algumas bibliotecas externas (pynput, customtkinter).
    Esta função verifica se elas estão instaladas.
    
    Se alguma estiver faltando, mostra como instalar:
    pip install -r requirements.txt
    
    EXPLICAÇÃO TÉCNICA:
    Tenta importar cada dependência e captura ImportError para
    dependências faltantes. Mostra instruções de instalação.
    
    Returns:
        bool: True se todas as dependências estão OK, False caso contrário
    """
    # Lista de dependências necessárias
    # Formato: (nome do pacote para import, nome do pacote para pip)
    dependencies = [
        ("pynput", "pynput"),
        ("customtkinter", "customtkinter"),
        ("PIL", "Pillow"),  # PIL é o módulo, Pillow é o pacote pip
    ]
    
    missing = []
    
    for import_name, pip_name in dependencies:
        try:
            # Tenta importar o módulo
            __import__(import_name)
        except ImportError:
            # Não encontrou - adiciona à lista de faltantes
            missing.append(pip_name)
    
    if missing:
        # Tem dependências faltando - mostra erro e instruções
        print("=" * 60)
        print(f"ERRO: Dependências faltando!")
        print("=" * 60)
        print(f"")
        print(f"Os seguintes pacotes não estão instalados:")
        for pkg in missing:
            print(f"  • {pkg}")
        print(f"")
        print(f"Para instalar, execute um dos comandos abaixo:")
        print(f"")
        print(f"  Opção 1 - Instalar tudo de uma vez:")
        print(f"    pip install -r requirements.txt")
        print(f"")
        print(f"  Opção 2 - Instalar manualmente:")
        print(f"    pip install {' '.join(missing)}")
        print(f"")
        
        # Dica específica para cada sistema
        system = platform.system()
        if system == "Windows":
            print(f"  Dica para Windows:")
            print(f"    Se 'pip' não funcionar, tente 'py -m pip install ...'")
        elif system == "Linux":
            print(f"  Dica para Linux:")
            print(f"    Se 'pip' não funcionar, tente 'pip3 install ...'")
            print(f"    Você pode precisar de: sudo apt install python3-tk")
        
        print("=" * 60)
        return False
    
    return True


def check_platform_compatibility() -> bool:
    """
    Verifica compatibilidade da plataforma e mostra avisos se necessário.
    
    EXPLICAÇÃO PARA INICIANTES:
    O TarefAuto funciona em Windows, Linux e macOS, mas com algumas
    diferenças. Esta função mostra avisos importantes para sua plataforma.
    
    - Windows: Funciona perfeitamente ✅
    - Linux (X11): Funciona bem ✅
    - Linux (Wayland): Funcionalidade limitada ⚠️
    - macOS: Precisa de permissões especiais ⚠️
    
    EXPLICAÇÃO TÉCNICA:
    Detecta a plataforma e compositor de display (Linux) para
    exibir avisos relevantes ao usuário.
    
    Returns:
        bool: True (sempre, apenas mostra avisos)
    """
    system = platform.system()
    
    if system == "Linux":
        # Verifica se está usando Wayland
        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        xdg_session = os.environ.get("XDG_SESSION_TYPE", "")
        
        if wayland_display or xdg_session.lower() == "wayland":
            print("=" * 60)
            print("⚠️  AVISO: Sessão Wayland detectada")
            print("=" * 60)
            print("")
            print("O TarefAuto funciona melhor com X11.")
            print("No Wayland, a captura global de eventos pode não funcionar.")
            print("")
            print("Opções:")
            print("  1. Execute em uma sessão X11 (Xorg)")
            print("  2. Use XWayland para apps específicos")
            print("")
            print("O programa tentará funcionar, mas pode haver limitações.")
            print("=" * 60)
            print("")
    
    elif system == "Darwin":  # macOS
        print("=" * 60)
        print("ℹ️  AVISO: macOS detectado")
        print("=" * 60)
        print("")
        print("No macOS, você precisa conceder permissões de acessibilidade")
        print("ao terminal ou ao Python para capturar eventos de teclado.")
        print("")
        print("Vá em: Preferências do Sistema > Segurança e Privacidade")
        print("       > Privacidade > Acessibilidade")
        print("")
        print("E adicione o Terminal ou Python à lista de apps permitidos.")
        print("=" * 60)
        print("")
    
    return True


def show_startup_banner() -> None:
    """
    Mostra o banner de inicialização do programa.
    
    EXPLICAÇÃO PARA INICIANTES:
    Mostra uma mensagem bonita quando o programa inicia, com o nome,
    versão e informações úteis.
    
    EXPLICAÇÃO TÉCNICA:
    Imprime ASCII art e informações do projeto no console.
    """
    # Banner simples em ASCII - TAREFAUTO
    banner = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║  ████████╗ █████╗ ██████╗ ███████╗███████╗ █████╗ ██╗   ██╗████████╗ ██████╗   ║
║  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗  ║
║     ██║   ███████║██████╔╝█████╗  █████╗  ███████║██║   ██║   ██║   ██║   ██║  ║
║     ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██║██║   ██║   ██║   ██║   ██║  ║
║     ██║   ██║  ██║██║  ██║███████╗██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝  ║
║     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝   ║
║                                                                                ║
║                   🤖 Automação de Tarefas Repetitivas 🤖                       ║
║                                                                                ║
║                          Desenvolvido por:                                     ║
║                          Matheus Laidler                                       ║
║                https://github.com/matheuslaidler/tarefauto                     ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main() -> int:
    """
    Função principal - ponto de entrada do programa.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta é a função que "roda tudo". Ela:
    1. Mostra o banner de boas-vindas
    2. Verifica se tudo está instalado corretamente
    3. Inicia a interface gráfica
    
    Se algo der errado, mostra uma mensagem explicando o problema.
    
    EXPLICAÇÃO TÉCNICA:
    Entry point que realiza verificações e inicia a aplicação.
    Retorna código de saída (0 = sucesso, 1 = erro).
    
    Returns:
        int: Código de saída (0 = sucesso, 1 = erro)
    """
    # Mostra o banner
    show_startup_banner()
    
    print("Iniciando verificações...")
    print("")
    
    # ========================================================================
    # VERIFICAÇÃO 1: Versão do Python
    # ========================================================================
    
    print("[1/3] Verificando versão do Python...", end=" ")
    if not check_python_version():
        return 1
    print(f"✅ Python {sys.version_info[0]}.{sys.version_info[1]}")
    
    # ========================================================================
    # VERIFICAÇÃO 2: Dependências
    # ========================================================================
    
    print("[2/3] Verificando dependências...", end=" ")
    if not check_dependencies():
        return 1
    print("✅ Todas instaladas")
    
    # ========================================================================
    # VERIFICAÇÃO 3: Plataforma
    # ========================================================================
    
    print("[3/3] Verificando plataforma...", end=" ")
    check_platform_compatibility()
    print(f"✅ {platform.system()}")
    
    print("")
    print("=" * 60)
    print("Iniciando interface gráfica...")
    print("=" * 60)
    print("")
    
    # ========================================================================
    # INICIA A APLICAÇÃO
    # ========================================================================
    
    try:
        # Importa aqui (lazy import) para só carregar depois das verificações
        from src.gui.main_window import MainWindow
        
        # Cria a janela principal
        app = MainWindow()
        
        # Executa o loop principal da interface
        # mainloop() bloqueia até a janela ser fechada
        app.mainloop()
        
        print("")
        print("=" * 60)
        print("TarefAuto encerrado. Até a próxima! 👋")
        print("=" * 60)
        
        return 0  # Sucesso
        
    except Exception as e:
        # Algum erro inesperado aconteceu
        print("")
        print("=" * 60)
        print("❌ ERRO INESPERADO!")
        print("=" * 60)
        print(f"")
        print(f"Ocorreu um erro ao iniciar o TarefAuto:")
        print(f"")
        print(f"  {type(e).__name__}: {e}")
        print(f"")
        print(f"Se o problema persistir, por favor abra uma issue no GitHub:")
        print(f"https://github.com/matheuslaidler/tarefauto/issues")
        print(f"")
        print(f"Inclua a mensagem de erro acima e descreva o que você")
        print(f"estava fazendo quando o erro aconteceu.")
        print("=" * 60)
        
        # Para debug, imprime o traceback completo
        import traceback
        print("\nTraceback completo (para debug):")
        traceback.print_exc()
        
        return 1  # Erro


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    """
    EXPLICAÇÃO PARA INICIANTES:
    Este bloco só executa quando você roda o arquivo diretamente:
      python main.py
    
    Não executa se você importar este arquivo de outro lugar.
    O sys.exit() finaliza o programa com o código de retorno apropriado.
    
    EXPLICAÇÃO TÉCNICA:
    Padrão Python para entry point. O código de saída é usado pelo
    sistema operacional (0 = sucesso, outros = erro).
    """
    sys.exit(main())
