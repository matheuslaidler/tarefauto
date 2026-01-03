# 🤖 TarefAuto: Tarefas Automatizadas 

<div align="center">

<img width="137" height="146" alt="image" src="https://github.com/user-attachments/assets/93e68c26-0643-4087-a79c-a3153108107b" />

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Automação de Tarefas Simples Repetitivas**

*Um macro avançado que grava e reproduz ações de mouse e teclado de forma rápida e fácil*

[Instalação](#-instalação) •
[Como Usar](#-como-usar) •
[Recursos](#-recursos) •
[FAQ](#-faq) •
[Contribuir](#-contribuir)

</div>


---

## 📖 O que é o Tarefauto?

Uma ferramenta de automação que grava suas ações no computador (cliques e movimentos do mouse, além de teclas digitadas) e depois reproduz tudo automaticamente. 

Na prática, funciona como um gravador de macros, tal qual um autoclicker ou autotyper, só que mais completo: você executa uma sequência uma vez, e o programa pode repeti-la quantas vezes quiser ou até você parar. Uma mesma ação gravada pode ser executada/reproduzida de diferentes velocidades, durações ou repetições. 

Durante a reprodução, o TarefAuto assume o controle de mouse e teclado para repetir a tarefa e por isso, o computador pode ficar limitado para outras atividades até a execução terminar ou ser cancelada pelo usuário.

<img width="50%" alt="Captura de tela 2026-01-02 053243" src="https://github.com/user-attachments/assets/b2a90dd2-5f29-4858-aaa4-6c57b5ff5da2" />
<img width="40%" alt="image" src="https://github.com/user-attachments/assets/77352a32-9c6b-4ef1-a784-de521e592b4f" />

### Para que serve?

- 🎮 **Jogos**: Automatizar ações repetitivas em jogos (PERIGOSO)
- 📊 **Trabalho**: Automatizar preenchimento de determinados tipos de planilhas/formulários ou outras atividades do gênero, que sejam repetitivas
- 🧪 **Testes**: Criar testes repetitivos automatizados de interface
- 🔄 **Tarefas repetitivas**: Qualquer ação que você faz várias vezes

>Para gamers: Use por conta e risco,visto que muitos anti-cheaters podem sim detectar o comportamento automatizado. O software não foi feito para ser um cheat e sim uma ferramenta de trabalho.

### Diferenciais

- ✅ **Interface amigável**: GUI moderna e intuitiva
- ✅ **Cross-platform**: Funciona em Windows, Linux e macOS
- ✅ **Atalhos globais**: Controle o programa sem precisar clicar nele, gravando ou reproduzindo ações através de teclas de atalho
- ✅ **Múltiplos modos de repetição**: Uma vez, X vezes, por tempo, infinito
- ✅ **Controle de velocidade**: Reproduza mais rápido ou mais devagar
- ✅ **Código aberto**: 100% gratuito e transparente

---

## 🤖 Abrindo o TarefAuto

Baixe sempre do último release, escolhendo o ZIP do executável de acordo com seu sistema operacional.

Pode também pegar pelo clone da raiz original do projeto, a pasta/diretório `/dist/` estará os executáveis disponíveis diretamente.

### Windows

- [Baixar a última versão](https://github.com/matheuslaidler/tarefauto/releases/latest) escolhendo o ZIP relacionado ao WINDOWS.
- Extrair o .zip, clicando com botão direito e extrair aqui
- Execute o `tarefauto.exe`
- PRONTO!

### Linux

- [Baixar a última versão](https://github.com/matheuslaidler/tarefauto/releases/latest) escolhendo o ZIP relacionado ao LINUX.
- Extrair o .zip, clicando com botão direito ou com comando `unzip *tarefauto*.zip`
- Execute o `tarefauto` pelo terminal:

**Se for primeira vez:**

```bash
#permissao
chmod +x ./tarefauto
#movendo para pasta de binario
sudo mv ./tarefauto /usr/local/bin/tarefauto
#abrindo programa
tarefauto
```
A partir de agora, sempre que quiser abrir o programa basta executar o binário digitando `tarefauto` no terminal (de qualquer diretório).

**Se apenas quiser executar logo**

```bash
#se pedir permissão
chmod +x ./tarefauto
#execução do binario
./tarefauto
```

### macOS

[Baixar a última versão](https://github.com/matheuslaidler/tarefauto/releases/latest) escolhendo o ZIP relacionado ao MACOS, se disponível.

Use o arquivo `.app` (quando disponível) ou um build específico para macOS.

Já me falaram que um binário criado em linux funcionaria para macOS por ser Unix-like, mas isso não parece fazer sentido. O binário gerado no Linux é de formato *ELF* e para o macOS deveria ser *Mach-O*. Geralmente, cada sistema precisa do seu próprio build.

Em outras palavras, um output comum para macOS seria um .app (bundle) e/ou um executável Mach‑O dentro dele.

> Caso não tenha o executável para macOS nas releases ou no repositório atual, considere criar um você mesmo com pyinstaller - *tutorial ainda neste readme*. Se quiser pode criar e fazer a contribuição.

---

**Pronto!! Agora só utilizar o software como quiser.**

Agora, caso queira o projeto completo (e quem sabe até modificar), siga os próximos passos:

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8 ou superior** ([Download](https://www.python.org/downloads/))
- **pip** (geralmente já vem com o Python)

### Passo a Passo

#### Windows (PowerShell)

```powershell
# 1. Clone o repositório (ou baixe o ZIP, caso tenha em releases)
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

### Modo de Edição

Após sua primeira gravação será liberada opções como salvar (caso não use o auto-save ou queira salvar com outro nome em outro diretório) e editar.
A opção de editar é exatamente isso, editar essa gravação. 

Como falado anteriormente, toda a gravação que o programa faz da tela ele transforma em JSON e que você pode modificar isso (ou até pedir para uma IA mudar algo para você) antes de utilizar para reprodução.

O botão editar facilita isso já abrindo para você direto. No windows, por exemplo, ele abrirá o bloco de notas com o JSON da sua gravação. Bom para quem teve que clicar em parar manualmente e quer tentar retirar essa parte.

Exemplo de JSON para edição:

```JSON
{
  "version": "1.0.0",
  "name": "Gravação sem nome",
  "description": "",
  "created_at": "2026-01-02T08:00:44.611127",
  "settings": {
    "record_mouse": true,
    "record_keyboard": true
  },
  "events": [
    {
      "t": 0.06884622573852539,
      "type": "MOUSE_CLICK",
      "x": 950,
      "y": 611,
      "btn": "left",
      "pressed": false
    },
    {
      "t": 0.6830654144287109,
      "type": "MOUSE_CLICK",
      "x": 950,
      "y": 611,
      "btn": "left",
      "pressed": true
    }
  ]
}
```


---

## ⚠️ Notas Importantes

### Antivírus

Supostamente alguns antivírus podem detectar o TarefAuto (meu malwarebytes e windows defender não se confundiram) porque ele:
- Captura eventos de teclado (como um keylogger faria)
- Simula cliques de mouse (como malware faria)

**Se acontecer, o que é difícil, entenda: isso é um falso positivo!** O Tarefauto:
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

### Executável

O projeto já conta com executável para windows e binário para linux, assim vocês podem apenas abrir o programa diretamente, sem precisar passar por todo o procedimento de instalação. Porém, caso queira criar seu próprio executável, como por exemplo criar um depois de ter modificado coisas do código, então pode seguir os passos abaixo.

### PyInstaller

O PyInstaller gera saídas em dois formatos principais:

- **--onefile**: sai **um único arquivo** (ex.: `TarefAuto.exe` no Windows ou `TarefAuto` no Linux). Em geral você pode mover e rodar só ele.
- **--onedir**: sai uma **pasta** com o executável e dependências. Você precisa levar a pasta inteira.

> No Linux/macOS, mesmo no modo **--onefile**, a máquina destino pode precisar de bibliotecas do sistema (ex.: componentes gráficos/Tk).

### Criando um Executável

Para criar um arquivo executável de terafauto:

```powershell
# Instale o PyInstaller
pip install pyinstaller

# Crie o executável / Build "arquivo único" (Windows/Linux)
pyinstaller --onefile --name TarefAuto main.py

# Para windows com ícone
pyinstaller --onefile --windowed --name TarefAuto --icon build/assets/robot.ico main.py

# macOS com ícone (.icns) - gere no macOS
pyinstaller --windowed --name TarefAuto --icon build/assets/robot.icns main.py
```

>O executável estará em `dist/TarefAuto.exe`.
Sempre será criado o executável **para o sistema operacional em que você está compilando**, ou seja, o pyinstaller sempre criará um executável com base no sistema do agente.

---

### Criando atalho

Se você usa windows, pode criar atalho do executável dentro de `dist` para onde queira (como a raiz do programa).

Se você usa linux, pode fazer um alias com 'bashrc', ou criar o atalho com `sudo ln -s /caminho/para/TarefAuto /usr/local/bin/tarefauto`. Até mesmo criar um atalho `.desktop`, geralmente sendo posicionado em `~/.local/share/applications/` ou na área de trabalho, apontando para o `Exec=/caminho/para/TarefAuto`.

**Linux**

No Linux, o ícone mostrado no menu/launcher vem de um arquivo .desktop + um PNG/SVG instalado no tema de ícones.

Para rodar no menu e aparecer com ícone, crie um .desktop e aponte para o ícone.

Exemplo de .desktop (usuário atual):

```shell
# salve em: ~/.local/share/applications/tarefauto.desktop
[Desktop Entry]
Type=Application
Name=TarefAuto
Exec=/caminho/absoluto/para/tarefauto
Icon=/caminho/absoluto/para/tarefauto/build/assets/robot.png
Terminal=false
Categories=Utility;
```

E depois:

```shell
chmod +x ~/.local/share/applications/tarefauto.desktop
update-desktop-database ~/.local/share/applications 2>/dev/null || true
```

Criar um symlink em /usr/local/bin facilita chamada no terminal.

```shell
ln -s /caminho/absoluto/para/tarefauto /usr/local/bin/tarefauto
```

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
