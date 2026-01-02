# ============================================================================
# TarefAuto - Tema e Estilização (theme.py)
# ============================================================================
#
# EXPLICAÇÃO PARA INICIANTES:
# Este arquivo define a "aparência" do programa - as cores, fontes e estilos
# de todos os elementos visuais. Ele cria a estética "hacker" com cores
# ciano (#00FFFF), verde (#00FF00) e preto (#0D0D0D).
#
# Pense neste arquivo como a "roupa" do programa. A lógica fica em outros
# arquivos; este só cuida de como as coisas se parecem.
#
# EXPLICAÇÃO TÉCNICA:
# Define constantes de tema e funções auxiliares para estilização consistente
# em toda a aplicação CustomTkinter. Centraliza configurações visuais para
# facilitar manutenção e permitir futuras customizações de tema.
#
# ============================================================================

"""
Tema e estilização do TarefAuto.

Este módulo define todas as cores, fontes e estilos utilizados na
interface gráfica do programa, criando uma estética "hacker" consistente.

Classes:
    TarefAutoTheme: Classe com constantes e métodos de tema

Autor: Matheus Laidler
GitHub: https://github.com/matheuslaidler/tarefauto
"""

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

# customtkinter: Framework de GUI que vamos estilizar
import customtkinter as ctk

# typing: Anotações de tipo
from typing import Dict, Tuple, Optional


# ============================================================================
# CLASSE DE TEMA
# ============================================================================

