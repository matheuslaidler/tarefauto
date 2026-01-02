# ============================================================================
# TarefAuto - Módulo de Configurações (config.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este módulo cuida de salvar e carregar as configurações do programa.
# Quando você define um atalho de teclado ou escolhe onde salvar suas
# gravações, essas preferências são salvas em um arquivo para que o
# programa lembre delas na próxima vez que você abrir.
#
# É como o programa "lembrar" suas preferências entre uma sessão e outra.
#
# EXPLICAÇÃO TÉCNICA:
# Implementa persistência de configurações usando JSON em um arquivo
# no diretório do usuário. Utiliza padrão Singleton para garantir uma
# única instância de configurações em toda a aplicação.
#
# ============================================================================

"""
Módulo de gerenciamento de configurações do TarefAuto.

Este módulo fornece a classe Config para salvar, carregar e gerenciar
configurações do usuário de forma persistente.

Classes:
    Config: Gerenciador de configurações com persistência em JSON

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# json: Para salvar/carregar configurações em formato JSON
import json

# os: Para manipulação de caminhos e diretórios
import os

# pathlib: Para trabalhar com caminhos de forma moderna e cross-platform
from pathlib import Path

# typing: Anotações de tipo
from typing import Any, Dict, Optional


# ============================================================================
# CONFIGURAÇÕES PADRÃO
# ============================================================================

# Estas são as configurações iniciais quando o programa é executado pela
# primeira vez ou quando o arquivo de configurações não existe

DEFAULT_CONFIG = {
    # ========================================================================
    # CONFIGURAÇÕES DE GRAVAÇÃO
    # ========================================================================
    "recording": {
        "record_mouse": True,           # Gravar movimentos do mouse?
        "record_keyboard": True,        # Gravar teclas do teclado?
        "record_mouse_movement": True,  # Gravar movimento (não só cliques)?
    },
    
    # ========================================================================
    # CONFIGURAÇÕES DE REPRODUÇÃO
    # ========================================================================
    "playback": {
        "loop_mode": "single",          # Modo de loop: single, count, duration, infinite
        "loop_value": 1,                # Valor do loop (quantidade ou segundos)
        "speed_multiplier": 1.0,        # Velocidade de reprodução
    },
    
    # ========================================================================
    # CONFIGURAÇÕES DE HOTKEYS (Sistema Toggle - uma tecla para iniciar/parar)
    # ========================================================================
    "hotkeys": {
        "toggle_recording": "f9",    # Iniciar/Parar gravação
        "toggle_playback": "f10",    # Iniciar/Parar reprodução
        "emergency_stop": "escape",  # Parar tudo (emergência)
    },
    
    # ========================================================================
    # CONFIGURAÇÕES DE INTERFACE
    # ========================================================================
    "ui": {
        "theme": "dark",                # Tema: dark ou light
        "window_width": 800,            # Largura da janela
        "window_height": 600,           # Altura da janela
        "always_on_top": False,         # Janela sempre visível
    },
    
    # ========================================================================
    # CONFIGURAÇÕES DE ARQUIVOS
    # ========================================================================
    "files": {
        "recordings_folder": "",        # Pasta para gravações (vazio = pasta padrão)
        "last_recording": "",           # Último arquivo de gravação usado
        "auto_save": True,              # Salvar automaticamente ao parar gravação
    },
}


# ============================================================================
# CLASSE CONFIG
# ============================================================================

class Config:
    """
    Gerenciador de configurações do TarefAuto.
    
    EXPLICAÇÃO PARA INICIANTES:
    A classe Config é responsável por:
    1. Salvar suas preferências em um arquivo no computador
    2. Carregar essas preferências quando o programa abre
    3. Permitir que você altere qualquer configuração
    
    O arquivo de configurações fica em uma pasta especial do seu usuário,
    então cada pessoa que usa o computador pode ter suas próprias configs.
    
    EXPLICAÇÃO TÉCNICA:
    Implementa padrão Singleton para garantir instância única.
    Armazena configs em JSON no diretório de dados do usuário.
    Suporta acesso hierárquico via notação de ponto (ex: "recording.record_mouse").
    
    Attributes:
        config_path (Path): Caminho para o arquivo de configurações
        _config (Dict): Dicionário com todas as configurações
    
    Example:
        >>> config = Config()
        >>> config.get("recording.record_mouse")  # Retorna True
        >>> config.set("recording.record_mouse", False)
        >>> config.save()
    """
    
    # Instância única (Singleton)
    _instance: Optional["Config"] = None
    
    def __new__(cls) -> "Config":
        """
        Cria ou retorna a instância única de Config (Singleton).
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método especial garante que só existe UMA instância de Config
        em todo o programa. Não importa quantas vezes você faça Config(),
        sempre vai receber o mesmo objeto.
        
        Isso é importante porque as configurações devem ser as mesmas em
        todas as partes do programa.
        
        EXPLICAÇÃO TÉCNICA:
        Implementa o padrão Singleton usando __new__. Se _instance for None,
        cria uma nova instância. Caso contrário, retorna a existente.
        
        Returns:
            Config: A instância única de Config
        """
        if cls._instance is None:
            # super().__new__(cls) cria a instância do objeto
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Inicializa as configurações (só executa uma vez).
        
        EXPLICAÇÃO PARA INICIANTES:
        Configura os caminhos dos arquivos e carrega as configurações
        salvas anteriormente (ou usa as padrão se for primeira execução).
        
        EXPLICAÇÃO TÉCNICA:
        Usa flag _initialized para evitar reinicialização em chamadas
        subsequentes (comportamento do Singleton).
        """
        # Evita reinicialização no Singleton
        if self._initialized:
            return
        
        self._initialized = True
        
        # ====================================================================
        # CONFIGURAÇÃO DE CAMINHOS
        # ====================================================================
        
        # Obtém o diretório de dados do usuário
        # Windows: C:/Users/<user>/AppData/Local/TarefAuto
        # Linux: ~/.local/share/TarefAuto
        # macOS: ~/Library/Application Support/TarefAuto
        self._app_data_dir = self._get_app_data_dir()
        
        # Cria o diretório se não existir
        self._app_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Caminho para o arquivo de configurações
        self.config_path = self._app_data_dir / "config.json"
        
        # Caminho para a pasta de gravações
        self.recordings_dir = self._app_data_dir / "recordings"
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        
        # ====================================================================
        # CARREGAMENTO DE CONFIGURAÇÕES
        # ====================================================================
        
        # Começa com as configurações padrão
        self._config: Dict[str, Any] = self._deep_copy(DEFAULT_CONFIG)
        
        # Tenta carregar configurações salvas
        self._load()
        
        # Atualiza o caminho da pasta de gravações se estiver vazio
        if not self._config["files"]["recordings_folder"]:
            self._config["files"]["recordings_folder"] = str(self.recordings_dir)

    def _get_app_data_dir(self) -> Path:
        """
        Obtém o diretório de dados da aplicação específico do sistema.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cada sistema operacional tem um lugar "oficial" para guardar dados
        de aplicativos. Esta função descobre qual é esse lugar no sistema
        que você está usando.
        
        Windows: C:/Users/SeuNome/AppData/Local/TarefAuto
        Linux: /home/seunome/.local/share/TarefAuto
        Mac: /Users/seunome/Library/Application Support/TarefAuto
        
        EXPLICAÇÃO TÉCNICA:
        Usa variáveis de ambiente específicas de cada sistema para encontrar
        o diretório apropriado. Fallback para home do usuário se necessário.
        
        Returns:
            Path: Caminho para o diretório de dados da aplicação
        """
        import sys
        
        app_name = "TarefAuto"
        
        # Detecta o sistema operacional
        if sys.platform == "win32":
            # Windows: usa LOCALAPPDATA
            base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
        elif sys.platform == "darwin":
            # macOS: usa Library/Application Support
            base = Path.home() / "Library" / "Application Support"
        else:
            # Linux e outros: usa .local/share
            base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        
        return base / app_name

    def _deep_copy(self, obj: Any) -> Any:
        """
        Faz uma cópia profunda de um objeto (dicionário aninhado).
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você copia um dicionário normal em Python, as partes internas
        ainda apontam para os mesmos dados. Uma "cópia profunda" copia tudo,
        criando novos objetos para cada parte.
        
        Isso é importante para que as configurações padrão não sejam
        modificadas acidentalmente.
        
        EXPLICAÇÃO TÉCNICA:
        Implementa cópia recursiva sem depender do módulo copy.
        Funciona para dicts, lists e valores primitivos.
        
        Args:
            obj: Objeto a ser copiado
        
        Returns:
            Any: Cópia profunda do objeto
        """
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj

    def _load(self) -> bool:
        """
        Carrega configurações do arquivo.
        
        EXPLICAÇÃO PARA INICIANTES:
        Lê o arquivo de configurações salvo anteriormente e atualiza as
        configurações do programa. Se o arquivo não existir ou estiver
        corrompido, mantém as configurações padrão.
        
        EXPLICAÇÃO TÉCNICA:
        Carrega JSON do arquivo e faz merge com configurações padrão
        para garantir que novas opções sejam adicionadas automaticamente.
        
        Returns:
            bool: True se carregou com sucesso, False caso contrário
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                
                # Faz merge das configs salvas com as padrão
                # Isso garante que novas opções apareçam automaticamente
                self._merge_config(self._config, saved_config)
                
                print(f"Configurações carregadas de: {self.config_path}")
                return True
            
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
        
        return False

    def _merge_config(self, base: Dict, updates: Dict) -> None:
        """
        Faz merge recursivo de dois dicionários.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função combina dois dicionários: o "base" (padrão) e o
        "updates" (salvo pelo usuário). Se uma configuração existe no
        arquivo salvo, ela é usada. Senão, usa-se o padrão.
        
        EXPLICAÇÃO TÉCNICA:
        Merge in-place recursivo que preserva valores padrão para chaves
        ausentes no dicionário de updates. Modifica 'base' diretamente.
        
        Args:
            base: Dicionário base (será modificado)
            updates: Dicionário com atualizações
        """
        for key, value in updates.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    # Merge recursivo para dicionários aninhados
                    self._merge_config(base[key], value)
                else:
                    # Atualiza o valor
                    base[key] = value

    def save(self) -> bool:
        """
        Salva as configurações atuais no arquivo.
        
        EXPLICAÇÃO PARA INICIANTES:
        Grava todas as suas preferências atuais no arquivo de configuração.
        Na próxima vez que você abrir o programa, ele vai lembrar de tudo.
        
        EXPLICAÇÃO TÉCNICA:
        Serializa o dicionário de configurações para JSON e escreve no
        arquivo. Usa indentação para legibilidade.
        
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            print(f"Configurações salvas em: {self.config_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém uma configuração pelo caminho da chave.
        
        EXPLICAÇÃO PARA INICIANTES:
        Busca uma configuração específica. Você pode usar "." para acessar
        configurações dentro de categorias.
        
        Exemplos:
            config.get("recording.record_mouse")  # True ou False
            config.get("playback.speed_multiplier")  # 1.0
            config.get("ui.theme")  # "dark" ou "light"
        
        EXPLICAÇÃO TÉCNICA:
        Navega pelo dicionário usando chave com notação de ponto.
        Retorna default se a chave não existir.
        
        Args:
            key (str): Caminho da chave (ex: "recording.record_mouse")
            default (Any): Valor retornado se a chave não existir
        
        Returns:
            Any: Valor da configuração ou default
        """
        try:
            # Divide a chave em partes (ex: "recording.record_mouse" -> ["recording", "record_mouse"])
            keys = key.split('.')
            
            # Navega pelo dicionário
            value = self._config
            for k in keys:
                value = value[k]
            
            return value
            
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> bool:
        """
        Define uma configuração pelo caminho da chave.
        
        EXPLICAÇÃO PARA INICIANTES:
        Altera uma configuração específica. Use "." para acessar
        configurações dentro de categorias.
        
        Exemplos:
            config.set("recording.record_mouse", False)
            config.set("playback.speed_multiplier", 2.0)
        
        NOTA: As mudanças só são salvas permanentemente quando você
        chama config.save()
        
        EXPLICAÇÃO TÉCNICA:
        Navega pelo dicionário até o penúltimo nível e define o valor.
        Cria dicionários intermediários se necessário.
        
        Args:
            key (str): Caminho da chave (ex: "recording.record_mouse")
            value (Any): Valor a ser definido
        
        Returns:
            bool: True se definiu com sucesso
        """
        try:
            keys = key.split('.')
            
            # Navega até o penúltimo nível
            obj = self._config
            for k in keys[:-1]:
                if k not in obj:
                    obj[k] = {}  # Cria dicionário intermediário se necessário
                obj = obj[k]
            
            # Define o valor
            obj[keys[-1]] = value
            return True
            
        except Exception as e:
            print(f"Erro ao definir configuração '{key}': {e}")
            return False

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Obtém uma seção inteira de configurações.
        
        EXPLICAÇÃO PARA INICIANTES:
        Em vez de pegar uma configuração específica, pega toda uma
        categoria de uma vez. Útil quando você precisa de várias
        configurações relacionadas.
        
        Exemplo:
            recording_config = config.get_section("recording")
            # Retorna: {"record_mouse": True, "record_keyboard": True, ...}
        
        EXPLICAÇÃO TÉCNICA:
        Retorna cópia do dicionário da seção especificada.
        
        Args:
            section (str): Nome da seção (ex: "recording", "playback")
        
        Returns:
            Dict: Dicionário com as configurações da seção
        """
        return self._deep_copy(self._config.get(section, {}))

    def reset_to_defaults(self) -> None:
        """
        Reseta todas as configurações para os valores padrão.
        
        EXPLICAÇÃO PARA INICIANTES:
        Descarta todas as suas personalizações e volta tudo para as
        configurações originais do programa. Útil se algo ficou errado.
        
        NOTA: As mudanças só são permanentes após chamar save().
        
        EXPLICAÇÃO TÉCNICA:
        Substitui o dicionário de configurações por uma cópia fresca
        das configurações padrão.
        
        Returns:
            None
        """
        self._config = self._deep_copy(DEFAULT_CONFIG)
        
        # Redefine o caminho da pasta de gravações
        self._config["files"]["recordings_folder"] = str(self.recordings_dir)
        
        print("Configurações resetadas para valores padrão")

    def get_recordings_folder(self) -> Path:
        """
        Obtém o caminho da pasta de gravações.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna o caminho da pasta onde suas gravações são salvas.
        
        EXPLICAÇÃO TÉCNICA:
        Converte a string de configuração para Path.
        
        Returns:
            Path: Caminho da pasta de gravações
        """
        folder = self.get("files.recordings_folder", "")
        if folder:
            return Path(folder)
        return self.recordings_dir


# ============================================================================
# BLOCO DE TESTE
# ============================================================================

if __name__ == "__main__":
    print("=== Teste do módulo config.py ===")
    print()
    
    # Cria/obtém a instância de Config
    config = Config()
    
    # Mostra informações
    print(f"Diretório de dados: {config._app_data_dir}")
    print(f"Arquivo de config: {config.config_path}")
    print(f"Pasta de gravações: {config.recordings_dir}")
    print()
    
    # Testa get/set
    print("Testando get/set:")
    print(f"  record_mouse: {config.get('recording.record_mouse')}")
    print(f"  theme: {config.get('ui.theme')}")
    
    # Altera uma config
    config.set("ui.theme", "light")
    print(f"  theme (após set): {config.get('ui.theme')}")
    
    # Volta ao original
    config.set("ui.theme", "dark")
    
    # Mostra uma seção inteira
    print()
    print("Seção de hotkeys:")
    hotkeys = config.get_section("hotkeys")
    for key, value in hotkeys.items():
        print(f"  {key}: {value}")
    
    # Testa Singleton
    print()
    print("Testando Singleton:")
    config2 = Config()
    print(f"  config is config2: {config is config2}")
    
    print()
    print("=== Teste concluído! ===")
