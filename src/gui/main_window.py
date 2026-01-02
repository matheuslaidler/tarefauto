# ============================================================================
# TarefAuto - Janela Principal (main_window.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este é o arquivo que cria a janela principal do programa - aquela que
# você vê quando abre o TarefAuto. Ela contém:
# - O título e logo do programa
# - As três abas (Gravação, Reprodução, Configurações)
# - A barra de status na parte inferior
#
# A janela principal coordena todas as outras partes do programa.
# Quando você clica em "Gravar" na aba de gravação, por exemplo,
# esta janela passa a informação para onde precisa ir.
#
# EXPLICAÇÃO TÉCNICA:
# Implementa a janela principal usando CTkToplevel/CTk. Contém um
# CTkTabview com as três abas principais. Gerencia o ciclo de vida
# da aplicação e a comunicação entre componentes.
#
# ============================================================================

"""
Janela principal do TarefAuto.

Este módulo contém a classe MainWindow que implementa a janela
principal do aplicativo, integrando todas as abas e funcionalidades.

Classes:
    MainWindow: Janela principal da aplicação

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# customtkinter: Framework de GUI
import customtkinter as ctk

# typing: Anotações de tipo
from typing import Optional, Dict, Callable

# Importações internas
from src.gui.theme import TarefAutoTheme
from src.gui.recording_tab import RecordingTab
from src.gui.playback_tab import PlaybackTab
from src.gui.settings_tab import SettingsTab
from src.core.events import RecordingSession
from src.core.hotkeys import HotkeyManager
from src.utils.config import Config


# ============================================================================
# CLASSE MAIN WINDOW
# ============================================================================

class MainWindow(ctk.CTk):
    """
    Janela principal do aplicativo TarefAuto.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta é a classe que cria a janela que você vê quando abre o programa.
    Ela organiza tudo:
    
    1. TÍTULO E ÍCONE
       O nome do programa aparece na barra de título
       
    2. ABAS
       Três abas organizadas em cima:
       - 📹 Gravação: Para gravar suas ações
       - ▶️ Reprodução: Para executar gravações
       - ⚙️ Configurações: Para personalizar o programa
       
    3. BARRA DE STATUS
       Na parte de baixo, mostra o estado atual do programa
       
    4. ATALHOS DE TECLADO
       Configura os atalhos globais para controlar o programa
    
    EXPLICAÇÃO TÉCNICA:
    Herda de CTk (janela principal do CustomTkinter). Usa CTkTabview
    para organizar as abas. Integra HotkeyManager para atalhos globais.
    
    Attributes:
        tab_recording (RecordingTab): Aba de gravação
        tab_playback (PlaybackTab): Aba de reprodução
        tab_settings (SettingsTab): Aba de configurações
        hotkey_manager (HotkeyManager): Gerenciador de atalhos
        _status_label (CTkLabel): Label de status
    
    Example:
        >>> app = MainWindow()
        >>> app.mainloop()
    """
    
    def __init__(self):
        """
        Inicializa a janela principal.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria a janela com todas as suas partes: abas, botões, etc.
        Também configura o tema visual (cores, fontes).
        
        EXPLICAÇÃO TÉCNICA:
        Construtor que inicializa o tema, configura geometria,
        cria widgets e configura hotkeys.
        """
        # Inicializa janela principal
        super().__init__()
        
        # ====================================================================
        # CONFIGURAÇÃO DA JANELA
        # ====================================================================
        
        # Título da janela
        self.title(f"{TarefAutoTheme.PROJECT_INFO['name']} v{TarefAutoTheme.PROJECT_INFO['version']}")
        
        # Tamanho e posição - aumentado para garantir visibilidade do conteúdo
        window_width = 800
        window_height = 700
        
        # Centraliza na tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Tamanho mínimo aumentado para evitar corte de conteúdo
        self.minsize(750, 650)
        
        # ====================================================================
        # CONFIGURAÇÃO DO TEMA
        # ====================================================================
        
        # Carrega configurações e aplica tema salvo
        config = Config()
        saved_theme = config.get("ui.theme", "dark")
        ctk.set_appearance_mode(saved_theme)
        ctk.set_default_color_theme("dark-blue")
        
        # Cor de fundo da janela principal
        self.configure(fg_color=TarefAutoTheme.BACKGROUND)
        
        # ====================================================================
        # ESTADO INTERNO
        # ====================================================================
        
        # Gerenciador de atalhos
        self.hotkey_manager: Optional[HotkeyManager] = None
        
        # ====================================================================
        # CONSTRUÇÃO DA INTERFACE
        # ====================================================================
        
        self._build_ui()
        
        # ====================================================================
        # CONFIGURAÇÃO DE ATALHOS
        # ====================================================================
        
        self._setup_hotkeys()
        
        # ====================================================================
        # EVENTOS DE FECHAMENTO
        # ====================================================================
        
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _build_ui(self) -> None:
        """
        Constrói todos os elementos da interface.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria todas as partes visuais da janela:
        - Cabeçalho com logo
        - Abas no centro
        - Barra de status embaixo
        
        EXPLICAÇÃO TÉCNICA:
        Instancia e posiciona todos os widgets principais usando pack.
        """
        # ====================================================================
        # CABEÇALHO - Título e subtítulo
        # ====================================================================
        
        header_frame = ctk.CTkFrame(
            self,
            height=60,
            **TarefAutoTheme.get_frame_style("transparent")
        )
        header_frame.pack(fill="x", padx=15, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Container central para título e subtítulo
        center_container = ctk.CTkFrame(header_frame, **TarefAutoTheme.get_frame_style("transparent"))
        center_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título centralizado
        logo_label = ctk.CTkLabel(
            center_container,
            text=TarefAutoTheme.PROJECT_INFO['name'],
            font=ctk.CTkFont(
                family=TarefAutoTheme.FONT_FAMILY,
                size=22,
                weight="bold"
            ),
            text_color=TarefAutoTheme.PRIMARY  # Ciano
        )
        logo_label.pack()
        
        # Subtítulo/Descrição
        subtitle_label = ctk.CTkLabel(
            center_container,
            text="Automação de tarefas repetitivas",
            font=ctk.CTkFont(size=11),
            text_color=TarefAutoTheme.TEXT_MUTED
        )
        subtitle_label.pack()
        
        # ====================================================================
        # TABVIEW (ABAS) - Botões dentro do container
        # ====================================================================
        
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=TarefAutoTheme.BACKGROUND_SECONDARY,
            segmented_button_fg_color=TarefAutoTheme.BACKGROUND_TERTIARY,
            segmented_button_selected_color="#2D5A5A",  # Verde-azulado escuro
            segmented_button_selected_hover_color="#3D6A6A",
            segmented_button_unselected_color=TarefAutoTheme.BACKGROUND_LIGHTER,
            segmented_button_unselected_hover_color="#3A3A3A",
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            text_color_disabled=TarefAutoTheme.TEXT_MUTED,
            corner_radius=8
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Configura a fonte dos botões das abas
        self.tabview._segmented_button.configure(
            font=ctk.CTkFont(family=TarefAutoTheme.FONT_FAMILY, size=12, weight="bold")
        )
        
        # Cria as abas
        self.tabview.add("📹 Gravação")
        self.tabview.add("▶️ Reprodução")
        self.tabview.add("⚙️ Configurações")
        
        # ====================================================================
        # CONTEÚDO DAS ABAS
        # ====================================================================
        
        # Aba de Gravação
        self.tab_recording = RecordingTab(
            self.tabview.tab("📹 Gravação"),
            on_session_ready=self._on_recording_ready
        )
        self.tab_recording.pack(fill="both", expand=True)
        
        # Aba de Reprodução
        self.tab_playback = PlaybackTab(
            self.tabview.tab("▶️ Reprodução"),
            on_playback_started=self._on_playback_started,
            on_playback_stopped=self._on_playback_stopped
        )
        self.tab_playback.pack(fill="both", expand=True)
        
        # Aba de Configurações
        self.tab_settings = SettingsTab(
            self.tabview.tab("⚙️ Configurações"),
            on_hotkeys_changed=self._on_hotkeys_changed
        )
        self.tab_settings.pack(fill="both", expand=True)
        
        # ====================================================================
        # BARRA DE STATUS
        # ====================================================================
        
        status_frame = ctk.CTkFrame(
            self,
            height=40,
            **TarefAutoTheme.get_frame_style("transparent")
        )
        status_frame.pack(fill="x", padx=15, pady=(5, 10))
        status_frame.pack_propagate(False)
        
        self._status_label = ctk.CTkLabel(
            status_frame,
            text="✅ Pronto | Atalhos: F9 (gravar) | F10 (reproduzir) | Esc (parar)",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._status_label.pack(side="left", pady=5)
        
        # Versão e créditos à direita
        credits_frame = ctk.CTkFrame(status_frame, **TarefAutoTheme.get_frame_style("transparent"))
        credits_frame.pack(side="right", pady=5)
        
        version_label = ctk.CTkLabel(
            credits_frame,
            text=f"v{TarefAutoTheme.PROJECT_INFO['version']}",
            **TarefAutoTheme.get_label_style("muted")
        )
        version_label.pack(side="left", padx=(0, 10))
        
        credits_label = ctk.CTkLabel(
            credits_frame,
            text=f"por {TarefAutoTheme.PROJECT_INFO['author']}",
            **TarefAutoTheme.get_label_style("muted")
        )
        credits_label.pack(side="left")

    def _setup_hotkeys(self) -> None:
        """
        Configura os atalhos de teclado globais.
        
        EXPLICAÇÃO PARA INICIANTES:
        Os atalhos de teclado funcionam mesmo quando você está em outro
        programa. Isso é essencial porque você vai usar o TarefAuto para
        automatizar ações em outros programas.
        
        Por exemplo:
        - Ctrl+F9 inicia/para gravação
        - Ctrl+F10 inicia/para reprodução
        - Esc para tudo de emergência
        
        EXPLICAÇÃO TÉCNICA:
        Cria um HotkeyManager e registra callbacks para cada ação.
        Os atalhos são globais (capturados mesmo sem foco na janela).
        """
        # Cria o gerenciador de atalhos
        self.hotkey_manager = HotkeyManager()
        
        # Obtém atalhos das configurações
        hotkeys = self.tab_settings.get_hotkeys()
        
        # Registra atalhos (toggle - uma tecla para iniciar/parar)
        if "toggle_recording" in hotkeys:
            self.hotkey_manager.register_hotkey(
                hotkeys["toggle_recording"],
                self._hotkey_toggle_recording
            )
        
        if "toggle_playback" in hotkeys:
            self.hotkey_manager.register_hotkey(
                hotkeys["toggle_playback"],
                self._hotkey_toggle_playback
            )
        
        if "emergency_stop" in hotkeys:
            self.hotkey_manager.register_hotkey(
                hotkeys["emergency_stop"],
                self._hotkey_emergency_stop
            )
        
        # Inicia escuta
        self.hotkey_manager.start()

    def _on_hotkeys_changed(self, hotkeys: Dict[str, str]) -> None:
        """
        Callback quando os atalhos são alterados nas configurações.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você muda um atalho na aba de configurações, esta função
        atualiza os atalhos ativos no programa.
        
        EXPLICAÇÃO TÉCNICA:
        Recria o HotkeyManager com os novos atalhos.
        
        Args:
            hotkeys: Novos atalhos configurados
        """
        # Para o gerenciador atual
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        # Reconfigura com novos atalhos
        self._setup_hotkeys()
        
        # Atualiza status
        self._update_status("✅ Atalhos atualizados")

    # ========================================================================
    # CALLBACKS DE COMUNICAÇÃO ENTRE ABAS
    # ========================================================================

    def _on_recording_ready(self, session: RecordingSession) -> None:
        """
        Callback quando uma gravação é concluída.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você termina de gravar, a gravação é automaticamente
        disponibilizada na aba de reprodução.
        
        EXPLICAÇÃO TÉCNICA:
        Passa a sessão para PlaybackTab e opcionalmente troca de aba.
        
        Args:
            session: Sessão de gravação concluída
        """
        # Disponibiliza a sessão na aba de reprodução
        self.tab_playback.set_session(session)
        
        # Atualiza status
        event_count = len(session.events)
        duration = session.get_duration()
        self._update_status(
            f"✅ Gravação concluída: {event_count} eventos, {duration:.1f}s"
        )

    def _on_playback_started(self) -> None:
        """
        Callback quando a reprodução inicia.
        
        EXPLICAÇÃO PARA INICIANTES:
        Atualiza a barra de status para mostrar que está reproduzindo.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza UI para refletir estado de reprodução.
        """
        self._update_status("▶️ Reproduzindo...")

    def _on_playback_stopped(self) -> None:
        """
        Callback quando a reprodução para.
        
        EXPLICAÇÃO PARA INICIANTES:
        Atualiza a barra de status quando a reprodução termina.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza UI para refletir estado parado.
        """
        self._update_status("✅ Reprodução finalizada")

    # ========================================================================
    # CALLBACKS DE ATALHOS
    # ========================================================================

    def _hotkey_toggle_recording(self) -> None:
        """
        Callback do atalho para alternar gravação (toggle).
        
        EXPLICAÇÃO PARA INICIANTES:
        Chamado quando você pressiona o atalho de gravação.
        Se está gravando, para. Se não está, inicia.
        Não permite gravar enquanto reproduz.
        
        EXPLICAÇÃO TÉCNICA:
        Executa na thread principal via after() para thread-safety.
        """
        def toggle():
            if self.tab_recording.is_recording():
                self.tab_recording.stop_recording_external()
                self._update_status("⏹️ Gravação parada")
            else:
                # Bloqueia se estiver reproduzindo
                if self.tab_playback.is_playing():
                    self._update_status("⚠️ Pare a reprodução antes de gravar")
                    return
                self.tab_recording.start_recording_external()
                self._update_status("⏺️ Gravando...")
        self.after(0, toggle)

    def _hotkey_toggle_playback(self) -> None:
        """
        Callback do atalho para alternar reprodução (toggle).
        
        EXPLICAÇÃO PARA INICIANTES:
        Chamado quando você pressiona o atalho de reprodução.
        Se está reproduzindo, para. Se não está, inicia.
        Para a gravação automaticamente se estiver gravando.
        
        EXPLICAÇÃO TÉCNICA:
        Executa via after() para thread-safety.
        """
        def toggle():
            if self.tab_playback.is_playing():
                self.tab_playback.stop_playback_external()
                self._update_status("⏹️ Reprodução parada")
            else:
                # Para gravação automaticamente se estiver gravando
                if self.tab_recording.is_recording():
                    self.tab_recording.stop_recording_external()
                    self._update_status("⏹️ Gravação parada → Iniciando reprodução...")
                self.tab_playback.start_playback_external()
                self._update_status("▶️ Reproduzindo...")
        self.after(0, toggle)

    def _hotkey_emergency_stop(self) -> None:
        """
        Callback do atalho de parada de emergência.
        
        EXPLICAÇÃO PARA INICIANTES:
        Para TUDO imediatamente quando você pressiona Esc. Use se algo
        der errado e você precisar parar o programa rapidamente.
        
        EXPLICAÇÃO TÉCNICA:
        Para gravação e reprodução simultaneamente.
        """
        self.after(0, self._emergency_stop)

    def _emergency_stop(self) -> None:
        """
        Para todas as operações de emergência.
        
        EXPLICAÇÃO PARA INICIANTES:
        Interrompe qualquer gravação ou reprodução em andamento.
        É o "botão de pânico" do programa.
        
        EXPLICAÇÃO TÉCNICA:
        Chama stop em todas as operações ativas.
        """
        # Para gravação se ativa
        if self.tab_recording.is_recording():
            self.tab_recording.stop_recording_external()
        
        # Para reprodução se ativa
        if self.tab_playback.is_playing():
            self.tab_playback.stop_playback_external()
        
        self._update_status("⚠️ PARADA DE EMERGÊNCIA")

    # ========================================================================
    # MÉTODOS AUXILIARES
    # ========================================================================

    def _update_status(self, message: str) -> None:
        """
        Atualiza a mensagem da barra de status.
        
        EXPLICAÇÃO PARA INICIANTES:
        Muda o texto que aparece na parte de baixo da janela.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza o texto do label de status.
        
        Args:
            message: Nova mensagem de status
        """
        self._status_label.configure(text=message)

    def _on_closing(self) -> None:
        """
        Callback quando a janela é fechada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Limpa tudo antes de fechar o programa:
        - Para gravações em andamento
        - Para reproduções em andamento
        - Desativa os atalhos de teclado
        
        EXPLICAÇÃO TÉCNICA:
        Cleanup de recursos antes de destruir a janela.
        """
        # Para operações ativas
        if self.tab_recording.is_recording():
            self.tab_recording.stop_recording_external()
        
        if self.tab_playback.is_playing():
            self.tab_playback.stop_playback_external()
        
        # Para gerenciador de atalhos
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        # Destrói a janela
        self.destroy()


# ============================================================================
# EXECUÇÃO DIRETA (PARA TESTES)
# ============================================================================

if __name__ == "__main__":
    """
    EXPLICAÇÃO PARA INICIANTES:
    Este bloco só executa quando você roda este arquivo diretamente.
    Útil para testar se a janela principal está funcionando.
    
    EXPLICAÇÃO TÉCNICA:
    Ponto de entrada para teste isolado do módulo.
    """
    print("=" * 60)
    print("TarefAuto - Teste da Janela Principal")
    print("=" * 60)
    
    # Cria e executa a janela
    app = MainWindow()
    app.mainloop()
