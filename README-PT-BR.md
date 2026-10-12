# 🕹️ Silent Hill 5: Homecoming — Camera Fix (Patch de Correção de Câmera)

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Documentação-Português%20(PT--BR)-009c3b?style=for-the-badge&logo=readme&logoColor=white" alt="Versão em Português"></a>
  <a href="README-EN.md"><img src="https://img.shields.io/badge/Documentation-English-0052cc?style=for-the-badge&logo=readme&logoColor=white" alt="English Version"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Versão-v1.0.0-blue?style=for-the-badge" alt="Versão">
  <img src="https://img.shields.io/badge/Status-100%25%20Funcional-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Plataforma-PC%20Windows-0078D6?style=for-the-badge&logo=windows" alt="Plataforma">
  <img src="https://img.shields.io/badge/Licença-MIT-purple?style=for-the-badge" alt="Licença">
</p>

Mod definitivo de correção de câmera normal no analógico direito do controle (gamepad), acompanhamento inteligente atrás do personagem e sensibilidade vertical e de mira totalmente independente para **Silent Hill 5: Homecoming (PC)**, desenvolvido, calibrado e testado por **Emerson Teles**.

---

## 📋 Sumário

1. [Apresentação e Compatibilidade](#-apresentação-e-compatibilidade)
2. [Download da Versão 1.0.0](#-download-da-versão-100)
3. [Arquivos e Estrutura do Pacote](#-arquivos-e-estrutura-do-pacote)
4. [Instalação Passo a Passo](#-instalação-passo-a-passo)
5. [Configuração do INI (Sensibilidades)](#-configuração-do-ini-sensibilidades)
6. [Valores, Decimais e Escalas Suportadas](#-valores-decimais-e-escalas-suportadas)
7. [Cálculo da Câmera Normal e Calibração Vertical](#-cálculo-da-câmera-normal-e-calibração-vertical)
8. [Mira e Acompanhamento do Personagem](#-mira-e-acompanhamento-do-personagem)
9. [Correção de Memória (Crash Antes do Menu)](#-correção-de-memória-crash-antes-do-menu)
10. [Backup Original e Restauração](#-backup-original-e-restauração)
11. [Código-Fonte e Build](#-código-fonte-e-build)
12. [Créditos e Autoria](#-créditos-e-autoria)
13. [Sobre o Autor & Redes Oficiais](#-sobre-o-autor--redes-oficiais)

---

## 🌟 Apresentação e Compatibilidade

**Versão 1.0.0 • Mod by Emerson Teles — EMERSON TELES**.

Na versão de PC de *Silent Hill: Homecoming*, a câmera no controle sofre de graves problemas nativos: resposta excessivamente lenta no analógico direito, curva de aceleração quadrática vertical desagradável, falta de sincronização entre o giro da câmera e o corpo de Alex Shepherd, e mira (câmera Precision) com sensibilidade travada.

Este mod soluciona todos esses problemas:
- **Giro horizontal responsivo e natural:** O personagem e a câmera giram em perfeita sincronia pela rotina nativa, calculando o ângulo da câmera pela direção real do personagem.
- **Resposta vertical linear e calibrada:** Remove a curva ao quadrado da entrada do controle, garantindo movimentação vertical suave e proporcional. A sensibilidade vertical padrão (1.0) foi normalizada para corresponder perfeitamente à sensação do horizontal.
- **Sensibilidade de mira independente:** Permite ajustar a sensibilidade horizontal e vertical durante o modo de mira (*Precision*), sem comprometer a movimentação da câmera normal.
- **Configuração simples em INI:** Ajuste em tempo real através do arquivo `camera_axis_fix.ini`.
- **Compatibilidade:** Desenvolvido e validado na instalação **Unknown Project 3.20** de *Silent Hill: Homecoming*.

---

## 📥 Download da Versão 1.0.0

### [⬇️ Baixar Silent Hill 5 Camera Fix v1.0.0 (ZIP)](https://github.com/Emertels/Silent-Hill-5-Camera-Fix/releases/download/v1.0.0/Silent-Hill-5-Camera-Fix-v1.0.0.zip)

> [!IMPORTANT]
> O arquivo ZIP de lançamento contém **apenas os arquivos funcionais** necessários para substituição e instalação (`Files/Bin`) e a pasta de segurança com o arquivo original (`Files/_Backup Original`). Manuais e documentações estão disponíveis aqui na página oficial do repositório no GitHub.

---

## 📂 Arquivos e Estrutura do Pacote

O pacote funcional do mod está estruturado da seguinte forma:

```text
Files/
├── Bin/
│   ├── g_SilentHill.sgl          # Único binário do jogo modificado com os hooks de giro, mira e vertical
│   ├── xinput1_3.dll             # Wrapper nativo que carrega o INI e aplica as constantes em memória
│   ├── camera_input_base.dll     # DLL de entrada nativa para encaminhamento de funções
│   └── camera_axis_fix.ini       # Arquivo de configuração das sensibilidades
└── _Backup Original/
    └── Bin/
        └── g_SilentHill.sgl      # Arquivo original preservado para desinstalação segura
```

> [!NOTE]
> Executável principal (`SilentHill.exe`), `shv.dll`, arquivos `.PAK`, traduções e saves do jogo permanecem totalmente intactos e não são afetados por este mod.

---

## 🛠️ Instalação Passo a Passo

### Passo 1: Backup Preventivo
Feche o jogo. Caso deseje, faça backup da sua pasta `Bin` e dos arquivos de configuração `Engine/binds_pc_mjs.cfg` e `Engine/bindcfgs_pc.cfg`.

### Passo 2: Copiar os Arquivos
Copie todo o conteúdo de `Files/Bin` para a pasta `Bin` da instalação do seu jogo, substituindo o arquivo `g_SilentHill.sgl` quando solicitado.

### Passo 3: Configurar os Binds do Analógico
Abra os arquivos `Engine/binds_pc_mjs.cfg` e `Engine/bindcfgs_pc.cfg` em um editor de texto (como Bloco de Notas ou VS Code). Localize os comandos abaixo e garanta que estejam exatamente assim:

```text
setbind 1 COMMAND_CAMERA_X CONTROLLER 0 AXIS_RX -1.0 1.0 1.0
setbind 1 COMMAND_CAMERA_Y CONTROLLER 0 AXIS_RY -1.0 1.0 1.0
setbind 1 COMMAND_TURNLEFT DEVICE_INVALID 0 0
setbind 1 COMMAND_TURNRIGHT DEVICE_INVALID 0 0
```

> [!TIP]
> **Por que desativar TURNLEFT e TURNRIGHT do analógico?**
> Como o mod gira o corpo de Alex perfeitamente junto com a câmera, manter `COMMAND_TURNLEFT` e `COMMAND_TURNRIGHT` atribuídos ao analógico direito somaria dois giros simultâneos. Mantê-los como `DEVICE_INVALID` garante rotação suave e uniforme. Preserve os demais comandos e os `addbind` do teclado.

### Passo 4: Jogar e Ajustar
Inicie o jogo e aproveite a movimentação fluida!

---

## ⚙️ Configuração do INI (Sensibilidades)

Com o jogo fechado, edite o arquivo `Bin/camera_axis_fix.ini`. A configuração padrão é:

```ini
; Patch Fix Camera 1.0 - By Emerson Teles
; Silent Hill: Homecoming - Unknown Project 3.20
[Camera]

; Câmera normal horizontal e giro do personagem (1.0 = referência 1.5 rad/s)
HorizontalCameraSpeed=1.0

; Câmera normal vertical (1.0 calibrado para corresponder à sensação horizontal)
VerticalCameraSpeed=1.0

; Mira (câmera Precision) - sensibilidade horizontal
AimHorizontalSpeed=1.0

; Mira (câmera Precision) - sensibilidade vertical
AimVerticalSpeed=1.0

; Configurações legadas (manter 1.0 para neutralidade)
RightStickXExponent=1.0
RightStickYExponent=1.0
RightStickXGain=1.0
RightStickYGain=1.0
```

- `HorizontalCameraSpeed`: Velocidade de giro horizontal da câmera normal e rotação corporal do personagem. Não altera velocidade de caminhada ou corrida.
- `VerticalCameraSpeed`: Velocidade vertical da câmera normal. A calibração padrão 1.0 já vem dobrada (ganho 2.864789) em relação às tentativas iniciais, alinhando-se à horizontal.
- `AimHorizontalSpeed`: Multiplicador horizontal exclusivo para a mira com armas (câmera Precision).
- `AimVerticalSpeed`: Multiplicador vertical exclusivo para a mira com armas (câmera Precision).

---

## 📊 Valores, Decimais e Escalas Suportadas

As opções principais aceitam valores decimais de **0.25 a 3.0** com ponto decimal (`.`):

| Valor | Variação vs. Padrão | Descrição |
| :---: | :---: | :--- |
| `0.25` | −75% | Câmera extremamente lenta |
| `0.50` | −50% | Metade da velocidade padrão |
| `0.75` | −25% | Velocidade moderada / suave |
| `1.00` | **Padrão** | **Sensibilidade padrão calibrada e aprovada** |
| `1.20` | +20% | Levemente mais rápida |
| `1.50` | +50% | Resposta ágil |
| `2.00` | +100% | O dobro da velocidade padrão |
| `2.50` | +150% | Resposta muito rápida |
| `3.00` | +200% | Velocidade máxima recomendada |

> [!NOTE]
> Salve o arquivo e reinicie o jogo após qualquer alteração no INI para carregar os novos valores.

---

## 📐 Cálculo da Câmera Normal e Calibração Vertical

- **Horizontal:** Solicita `1.5 × HorizontalCameraSpeed × entrada × dt` radianos por quadro. Com 1.0 e deflexão total da alavanca, a referência é de ~85.94 graus por segundo.
- **Vertical:** O jogo original elevava a entrada ao quadrado ($0.5^2 = 0.25$), gerando sensação pesada no início e descontrolada no final. O mod utiliza o módulo da entrada (`ANDPD`), transformando a curva em linear enquanto preserva zonas mortas, inversões e tempos de quadro nativos.
- **Calibração:** As constantes originais do SGL são 60 graus/s em `VA 0x10F91290` e fator radiano `0.01745329` em `VA 0x10F93F48`, com ganho base de $1.432394$. Para parear a percepção vertical com a horizontal de 1.0, o mod aplica o fator de calibração empírico aprovado por Emerson Teles, totalizando ganho efetivo de $2.864789 \times \text{VerticalCameraSpeed}$.

---

## 🎯 Mira e Acompanhamento do Personagem

- A mira aplica o escalonamento `opção / 3.0` logo após a saída da curva nativa, ativando-se **exclusivamente quando a câmera Precision estiver em execução**.
- Isso elimina o comportamento desordenado de versões anteriores e proporciona mira cirúrgica, gradual e customizável.
- Em repouso analógico (neutro), o algoritmo preserva integralmente a lógica nativa de acompanhamento suave atrás do personagem.

---

## 🛡️ Correção de Memória (Crash Antes do Menu)

Durante o desenvolvimento, identificou-se via dump de memória (`SilentHill.exe.20612.dmp`) uma falha crítica `0xC0000005` (Access Violation) causada pela escrita na instrução VA `0x10386303` para o endereço `0x103863F8`. Esse local ficava na seção executável protegida contra escrita do `g_SilentHill.sgl`.

A solução desenvolvida:
1. Moveu o armazenamento da flag `PrecisionMode` para a memória gravável da DLL wrapper (`xinput1_3.dll`).
2. Implementou checagem segura contra ponteiros nulos nos hooks de montagem.
3. Garantiu que as páginas de memória voltem à proteção estrita de execução (`PAGE_EXECUTE_READ`) após a inicialização.
4. Validado por testes de estresse em assembly x86 e regressão de memória nativa.

---

## 💾 Backup Original e Restauração

O projeto preserva o arquivo original do jogo antes de qualquer modificação, permitindo desinstalação limpa a qualquer momento:

- **Arquivo:** `Files/_Backup Original/Bin/g_SilentHill.sgl`
- **Hash SHA256:** `2A7C30031A3146036115292EED7D6022C603470C257A5659BED8D4423F2DFD61`

> [!NOTE]
> Este arquivo foi comparado com duas cópias antigas idênticas da versão Unknown Project 3.20 e validado por Emerson Teles. Como apenas o `g_SilentHill.sgl` é modificado, a restauração é imediata.

### Como Desinstalar ou Restaurar o Jogo Original:
1. **Feche o jogo** completamente.
2. Copie `Files/_Backup Original/Bin/g_SilentHill.sgl` para a pasta `Bin` do jogo, substituindo o arquivo modificado.
3. Exclua da pasta `Bin` do jogo os arquivos complementares do mod:
   - `camera_axis_fix.ini`
   - `camera_input_base.dll`
   - `xinput1_3.dll`
4. Seus binds originais e o comportamento padrão do jogo estarão 100% restaurados.

---

## 💻 Código-Fonte e Build

O repositório disponibiliza na pasta [`Source/`](Source/) o código-fonte C/C++ completo do wrapper e os scripts de geração e teste:

- `src/camera_xinput_proxy.cpp`: Wrapper de interceptação XInput e injeção em tempo de execução.
- `src/camera_input_base.c`: Camada nativa de entrada.
- `build_test/`: Testes automatizados de assinatura de memória e proteção de páginas.
- `work/`: Scripts Python de emulação matemática, reconstrução de offsets e validação.

---

## ✍️ Créditos e Autoria

- **Criação, Calibração, Testes e Organização:** **Emerson Teles (EMERSON TELES)**
- **Desenvolvimento e Verificação Técnica:** Emerson Teles com assistência de Codex
- **Versão:** 1.0.0
- **Licença:** [MIT](LICENSE)

*Silent Hill: Homecoming* e *Unknown Project* são propriedades intelectuais de seus respectivos detentores de direitos autorais. Este é um mod independente sem fins lucrativos desenvolvido pela comunidade.

---

## 👨‍💻 Sobre o Autor & Redes Oficiais

Desenvolvido e mantido por **Emerson Teles** (conhecido na comunidade como **Emertels**).

Entusiasta de tecnologia, informática, jogos, manutenção de sistemas e tradução/localização de softwares para Português do Brasil (PT-BR). Desenvolvedor focado em utilitários práticos, ferramentas de produtividade, automação inteligente em PowerShell e mods técnicos para PC.

### 🌐 Conecte-se comigo & Comunidades Oficiais

<div align="left">

[![GitHub](https://img.shields.io/badge/GitHub-Emertels-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emertels)
[![Website](https://img.shields.io/badge/Website-Emerson_Teles-0070F3?style=for-the-badge&logo=googlechrome&logoColor=white)](https://emertels.github.io)
[![Discord](https://img.shields.io/badge/Discord-Emertels%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://emertels.github.io/discord)
[![X / Twitter](https://img.shields.io/badge/X_Twitter-@emertels-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/emertels)
[![YouTube](https://img.shields.io/badge/YouTube-Emerson_Teles-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@emersonteles2379)
[![Telegram](https://img.shields.io/badge/Telegram-Aplicativos%20Mods-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/apksmodsandroid)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Apoiar%20Projeto-FF5E5B?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/emertels)

</div>