class TarefAutoTheme:
    """
    Definição do tema visual do TarefAuto.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta classe é como um "manual de estilo" do programa. Ela define:
    - Quais cores usar em cada lugar
    - Quais fontes e tamanhos de texto
    - Como os botões, campos de texto e outros elementos devem se parecer
    
    Tudo é organizado em "constantes" (valores que não mudam) para que
    seja fácil manter a aparência consistente em todo o programa.
    
    A estética escolhida é "hacker" ou "cyberpunk":
    - Fundo escuro (preto/cinza escuro)
    - Destaques em ciano (azul-verde brilhante)
    - Destaques em verde (estilo Matrix)
    - Texto claro para contraste
    
    EXPLICAÇÃO TÉCNICA:
    Classe de configuração com atributos de classe (class attributes)
    que funcionam como constantes. Todos os valores são acessíveis
    sem instanciar a classe (TarefAutoTheme.PRIMARY ao invés de
    TarefAutoTheme().PRIMARY).
    
    Attributes:
        PRIMARY: Cor ciano principal (#00FFFF)
        SECONDARY: Cor verde secundária (#00FF00)
        BACKGROUND: Cor de fundo escura (#0D0D0D)
        etc.
    
    Example:
        >>> button = ctk.CTkButton(
        ...     fg_color=TarefAutoTheme.PRIMARY,
        ...     hover_color=TarefAutoTheme.PRIMARY_HOVER
        ... )
    """
    
    # ========================================================================
    # CORES PRINCIPAIS
    # ========================================================================
    
    # Ciano - Cor principal de destaque
    # Usada em: botões primários, títulos, elementos ativos
    PRIMARY = "#00FFFF"              # Ciano brilhante
    PRIMARY_HOVER = "#00CCCC"        # Ciano mais escuro (quando passa o mouse)
    PRIMARY_DARK = "#008B8B"         # Ciano escuro
    PRIMARY_LIGHT = "#7FFFD4"        # Ciano claro/água-marinha
    
    # Verde - Cor secundária de destaque
    # Usada em: indicadores de sucesso, botão de play, status ativo
    SECONDARY = "#00FF00"            # Verde Matrix
    SECONDARY_HOVER = "#00CC00"      # Verde mais escuro
    SECONDARY_DARK = "#006400"       # Verde floresta
    SECONDARY_LIGHT = "#90EE90"      # Verde claro
    
    # ========================================================================
    # CORES DE FUNDO
    # ========================================================================
    
    # Fundos - Tons de preto/cinza escuro
    BACKGROUND = "#0D0D0D"           # Preto quase total (fundo principal)
    BACKGROUND_LIGHT = "#1A1A1A"     # Cinza muito escuro (painéis)
    BACKGROUND_LIGHTER = "#2D2D2D"   # Cinza escuro (campos de entrada)
    BACKGROUND_CARD = "#1F1F1F"      # Fundo de cards/frames
    BACKGROUND_SECONDARY = "#1A1A1A" # Fundo secundário (alias para LIGHT)
    BACKGROUND_TERTIARY = "#252525"  # Fundo terciário (entre LIGHT e LIGHTER)
    
    # ========================================================================
    # CORES DE TEXTO
    # ========================================================================
    
    # Texto - Tons de branco/cinza claro
    TEXT_PRIMARY = "#FFFFFF"         # Branco puro (texto principal)
    TEXT_SECONDARY = "#B0B0B0"       # Cinza claro (texto secundário)
    TEXT_MUTED = "#707070"           # Cinza médio (texto desabilitado)
    TEXT_DARK = "#0D0D0D"            # Preto (texto em fundo claro)
    
    # ========================================================================
    # CORES DE ESTADO
    # ========================================================================
    
    # Cores semânticas para estados/feedback
    SUCCESS = "#00FF00"              # Verde - Sucesso/Gravando
    WARNING = "#FFD700"              # Amarelo/Dourado - Alerta
    ERROR = "#FF4444"                # Vermelho - Erro/Parado
    INFO = "#00FFFF"                 # Ciano - Informação
    
    # Cores de estado para gravação/reprodução
    RECORDING = "#FF4444"            # Vermelho - Está gravando
    PLAYING = "#00FF00"              # Verde - Está reproduzindo
    IDLE = "#707070"                 # Cinza - Parado/Ocioso
    
    # ========================================================================
    # CORES DE BORDA
    # ========================================================================
    
    BORDER = "#333333"               # Borda padrão (cinza escuro)
    BORDER_FOCUS = "#00FFFF"         # Borda quando focado (ciano)
    BORDER_ERROR = "#FF4444"         # Borda de erro (vermelho)
    
    # ========================================================================
    # FONTES
    # ========================================================================
    
    # Família de fontes (em ordem de preferência)
    # O sistema tentará cada uma até encontrar uma disponível
    FONT_FAMILY = "Consolas"         # Fonte monoespaçada (estilo terminal)
    FONT_FAMILY_FALLBACK = "Courier New"  # Fallback se Consolas não existir
    
    # Tamanhos de fonte (em pixels)
    FONT_SIZE_TITLE = 24             # Títulos grandes
    FONT_SIZE_HEADING = 18           # Cabeçalhos de seção
    FONT_SIZE_SUBHEADING = 14        # Subcabeçalhos
    FONT_SIZE_BODY = 12              # Texto normal
    FONT_SIZE_SMALL = 10             # Texto pequeno (rodapés, dicas)
    
    # ========================================================================
    # DIMENSÕES E ESPAÇAMENTO
    # ========================================================================
    
    # Padding (espaçamento interno)
    PADDING_SMALL = 5                # Espaçamento pequeno
    PADDING_MEDIUM = 10              # Espaçamento médio
    PADDING_LARGE = 20               # Espaçamento grande
    
    # Border radius (arredondamento de cantos)
    CORNER_RADIUS_SMALL = 4          # Cantos levemente arredondados
    CORNER_RADIUS_MEDIUM = 8         # Cantos médios
    CORNER_RADIUS_LARGE = 12         # Cantos bem arredondados
    
    # Dimensões de componentes
    BUTTON_HEIGHT = 35               # Altura padrão de botões
    ENTRY_HEIGHT = 35                # Altura padrão de campos de texto
    SIDEBAR_WIDTH = 200              # Largura da barra lateral (se houver)
    
    # ========================================================================
    # INFORMAÇÕES DO PROJETO
    # ========================================================================
    
    # Informações do projeto para exibição na interface
    PROJECT_INFO = {
        "name": "TarefAuto",
        "version": "1.0.0",
        "author": "Matheus Laidler",
        "github_profile": "https://github.com/matheuslaidler",
        "github": "https://github.com/matheuslaidler/tarefauto",
        "description": "Ferramenta de automação de tarefas repetitivas",
    }
    
    # ========================================================================
    # MÉTODOS DE CLASSE
    # ========================================================================
    
    @classmethod
    def apply_theme(cls) -> None:
        """
        Aplica o tema escuro ao CustomTkinter.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função configura o CustomTkinter para usar modo escuro
        por padrão. Deve ser chamada antes de criar qualquer janela.
        
        EXPLICAÇÃO TÉCNICA:
        Configura aparência e tema de cores padrão do CustomTkinter.
        
        Example:
            >>> TarefAutoTheme.apply_theme()
            >>> window = ctk.CTk()  # Janela já estará em modo escuro
        """
        # Define o modo de aparência como escuro
        ctk.set_appearance_mode("dark")
        
        # Define o tema de cores padrão (pode ser "blue", "green", "dark-blue")
        # Usamos "dark-blue" como base e sobrescrevemos com nossas cores
        ctk.set_default_color_theme("dark-blue")

    @classmethod
    def get_font(cls, size: str = "body", bold: bool = False) -> Tuple[str, int, str]:
        """
        Retorna tupla de fonte no formato do CustomTkinter.
        
        EXPLICAÇÃO PARA INICIANTES:
        Esta função facilita criar fontes consistentes. Você só precisa
        dizer o "tipo" de texto (título, cabeçalho, corpo, etc.) e ela
        retorna as configurações certas.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna tupla (família, tamanho, peso) compatível com CTkFont.
        
        Args:
            size (str): Tamanho da fonte: "title", "heading", "subheading", "body", "small"
            bold (bool): Se deve usar negrito
        
        Returns:
            Tuple[str, int, str]: (família, tamanho, peso)
        
        Example:
            >>> TarefAutoTheme.get_font("heading", bold=True)
            ("Consolas", 18, "bold")
        """
        # Mapa de tamanhos
        size_map = {
            "title": cls.FONT_SIZE_TITLE,
            "heading": cls.FONT_SIZE_HEADING,
            "subheading": cls.FONT_SIZE_SUBHEADING,
            "body": cls.FONT_SIZE_BODY,
            "small": cls.FONT_SIZE_SMALL,
        }
        
        font_size = size_map.get(size, cls.FONT_SIZE_BODY)
        weight = "bold" if bold else "normal"
        
        return (cls.FONT_FAMILY, font_size, weight)

    @classmethod
    def get_button_style(cls, variant: str = "primary") -> Dict:
        """
        Retorna dicionário de estilos para botões.
        
        EXPLICAÇÃO PARA INICIANTES:
        Facilita criar botões com aparência consistente. Você escolhe o
        "tipo" do botão (primário, secundário, etc.) e recebe todas as
        configurações de cor prontas para usar.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna kwargs para passar diretamente ao construtor de CTkButton.
        
        Args:
            variant (str): Variante do botão: "primary", "secondary", "danger", "ghost"
        
        Returns:
            Dict: Dicionário de configurações do botão
        
        Example:
            >>> style = TarefAutoTheme.get_button_style("primary")
            >>> button = ctk.CTkButton(master, text="Clique", **style)
        """
        styles = {
            "primary": {
                "fg_color": cls.PRIMARY,
                "hover_color": cls.PRIMARY_HOVER,
                "text_color": cls.TEXT_DARK,
                "corner_radius": cls.CORNER_RADIUS_MEDIUM,
            },
            "secondary": {
                "fg_color": cls.SECONDARY,
                "hover_color": cls.SECONDARY_HOVER,
                "text_color": cls.TEXT_DARK,
                "corner_radius": cls.CORNER_RADIUS_MEDIUM,
            },
            "danger": {
                "fg_color": cls.ERROR,
                "hover_color": "#CC3333",
                "text_color": cls.TEXT_PRIMARY,
                "corner_radius": cls.CORNER_RADIUS_MEDIUM,
            },
            "ghost": {
                "fg_color": "transparent",
                "hover_color": cls.BACKGROUND_LIGHTER,
                "text_color": cls.TEXT_PRIMARY,
                "border_width": 1,
                "border_color": cls.BORDER,
                "corner_radius": cls.CORNER_RADIUS_MEDIUM,
            },
            "outline": {
                "fg_color": "transparent",
                "hover_color": cls.PRIMARY_DARK,
                "text_color": cls.PRIMARY,
                "border_width": 2,
                "border_color": cls.PRIMARY,
                "corner_radius": cls.CORNER_RADIUS_MEDIUM,
            },
        }
        
        return styles.get(variant, styles["primary"])

    @classmethod
    def get_entry_style(cls, variant: str = "default") -> Dict:
        """
        Retorna dicionário de estilos para campos de entrada.
        
        EXPLICAÇÃO PARA INICIANTES:
        Retorna configurações visuais para campos onde o usuário digita
        texto (campos de entrada, caixas de texto).
        
        EXPLICAÇÃO TÉCNICA:
        Retorna kwargs para CTkEntry ou CTkTextbox.
        
        Args:
            variant (str): Variante do estilo (reservado para uso futuro)
        
        Returns:
            Dict: Dicionário de configurações
        """
        return {
            "fg_color": cls.BACKGROUND_LIGHTER,
            "text_color": cls.TEXT_PRIMARY,
            "border_color": cls.BORDER,
            "border_width": 1,
            "corner_radius": cls.CORNER_RADIUS_SMALL,
        }

    @classmethod
    def get_frame_style(cls, variant: str = "default") -> Dict:
        """
        Retorna dicionário de estilos para frames/containers.
        
        EXPLICAÇÃO PARA INICIANTES:
        Frames são como "caixas" que contêm outros elementos. Esta função
        retorna as configurações visuais para essas caixas.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna kwargs para CTkFrame.
        
        Args:
            variant (str): Variante: "default", "card", "transparent"
        
        Returns:
            Dict: Dicionário de configurações
        """
        styles = {
            "default": {
                "fg_color": cls.BACKGROUND,
                "corner_radius": 0,
            },
            "card": {
                "fg_color": cls.BACKGROUND_CARD,
                "corner_radius": cls.CORNER_RADIUS_LARGE,
            },
            "transparent": {
                "fg_color": "transparent",
                "corner_radius": 0,
            },
            "bordered": {
                "fg_color": cls.BACKGROUND_LIGHT,
                "corner_radius": cls.CORNER_RADIUS_MEDIUM,
                "border_width": 1,
                "border_color": cls.BORDER,
            },
        }
        
        return styles.get(variant, styles["default"])

    @classmethod
    def get_label_style(cls, variant: str = "default") -> Dict:
        """
        Retorna dicionário de estilos para labels (textos).
        
        EXPLICAÇÃO PARA INICIANTES:
        Labels são textos estáticos na interface. Esta função define
        como eles devem aparecer.
        
        EXPLICAÇÃO TÉCNICA:
        Retorna kwargs para CTkLabel.
        
        Args:
            variant (str): Variante: "default", "title", "heading", "muted"
        
        Returns:
            Dict: Dicionário de configurações
        """
        styles = {
            "default": {
                "text_color": cls.TEXT_PRIMARY,
            },
            "title": {
                "text_color": cls.PRIMARY,
                "font": ctk.CTkFont(family=cls.FONT_FAMILY, size=cls.FONT_SIZE_TITLE, weight="bold"),
            },
            "heading": {
                "text_color": cls.TEXT_PRIMARY,
                "font": ctk.CTkFont(family=cls.FONT_FAMILY, size=cls.FONT_SIZE_HEADING, weight="bold"),
            },
            "muted": {
                "text_color": cls.TEXT_MUTED,
                "font": ctk.CTkFont(family=cls.FONT_FAMILY, size=cls.FONT_SIZE_SMALL),
            },
            "success": {
                "text_color": cls.SUCCESS,
            },
            "error": {
                "text_color": cls.ERROR,
            },
            "warning": {
                "text_color": cls.WARNING,
            },
        }
        
        return styles.get(variant, styles["default"])

    @classmethod
    def get_status_color(cls, status: str) -> str:
        """
        Retorna a cor apropriada para um status.
        
        EXPLICAÇÃO PARA INICIANTES:
        Diferentes estados do programa têm cores diferentes:
        - Gravando = Vermelho
        - Reproduzindo = Verde
        - Parado = Cinza
        
        Esta função retorna a cor certa para cada situação.
        
        EXPLICAÇÃO TÉCNICA:
        Mapeia strings de status para cores hexadecimais.
        
        Args:
            status (str): Status: "recording", "playing", "idle", "success", "error"
        
        Returns:
            str: Cor hexadecimal
        """
        status_colors = {
            "recording": cls.RECORDING,
            "playing": cls.PLAYING,
            "idle": cls.IDLE,
            "success": cls.SUCCESS,
            "error": cls.ERROR,
            "warning": cls.WARNING,
            "info": cls.INFO,
        }
        
        return status_colors.get(status, cls.TEXT_PRIMARY)


