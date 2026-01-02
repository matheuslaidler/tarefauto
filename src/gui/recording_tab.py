# ============================================================================
# TarefAuto - Aba de Gravação (recording_tab.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este arquivo cria a primeira aba do programa - a aba de gravação. Aqui o
# usuário pode:
# - Escolher se quer gravar mouse, teclado ou ambos
# - Iniciar e parar a gravação
# - Ver quantos eventos foram gravados
# - Salvar a gravação em um arquivo
#
# A aba mostra em tempo real o status da gravação (se está gravando ou não)
# e quantas ações foram capturadas.
#
# EXPLICAÇÃO TÉCNICA:
# Implementa um CTkFrame que contém todos os controles relacionados à
# gravação de eventos. Comunica-se com a classe Recorder através de
# callbacks e atualiza a UI de forma thread-safe usando after().
#
# ============================================================================

"""
Aba de controle de gravação do TarefAuto.

Este módulo contém a classe RecordingTab que implementa a interface
para configurar e controlar a gravação de eventos de mouse e teclado.

Classes:
    RecordingTab: Frame com controles de gravação

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# Módulos padrão
import os
from datetime import datetime

# customtkinter: Framework de GUI
import customtkinter as ctk

# tkinter: Para diálogos de arquivo
from tkinter import filedialog, messagebox

# typing: Anotações de tipo
from typing import Optional, Callable

# Importações internas
from src.gui.theme import TarefAutoTheme
from src.core.recorder import Recorder
from src.core.events import RecordingSession, InputEvent


# ============================================================================
# CLASSE RECORDING TAB
# ============================================================================

class RecordingTab(ctk.CTkFrame):
    """
    Aba de controle de gravação.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta classe cria a interface da aba de gravação. Pense nela como um
    "painel de controle" onde você:
    
    1. Escolhe O QUE gravar (mouse, teclado ou ambos)
    2. Clica em "Iniciar Gravação" para começar
    3. Vê em tempo real quantas ações foram capturadas
    4. Clica em "Parar" quando terminar
    5. Salva a gravação em um arquivo para usar depois
    
    A interface mostra:
    - Checkboxes para escolher o que gravar
    - Botão grande de gravar/parar
    - Contador de eventos
    - Duração da gravação
    - Botão para salvar
    
    EXPLICAÇÃO TÉCNICA:
    Herda de CTkFrame e implementa a UI de gravação. Usa um Recorder
    interno para capturar eventos e atualiza a UI periodicamente usando
    root.after() para thread-safety.
    
    Attributes:
        recorder (Recorder): Instância do gravador de eventos
        current_session (RecordingSession): Sessão atual de gravação
        on_session_ready (Callable): Callback quando gravação está pronta
        _event_count_label (CTkLabel): Label do contador de eventos
        _duration_label (CTkLabel): Label da duração
        _status_indicator (CTkLabel): Indicador visual de status
    
    Example:
        >>> tab = RecordingTab(parent_frame)
        >>> tab.pack(fill="both", expand=True)
    """
    
    def __init__(
        self,
        master,
        on_session_ready: Optional[Callable[[RecordingSession], None]] = None,
        **kwargs
    ):
        """
        Inicializa a aba de gravação.
        
        EXPLICAÇÃO PARA INICIANTES:
        Cria todos os elementos visuais da aba: botões, checkboxes, labels.
        O parâmetro 'master' é a janela ou frame onde esta aba será colocada.
        
        EXPLICAÇÃO TÉCNICA:
        Construtor que inicializa o frame e cria todos os widgets filhos.
        O callback on_session_ready permite notificar outras partes da
        aplicação quando uma gravação é concluída.
        
        Args:
            master: Widget pai (geralmente um CTkTabview)
            on_session_ready: Callback chamado com a sessão quando gravação termina
            **kwargs: Argumentos adicionais para CTkFrame
        """
        # Inicializa o frame pai com estilo do tema
        super().__init__(master, **TarefAutoTheme.get_frame_style("default"), **kwargs)
        
        # ====================================================================
        # ESTADO INTERNO
        # ====================================================================
        
        # Callback para quando a gravação estiver pronta
        self.on_session_ready = on_session_ready
        
        # Gravador de eventos
        self.recorder: Optional[Recorder] = None
        
        # Sessão atual de gravação
        self.current_session: Optional[RecordingSession] = None
        
        # Caminho do último arquivo salvo
        self._last_saved_file: Optional[str] = None
        
        # Variáveis de controle para checkboxes
        # BooleanVar mantém sincronizado o estado do checkbox
        self._record_mouse = ctk.BooleanVar(value=True)
        self._record_keyboard = ctk.BooleanVar(value=True)
        self._record_mouse_movement = ctk.BooleanVar(value=True)
        
        # Auto-save (carregar da config)
        from src.utils.config import Config
        config = Config()
        self._auto_save = ctk.BooleanVar(value=config.get("files.auto_save", True))
        
        # Flag de atualização da UI
        self._update_job = None
        
        # ====================================================================
        # CONSTRUÇÃO DA INTERFACE
        # ====================================================================
        
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Constrói todos os elementos da interface.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função cria e posiciona todos os elementos visuais da aba:
        - Título
        - Checkboxes de configuração
        - Botão de gravação
        - Indicadores de status
        - Botão de salvar
        
        Cada seção é organizada em "frames" (caixas) para manter tudo alinhado.
        
        EXPLICAÇÃO TÉCNICA:
        Método privado que instancia e configura todos os widgets.
        Usa grid e pack para layout. Organiza em seções lógicas.
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
        # TÍTULO DA SEÇÃO
        # ====================================================================
        
        title_label = ctk.CTkLabel(
            content_frame,
            text="⚙️ Configuração de Gravação",
            **TarefAutoTheme.get_label_style("heading")
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # ====================================================================
        # FRAME DE OPÇÕES DE GRAVAÇÃO
        # ====================================================================
        
        options_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        options_frame.pack(fill="x", padx=15, pady=10)
        
        # Subtítulo
        options_label = ctk.CTkLabel(
            options_frame,
            text="O que deseja gravar?",
            **TarefAutoTheme.get_label_style("default")
        )
        options_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Checkbox: Gravar Mouse
        self._mouse_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="🖱️ Gravar Mouse (cliques e movimentos)",
            variable=self._record_mouse,
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            command=self._on_options_changed
        )
        self._mouse_checkbox.pack(anchor="w", padx=15, pady=5)
        
        # Checkbox: Gravar movimento do mouse (sub-opção)
        self._mouse_movement_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="    ↳ Incluir movimento (além de cliques)",
            variable=self._record_mouse_movement,
            fg_color=TarefAutoTheme.PRIMARY_DARK,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_SECONDARY,
        )
        self._mouse_movement_checkbox.pack(anchor="w", padx=15, pady=5)
        
        # Checkbox: Gravar Teclado
        self._keyboard_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="⌨️ Gravar Teclado (teclas pressionadas)",
            variable=self._record_keyboard,
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_PRIMARY,
            command=self._on_options_changed
        )
        self._keyboard_checkbox.pack(anchor="w", padx=15, pady=(5, 15))
        
        # ====================================================================
        # FRAME DE CONTROLE DE GRAVAÇÃO
        # ====================================================================
        
        control_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        control_frame.pack(fill="x", padx=15, pady=10)
        
        # Indicador de status (ponto colorido + texto)
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
            text="Pronto para gravar",
            **TarefAutoTheme.get_label_style("default")
        )
        self._status_label.pack(side="left", padx=10)
        
        # Container para informações durante gravação
        info_container = ctk.CTkFrame(control_frame, **TarefAutoTheme.get_frame_style("transparent"))
        info_container.pack(fill="x", padx=15, pady=(0, 10))
        
        # Contador de eventos
        self._event_count_label = ctk.CTkLabel(
            info_container,
            text="Eventos: 0",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._event_count_label.pack(side="left")
        
        # Duração
        self._duration_label = ctk.CTkLabel(
            info_container,
            text="Duração: 0.0s",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._duration_label.pack(side="right")
        
        # ====================================================================
        # BOTÃO DE GRAVAÇÃO
        # ====================================================================
        
        self._record_button = ctk.CTkButton(
            control_frame,
            text="⏺️ INICIAR GRAVAÇÃO",
            height=50,
            font=ctk.CTkFont(family=TarefAutoTheme.FONT_FAMILY, size=16, weight="bold"),
            **TarefAutoTheme.get_button_style("primary"),
            command=self._toggle_recording
        )
        self._record_button.pack(fill="x", padx=15, pady=(5, 15))
        
        # ====================================================================
        # FRAME DE AÇÕES PÓS-GRAVAÇÃO
        # ====================================================================
        
        actions_frame = ctk.CTkFrame(content_frame, **TarefAutoTheme.get_frame_style("card"))
        actions_frame.pack(fill="x", padx=15, pady=10)
        
        actions_label = ctk.CTkLabel(
            actions_frame,
            text="Após gravar:",
            **TarefAutoTheme.get_label_style("default")
        )
        actions_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Linha do arquivo atual
        file_row = ctk.CTkFrame(actions_frame, **TarefAutoTheme.get_frame_style("transparent"))
        file_row.pack(fill="x", padx=15, pady=(0, 10))
        
        self._file_label = ctk.CTkLabel(
            file_row,
            text="📁 Nenhuma gravação",
            **TarefAutoTheme.get_label_style("muted")
        )
        self._file_label.pack(side="left")
        
        # Checkbox de auto-save
        self._auto_save_checkbox = ctk.CTkCheckBox(
            file_row,
            text="Auto-salvar",
            variable=self._auto_save,
            fg_color=TarefAutoTheme.PRIMARY,
            hover_color=TarefAutoTheme.PRIMARY_HOVER,
            text_color=TarefAutoTheme.TEXT_SECONDARY,
            command=self._on_auto_save_changed,
            width=100
        )
        self._auto_save_checkbox.pack(side="right")
        
        # Botões de ação
        buttons_container = ctk.CTkFrame(actions_frame, **TarefAutoTheme.get_frame_style("transparent"))
        buttons_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self._save_button = ctk.CTkButton(
            buttons_container,
            text="💾 Salvar",
            width=90,
            **TarefAutoTheme.get_button_style("outline"),
            command=self._save_recording,
            state="disabled"
        )
        self._save_button.pack(side="left", padx=(0, 5))
        
        self._edit_button = ctk.CTkButton(
            buttons_container,
            text="✏️ Editar",
            width=90,
            **TarefAutoTheme.get_button_style("outline"),
            command=self._edit_recording,
            state="disabled"
        )
        self._edit_button.pack(side="left", padx=(0, 5))
        
        self._clear_button = ctk.CTkButton(
            buttons_container,
            text="🗑️ Limpar",
            width=90,
            **TarefAutoTheme.get_button_style("ghost"),
            command=self._clear_recording,
            state="disabled"
        )
        self._clear_button.pack(side="left")
        
        # ====================================================================
        # DICA NO RODAPÉ
        # ====================================================================
        
        tip_label = ctk.CTkLabel(
            content_frame,
            text="💡 Dica: Configure atalhos na aba Configurações",
            **TarefAutoTheme.get_label_style("muted")
        )
        tip_label.pack(pady=15)

    def _on_options_changed(self) -> None:
        """
        Callback quando opções de gravação são alteradas.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você marca ou desmarca um checkbox, esta função é chamada.
        Ela verifica se pelo menos uma opção está marcada (precisa gravar
        alguma coisa!) e desabilita o checkbox de movimento se mouse
        estiver desmarcado.
        
        EXPLICAÇÃO TÉCNICA:
        Valida as opções de gravação e atualiza estados de widgets dependentes.
        """
        # Desabilita opção de movimento se mouse não está selecionado
        if self._record_mouse.get():
            self._mouse_movement_checkbox.configure(state="normal")
        else:
            self._mouse_movement_checkbox.configure(state="disabled")
            self._record_mouse_movement.set(False)
        
        # Verifica se pelo menos uma opção está selecionada
        if not self._record_mouse.get() and not self._record_keyboard.get():
            self._record_button.configure(state="disabled")
        else:
            self._record_button.configure(state="normal")

    def _on_auto_save_changed(self) -> None:
        """
        Callback quando a opção de auto-save é alterada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Salva a preferência de auto-save para que o programa lembre
        da sua escolha na próxima vez que abrir.
        
        EXPLICAÇÃO TÉCNICA:
        Persiste o valor do checkbox no arquivo de configuração.
        """
        from src.utils.config import Config
        config = Config()
        config.set("files.auto_save", self._auto_save.get())

    def _edit_recording(self) -> None:
        """
        Abre o arquivo de gravação no editor padrão do sistema.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você clica em "Editar", o arquivo JSON da gravação é aberto
        no seu editor de texto padrão (Notepad, VS Code, etc.). Assim você
        pode ver ou modificar a gravação manualmente se precisar.
        
        EXPLICAÇÃO TÉCNICA:
        Usa os.startfile() no Windows para abrir o arquivo com a aplicação
        associada ao tipo .json.
        """
        if self._last_saved_file and os.path.exists(self._last_saved_file):
            try:
                # Usar subprocess para garantir que funcione corretamente
                import subprocess
                subprocess.Popen(['notepad.exe', self._last_saved_file])
            except Exception as e:
                # Fallback para os.startfile
                try:
                    os.startfile(self._last_saved_file)
                except Exception as e2:
                    messagebox.showerror(
                        "Erro",
                        f"Não foi possível abrir o arquivo:\n{e2}"
                    )
        else:
            messagebox.showwarning(
                "Aviso",
                "Nenhuma gravação salva para editar."
            )

    def _toggle_recording(self) -> None:
        """
        Alterna entre iniciar e parar gravação.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você clica no botão de gravação, esta função decide o que fazer:
        - Se não está gravando: começa a gravar
        - Se está gravando: para a gravação
        
        É como um botão de "play/pause" de um gravador.
        
        EXPLICAÇÃO TÉCNICA:
        Verifica o estado atual do recorder e chama start_recording()
        ou stop_recording() conforme apropriado.
        """
        if self.recorder and self.recorder.is_recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self) -> None:
        """
        Inicia a gravação de eventos.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função:
        1. Cria um novo gravador com suas configurações
        2. Começa a capturar tudo que você faz
        3. Atualiza a interface para mostrar que está gravando
        4. Começa a atualizar o contador de eventos
        
        EXPLICAÇÃO TÉCNICA:
        Instancia um novo Recorder com as opções selecionadas e inicia
        a captura. Agenda atualizações periódicas da UI via after().
        """
        # Cria o recorder com as opções selecionadas
        self.recorder = Recorder(
            record_mouse=self._record_mouse.get(),
            record_keyboard=self._record_keyboard.get(),
            on_event_callback=self._on_event_captured
        )
        
        # Inicia a gravação
        self.recorder.start()
        
        # Atualiza a interface para estado "gravando"
        self._update_ui_recording_state(True)
        
        # Inicia atualização periódica dos contadores
        self._start_ui_updates()

    def _stop_recording(self) -> None:
        """
        Para a gravação e disponibiliza a sessão.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando você clica em parar:
        1. A gravação é interrompida
        2. Todos os eventos são salvos em uma "sessão"
        3. Se auto-save estiver ativo, salva automaticamente
        4. A interface volta ao normal
        5. Os botões de salvar/limpar são habilitados
        
        EXPLICAÇÃO TÉCNICA:
        Para o recorder, obtém a sessão resultante e atualiza a UI.
        Se auto_save estiver ativado, salva automaticamente com timestamp.
        Chama o callback on_session_ready se configurado.
        """
        if not self.recorder:
            return
        
        # Para a gravação e obtém a sessão
        self.current_session = self.recorder.stop()
        
        # Para as atualizações da UI
        self._stop_ui_updates()
        
        # Atualiza a interface para estado "parado"
        self._update_ui_recording_state(False)
        
        # Habilita botões de ação se há eventos
        if self.current_session and len(self.current_session.events) > 0:
            self._save_button.configure(state="normal")
            self._clear_button.configure(state="normal")
            
            # Auto-save se habilitado
            if self._auto_save.get():
                self._perform_auto_save()
            
            # Notifica que a sessão está pronta
            if self.on_session_ready:
                self.on_session_ready(self.current_session)

    def _perform_auto_save(self) -> None:
        """
        Executa o salvamento automático da gravação.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando o auto-save está ativado, esta função salva a gravação
        automaticamente em um arquivo com nome baseado na data/hora.
        Assim você não precisa se preocupar em salvar manualmente.
        
        EXPLICAÇÃO TÉCNICA:
        Gera um nome de arquivo único com timestamp e salva no diretório
        configurado. Atualiza a UI para mostrar o arquivo salvo.
        """
        if not self.current_session:
            return
        
        # Obtém o diretório de gravações da config
        from src.utils.config import Config
        config = Config()
        recordings_dir = config.get("files.default_directory", "recordings")
        
        # Garante que o diretório existe
        if not os.path.isabs(recordings_dir):
            recordings_dir = os.path.join(os.getcwd(), recordings_dir)
        os.makedirs(recordings_dir, exist_ok=True)
        
        # Gera nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        num_events = len(self.current_session.events)
        filename = f"gravacao_{timestamp}_{num_events}eventos.json"
        filepath = os.path.join(recordings_dir, filename)
        
        # Tenta salvar
        if self.current_session.save(filepath):
            self._last_saved_file = filepath
            self._file_label.configure(text=f"📁 {filename}")
            self._edit_button.configure(state="normal")
            self._status_label.configure(text=f"Auto-salvo: {filename}")
        else:
            self._file_label.configure(text="📁 Erro ao auto-salvar!")
            self._status_label.configure(text="Falha no auto-save")

    def _on_event_captured(self, event: InputEvent) -> None:
        """
        Callback chamado quando um evento é capturado.
        
        EXPLICAÇÃO PARA INICIANTES:
        Toda vez que você faz algo (clica, move mouse, aperta tecla),
        esta função é chamada. Não fazemos muito aqui porque a atualização
        da interface acontece em outro lugar (para ser mais eficiente).
        
        EXPLICAÇÃO TÉCNICA:
        Callback do Recorder. Pode ser usado para processamento em tempo
        real, mas atualizações de UI devem ser feitas via after() para
        thread-safety.
        
        Args:
            event: O evento capturado
        """
        # A atualização do contador é feita em _update_ui() para thread-safety
        pass

    def _update_ui_recording_state(self, is_recording: bool) -> None:
        """
        Atualiza a interface com base no estado de gravação.
        
        EXPLICAÇÃO PARA INICIANTES:
        Muda a aparência dos elementos para refletir se está gravando ou não:
        - Gravando: indicador vermelho, botão diz "PARAR", opções desabilitadas
        - Parado: indicador cinza, botão diz "INICIAR", opções habilitadas
        
        EXPLICAÇÃO TÉCNICA:
        Atualiza cores, textos e estados de widgets baseado no flag is_recording.
        
        Args:
            is_recording: True se está gravando, False se parado
        """
        if is_recording:
            # Estado: Gravando
            self._status_indicator.configure(text_color=TarefAutoTheme.RECORDING)
            self._status_label.configure(text="Gravando...")
            self._record_button.configure(
                text="⏹️ PARAR GRAVAÇÃO",
                **TarefAutoTheme.get_button_style("danger")
            )
            
            # Desabilita checkboxes durante gravação
            self._mouse_checkbox.configure(state="disabled")
            self._keyboard_checkbox.configure(state="disabled")
            self._mouse_movement_checkbox.configure(state="disabled")
            
            # Desabilita botões de ação
            self._save_button.configure(state="disabled")
            self._clear_button.configure(state="disabled")
        else:
            # Estado: Parado
            self._status_indicator.configure(text_color=TarefAutoTheme.IDLE)
            self._status_label.configure(text="Gravação finalizada" if self.current_session else "Pronto para gravar")
            self._record_button.configure(
                text="⏺️ INICIAR GRAVAÇÃO",
                **TarefAutoTheme.get_button_style("primary")
            )
            
            # Habilita checkboxes
            self._mouse_checkbox.configure(state="normal")
            self._keyboard_checkbox.configure(state="normal")
            self._on_options_changed()  # Atualiza estado do checkbox de movimento

    def _start_ui_updates(self) -> None:
        """
        Inicia as atualizações periódicas da UI.
        
        EXPLICAÇÃO PARA INICIANTES:
        Durante a gravação, queremos mostrar quantos eventos foram
        capturados e quanto tempo passou. Esta função configura uma
        atualização a cada 100ms (10 vezes por segundo).
        
        EXPLICAÇÃO TÉCNICA:
        Usa after() para agendar chamadas periódicas a _update_ui().
        after() é thread-safe e executa na thread principal.
        """
        self._update_ui()

    def _stop_ui_updates(self) -> None:
        """
        Para as atualizações periódicas da UI.
        
        EXPLICAÇÃO PARA INICIANTES:
        Quando a gravação para, não precisamos mais atualizar o contador.
        Esta função cancela as atualizações.
        
        EXPLICAÇÃO TÉCNICA:
        Cancela o job agendado com after_cancel().
        """
        if self._update_job:
            self.after_cancel(self._update_job)
            self._update_job = None

    def _update_ui(self) -> None:
        """
        Atualiza contadores e informações na interface.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função é chamada várias vezes por segundo durante a gravação.
        Ela atualiza:
        - O número de eventos capturados
        - A duração da gravação
        
        EXPLICAÇÃO TÉCNICA:
        Lê dados do recorder e atualiza labels. Re-agenda a si mesma
        usando after() para criar um loop de atualização.
        """
        if self.recorder and self.recorder.is_recording:
            # Atualiza contador de eventos
            count = self.recorder.get_event_count()
            self._event_count_label.configure(text=f"Eventos: {count}")
            
            # Atualiza duração
            duration = self.recorder.session.get_duration()
            self._duration_label.configure(text=f"Duração: {duration:.1f}s")
            
            # Agenda próxima atualização (100ms = 10 updates por segundo)
            self._update_job = self.after(100, self._update_ui)

    def _save_recording(self) -> None:
        """
        Salva a gravação atual em um arquivo.
        
        EXPLICAÇÃO PARA INICIANTES:
        Abre uma janela para você escolher onde salvar o arquivo.
        O arquivo é salvo em formato JSON, que é um texto organizado
        que pode ser aberto em qualquer editor se você quiser ver.
        
        EXPLICAÇÃO TÉCNICA:
        Usa filedialog para seleção de arquivo e chama session.save().
        """
        if not self.current_session:
            return
        
        # Obtém diretório padrão da configuração
        from src.utils.config import Config
        config = Config()
        initial_dir = config.get("files.default_directory", "")
        if not initial_dir:
            initial_dir = str(config.recordings_dir)
        
        # Abre diálogo para escolher onde salvar
        filepath = filedialog.asksaveasfilename(
            title="Salvar Gravação",
            defaultextension=".json",
            filetypes=[
                ("Arquivos JSON", "*.json"),
                ("Todos os arquivos", "*.*")
            ],
            initialdir=initial_dir,
            initialfile=f"gravacao_{len(self.current_session.events)}_eventos.json"
        )
        
        if filepath:
            # Tenta salvar
            if self.current_session.save(filepath):
                # Atualiza referência do último arquivo salvo
                self._last_saved_file = filepath
                filename = os.path.basename(filepath)
                self._file_label.configure(text=f"📁 {filename}")
                self._edit_button.configure(state="normal")
                
                messagebox.showinfo(
                    "Sucesso",
                    f"Gravação salva com sucesso!\n\n"
                    f"Arquivo: {filepath}\n"
                    f"Eventos: {len(self.current_session.events)}\n"
                    f"Duração: {self.current_session.get_duration():.1f}s"
                )
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível salvar a gravação.\n"
                    "Verifique se você tem permissão para salvar neste local."
                )

    def _clear_recording(self) -> None:
        """
        Limpa a gravação atual.
        
        EXPLICAÇÃO PARA INICIANTES:
        Descarta a gravação atual sem salvar. Pede confirmação primeiro
        para evitar que você perca dados por acidente.
        
        EXPLICAÇÃO TÉCNICA:
        Exibe diálogo de confirmação e reseta o estado se confirmado.
        """
        if not self.current_session:
            return
        
        # Confirma com o usuário
        result = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja descartar a gravação atual?\n"
            f"({len(self.current_session.events)} eventos serão perdidos)"
        )
        
        if result:
            self.current_session = None
            self._last_saved_file = None
            self._event_count_label.configure(text="Eventos: 0")
            self._duration_label.configure(text="Duração: 0.0s")
            self._file_label.configure(text="📁 Nenhuma gravação")
            self._save_button.configure(state="disabled")
            self._clear_button.configure(state="disabled")
            self._edit_button.configure(state="disabled")
            self._status_label.configure(text="Pronto para gravar")

    # ========================================================================
    # MÉTODOS PÚBLICOS
    # ========================================================================

    def start_recording_external(self) -> None:
        """
        Inicia a gravação (chamado externamente, ex: por hotkey).
        
        EXPLICAÇÃO PARA INICIANTES:
        Este método permite que outras partes do programa (como os
        atalhos de teclado) iniciem a gravação.
        
        EXPLICAÇÃO TÉCNICA:
        Interface pública para iniciar gravação via hotkey ou outra fonte.
        """
        if not self.recorder or not self.recorder.is_recording:
            self._start_recording()

    def stop_recording_external(self) -> None:
        """
        Para a gravação (chamado externamente, ex: por hotkey).
        
        EXPLICAÇÃO PARA INICIANTES:
        Permite que atalhos de teclado parem a gravação.
        
        EXPLICAÇÃO TÉCNICA:
        Interface pública para parar gravação via hotkey ou outra fonte.
        """
        if self.recorder and self.recorder.is_recording:
            self._stop_recording()

    def get_current_session(self) -> Optional[RecordingSession]:
        """
        Retorna a sessão de gravação atual.
        
        EXPLICAÇÃO PARA INICIANTES:
        Permite que outras partes do programa acessem a gravação atual.
        
        EXPLICAÇÃO TÉCNICA:
        Getter para current_session.
        
        Returns:
            Optional[RecordingSession]: A sessão atual ou None
        """
        return self.current_session

    def is_recording(self) -> bool:
        """
        Verifica se está gravando no momento.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna True se a gravação está em andamento.
        
        EXPLICAÇÃO TÉCNICA:
        Verifica o estado do recorder.
        
        Returns:
            bool: True se gravando, False caso contrário
        """
        return self.recorder is not None and self.recorder.is_recording
