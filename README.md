# 🤖 TarefAuto

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Automação de Tarefas Repetitivas**

*Um macro avançado que grava e reproduz ações de mouse e teclado*

[Instalação](#-instalação) •
[Como Usar](#-como-usar) •
[Recursos](#-recursos) •
[FAQ](#-faq) •
[Contribuir](#-contribuir)

</div>


---

## 📖 O que é o TarefAuto?

O **Tarefauto** é uma ferramenta de automação que permite gravar suas ações no computador (desde cliques do mouse e seus movimentos até teclas digitadas) e reproduzi-las automaticamente. É como um "gravador de macros", "autoclicker" ou "autotyper" avançado.

<img width="50%" alt="Captura de tela 2026-01-02 053243" src="https://github.com/user-attachments/assets/b2a90dd2-5f29-4858-aaa4-6c57b5ff5da2" />
<img width="40%" alt="image" src="https://github.com/user-attachments/assets/77352a32-9c6b-4ef1-a784-de521e592b4f" />

### Para que serve?

- 🎮 **Jogos**: Automatizar ações repetitivas em jogos (PERIGOSO)
- 📊 **Trabalho**: Automatizar preenchimento de determinados tipos de planilhas/formulários ou outras atividades do gênero que sejam repetitivas
- 🧪 **Testes**: Criar testes automatizados de interface
- 🔄 **Tarefas repetitivas**: Qualquer ação que você faz várias vezes

>Para gamers: Use por conta e risco, muitos anti-cheaters podem detectar, o software não foi feito para ser um cheat e sim uma ferramenta de trabalho.

### Diferenciais

- ✅ **Interface amigável**: GUI moderna e intuitiva
- ✅ **Cross-platform**: Funciona em Windows, Linux e macOS
- ✅ **Atalhos globais**: Controle o programa sem precisar clicar nele por teclas de atalho
- ✅ **Múltiplos modos de repetição**: Uma vez, X vezes, por tempo, infinito
- ✅ **Controle de velocidade**: Reproduza mais rápido ou mais devagar
- ✅ **Código aberto**: 100% gratuito e transparente

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8 ou superior** ([Download](https://www.python.org/downloads/))
- **pip** (geralmente já vem com o Python)

### Passo a Passo

#### Windows (PowerShell)

```powershell
# 1. Clone o repositório (ou baixe o ZIP)
git clone https://github.com/matheuslaidler/tarefauto.git

# 2. Entre na pasta
cd tarefauto

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o programa
python main.py
```

#### Windows (CMD)

```cmd
REM 1. Clone o repositório
git clone https://github.com/matheuslaidler/tarefauto.git

REM 2. Entre na pasta
cd tarefauto

REM 3. Instale as dependências
pip install -r requirements.txt

REM 4. Execute o programa
python main.py
```

#### Linux

```bash
# 1. Clone o repositório
git clone https://github.com/matheuslaidler/tarefauto.git

# 2. Entre na pasta
cd tarefauto

# 3. Instale dependências do sistema (Debian/Ubuntu)
sudo apt update
sudo apt install python3-tk python3-dev

# 4. Instale as dependências Python
pip3 install -r requirements.txt

# 5. Execute o programa
python3 main.py
```

#### macOS

```bash
# 1. Clone o repositório
git clone https://github.com/matheuslaidler/tarefauto.git

# 2. Entre na pasta
cd tarefauto

# 3. Instale as dependências
pip3 install -r requirements.txt

# 4. Execute o programa
python3 main.py

# IMPORTANTE: No macOS, você precisa dar permissão de acessibilidade
# Vá em: Preferências do Sistema > Segurança e Privacidade > Acessibilidade
# E adicione o Terminal à lista
```

### Problemas Comuns na Instalação

<details>
<summary><b>❌ "pip não é reconhecido"</b></summary>

**Windows:** Use `py -m pip` em vez de `pip`:
```powershell
py -m pip install -r requirements.txt
```

**Linux/macOS:** Use `pip3`:
```bash
pip3 install -r requirements.txt
```
</details>

<details>
<summary><b>❌ "ModuleNotFoundError: No module named 'tkinter'"</b></summary>

**Linux:**
```bash
sudo apt install python3-tk
```

**macOS:** Reinstale o Python pelo site oficial (o Homebrew às vezes não inclui o Tk)
</details>

<details>
<summary><b>❌ "Permission denied" ao instalar</b></summary>

**Linux/macOS:** Use `--user`:
```bash
pip3 install --user -r requirements.txt
```

Ou crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
</details>

---

## 📱 Como Usar

### Interface Principal

Ao abrir o programa, você verá três abas:

| Aba | Descrição |
|-----|-----------|
| 📹 **Gravação** | Configure e inicie/pare gravações |
| ▶️ **Reprodução** | Carregue e reproduza gravações |
| ⚙️ **Configurações** | Configure atalhos e preferências |

### Gravando Ações

1. Vá na aba **📹 Gravação**
2. Escolha o que deseja gravar:
   - ☑️ Mouse (cliques e movimentos)
   - ☑️ Teclado (teclas pressionadas)
3. Clique em **⏺️ INICIAR GRAVAÇÃO** (ou use `F9`)
4. Execute as ações que deseja automatizar
5. Clique em **⏹️ PARAR GRAVAÇÃO** (ou use `F9` / `ESC`)
6. Com auto-save ligado, sua gravação já estará salva. Clique em **💾 Salvar Gravação** para guardar o JSON em algum lugar, caso queira ou o auto-save estiver desligado.

### Reproduzindo Ações

1. Vá na aba **▶️ Reprodução**
2. Clique em **📂 Carregar** e selecione uma gravação
3. Configure as opções:
   - **Modo de repetição**: Uma vez, X vezes, por tempo, ou infinito
   - **Velocidade**: 0.5x (devagar) até 5x (rápido)
4. Clique em **▶️ INICIAR REPRODUÇÃO** ou (ou use `F10`)
5. Para encerrar reprodução, clique em **⏹️ PARAR** ou use `F10`, ou então pressione  `Esc` como emergência para parar tudo.

### Atalhos de Teclado

| Atalho | Ação |
| ------ | ---- |
| `F9` | Iniciar/Parar gravação |
| `F10` | Iniciar/Parar reprodução |
| `Esc` | Parar tudo (emergência) |

> 💡 **Dica**: Os atalhos funcionam mesmo quando o TarefAuto está em segundo plano! Você pode configurá-los na aba **⚙️ Configurações**.

---

## ✨ Recursos

### Modos de Repetição

| Modo | Descrição |
|------|-----------|
| 🔂 **Uma vez** | Reproduz uma única vez |
| 🔢 **X vezes** | Reproduz um número específico de vezes |
| ⏱️ **Por tempo** | Reproduz por X segundos |
| ♾️ **Infinito** | Reproduz até você parar manualmente |

### Controle de Velocidade

- **0.5x** - Metade da velocidade (mais lento)
- **1.0x** - Velocidade normal (como foi gravado)
- **2.0x** - Dobro da velocidade
- **5.0x** - 5 vezes mais rápido

### Formato de Arquivo

As gravações são salvas em formato **JSON**, que é um formato de texto legível. Você pode:

- Abrir o arquivo em qualquer editor de texto
- Editar manualmente se necessário
- Compartilhar com outras pessoas
- Versionar com Git

Exemplo de estrutura:
```json
{
  "metadata": {
    "created_at": "2024-01-15T10:30:00",
    "platform": "Windows",
    "version": "1.0.0"
  },
  "events": [
    {
      "type": "MOUSE_CLICK",
      "timestamp": 0.0,
      "x": 500,
      "y": 300,
      "button": "left"
    }
  ]
}
```

---

## ⚠️ Notas Importantes

### Antivírus

Alguns antivírus podem detectar o TarefAuto como suspeito porque ele:
- Captura eventos de teclado (como um keylogger faria)
- Simula cliques de mouse (como malware faria)

**Isso é um falso positivo!** O TarefAuto:
- ✅ É código aberto - você pode verificar o código
- ✅ Não envia nenhum dado para a internet
- ✅ Não salva senhas ou informações sensíveis
- ✅ Só grava o que você explicitamente pedir

**Para adicionar exceção:**
1. Abra seu antivírus
2. Vá em "Exceções" ou "Lista branca"
3. Adicione a pasta do TarefAuto

### Linux com Wayland

O TarefAuto funciona melhor no **X11**. No Wayland, a captura de eventos globais pode não funcionar corretamente.

**Soluções:**
1. Use uma sessão X11/Xorg em vez de Wayland
2. Execute aplicativos específicos com XWayland

Para verificar qual display server você está usando:
```bash
echo $XDG_SESSION_TYPE
```

### macOS

No macOS, você precisa conceder **permissões de acessibilidade**:

1. Vá em **Preferências do Sistema**
2. **Segurança e Privacidade**
3. **Privacidade**
4. **Acessibilidade**
5. Adicione o Terminal (ou Python) à lista

---

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
tarefauto/
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── README.md               # Este arquivo
│
└── src/
    ├── __init__.py
    │
    ├── core/               # Lógica principal
    │   ├── __init__.py
    │   ├── events.py       # Classes de eventos
    │   ├── recorder.py     # Gravação de ações
    │   ├── player.py       # Reprodução de ações
    │   └── hotkeys.py      # Atalhos de teclado
    │
    ├── gui/                # Interface gráfica
    │   ├── __init__.py
    │   ├── theme.py        # Tema visual
    │   ├── main_window.py  # Janela principal
    │   ├── recording_tab.py
    │   ├── playback_tab.py
    │   └── settings_tab.py
    │
    └── utils/              # Utilitários
        ├── __init__.py
        ├── config.py       # Configurações
        └── platform_utils.py
```

### Tecnologias Usadas

| Tecnologia | Uso |
|------------|-----|
| [Python 3.8+](https://python.org) | Linguagem principal |
| [pynput](https://pynput.readthedocs.io/) | Captura e simulação de mouse/teclado |
| [CustomTkinter](https://customtkinter.tomschimansky.com/) | Interface gráfica moderna |
| [Pillow](https://pillow.readthedocs.io/) | Manipulação de imagens |

### Criando um Executável

Em breve criaremos o executável para windows e o binário para linux, assim facilitaria para muitos usuários.

Como a maioria dos usuários leigos usam windows, vou deixar abaixo uma forma de criar o executável você mesmo.

Para criar um arquivo `.exe` executável em windows:

```powershell
# Instale o PyInstaller
pip install pyinstaller

# Crie o executável
pyinstaller --onefile --windowed --name TarefAuto main.py
```

O executável estará em `dist/TarefAuto.exe`.

---

## ❓ FAQ

<details>
<summary><b>É seguro usar?</b></summary>

Sim! O TarefAuto é código aberto e você pode verificar exatamente o que ele faz. Ele não coleta dados, não se conecta à internet, e não armazena informações sensíveis.
</details>

<details>
<summary><b>Posso usar em jogos online?</b></summary>

⚠️ **Cuidado!** Muitos jogos online proíbem ferramentas de automação em seus Termos de Serviço. Usar o TarefAuto pode resultar em banimento. Use por sua conta e risco em jogos online.
</details>

<details>
<summary><b>Por que a gravação não captura algumas teclas?</b></summary>

Algumas teclas especiais ou combinações podem não ser capturadas em certos sistemas. Além disso, se você estiver usando Wayland no Linux, a captura global pode não funcionar.
</details>

<details>
<summary><b>Posso editar gravações manualmente?</b></summary>

Sim! As gravações são arquivos JSON que podem ser abertos em qualquer editor de texto. Você pode adicionar, remover ou modificar eventos.
</details>

<details>
<summary><b>Funciona em múltiplos monitores?</b></summary>

Sim, as coordenadas do mouse são absolutas e funcionam com múltiplos monitores.
</details>

---

## 🤝 Contribuir

Contribuições são bem-vindas! Veja como você pode ajudar:

1. **🐛 Reporte bugs**: Abra uma [Issue](https://github.com/matheuslaidler/tarefauto/issues)
2. **💡 Sugira recursos**: Abra uma [Issue](https://github.com/matheuslaidler/tarefauto/issues) com sua ideia
3. **🔧 Envie código**: Faça um [Pull Request](https://github.com/matheuslaidler/tarefauto/pulls)

### Como contribuir com código

```bash
# 1. Faça um fork do repositório

# 2. Clone seu fork
git clone https://github.com/SEU_USUARIO/tarefauto.git

# 3. Crie uma branch para sua feature
git checkout -b minha-feature

# 4. Faça suas alterações e commit
git commit -m "Adiciona minha feature"

# 5. Envie para seu fork
git push origin minha-feature

# 6. Abra um Pull Request
```

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Matheus Laidler**

- 🌐 [Website](https://matheuslaidler.github.io)
- 🐙 [GitHub](https://github.com/matheuslaidler)

---

<div align="center">

⭐ **Se este projeto te ajudou, considere dar uma estrela!** ⭐

</div>
