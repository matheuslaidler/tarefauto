# ============================================================================
# TarefAuto - Módulo de Hotkeys Globais (hotkeys.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# "Hotkeys" são atalhos de teclado - combinações de teclas que você aperta
# para fazer algo acontecer. Por exemplo, Ctrl+C para copiar.
#
# Este módulo permite que você defina atalhos personalizados para controlar
# o TarefAuto mesmo quando a janela do programa não está em foco. Isso é
# chamado de "hotkeys globais" - funcionam em qualquer lugar do sistema.
#
# Exemplos de uso:
# - Ctrl+Shift+R para iniciar/parar gravação
# - Ctrl+Shift+P para iniciar/parar reprodução
# - Escape para parar tudo de emergência
#
# EXPLICAÇÃO TÉCNICA:
# Utiliza pynput.keyboard.GlobalHotKeys para registrar atalhos que funcionam
# em nível de sistema operacional. As hotkeys são processadas em uma thread
# separada para não bloquear a aplicação principal.
#
# ============================================================================

"""
Módulo de gerenciamento de hotkeys globais para o TarefAuto.

Este módulo contém a classe HotkeyManager, que gerencia atalhos de teclado
globais para controlar gravação e reprodução sem focar na janela do programa.

Classes:
    HotkeyManager: Gerencia registro e execução de hotkeys globais

Dependencies:
    - pynput: Para captura de hotkeys globais
    - threading: Para execução em background

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# threading: Para executar o listener em thread separada
import threading

# typing: Anotações de tipo
from typing import Dict, Callable, Optional, Set

# pynput: Para hotkeys globais
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, HotKey


# ============================================================================
# CLASSE HOTKEY MANAGER
# ============================================================================

class HotkeyManager:
    """
    Gerenciador de atalhos de teclado globais.
    
    EXPLICAÇÃO PARA INICIANTES:
    O HotkeyManager é como um "ouvinte" que fica prestando atenção em
    todas as teclas que você aperta, em qualquer lugar do computador.
    Quando você aperta uma combinação específica (como Ctrl+Shift+R),
    ele executa a ação que você configurou.
    
    Isso é útil porque você pode:
    - Iniciar uma gravação com um atalho, sem precisar clicar na janela
    - Parar uma reprodução de emergência, mesmo em outro programa
    - Controlar tudo pelo teclado de forma rápida
    
    EXPLICAÇÃO TÉCNICA:
    Implementa um sistema de hotkeys usando pynput.keyboard.Listener.
    Diferente de GlobalHotKeys do pynput (que tem limitações), este
    implementa detecção manual de combinações para maior flexibilidade.
    
    O listener roda em uma thread daemon, processando todas as teclas
    e verificando se alguma combinação configurada foi ativada.
    
    Attributes:
        _hotkeys (Dict): Mapa de combinação -> callback
        _pressed_keys (Set): Teclas atualmente pressionadas
        _listener (Listener): Listener do pynput
        _enabled (bool): Se as hotkeys estão ativadas
        _lock (Lock): Lock para thread-safety
    
    Example:
        >>> manager = HotkeyManager()
        >>> manager.register_hotkey('<ctrl>+<shift>+r', start_recording)
        >>> manager.register_hotkey('<escape>', stop_all)
        >>> manager.start()
        >>> # ... hotkeys funcionam globalmente ...
        >>> manager.stop()
    """
    
    def __init__(self):
        """
        Inicializa o gerenciador de hotkeys.
        
        EXPLICAÇÃO PARA INICIANTES:
        Prepara o sistema de atalhos para uso. Neste momento, nenhum
        atalho está registrado ainda - você precisa usar register_hotkey()
        para adicionar os atalhos que deseja.
        
        EXPLICAÇÃO TÉCNICA:
        Inicializa as estruturas de dados internas e o estado do manager.
        O listener não é criado aqui - é criado em start().
        """
        # ====================================================================
        # ARMAZENAMENTO DE HOTKEYS
        # ====================================================================
        
        # Dicionário que mapeia combinações para funções callback
        # Chave: string da combinação (ex: '<ctrl>+<shift>+r')
        # Valor: função a ser chamada quando a combinação for pressionada
        self._hotkeys: Dict[str, Callable[[], None]] = {}
        
        # Conjunto de teclas atualmente pressionadas
        # Usado para detectar combinações (Ctrl+Shift+R, por exemplo)
        self._pressed_keys: Set[str] = set()
        
        # ====================================================================
        # LISTENER DO PYNPUT
        # ====================================================================
        
        # O listener que observa todas as teclas
        # Será criado quando start() for chamado
        self._listener: Optional[keyboard.Listener] = None
        
        # ====================================================================
        # ESTADO
        # ====================================================================
        
        # Se as hotkeys estão ativadas (listener rodando)
        self._enabled = False
        
        # Se devemos processar hotkeys (pode ser desativado temporariamente)
        self._processing_enabled = True
        
        # ====================================================================
        # CONTROLE DE THREAD-SAFETY
        # ====================================================================
        
        # Lock para acessar _pressed_keys de forma segura
        self._lock = threading.Lock()

    def _normalize_key(self, key) -> str:
        """
        Converte uma tecla do pynput para string normalizada.
        
        EXPLICAÇÃO PARA INICIANTES:
        O pynput representa teclas de várias formas diferentes. Esta função
        converte qualquer formato para uma string padronizada que podemos
        comparar facilmente.
        
        Exemplos:
        - keyboard.Key.ctrl_l -> '<ctrl>'
        - keyboard.Key.shift -> '<shift>'
        - KeyCode(char='a') -> 'a'
        
        EXPLICAÇÃO TÉCNICA:
        Normaliza a representação de teclas para formato consistente.
        Teclas modificadoras (ctrl, shift, alt) são convertidas para
        versão genérica (sem _l ou _r).
        
        Args:
            key: Objeto tecla do pynput (Key ou KeyCode)
        
        Returns:
            str: Representação normalizada da tecla
        """
        try:
            # Se é um caractere normal (letra, número)
            if hasattr(key, 'char') and key.char is not None:
                return key.char.lower()  # Retorna em minúsculo
            
            # Se é uma tecla especial
            if hasattr(key, 'name'):
                name = key.name.lower()
                
                # Normaliza variações de teclas modificadoras
                # ctrl_l e ctrl_r viram apenas ctrl
                if name.startswith('ctrl'):
                    return '<ctrl>'
                elif name.startswith('shift'):
                    return '<shift>'
                elif name.startswith('alt'):
                    return '<alt>'
                elif name.startswith('cmd') or name.startswith('super'):
                    return '<cmd>'
                elif name == 'esc' or name == 'escape':
                    return '<escape>'
                else:
                    return f'<{name}>'
            
            return str(key).lower()
            
        except Exception:
            return str(key).lower()

    def _check_hotkeys(self) -> None:
        """
        Verifica se alguma hotkey registrada foi ativada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função olha para todas as teclas que estão pressionadas
        neste momento e verifica se alguma combinação registrada está
        completa. Se estiver, executa a função associada.
        
        Exemplo: Se você registrou Ctrl+Shift+R e ambas Ctrl, Shift e R
        estão pressionadas, a função associada será chamada.
        
        EXPLICAÇÃO TÉCNICA:
        Itera sobre todas as hotkeys registradas e verifica se todas
        as teclas da combinação estão no conjunto _pressed_keys.
        Se sim, executa o callback em uma thread separada para não
        bloquear o listener.
        
        Returns:
            None
        """
        if not self._processing_enabled:
            return
        
        with self._lock:
            current_keys = self._pressed_keys.copy()
        
        # Verifica cada hotkey registrada
        for hotkey_str, callback in self._hotkeys.items():
            # Parse da string de hotkey para conjunto de teclas
            required_keys = self._parse_hotkey(hotkey_str)
            
            # Verifica se todas as teclas necessárias estão pressionadas
            if required_keys and required_keys.issubset(current_keys):
                # Executa o callback em thread separada para não bloquear
                # daemon=True garante que não trava o programa ao fechar
                threading.Thread(target=callback, daemon=True).start()
                
                # Limpa as teclas para evitar ativações múltiplas
                with self._lock:
                    self._pressed_keys.clear()
                break

    def _parse_hotkey(self, hotkey_str: str) -> Set[str]:
        """
        Converte string de hotkey para conjunto de teclas.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você escreve uma hotkey como '<ctrl>+<shift>+r', esta
        função quebra em partes e cria um conjunto: {'<ctrl>', '<shift>', 'r'}
        
        Isso facilita comparar se todas as teclas estão pressionadas.
        
        EXPLICAÇÃO TÉCNICA:
        Faz parsing da notação de hotkey usando '+' como separador.
        Normaliza cada parte para formato consistente.
        
        Args:
            hotkey_str (str): String da hotkey (ex: '<ctrl>+<shift>+r')
        
        Returns:
            Set[str]: Conjunto de teclas necessárias
        """
        # Divide pelo separador '+'
        parts = hotkey_str.lower().split('+')
        
        # Lista de teclas especiais que precisam de brackets
        special_keys = {
            'ctrl', 'shift', 'alt', 'cmd', 'super',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
            'escape', 'esc', 'enter', 'return', 'space', 'tab',
            'backspace', 'delete', 'insert', 'home', 'end', 'page_up', 'page_down',
            'up', 'down', 'left', 'right', 'caps_lock', 'num_lock', 'scroll_lock',
            'print_screen', 'pause', 'menu'
        }
        
        # Normaliza cada parte
        keys = set()
        for part in parts:
            part = part.strip()
            if part:
                # Remove brackets se existirem para normalizar
                clean_part = part.strip('<>')
                
                # Adiciona brackets se for tecla especial
                if clean_part in special_keys:
                    # Normaliza 'esc' para 'escape'
                    if clean_part == 'esc':
                        clean_part = 'escape'
                    keys.add(f'<{clean_part}>')
                elif part.startswith('<') and part.endswith('>'):
                    # Já está com brackets
                    keys.add(part)
                else:
                    # Tecla normal (letra, número)
                    keys.add(part)
        
        return keys

    def _on_key_press(self, key) -> None:
        """
        Callback chamado quando uma tecla é pressionada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Toda vez que você aperta qualquer tecla, esta função é chamada.
        Ela adiciona a tecla à nossa lista de "teclas pressionadas agora"
        e verifica se alguma combinação foi completada.
        
        EXPLICAÇÃO TÉCNICA:
        Adiciona a tecla normalizada ao conjunto _pressed_keys e
        dispara a verificação de hotkeys.
        
        Args:
            key: Objeto tecla do pynput
        """
        if not self._enabled:
            return
        
        # Normaliza a tecla
        key_str = self._normalize_key(key)
        
        # Adiciona ao conjunto de teclas pressionadas
        with self._lock:
            self._pressed_keys.add(key_str)
        
        # Verifica se alguma hotkey foi ativada
        self._check_hotkeys()

    def _on_key_release(self, key) -> None:
        """
        Callback chamado quando uma tecla é solta.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você solta uma tecla, ela é removida da nossa lista de
        "teclas pressionadas agora". Isso é importante para que as
        combinações funcionem corretamente.
        
        EXPLICAÇÃO TÉCNICA:
        Remove a tecla do conjunto _pressed_keys quando é solta.
        
        Args:
            key: Objeto tecla do pynput
        """
        if not self._enabled:
            return
        
        key_str = self._normalize_key(key)
        
        with self._lock:
            self._pressed_keys.discard(key_str)  # discard não dá erro se não existir

    def register_hotkey(self, hotkey: str, callback: Callable[[], None]) -> bool:
        """
        Registra uma nova hotkey global.
        
        EXPLICAÇÃO PARA INICIANTES:
        Use este método para adicionar um novo atalho de teclado.
        Você passa:
        1. A combinação de teclas (como '<ctrl>+<shift>+r')
        2. A função que deve ser executada quando o atalho for usado
        
        Formato das teclas:
        - Letras e números: 'a', 'b', '1', '2'
        - Teclas especiais: '<space>', '<enter>', '<escape>', '<f1>'
        - Modificadores: '<ctrl>', '<shift>', '<alt>'
        
        Exemplos:
            register_hotkey('<ctrl>+<shift>+r', iniciar_gravacao)
            register_hotkey('<escape>', parar_tudo)
            register_hotkey('<f5>', reproduzir)
        
        EXPLICAÇÃO TÉCNICA:
        Adiciona a hotkey ao dicionário interno. A verificação de ativação
        acontece em _check_hotkeys() quando teclas são pressionadas.
        
        Args:
            hotkey (str): Combinação de teclas (ex: '<ctrl>+<shift>+r')
            callback (Callable): Função a ser chamada (sem argumentos)
        
        Returns:
            bool: True se registrou com sucesso
        """
        try:
            # Normaliza a hotkey
            normalized = hotkey.lower().strip()
            
            # Valida que a hotkey pode ser parseada
            keys = self._parse_hotkey(normalized)
            if not keys:
                print(f"Hotkey inválida: {hotkey}")
                return False
            
            # Registra no dicionário
            self._hotkeys[normalized] = callback
            print(f"Hotkey registrada: {hotkey}")
            return True
            
        except Exception as e:
            print(f"Erro ao registrar hotkey '{hotkey}': {e}")
            return False

    def unregister_hotkey(self, hotkey: str) -> bool:
        """
        Remove uma hotkey registrada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Se você não quer mais que um atalho funcione, use este método
        para removê-lo.
        
        EXPLICAÇÃO TÉCNICA:
        Remove a hotkey do dicionário interno.
        
        Args:
            hotkey (str): A combinação a ser removida
        
        Returns:
            bool: True se removeu, False se não existia
        """
        normalized = hotkey.lower().strip()
        
        if normalized in self._hotkeys:
            del self._hotkeys[normalized]
            print(f"Hotkey removida: {hotkey}")
            return True
        
        return False

    def clear_hotkeys(self) -> None:
        """
        Remove todas as hotkeys registradas.
        
        EXPLICAÇÃO PARA INICIANTES:
        Limpa todos os atalhos de uma vez. Útil quando você quer
        reconfigurar todos os atalhos do zero.
        
        EXPLICAÇÃO TÉCNICA:
        Limpa o dicionário de hotkeys.
        
        Returns:
            None
        """
        self._hotkeys.clear()
        print("Todas as hotkeys foram removidas")

    def start(self) -> bool:
        """
        Inicia o listener de hotkeys globais.
        
        EXPLICAÇÃO PARA INICIANTES:
        Chame este método para "ligar" o sistema de atalhos. A partir
        deste momento, todas as hotkeys registradas começam a funcionar.
        
        Você deve chamar start() após registrar suas hotkeys.
        
        EXPLICAÇÃO TÉCNICA:
        Cria e inicia o keyboard.Listener em uma thread daemon.
        O listener captura todas as teclas e dispara os callbacks.
        
        Returns:
            bool: True se iniciou com sucesso
        """
        if self._enabled:
            print("Hotkey listener já está rodando!")
            return False
        
        try:
            # Cria o listener
            self._listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            
            # Inicia (roda em thread separada automaticamente)
            self._listener.start()
            
            self._enabled = True
            print("Hotkey listener iniciado")
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar hotkey listener: {e}")
            return False

    def stop(self) -> None:
        """
        Para o listener de hotkeys.
        
        EXPLICAÇÃO PARA INICIANTES:
        "Desliga" o sistema de atalhos. Nenhuma hotkey vai funcionar
        até você chamar start() novamente.
        
        EXPLICAÇÃO TÉCNICA:
        Para o listener do pynput e limpa o estado.
        
        Returns:
            None
        """
        if not self._enabled:
            return
        
        if self._listener:
            self._listener.stop()
            self._listener = None
        
        self._enabled = False
        
        with self._lock:
            self._pressed_keys.clear()
        
        print("Hotkey listener parado")

    def set_enabled(self, enabled: bool) -> None:
        """
        Ativa ou desativa temporariamente o processamento de hotkeys.
        
        EXPLICAÇÃO PARA INICIANTES:
        Às vezes você quer que os atalhos parem de funcionar temporariamente
        sem ter que parar e reiniciar todo o sistema. Este método faz isso.
        
        Útil durante a gravação, para evitar que as hotkeys sejam gravadas.
        
        EXPLICAÇÃO TÉCNICA:
        Apenas define o flag _processing_enabled. O listener continua
        rodando, mas os callbacks não são executados.
        
        Args:
            enabled (bool): True para ativar, False para desativar
        """
        self._processing_enabled = enabled

    def is_enabled(self) -> bool:
        """
        Verifica se o listener está ativo.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna True se o sistema de atalhos está funcionando.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna o estado atual do listener.
        
        Returns:
            bool: True se ativo, False se parado
        """
        return self._enabled

    def get_registered_hotkeys(self) -> Dict[str, str]:
        """
        Retorna todas as hotkeys registradas.
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método lista todos os atalhos que foram configurados.
        Útil para mostrar na interface quais atalhos estão disponíveis.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna cópia do dicionário de hotkeys com nomes de callback.
        
        Returns:
            Dict[str, str]: Mapa de hotkey -> nome do callback
        """
        return {
            hotkey: callback.__name__ if hasattr(callback, '__name__') else str(callback)
            for hotkey, callback in self._hotkeys.items()
        }


# ============================================================================
# BLOCO DE TESTE
# ============================================================================

if __name__ == "__main__":
    import time
    
    print("=== Teste do módulo hotkeys.py ===")
    print()
    print("Hotkeys de teste:")
    print("  Ctrl+Shift+R - Mostra 'Gravação!'")
    print("  Ctrl+Shift+P - Mostra 'Reprodução!'")
    print("  Escape       - Para o teste")
    print()
    print("Pressione Escape para sair...")
    print()
    
    # Flag para controle do loop
    running = True
    
    # Callbacks de teste
    def on_record():
        print(">>> Hotkey ativada: GRAVAÇÃO!")
    
    def on_playback():
        print(">>> Hotkey ativada: REPRODUÇÃO!")
    
    def on_stop():
        global running
        print(">>> Hotkey ativada: PARAR!")
        running = False
    
    # Cria o manager
    manager = HotkeyManager()
    
    # Registra as hotkeys
    manager.register_hotkey('<ctrl>+<shift>+r', on_record)
    manager.register_hotkey('<ctrl>+<shift>+p', on_playback)
    manager.register_hotkey('<escape>', on_stop)
    
    # Mostra hotkeys registradas
    print(f"Hotkeys registradas: {manager.get_registered_hotkeys()}")
    
    # Inicia o listener
    manager.start()
    
    # Loop principal
    while running:
        time.sleep(0.1)
    
    # Para o listener
    manager.stop()
    
    print("\n=== Teste concluído! ===")