# ============================================================================
# BLOCO DE TESTE
# ============================================================================

if __name__ == "__main__":
    print("=== Demonstração do Tema TarefAuto ===")
    print()
    
    # Exibe cores principais
    print("Cores Principais:")
    print(f"  PRIMARY:     {TarefAutoTheme.PRIMARY}")
    print(f"  SECONDARY:   {TarefAutoTheme.SECONDARY}")
    print(f"  BACKGROUND:  {TarefAutoTheme.BACKGROUND}")
    print(f"  TEXT:        {TarefAutoTheme.TEXT_PRIMARY}")
    print()
    
    # Exibe fontes
    print("Fontes:")
    print(f"  Title:    {TarefAutoTheme.get_font('title')}")
    print(f"  Heading:  {TarefAutoTheme.get_font('heading')}")
    print(f"  Body:     {TarefAutoTheme.get_font('body')}")
    print()
    
    # Exibe informações do projeto
    print("Informações do Projeto:")
    for key, value in TarefAutoTheme.PROJECT_INFO.items():
        print(f"  {key}: {value}")
    print()
    
    # Demonstração visual (se quiser ver a janela, descomente o código abaixo)
    print("Para ver uma demonstração visual, execute:")
    print("  python -c \"from src.gui.theme import *; demo()\"")
    print()
    print("=== Teste concluído! ===")

