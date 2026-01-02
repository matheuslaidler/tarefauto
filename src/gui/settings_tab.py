# ============================================================================
# TarefAuto - Aba de Configurações (settings_tab.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este arquivo cria a terceira aba do programa - a aba de configurações.
# Aqui o usuário pode:
# - Definir atalhos de teclado (hotkeys) para controlar o programa
# - Escolher onde salvar os arquivos por padrão
# - Personalizar a aparência (claro/escuro)
# - Ver informações sobre o programa
#
# Os atalhos de teclado são muito úteis porque permitem controlar a
# gravação/reprodução sem precisar clicar na janela do programa.
#
# EXPLICAÇÃO TÉCNICA:
# Implementa um CTkFrame com controles de configuração. Usa a classe
# Config para persistir as configurações em arquivo JSON. Os atalhos
# são capturados usando pynput em um estado especial de "escuta".
#
# ============================================================================

"""
Aba de configurações do TarefAuto.

Este módulo contém a classe SettingsTab que implementa a interface
para configurar atalhos de teclado, aparência e outras opções.

Classes:
    SettingsTab: Frame com controles de configuração

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# customtkinter: Framework de GUI
import customtkinter as ctk

# tkinter: Para diálogos
from tkinter import filedialog, messagebox

# typing: Anotações de tipo
from typing import Optional, Dict, Callable
import webbrowser
import threading

# pynput para captura de teclas
from pynput import keyboard

# Importações internas
from src.gui.theme import TarefAutoTheme
from src.utils.config import Config
from src.utils.platform_utils import PlatformUtils


# ============================================================================
# CLASSE SETTINGS TAB
# ============================================================================

class SettingsTab(ctk.CTkFrame):
    """
    Aba de configurações do aplicativo.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta classe cria a interface de configurações. É onde você personaliza
    como o programa funciona:
    
    1. ATALHOS DE TECLADO
       Define teclas de atalho para:
       - Iniciar/parar gravação (ex: Ctrl+F9)
       - Iniciar/parar reprodução (ex: Ctrl+F10)
       - Parar tudo de emergência (ex: Esc)
       
    2. ARQUIVOS
       Define onde os arquivos são salvos por padrão
       
    3. APARÊNCIA
       Escolhe tema claro ou escuro
       
    4. SOBRE
       Informações sobre o programa, versão, autor
    
    EXPLICAÇÃO TÉCNICA:
    Herda de CTkFrame e gerencia configurações via classe Config.
    Os atalhos são capturados entrando em modo "listening" que usa
    pynput para capturar a próxima combinação de teclas.
    
    Attributes:
        config (Config): Instância de configuração
        _listening_for (str): Qual atalho está sendo configurado
        on_hotkeys_changed (Callable): Callback quando atalhos mudam
    
    Example:
        >>> tab = SettingsTab(parent_frame)
        >>> tab.pack(fill="both", expand=True)
    """
    
    def __init__(
        self,
        master,
        on_hotkeys_changed: Optional[Callable[[Dict[str, str]], None]] = None,
        **kwargs
    ):
        """
        Inicializa a aba de configurações.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria todos os elementos de configuração: campos para atalhos,
        opções de aparência, informações sobre o programa.
        
        EXPLICAÇÃO TÉCNICA:
        Construtor que inicializa widgets e carrega configurações existentes.
        
        Args:
            master: Widget pai
            on_hotkeys_changed: Callback chamado quando atalhos são alterados
            **kwargs: Argumentos adicionais para CTkFrame
        """
        super().__init__(master, **TarefAutoTheme.get_frame_style("default"), **kwargs)
        
        # ====================================================================
        # ESTADO
        # ====================================================================
        
        # Configurações
        self.config = Config()
        
        # Callback
        self.on_hotkeys_changed = on_hotkeys_changed
        
        # Variáveis para captura de atalhos
        self._listening_for: Optional[str] = None
        self._hotkey_buttons: Dict[str, ctk.CTkButton] = {}
        self._hotkey_labels: Dict[str, ctk.CTkLabel] = {}
        
        # Listener de teclado para captura
        self._keyboard_listener: Optional[keyboard.Listener] = None
        self._pressed_keys: set = set()
        self._captured_hotkey: str = ""
        
        # Variáveis de controle
        self._theme_var = ctk.StringVar(value=self.config.get("ui.theme", "dark"))
        
        # ====================================================================
        # CONSTRUÇÃO DA INTERFACE
        # ====================================================================
        
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Constrói todos os elementos da interface.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria seções organizadas:
        - Atalhos de teclado
        - Configurações de arquivo
        - Aparência
        - Informações do programa
        
        EXPLICAÇÃO TÉCNICA:
        Instancia widgets em seções lógicas usando frames como containers.
        """
        # Container com scroll para conteúdo
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=TarefAutoTheme.BACKGROUND_LIGHTER,
            scrollbar_button_hover_color=TarefAutoTheme.PRIMARY_DARK
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ====================================================================
        # SEÇÃO: ATALHOS DE TECLADO
        # ====================================================================
        
        hotkeys_title = ctk.CTkLabel(
            scroll_frame,
            text="⌨️ Atalhos de Teclado",
            **TarefAutoTheme.get_label_style("heading")
        )
        hotkeys_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        hotkeys_desc = ctk.CTkLabel(
            scroll_frame,
            text="Clique no botão e pressione a combinação de teclas desejada",
            **TarefAutoTheme.get_label_style("muted")
        )
        hotkeys_desc.pack(anchor="w", padx=10, pady=(0, 10))
        
        hotkeys_frame = ctk.CTkFrame(scroll_frame, **TarefAutoTheme.get_frame_style("card"))
        hotkeys_frame.pack(fill="x", padx=10, pady=5)
        
        # Cria controles para cada atalho
        # Nota: toggle_recording e toggle_playback funcionam como liga/desliga
        hotkey_configs = [
            ("toggle_recording", "Gravar / Parar Gravação", "f9"),
            ("toggle_playback", "Reproduzir / Parar", "f10"),
            ("emergency_stop", "Parar Tudo (Emergência)", "escape"),
        ]
        
        for hotkey_id, label, default in hotkey_configs:
            self._create_hotkey_row(hotkeys_frame, hotkey_id, label, default)
        
        # ====================================================================
        # SEÇÃO: CONFIGURAÇÕES DE ARQUIVO
        # ====================================================================
        
        files_title = ctk.CTkLabel(
            scroll_frame,
            text="📁 Arquivos",
            **TarefAutoTheme.get_label_style("heading")
        )
        files_title.pack(anchor="w", padx=10, pady=(20, 5))
        
        files_frame = ctk.CTkFrame(scroll_frame, **TarefAutoTheme.get_frame_style("card"))
        files_frame.pack(fill="x", padx=10, pady=5)
        
        # Pasta padrão para salvamento
        folder_row = ctk.CTkFrame(files_frame, **TarefAutoTheme.get_frame_style("transparent"))
        folder_row.pack(fill="x", padx=15, pady=10)
        
        folder_label = ctk.CTkLabel(
            folder_row,
            text="Pasta padrão para gravações:",
            **TarefAutoTheme.get_label_style("default")
        )
        folder_label.pack(anchor="w")
        
        folder_input_row = ctk.CTkFrame(folder_row, **TarefAutoTheme.get_frame_style("transparent"))
        folder_input_row.pack(fill="x", pady=(5, 0))
        
        self._folder_entry = ctk.CTkEntry(
            folder_input_row,
            **TarefAutoTheme.get_entry_style("default")
        )
        self._folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Usa diretório padrão do sistema se não houver configuração
        default_folder = self.config.get("files.default_directory", "")
        if not default_folder:
            # Usa o diretório de gravações do config
            default_folder = str(self.config.recordings_dir)
            self.config.set("files.default_directory", default_folder)
        if default_folder:
            self._folder_entry.insert(0, default_folder)
        
        browse_button = ctk.CTkButton(
            folder_input_row,
            text="📂 Procurar",
            width=100,
            **TarefAutoTheme.get_button_style("outline"),
            command=self._browse_folder
        )
        browse_button.pack(side="right")
        
        # ====================================================================
        # SEÇÃO: APARÊNCIA (Comentado - tema hardcoded como dark)
        # ====================================================================
        # TODO: Implementar suporte completo a temas no futuro
        # Por enquanto, o tema está fixo como "dark" pois as cores
        # são hardcoded em TarefAutoTheme
        #
        # appearance_title = ctk.CTkLabel(
        #     scroll_frame,
        #     text="🎨 Aparência",
        #     **TarefAutoTheme.get_label_style("heading")
        # )
        # appearance_title.pack(anchor="w", padx=10, pady=(20, 5))
        #
        # appearance_frame = ctk.CTkFrame(scroll_frame, **TarefAutoTheme.get_frame_style("card"))
        # appearance_frame.pack(fill="x", padx=10, pady=5)
        #
        # theme_row = ctk.CTkFrame(appearance_frame, **TarefAutoTheme.get_frame_style("transparent"))
        # theme_row.pack(fill="x", padx=15, pady=10)
        #
        # theme_label = ctk.CTkLabel(
        #     theme_row,
        #     text="Tema:",
        #     **TarefAutoTheme.get_label_style("default")
        # )
        # theme_label.pack(side="left")
        #
        # theme_menu = ctk.CTkOptionMenu(
        #     theme_row,
        #     values=["dark", "light", "system"],
        #     variable=self._theme_var,
        #     fg_color=TarefAutoTheme.BACKGROUND_SECONDARY,
        #     button_color=TarefAutoTheme.PRIMARY_DARK,
        #     button_hover_color=TarefAutoTheme.PRIMARY_HOVER,
        #     dropdown_fg_color=TarefAutoTheme.BACKGROUND_SECONDARY,
        #     dropdown_hover_color=TarefAutoTheme.PRIMARY_DARK,
        #     command=self._on_theme_changed
        # )
        # theme_menu.pack(side="right")
        
        # ====================================================================
        # SEÇÃO: INFORMAÇÕES DA PLATAFORMA
        # ====================================================================
        
        platform_title = ctk.CTkLabel(
            scroll_frame,
            text="💻 Informações do Sistema",
            **TarefAutoTheme.get_label_style("heading")
        )
        platform_title.pack(anchor="w", padx=10, pady=(20, 5))
        
        platform_frame = ctk.CTkFrame(scroll_frame, **TarefAutoTheme.get_frame_style("card"))
        platform_frame.pack(fill="x", padx=10, pady=5)
        
        platform_info = PlatformUtils.get_platform_info()
        
        for key, value in platform_info.items():
            if key == "wayland_detected" and value:
                value_text = "⚠️ Sim (funcionalidade limitada)"
            else:
                value_text = str(value)
            
            row = ctk.CTkFrame(platform_frame, **TarefAutoTheme.get_frame_style("transparent"))
            row.pack(fill="x", padx=15, pady=3)
            
            key_label = ctk.CTkLabel(
                row,
                text=f"{key.replace('_', ' ').title()}:",
                **TarefAutoTheme.get_label_style("default")
            )
            key_label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                row,
                text=value_text,
                **TarefAutoTheme.get_label_style("muted")
            )
            value_label.pack(side="right")
        
        # ====================================================================
        # SEÇÃO: SOBRE
        # ====================================================================
        
        about_title = ctk.CTkLabel(
            scroll_frame,
            text="ℹ️ Sobre o TarefAuto",
            **TarefAutoTheme.get_label_style("heading")
        )
        about_title.pack(anchor="w", padx=10, pady=(20, 5))
        
        about_frame = ctk.CTkFrame(scroll_frame, **TarefAutoTheme.get_frame_style("card"))
        about_frame.pack(fill="x", padx=10, pady=5)
        
        # Informações do projeto
        project_info = TarefAutoTheme.PROJECT_INFO
        
        about_text = ctk.CTkLabel(
            about_frame,
            text=f"""
{project_info['name']} v{project_info['version']}

{project_info['description']}

Desenvolvido por: {project_info['author']}
            """,
            **TarefAutoTheme.get_label_style("default"),
            justify="center"
        )
        about_text.pack(pady=15)
        
        # Botões de link
        links_row = ctk.CTkFrame(about_frame, **TarefAutoTheme.get_frame_style("transparent"))
        links_row.pack(pady=(0, 15))
        
        github_button = ctk.CTkButton(
            links_row,
            text="🔗 GitHub",
            **TarefAutoTheme.get_button_style("outline"),
            command=lambda: webbrowser.open(project_info['github'])
        )
        github_button.pack(side="left", padx=5)
        
        # ====================================================================
        # BOTÕES DE AÇÃO
        # ====================================================================
        
        buttons_frame = ctk.CTkFrame(scroll_frame, **TarefAutoTheme.get_frame_style("transparent"))
        buttons_frame.pack(fill="x", padx=10, pady=20)
        
        # Botão de restaurar padrões (ciano escuro)
        reset_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Restaurar Padrões",
            height=40,
            fg_color=TarefAutoTheme.PRIMARY_DARK,
            hover_color="#006666",
            text_color="white",
            command=self._reset_to_defaults
        )
        reset_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Botão de salvar
        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar Configurações",
            height=40,
            **TarefAutoTheme.get_button_style("primary"),
            command=self._save_settings
        )
        save_button.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def _create_hotkey_row(
        self,
        parent: ctk.CTkFrame,
        hotkey_id: str,
        label: str,
        default: str
    ) -> None:
        """
        Cria uma linha de configuração de atalho.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cada atalho tem sua própria linha com:
        - Nome do que ele faz (ex: "Iniciar Gravação")
        - O atalho atual (ex: "Ctrl+F9")
        - Um botão para mudar o atalho
        
        EXPLICAÇÃO TÉCNICA:
        Cria widgets para uma entrada de hotkey e os adiciona aos
        dicionários de controle para acesso posterior.
        
        Args:
            parent: Frame pai
            hotkey_id: Identificador único do atalho
            label: Texto descritivo
            default: Atalho padrão
        """
        row = ctk.CTkFrame(parent, **TarefAutoTheme.get_frame_style("transparent"))
        row.pack(fill="x", padx=15, pady=8)
        
        # Label do atalho
        label_widget = ctk.CTkLabel(
            row,
            text=label,
            **TarefAutoTheme.get_label_style("default")
        )
        label_widget.pack(side="left")
        
        # Valor atual do atalho
        current_hotkey = self.config.get(f"hotkeys.{hotkey_id}", default)
        
        hotkey_label = ctk.CTkLabel(
            row,
            text=current_hotkey.upper(),
            **TarefAutoTheme.get_label_style("muted"),
            width=150
        )
        hotkey_label.pack(side="right", padx=10)
        self._hotkey_labels[hotkey_id] = hotkey_label
        
        # Botão para configurar
        config_button = ctk.CTkButton(
            row,
            text="⚙️ Configurar",
            width=100,
            **TarefAutoTheme.get_button_style("ghost"),
            command=lambda hid=hotkey_id: self._start_listening(hid)
        )
        config_button.pack(side="right")
        self._hotkey_buttons[hotkey_id] = config_button

    def _start_listening(self, hotkey_id: str) -> None:
        """
        Inicia a escuta para capturar um novo atalho.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você clica em "Configurar", o programa entra em modo de
        escuta. A próxima combinação de teclas que você pressionar será
        salva como o novo atalho.
        
        EXPLICAÇÃO TÉCNICA:
        Define _listening_for e inicia um listener pynput para captura
        global de teclas.
        
        Args:
            hotkey_id: ID do atalho sendo configurado
        """
        if self._listening_for:
            # Cancela escuta anterior
            self._stop_listening()
        
        self._listening_for = hotkey_id
        self._pressed_keys = set()
        self._captured_hotkey = ""
        
        # Atualiza visual do botão
        button = self._hotkey_buttons[hotkey_id]
        button.configure(
            text="⏳ Aguardando...",
            fg_color=TarefAutoTheme.WARNING
        )
        
        # Atualiza label
        label = self._hotkey_labels[hotkey_id]
        label.configure(text="Pressione as teclas...")
        
        # Inicia listener pynput
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_pynput_key_press,
            on_release=self._on_pynput_key_release
        )
        self._keyboard_listener.start()

    def _stop_listening(self) -> None:
        """
        Para a escuta de atalho.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cancela o modo de escuta e restaura a interface ao normal.
        
        EXPLICAÇÃO TÉCNICA:
        Para o listener pynput e reseta estado.
        """
        # Para o listener pynput
        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None
        
        if not self._listening_for:
            return
        
        # Restaura visual do botão
        hotkey_id = self._listening_for
        button = self._hotkey_buttons[hotkey_id]
        button.configure(
            text="⚙️ Configurar",
            **TarefAutoTheme.get_button_style("ghost")
        )
        
        self._listening_for = None
        self._pressed_keys = set()

    def _normalize_key(self, key) -> str:
        """
        Normaliza uma tecla pynput para string legível.
        
        Args:
            key: Objeto de tecla pynput
            
        Returns:
            str: Nome normalizado da tecla
        """
        try:
            # Tecla de caractere
            return key.char.lower() if key.char else ""
        except AttributeError:
            # Tecla especial
            key_name = str(key).replace("Key.", "").lower()
            # Mapeia nomes especiais
            key_map = {
                "ctrl_l": "ctrl", "ctrl_r": "ctrl",
                "shift_l": "shift", "shift_r": "shift",
                "alt_l": "alt", "alt_r": "alt",
                "cmd": "super", "cmd_l": "super", "cmd_r": "super",
                "space": "space",
                "esc": "escape",
                "return": "enter",
                "backspace": "backspace",
                "delete": "delete",
                "tab": "tab",
            }
            return key_map.get(key_name, key_name)

    def _on_pynput_key_press(self, key) -> None:
        """
        Callback quando uma tecla é pressionada (via pynput).
        
        Args:
            key: Tecla pressionada
        """
        if not self._listening_for:
            return
        
        key_name = self._normalize_key(key)
        if not key_name:
            return
        
        # Adiciona ao set de teclas pressionadas
        self._pressed_keys.add(key_name)
        
        # Se for modificador sozinho, não mostra ainda
        if key_name in ("ctrl", "shift", "alt", "super"):
            return
        
        # Constrói combinação
        modifiers = []
        if "ctrl" in self._pressed_keys:
            modifiers.append("ctrl")
        if "shift" in self._pressed_keys:
            modifiers.append("shift")
        if "alt" in self._pressed_keys:
            modifiers.append("alt")
        if "super" in self._pressed_keys:
            modifiers.append("super")
        
        # Adiciona tecla final (não-modificador)
        parts = modifiers + [key_name]
        hotkey = "+".join(parts)
        
        self._captured_hotkey = hotkey
        
        # Atualiza label na thread principal
        self.after(0, lambda: self._update_hotkey_label(hotkey))

    def _update_hotkey_label(self, hotkey: str) -> None:
        """Atualiza o label do hotkey na thread principal."""
        if self._listening_for and self._listening_for in self._hotkey_labels:
            label = self._hotkey_labels[self._listening_for]
            label.configure(text=hotkey.upper())

    def _on_pynput_key_release(self, key) -> None:
        """
        Callback quando uma tecla é solta (via pynput).
        
        Args:
            key: Tecla solta
        """
        if not self._listening_for:
            return
        
        key_name = self._normalize_key(key)
        self._pressed_keys.discard(key_name)
        
        # Se soltou ESC sem outros modificadores, cancela
        if key_name == "escape" and self._captured_hotkey in ("escape", ""):
            self.after(0, self._cancel_listening)
            return
        
        # Se tem hotkey capturada e todas teclas soltas, finaliza
        if self._captured_hotkey and not self._pressed_keys:
            self.after(0, self._finalize_hotkey_capture)

    def _cancel_listening(self) -> None:
        """Cancela a escuta e restaura valor anterior."""
        if not self._listening_for:
            return
            
        hotkey_id = self._listening_for
        
        # Restaura valor original
        default_hotkey = self.config.get(f"hotkeys.{hotkey_id}", "")
        if self._hotkey_labels.get(hotkey_id):
            self._hotkey_labels[hotkey_id].configure(
                text=default_hotkey.upper() if default_hotkey else "Não definido"
            )
        
        self._stop_listening()

    def _finalize_hotkey_capture(self) -> None:
        """Finaliza a captura e salva o hotkey."""
        if not self._listening_for or not self._captured_hotkey:
            return
            
        hotkey_id = self._listening_for
        hotkey = self._captured_hotkey
        
        # Salva na config
        self.config.set(f"hotkeys.{hotkey_id}", hotkey)
        
        # Para escuta
        self._stop_listening()
        
        # Atualiza label com valor final
        if hotkey_id in self._hotkey_labels:
            self._hotkey_labels[hotkey_id].configure(text=hotkey.upper())
        
        # Notifica mudança
        if self.on_hotkeys_changed:
            self.on_hotkeys_changed(self._get_all_hotkeys())
        
        self._captured_hotkey = ""

    def _browse_folder(self) -> None:
        """
        Abre diálogo para selecionar pasta padrão.
        
        EXPLICAÇÃO PARA INICIANTES:
        Abre uma janela para você escolher uma pasta onde as gravações
        serão salvas por padrão.
        
        EXPLICAÇÃO TÉCNICA:
        Usa filedialog para seleção de diretório.
        """
        folder = filedialog.askdirectory(title="Selecionar Pasta Padrão")
        if folder:
            self._folder_entry.delete(0, "end")
            self._folder_entry.insert(0, folder)

    def _on_theme_changed(self, theme: str) -> None:
        """
        Callback quando o tema é alterado.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você muda o tema (dark/light), esta função aplica a mudança.
        Nota: O tema light ainda não está totalmente implementado.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza o tema via CustomTkinter.
        
        Args:
            theme: Nome do tema selecionado
        """
        ctk.set_appearance_mode(theme)
        self.config.set("ui.theme", theme)
        
        # Aviso sobre tema light (funcionalidade parcial)
        if theme == "light":
            messagebox.showwarning(
                "Tema Light",
                "O tema claro ainda não está totalmente implementado.\n"
                "Algumas cores podem não aparecer corretamente.\n\n"
                "Para melhor experiência, use o tema escuro (dark)."
            )

    def _reset_to_defaults(self) -> None:
        """
        Restaura todas as configurações para os valores padrão.
        
        EXPLICAÇÃO PARA INICIANTES:
        Se você bagunçou as configurações, este botão volta tudo ao
        estado original do programa.
        
        EXPLICAÇÃO TÉCNICA:
        Chama config.reset() e atualiza a interface com os valores padrão.
        """
        # Confirma com o usuário
        result = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja restaurar todas as configurações para os valores padrão?\n\n"
            "Isso irá resetar:\n"
            "• Atalhos de teclado\n"
            "• Pasta de gravações\n"
            "• Outras preferências"
        )
        
        if result:
            # Reseta configurações
            self.config.reset_to_defaults()
            self.config.save()
            
            # Atualiza interface com valores padrão
            self._update_ui_from_config()
            
            # Notifica mudança de hotkeys
            if self.on_hotkeys_changed:
                self.on_hotkeys_changed(self._get_all_hotkeys())
            
            messagebox.showinfo(
                "Sucesso",
                "Configurações restauradas para os valores padrão!"
            )
    
    def _update_ui_from_config(self) -> None:
        """
        Atualiza a interface com valores da configuração.
        
        EXPLICAÇÃO PARA INICIANTES:
        Sincroniza o que está na tela com o que está salvo.
        
        EXPLICAÇÃO TÉCNICA:
        Lê valores da Config e atualiza widgets correspondentes.
        """
        # Atualiza labels de hotkeys
        for hotkey_id, label in self._hotkey_labels.items():
            value = self.config.get(f"hotkeys.{hotkey_id}", "")
            label.configure(text=value.upper() if value else "Não definido")
        
        # Atualiza pasta padrão
        folder = self.config.get("files.default_directory", "")
        self._folder_entry.delete(0, "end")
        if folder:
            self._folder_entry.insert(0, folder)

    def _save_settings(self) -> None:
        """
        Salva todas as configurações.
        
        EXPLICAÇÃO PARA INICIANTES:
        Salva suas preferências em um arquivo para que sejam lembradas
        na próxima vez que você abrir o programa.
        
        EXPLICAÇÃO TÉCNICA:
        Coleta valores dos widgets e persiste via Config.
        """
        # Salva pasta padrão
        folder = self._folder_entry.get()
        if folder:
            self.config.set("files.default_directory", folder)
        
        # Salva tema
        self.config.set("ui.theme", self._theme_var.get())
        
        # Salva config
        if self.config.save():
            messagebox.showinfo(
                "Sucesso",
                "Configurações salvas com sucesso!"
            )
        else:
            messagebox.showerror(
                "Erro",
                "Não foi possível salvar as configurações."
            )

    def _get_all_hotkeys(self) -> Dict[str, str]:
        """
        Retorna todos os atalhos configurados.
        
        EXPLICAÇÃO PARA INICIANTES:
        Coleta todos os atalhos atuais em um dicionário.
        
        EXPLICAÇÃO TÉCNICA:
        Lê valores das labels de hotkeys.
        
        Returns:
            Dict[str, str]: Mapa de hotkey_id para combinação de teclas
        """
        hotkeys = {}
        for hotkey_id, label in self._hotkey_labels.items():
            hotkeys[hotkey_id] = label.cget("text").lower()
        return hotkeys

    # ========================================================================
    # MÉTODOS PÚBLICOS
    # ========================================================================

    def get_hotkeys(self) -> Dict[str, str]:
        """
        Retorna os atalhos de teclado configurados.
        
        EXPLICAÇÃO PARA INICIANTES:
        Permite que outras partes do programa obtenham os atalhos atuais.
        
        EXPLICAÇÃO TÉCNICA:
        Interface pública para acessar hotkeys.
        
        Returns:
            Dict[str, str]: Atalhos configurados
        """
        return self._get_all_hotkeys()

    def get_default_folder(self) -> str:
        """
        Retorna a pasta padrão configurada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna onde as gravações serão salvas por padrão.
        
        EXPLICAÇÃO TÉCNICA:
        Lê valor do campo de pasta.
        
        Returns:
            str: Caminho da pasta padrão
        """
        return self._folder_entry.get()
