# ============================================================================
# TarefAuto - Aba de Reprodução (playback_tab.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este arquivo cria a segunda aba do programa - a aba de reprodução. Aqui o
# usuário pode:
# - Carregar uma gravação salva anteriormente
# - Escolher como reproduzir (uma vez, várias vezes, infinitamente, etc)
# - Ajustar a velocidade (mais rápido ou mais devagar)
# - Iniciar e parar a reprodução
#
# A reprodução executa exatamente as mesmas ações que foram gravadas,
# como se alguém estivesse usando seu computador.
#
# EXPLICAÇÃO TÉCNICA:
# Implementa um CTkFrame com controles de playback. Usa a classe Player
# para executar os eventos e fornece uma interface para configurar
# modo de loop, velocidade e outras opções.
#
# ============================================================================

"""
Aba de controle de reprodução do TarefAuto.

Este módulo contém a classe PlaybackTab que implementa a interface
para configurar e controlar a reprodução de eventos gravados.

Classes:
    PlaybackTab: Frame com controles de reprodução

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
from typing import Optional, Callable

# Importações internas
from src.gui.theme import TarefAutoTheme
from src.core.player import Player, LoopMode
from src.core.events import RecordingSession


# ============================================================================
# CLASSE PLAYBACK TAB
# ============================================================================

class PlaybackTab(ctk.CTkFrame):
    """
    Aba de controle de reprodução.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta classe cria a interface da aba de reprodução. É como o controle
    de um player de música, mas em vez de música, ele "toca" suas ações
    gravadas - mexe o mouse, clica nos lugares, digita textos.
    
    Você pode escolher:
    - Reproduzir uma vez só (SINGLE)
    - Reproduzir X vezes (COUNT)
    - Reproduzir por X segundos (DURATION)
    - Reproduzir infinitamente até você parar (INFINITE)
    
    Também pode ajustar a velocidade:
    - 0.5x = metade da velocidade (mais lento)
    - 1.0x = velocidade normal
    - 2.0x = dobro da velocidade (mais rápido)
    
    EXPLICAÇÃO TÉCNICA:
    Herda de CTkFrame e gerencia um Player interno. Os controles de
    loop mode e speed são configurados via widgets CustomTkinter.
    A reprodução acontece em thread separada para não travar a UI.
    
    Attributes:
        player (Player): Instância do reprodutor de eventos
        current_session (RecordingSession): Sessão carregada para reprodução
        _speed_var (DoubleVar): Velocidade de reprodução
        _loop_mode_var (StringVar): Modo de loop selecionado
        _loop_count_var (IntVar): Número de repetições
        _duration_var (IntVar): Duração em segundos
    
    Example:
        >>> tab = PlaybackTab(parent_frame)
        >>> tab.set_session(recording_session)
        >>> tab.pack(fill="both", expand=True)
    """
    
    def __init__(
        self,
        master,
        on_playback_started: Optional[Callable] = None,
        on_playback_stopped: Optional[Callable] = None,
        **kwargs
    ):
        """
        Inicializa a aba de reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria todos os controles para reprodução: botões, sliders, opções.
        
        EXPLICAÇÃO TÉCNICA:
        Construtor que inicializa widgets e callbacks de notificação.
        
        Args:
            master: Widget pai
            on_playback_started: Callback quando reprodução inicia
            on_playback_stopped: Callback quando reprodução para
            **kwargs: Argumentos adicionais para CTkFrame
        """
        super().__init__(master, **TarefAutoTheme.get_frame_style("default"), **kwargs)
        
        # ====================================================================
        # CALLBACKS
        # ====================================================================
        
        self.on_playback_started = on_playback_started
        self.on_playback_stopped = on_playback_stopped
        
        # ====================================================================
        # ESTADO INTERNO
        # ====================================================================
        
        # Player e sessão
        self.player: Optional[Player] = None
        self.current_session: Optional[RecordingSession] = None
        
        # Variáveis de controle
        self._speed_var = ctk.DoubleVar(value=1.0)
        self._loop_mode_var = ctk.StringVar(value="SINGLE")
        self._loop_count_var = ctk.IntVar(value=5)
        self._duration_var = ctk.IntVar(value=60)
        
        # Flags
        self._update_job = None
        
        # ====================================================================
        # CONSTRUÇÃO DA INTERFACE
        # ====================================================================
        
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Constrói todos os elementos da interface.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria a interface com:
        - Área para carregar arquivo
        - Informações da gravação carregada
        - Opções de repetição
        - Controle de velocidade
        - Botões de play/stop
        
        EXPLICAÇÃO TÉCNICA:
        Instancia e configura todos os widgets em seções organizadas.
        """
        # ====================================================================
        # FRAME SCROLLABLE PARA TODO O CONTEÚDO
        # ====================================================================
        
        content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=TarefAutoTheme.BACKGROUND_LIGHTER,
            scrollbar_button_hover_color=TarefAutoTheme.PRIMARY_DARK
        )
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # ====================================================================
        # TÍTULO
        # ====================================================================
        
        title_label = ctk.CTkLabel(
            content_frame,
            text="▶️ Controles de Reprodução",
            **TarefAutoTheme.get_label_style("heading")
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # ====================================================================
        # FRAME DE CARREGAMENTO DE ARQUIVO
        # ====================================================================
        
        file_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        file_frame.pack(fill="x", padx=15, pady=10)
        
        file_label = ctk.CTkLabel(
            file_frame,
            text="Arquivo de Gravação:",
            **TarefAutoTheme.get_label_style("default")
        )
        file_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Container para botão e nome do arquivo
        file_container = ctk.CTkFrame(file_frame, **TarefAutoTheme.get_frame_style("transparent"))
        file_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self._load_button = ctk.CTkButton(
            file_container,
            text="📂 Carregar",
            width=100,
            **TarefAutoTheme.get_button_style("outline"),
            command=self._load_recording
        )
        self._load_button.pack(side="left")
        
        self._file_label = ctk.CTkLabel(
            file_container,
            text="Nenhum arquivo carregado",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._file_label.pack(side="left", padx=15)
        
        # Informações da sessão carregada
        self._session_info_label = ctk.CTkLabel(
            file_frame,
            text="",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._session_info_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        # ====================================================================
        # FRAME DE MODO DE REPETIÇÃO
        # ====================================================================
        
        loop_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        loop_frame.pack(fill="x", padx=15, pady=10)
        
        loop_label = ctk.CTkLabel(
            loop_frame,
            text="Modo de Repetição:",
            **TarefAutoTheme.get_label_style("default")
        )
        loop_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Radio buttons para modo de loop
        modes_container = ctk.CTkFrame(loop_frame, **TarefAutoTheme.get_frame_style("transparent"))
        modes_container.pack(fill="x", padx=15, pady=(0, 10))
        
        # SINGLE - Uma vez
        self._radio_single = ctk.CTkRadioButton(
            modes_container,
            text="🔂 Uma vez",
            variable=self._loop_mode_var,
            value="SINGLE",
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            command=self._on_loop_mode_changed
        )
        self._radio_single.pack(anchor="w", pady=3)
        
        # COUNT - Número específico de vezes
        count_container = ctk.CTkFrame(modes_container, **TarefAutoTheme.get_frame_style("transparent"))
        count_container.pack(fill="x", pady=3)
        
        self._radio_count = ctk.CTkRadioButton(
            count_container,
            text="🔢 Repetir",
            variable=self._loop_mode_var,
            value="COUNT",
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            command=self._on_loop_mode_changed
        )
        self._radio_count.pack(side="left")
        
        self._count_entry = ctk.CTkEntry(
            count_container,
            width=60,
            textvariable=self._loop_count_var,
            **TarefAutoTheme.get_entry_style("default")
        )
        self._count_entry.pack(side="left", padx=5)
        
        count_suffix = ctk.CTkLabel(
            count_container,
            text="vezes",
            **TarefAutoTheme.get_label_style("default")
        )
        count_suffix.pack(side="left")
        
        # DURATION - Por tempo
        duration_container = ctk.CTkFrame(modes_container, **TarefAutoTheme.get_frame_style("transparent"))
        duration_container.pack(fill="x", pady=3)
        
        self._radio_duration = ctk.CTkRadioButton(
            duration_container,
            text="⏱️ Reproduzir por",
            variable=self._loop_mode_var,
            value="DURATION",
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            command=self._on_loop_mode_changed
        )
        self._radio_duration.pack(side="left")
        
        self._duration_entry = ctk.CTkEntry(
            duration_container,
            width=60,
            textvariable=self._duration_var,
            **TarefAutoTheme.get_entry_style("default")
        )
        self._duration_entry.pack(side="left", padx=5)
        
        duration_suffix = ctk.CTkLabel(
            duration_container,
            text="segundos",
            **TarefAutoTheme.get_label_style("default")
        )
        duration_suffix.pack(side="left")
        
        # INFINITE - Infinito
        self._radio_infinite = ctk.CTkRadioButton(
            modes_container,
            text="♾️ Infinito (até parar manualmente)",
            variable=self._loop_mode_var,
            value="INFINITE",
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            command=self._on_loop_mode_changed
        )
        self._radio_infinite.pack(anchor="w", pady=3)
        
        # Atualiza estado inicial dos campos
        self._on_loop_mode_changed()
        
        # ====================================================================
        # FRAME DE VELOCIDADE
        # ====================================================================
        
        speed_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        speed_frame.pack(fill="x", padx=15, pady=10)
        
        speed_header = ctk.CTkFrame(speed_frame, **TarefAutoTheme.get_frame_style("transparent"))
        speed_header.pack(fill="x", padx=15, pady=(15, 5))
        
        speed_label = ctk.CTkLabel(
            speed_header,
            text="⚡ Velocidade:",
            **TarefAutoTheme.get_label_style("default")
        )
        speed_label.pack(side="left")
        
        self._speed_value_label = ctk.CTkLabel(
            speed_header,
            text="1.0x",
            **TarefAutoTheme.get_label_style("default")
        )
        self._speed_value_label.pack(side="right")
        
        # Slider de velocidade
        self._speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=0.1,
            to=5.0,
            number_of_steps=49,  # Passos de 0.1
            variable=self._speed_var,
            progress_color=TarefAutoTheme.PRIMARY,
            button_color=TarefAutoTheme.PRIMARY,
            button_hover_color=TarefAutoTheme.PRIMARY_HOVER,
            fg_color=TarefAutoTheme.BACKGROUND_SECONDARY,
            command=self._on_speed_changed
        )
        self._speed_slider.pack(fill="x", padx=15, pady=(0, 10))
        
        # Botões de velocidade predefinida
        presets_container = ctk.CTkFrame(speed_frame, **TarefAutoTheme.get_frame_style("transparent"))
        presets_container.pack(fill="x", padx=15, pady=(0, 15))
        
        for speed in [0.5, 1.0, 2.0, 3.0, 5.0]:
            btn = ctk.CTkButton(
                presets_container,
                text=f"{speed}x",
                width=50,
                height=28,
                **TarefAutoTheme.get_button_style("ghost"),
                command=lambda s=speed: self._set_speed(s)
            )
            btn.pack(side="left", padx=2)
        
        # ====================================================================
        # FRAME DE CONTROLES DE REPRODUÇÃO
        # ====================================================================
        
        control_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        control_frame.pack(fill="x", padx=15, pady=10)
        
        # Status
        status_container = ctk.CTkFrame(control_frame, **TarefAutoTheme.get_frame_style("transparent"))
        status_container.pack(fill="x", padx=15, pady=15)
        
        self._status_indicator = ctk.CTkLabel(
            status_container,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color=TarefAutoTheme.IDLE
        )
        self._status_indicator.pack(side="left")
        
        self._status_label = ctk.CTkLabel(
            status_container,
            text="Aguardando gravação",
            **TarefAutoTheme.get_label_style("default")
        )
        self._status_label.pack(side="left", padx=10)
        
        # Progresso
        progress_container = ctk.CTkFrame(control_frame, **TarefAutoTheme.get_frame_style("transparent"))
        progress_container.pack(fill="x", padx=15, pady=(0, 10))
        
        self._progress_label = ctk.CTkLabel(
            progress_container,
            text="Loop: 0/0",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._progress_label.pack(side="left")
        
        self._time_label = ctk.CTkLabel(
            progress_container,
            text="Tempo: 0.0s",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._time_label.pack(side="right")
        
        # Botão de reprodução
        self._play_button = ctk.CTkButton(
            control_frame,
            text="▶️ INICIAR REPRODUÇÃO",
            height=50,
            font=ctk.CTkFont(family=TarefAutoTheme.FONT_FAMILY, size=16, weight="bold"),
            **TarefAutoTheme.get_button_style("secondary"),
            command=self._toggle_playback,
            state="disabled"
        )
        self._play_button.pack(fill="x", padx=15, pady=(5, 15))
        
        # ====================================================================
        # DICA
        # ====================================================================
        
        tip_label = ctk.CTkLabel(
            self,
            text="💡 Dica: Use o atalho de teclado para parar a reprodução a qualquer momento",
            **TarefAutoTheme.get_label_style("muted")
        )
        tip_label.pack(side="bottom", pady=20)

    def _on_loop_mode_changed(self) -> None:
        """
        Callback quando o modo de loop é alterado.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você seleciona um modo diferente (uma vez, X vezes, etc),
        esta função habilita ou desabilita os campos relacionados.
        Por exemplo, se você escolher "Uma vez", os campos de contagem
        e duração ficam desabilitados.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza o estado dos widgets de entrada baseado no modo selecionado.
        """
        mode = self._loop_mode_var.get()
        
        # Desabilita todos primeiro
        self._count_entry.configure(state="disabled")
        self._duration_entry.configure(state="disabled")
        
        # Habilita o campo relevante
        if mode == "COUNT":
            self._count_entry.configure(state="normal")
        elif mode == "DURATION":
            self._duration_entry.configure(state="normal")

    def _on_speed_changed(self, value: float) -> None:
        """
        Callback quando a velocidade é alterada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você move o slider de velocidade, esta função atualiza
        o número mostrado (ex: "2.5x").
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza o label de velocidade com o valor formatado.
        
        Args:
            value: Novo valor de velocidade
        """
        self._speed_value_label.configure(text=f"{value:.1f}x")

    def _set_speed(self, speed: float) -> None:
        """
        Define uma velocidade específica.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você clica em um dos botões de velocidade predefinida
        (0.5x, 1.0x, etc), esta função ajusta o slider.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza a variável de velocidade e o label.
        
        Args:
            speed: Velocidade desejada
        """
        self._speed_var.set(speed)
        self._speed_value_label.configure(text=f"{speed:.1f}x")

    def _load_recording(self) -> None:
        """
        Carrega uma gravação de um arquivo.
        
        EXPLICAÇÃO PARA INICIANTES:
        Abre uma janela para você escolher um arquivo de gravação (.json).
        Depois de carregar, você pode reproduzir as ações gravadas.
        
        EXPLICAÇÃO TÉCNICA:
        Usa filedialog para seleção e RecordingSession.load() para carregar.
        """
        filepath = filedialog.askopenfilename(
            title="Carregar Gravação",
            filetypes=[
                ("Arquivos JSON", "*.json"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if filepath:
            session = RecordingSession.load(filepath)
            if session:
                self.set_session(session)
                
                # Extrai nome do arquivo para exibição
                filename = filepath.split("/")[-1].split("\\")[-1]
                self._file_label.configure(text=filename)
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível carregar o arquivo.\n"
                    "Verifique se é um arquivo de gravação válido."
                )

    def _toggle_playback(self) -> None:
        """
        Alterna entre iniciar e parar reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Funciona como play/pause:
        - Se parado: começa a reproduzir
        - Se reproduzindo: para a reprodução
        
        EXPLICAÇÃO TÉCNICA:
        Verifica estado do player e chama start/stop conforme necessário.
        """
        if self.player and self.player.is_playing:
            self._stop_playback()
        else:
            self._start_playback()

    def _start_playback(self) -> None:
        """
        Inicia a reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Começa a reproduzir as ações gravadas com as configurações que
        você escolheu (velocidade, modo de repetição, etc).
        
        EXPLICAÇÃO TÉCNICA:
        Cria um Player com as configurações atuais e inicia a reprodução.
        O Player executa em thread separada.
        """
        if not self.current_session:
            return
        
        # Obtém modo de loop
        mode_str = self._loop_mode_var.get()
        loop_mode = LoopMode[mode_str]
        
        # Obtém valor do loop baseado no modo
        if mode_str == "COUNT":
            loop_value = self._loop_count_var.get()
        elif mode_str == "DURATION":
            loop_value = self._duration_var.get()
        else:
            loop_value = 1
        
        # Cria o player com callbacks
        self.player = Player(
            on_progress_callback=self._on_progress,
            on_complete_callback=self._on_playback_complete
        )
        
        # Configura o player
        self.player.set_loop_mode(loop_mode, loop_value)
        self.player.set_speed(self._speed_var.get())
        
        # Inicia a reprodução
        self.player.play(self.current_session)
        
        # Atualiza UI
        self._update_ui_playback_state(True)
        self._start_ui_updates()
        
        # Callback
        if self.on_playback_started:
            self.on_playback_started()

    def _stop_playback(self) -> None:
        """
        Para a reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Interrompe a reprodução imediatamente.
        
        EXPLICAÇÃO TÉCNICA:
        Chama player.stop() e atualiza a UI.
        """
        if self.player:
            self.player.stop()
            self._stop_ui_updates()
            self._update_ui_playback_state(False)
            
            if self.on_playback_stopped:
                self.on_playback_stopped()

    def _on_playback_complete(self) -> None:
        """
        Callback quando a reprodução termina naturalmente.
        
        EXPLICAÇÃO PARA INICIANTES:
        Chamado quando a reprodução termina sozinha (não foi interrompida
        pelo usuário). Atualiza a interface para mostrar que terminou.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza UI de forma thread-safe usando after().
        """
        # Usa after() para thread-safety
        self.after(0, self._handle_playback_complete)

    def _on_progress(self, current_loop: int, total_loops: int, event_index: int) -> None:
        """
        Callback de progresso da reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Chamado periodicamente durante a reprodução para mostrar
        o progresso atual (qual loop, qual evento).
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza UI de forma thread-safe usando after().
        
        Args:
            current_loop: Número do loop atual
            total_loops: Total de loops (-1 se infinito)
            event_index: Índice do evento atual
        """
        # Atualiza UI na thread principal
        self.after(0, lambda: self._update_progress_display(current_loop, total_loops, event_index))

    def _update_progress_display(self, current_loop: int, total_loops: int, event_index: int) -> None:
        """Atualiza o display de progresso na thread principal."""
        if total_loops > 0:
            self._progress_label.configure(text=f"Loop: {current_loop}/{total_loops}")
        else:
            self._progress_label.configure(text=f"Loop: {current_loop}")

    def _handle_playback_complete(self) -> None:
        """
        Processa o término da reprodução na thread principal.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função é chamada quando a reprodução termina e atualiza
        a interface para refletir isso.
        
        EXPLICAÇÃO TÉCNICA:
        Executa na main thread após ser agendado pelo callback do player.
        """
        self._stop_ui_updates()
        self._update_ui_playback_state(False)
        
        if self.on_playback_stopped:
            self.on_playback_stopped()

    def _update_ui_playback_state(self, is_playing: bool) -> None:
        """
        Atualiza a interface baseado no estado de reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Muda a aparência dos elementos:
        - Reproduzindo: indicador verde, botão diz "PARAR", opções bloqueadas
        - Parado: indicador cinza, botão diz "INICIAR", opções liberadas
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza cores, textos e estados baseado em is_playing.
        
        Args:
            is_playing: True se está reproduzindo
        """
        if is_playing:
            self._status_indicator.configure(text_color=TarefAutoTheme.PLAYING)
            self._status_label.configure(text="Reproduzindo...")
            self._play_button.configure(
                text="⏹️ PARAR REPRODUÇÃO",
                **TarefAutoTheme.get_button_style("danger")
            )
            
            # Desabilita controles
            self._load_button.configure(state="disabled")
            self._radio_single.configure(state="disabled")
            self._radio_count.configure(state="disabled")
            self._radio_duration.configure(state="disabled")
            self._radio_infinite.configure(state="disabled")
            self._count_entry.configure(state="disabled")
            self._duration_entry.configure(state="disabled")
            self._speed_slider.configure(state="disabled")
        else:
            self._status_indicator.configure(text_color=TarefAutoTheme.IDLE)
            self._status_label.configure(text="Reprodução finalizada" if self.player else "Pronto")
            self._play_button.configure(
                text="▶️ INICIAR REPRODUÇÃO",
                **TarefAutoTheme.get_button_style("secondary")
            )
            
            # Habilita controles
            self._load_button.configure(state="normal")
            self._radio_single.configure(state="normal")
            self._radio_count.configure(state="normal")
            self._radio_duration.configure(state="normal")
            self._radio_infinite.configure(state="normal")
            self._speed_slider.configure(state="normal")
            self._on_loop_mode_changed()  # Restaura estado dos campos

    def _start_ui_updates(self) -> None:
        """
        Inicia atualizações periódicas da UI.
        
        EXPLICAÇÃO PARA INICIANTES:
        Durante a reprodução, atualiza os contadores de tempo e loops.
        
        EXPLICAÇÃO TÉCNICA:
        Agenda chamadas periódicas via after().
        """
        self._update_ui()

    def _stop_ui_updates(self) -> None:
        """
        Para atualizações periódicas da UI.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cancela as atualizações quando a reprodução para.
        
        EXPLICAÇÃO TÉCNICA:
        Cancela o job agendado.
        """
        if self._update_job:
            self.after_cancel(self._update_job)
            self._update_job = None

    def _update_ui(self) -> None:
        """
        Atualiza informações durante a reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Mostra em tempo real:
        - Em qual loop está (ex: "Loop: 3/10")
        - Quanto tempo passou
        
        EXPLICAÇÃO TÉCNICA:
        Lê dados do player e atualiza labels.
        """
        if self.player and self.player.is_playing:
            # Atualiza contadores
            self._progress_label.configure(
                text=f"Loop: {self.player.get_current_loop()}"
            )
            
            elapsed = self.player.get_elapsed_time()
            self._time_label.configure(text=f"Tempo: {elapsed:.1f}s")
            
            # Agenda próxima atualização
            self._update_job = self.after(100, self._update_ui)

    # ========================================================================
    # MÉTODOS PÚBLICOS
    # ========================================================================

    def set_session(self, session: RecordingSession) -> None:
        """
        Define a sessão de gravação para reprodução.
        
        EXPLICAÇÃO PARA INICIANTES:
        Carrega uma gravação para ser reproduzida. Pode ser uma gravação
        que você acabou de fazer ou uma carregada de arquivo.
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza current_session e UI.
        
        Args:
            session: Sessão de gravação a ser reproduzida
        """
        self.current_session = session
        
        # Atualiza info da sessão
        event_count = len(session.events)
        duration = session.get_duration()
        self._session_info_label.configure(
            text=f"📊 {event_count} eventos | ⏱️ {duration:.1f}s de duração"
        )
        
        # Habilita botão de reprodução
        self._play_button.configure(state="normal")
        self._status_label.configure(text="Pronto para reproduzir")

    def start_playback_external(self) -> None:
        """
        Inicia reprodução (chamado externamente, ex: por hotkey).
        
        EXPLICAÇÃO PARA INICIANTES:
        Permite que atalhos de teclado iniciem a reprodução.
        
        EXPLICAÇÃO TÉCNICA:
        Interface pública para iniciar via hotkey.
        """
        if self.current_session and (not self.player or not self.player.is_playing):
            self._start_playback()

    def stop_playback_external(self) -> None:
        """
        Para reprodução (chamado externamente, ex: por hotkey).
        
        EXPLICAÇÃO PARA INICIANTES:
        Permite que atalhos de teclado parem a reprodução.
        
        EXPLICAÇÃO TÉCNICA:
        Interface pública para parar via hotkey.
        """
        if self.player and self.player.is_playing:
            self._stop_playback()

    def is_playing(self) -> bool:
        """
        Verifica se está reproduzindo.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna True se a reprodução está em andamento.
        
        EXPLICAÇÃO TÉCNICA:
        Verifica estado do player.
        
        Returns:
            bool: True se reproduzindo
        """
        return self.player is not None and self.player.is_playing