def demo():
    """
    Cria uma janela de demonstração do tema.
    
    EXPLICAÇÃO PARA INICIANTES:
    Esta função cria uma janela de teste para você ver como as cores
    e estilos ficam na prática. É útil para desenvolvimento e ajustes.
    
    Execute com: python -c "from src.gui.theme import *; demo()"
    """
    # Aplica o tema
    TarefAutoTheme.apply_theme()
    
    # Cria janela
    root = ctk.CTk()
    root.title("TarefAuto - Demo de Tema")
    root.geometry("600x500")
    root.configure(fg_color=TarefAutoTheme.BACKGROUND)
    
    # Frame principal
    main_frame = ctk.CTkFrame(root, **TarefAutoTheme.get_frame_style("default"))
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    title = ctk.CTkLabel(main_frame, text="TarefAuto", **TarefAutoTheme.get_label_style("title"))
    title.pack(pady=(0, 20))
    
    # Botões de demonstração
    btn_frame = ctk.CTkFrame(main_frame, **TarefAutoTheme.get_frame_style("transparent"))
    btn_frame.pack(fill="x", pady=10)
    
    for variant in ["primary", "secondary", "danger", "ghost", "outline"]:
        btn = ctk.CTkButton(
            btn_frame,
            text=variant.title(),
            **TarefAutoTheme.get_button_style(variant)
        )
        btn.pack(side="left", padx=5)
    
    # Campo de entrada
    entry_frame = ctk.CTkFrame(main_frame, **TarefAutoTheme.get_frame_style("transparent"))
    entry_frame.pack(fill="x", pady=10)
    
    entry_label = ctk.CTkLabel(entry_frame, text="Campo de texto:", **TarefAutoTheme.get_label_style("default"))
    entry_label.pack(anchor="w")
    
    entry = ctk.CTkEntry(entry_frame, **TarefAutoTheme.get_entry_style(), width=300)
    entry.pack(anchor="w", pady=5)
    entry.insert(0, "Digite algo aqui...")
    
    # Status labels
    status_frame = ctk.CTkFrame(main_frame, **TarefAutoTheme.get_frame_style("card"))
    status_frame.pack(fill="x", pady=10)
    
    for status in ["recording", "playing", "idle", "success", "error"]:
        lbl = ctk.CTkLabel(
            status_frame,
            text=f"● {status.title()}",
            text_color=TarefAutoTheme.get_status_color(status)
        )
        lbl.pack(side="left", padx=10, pady=10)
    
    # Rodapé
    footer = ctk.CTkLabel(
        main_frame,
        text=f"© {TarefAutoTheme.PROJECT_INFO['author']} | {TarefAutoTheme.PROJECT_INFO['github_profile']}",
        **TarefAutoTheme.get_label_style("muted")
    )
    footer.pack(side="bottom", pady=10)
    
    # Executa
    root.mainloop()
