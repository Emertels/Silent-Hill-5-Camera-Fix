# Patch Fix Camera 1.0 - By Emerson Teles — AGENTS

## Regras de manutenção

Preserve a versão pública 1.0, os créditos EMERSON TELES e os nomes escolhidos pelo usuário. Faça backup antes de mudanças; preserve valores pessoais do INI. Não recalibre a horizontal, a mira ou o acompanhamento aprovados sem evidência. Distinga fórmulas, testes simulados e validação do usuário. Não prometa paridade física ou compatibilidade com binários não testados. Não publique automaticamente no GitHub.

O estado atual usa calibração vertical 2; descrições anteriores de igualdade angular X/Y referem-se à base anterior e não ao padrão atual. O gameplay aprovado após a correção do fechamento não prova a comparação visual da normalização vertical mais recente.

## Hooks de giro e vertical

`work/build_navigation_response.py` compõe o alinhamento existente. Yaw principal VA `0x108DB3D6`, cave `0x10386000` e helper `0x10386100` preservam o alinhamento aprovado. A rotação usa a rotina nativa `0x10145F50`; o yaw deriva da direção efetiva por `_CIatan2`, com normalização e convenção original. `FXSAVE/FXRSTOR` preserva FPU/SSE. Não redesenhe esse caminho para ajustar mira.

Pitch do controle em `0x10386200`: `CVTSS2SD XMM1,[EBX+24]`, `ANDPD` com máscara absoluta em `0x103862D0`, `MULSD` por constante nativa 60 e ganho double em `0x103862F0`, retorno `0x108DB003`. EBX é o quadro de controle e XMM0 contém dt. O quadrado foi removido neste caminho; decisões nativas e caminho alternativo são preservados. O cabeçalho de referência contém ganho base 1.4323944989229112 e calibração 2, cujo produto efetivo é 2.8647889978458223.

## Hooks da mira e estado gravável

Hook de entrada `0x103851E0`, cave `0x10386300`: fixa referência 2 nos campos `+AE8/AEC` somente na câmera Precision. `0x103863F8` contém ponteiro para `precision_mode` em dados graváveis da DLL. Cada passagem verifica ponteiro não nulo, zera o estado e Precision o coloca em 1. Constante de referência 2 em `0x103863FC`.

O wrapper escreve opção/3 em `0x103863F0/F4`. X: site `0x10711F24`, cave `0x10386400`, escala local `[ESP+20]` e reexecuta `MOVSS XMM0,[0x10F8A2E4]`. Y: site `0x1071EA28`, cave `0x10386480`, escala XMM0 e reexecuta store `[ESP+1C]`. `PUSHFD/POPFD` preserva flags do CMP anterior; registradores e pilha precisam permanecer corretos. Não escreva estado mutável na página executável. Preserve verificação de ponteiro nulo e restauração de proteção.

## Assinaturas, testes e evidências

O wrapper verifica hooks, main/helper, pitch, máscara, entrada da mira, referência fixa e outputs antes de configurar ganhos. Não relaxe essa verificação para aceitar outro SGL sem análise.

Fontes de teste: `build_test/navigation_speed_smoke.c`, `build_test/camera_protection_smoke.c`, `work/smoke_camera_response.py` e `work/smoke_navigation_aligned.py`. A regressão real de proteção executa código x86 READ/EXECUTE com estado gravável; emulação usa stubs de rotinas internas. Após mudança de código, execute verificações pertinentes e teste gameplay. Não repita testes sem mudança ou risco concreto.

Evidência da falha: `work/menu_crash_dump_report.json`, dump `SilentHill.exe.20612.dmp`, escrita `0x10386303 → 0x103863F8`, C0000005. A build defeituosa foi separada antes da correção. Não execute `install_camera_v1_public.py` ou outros instaladores históricos supondo que representam o estado atual.

## Apresentação e compatibilidade

**Versão 1.0 • Atualizado em 12/10/2026 • Mod by Emerson Teles — EMERSON TELES**.

Correção da câmera normal com controle, acompanhamento do personagem e sensibilidade independente da mira. Desenvolvida e testada nesta instalação **Unknown Project 3.20** de Silent Hill: Homecoming. Outras versões e o jogo sem o mod não foram validados.

Emerson aprovou o giro horizontal e o acompanhamento atrás do personagem em 1.0 e 2.0. Após a correção do fechamento antes do menu, também aprovou a mira em 1.0 e 2.0 e a resposta geral em 2.0. A normalização vertical mais recente ainda precisa de comparação no jogo: novo vertical 1.0 corresponde ao ganho do antigo vertical 2.0. Esse é o padrão calibrado do mod; não é uma certificação de equivalência exata ao jogo original.

## Arquivos e escopo

O pacote de instalação contém quatro arquivos em `Files/Bin`:

1. `g_SilentHill.sgl`: único binário existente do jogo modificado; contém os caminhos corrigidos de giro, acompanhamento, vertical e mira.
2. `xinput1_3.dll`: wrapper do mod; lê o INI, verifica assinaturas, configura constantes em memória e encaminha funções XInput.
3. `camera_input_base.dll`: DLL de entrada nativa, necessária para o encaminhamento e para os ajustes opcionais da entrada do analógico.
4. `camera_axis_fix.ini`: configuração das quatro sensibilidades, com comentários em inglês e os créditos do mod.

Os dois CFGs em `Engine` também precisam dos binds descritos abaixo. Eles foram ajustados em revisões anteriores. Na última calibração vertical, somente a DLL principal mudou de comportamento; o INI recebeu organização e comentários. SGL e CFGs permanecem iguais; a DLL de base fornece a entrada nativa. Executável, shv.dll, PAK, tradução e saves não fazem parte desta atualização.

## Instalação em três passos

1. Feche o jogo. Faça backup dos arquivos do `Bin` e de `Engine/binds_pc_mjs.cfg` e `Engine/bindcfgs_pc.cfg`. Preserve DLLs e INI próprios que já tenham os mesmos nomes.
2. Copie os quatro arquivos de `Files/Bin` para o `Bin` do jogo compatível. Nos dois CFGs, localize os comandos pelo nome e mantenha os seguintes binds do analógico direito:

```text
setbind 1 COMMAND_CAMERA_X CONTROLLER 0 AXIS_RX -1.0 1.0 1.0
setbind 1 COMMAND_CAMERA_Y CONTROLLER 0 AXIS_RY -1.0 1.0 1.0
setbind 1 COMMAND_TURNLEFT DEVICE_INVALID 0 0
setbind 1 COMMAND_TURNRIGHT DEVICE_INVALID 0 0
```

Preserve os `addbind` do teclado e os demais comandos. O mod gira o corpo junto com a câmera; TURNLEFT/TURNRIGHT do analógico precisam ficar desativados para não somar outro giro. Não foi determinado qual CFG é carregado em todas as opções do Unknown Project; mantenha os dois consistentes.

3. Abra o jogo e teste giro contínuo para ambos os lados, parado e andando, movimento vertical e mira. Comece em 1.0, altere uma opção por vez e reinicie após editar.

## Todas as opções do INI

Edite `Bin/camera_axis_fix.ini` com o jogo fechado. Os quatro padrões do pacote são:

```ini
[Camera]
HorizontalCameraSpeed=1.0
VerticalCameraSpeed=1.0
AimHorizontalSpeed=1.0
AimVerticalSpeed=1.0
```

- `HorizontalCameraSpeed`: Câmera normal horizontal e giro do personagem; referência 1.5 rad/s em 1.0. Não altera a velocidade de caminhada ou corrida.
- `VerticalCameraSpeed`: Câmera normal vertical; novo 1.0 equivale ao antigo 2.0. Ganho efetivo 2.864788997846 × opção.
- `AimHorizontalSpeed`: Sensibilidade horizontal independente da câmera Precision; multiplicador aplicado após a curva nativa.
- `AimVerticalSpeed`: Sensibilidade vertical independente da câmera Precision; multiplicador aplicado após a curva nativa.
- `RightStickXExponent`: Curva legada da entrada horizontal; manter 1.0 para resposta neutra.
- `RightStickYExponent`: Curva legada da entrada vertical; manter 1.0 para resposta neutra.
- `RightStickXGain`: Ganho legado da entrada horizontal bruta; manter 1.0 para não somar ganhos.
- `RightStickYGain`: Ganho legado da entrada vertical bruta; manter 1.0 para não somar ganhos.

Mantenha os multiplicadores X/Y dos CFGs em 1.0 e ajuste a sensibilidade pelo INI. Alterar ambos combina ganhos. Os campos legados existem por compatibilidade com a DLL anterior; não substituem as quatro opções principais.

## Valores, percentuais e leitura

As quatro opções principais aceitam decimais entre **0.25 e 3.0**, incluindo 1.1, 1.15, 1.2, 1.5, 2.0 e 2.5. Use ponto decimal; vírgula, sinal negativo e expoente não são aceitos. Valor ausente ou texto inválido usa 1.0. Valores usuais fora da faixa são limitados; inteiros acima de 100 durante a leitura podem retornar a 1.0. Zero não desativa o mod. A faixa das quatro opções não se aplica aos campos legados.

Em relação a 1.0: 0.25 = −75%; 0.5 = −50%; 0.75 = −25%; 1.1 = +10%; 1.2 = +20%; 1.5 = +50%; 2.0 = +100%; 2.5 = +150%; 3.0 = +200%. Fórmula: `(valor - 1) × 100%`. Entre dois ajustes: `(novo / anterior - 1) × 100%`; de 1.1 para 1.2 é aproximadamente +9.09%, e de 2.0 para 2.5 é +25%.

Esses percentuais descrevem o ganho, não garantem a velocidade visual final. O log arredonda valores a duas casas, mas isso não limita a precisão lida. As opções são carregadas na inicialização: salve e feche/reabra o jogo. Veja [MANUAL.md](MANUAL.md) para mais exemplos e dicas.

## Cálculo da câmera normal e calibração vertical

A horizontal solicita `1.5 × HorizontalCameraSpeed × entrada × dt` radianos por quadro. Em 1.0 e deflexão máxima, a referência é aproximadamente 85.94 graus/s. A rotina nativa pode limitar o giro real; a câmera acompanha a direção efetiva do personagem.

O vertical original elevava a entrada ao quadrado: 0.5 virava 0.25. O mod usa o módulo da entrada no caminho do controle para obter resposta linear, preservando o tratamento do sentido, zona morta, tempo do quadro e limites nativos.

Referências extraídas do SGL: 60 graus/s em VA `0x10F91290` e conversão para radianos `0.01745329238474369` em VA `0x10F93F48`. O ganho base é `1.5 / (60 × 0.01745329238474369) = 1.4323944989229112`.

Emerson escolheu o antigo vertical 2.0 como padrão mais próximo da sensação da horizontal 1.0. A calibração atual aplica fator 2: ganho efetivo `2.8647889978458223 × VerticalCameraSpeed`. Antes dos limites, Y solicita `3 × opção` rad/s no máximo; X solicita `1.5 × opção`. Portanto, não são taxas físicas iguais. O ajuste é empírico, baseado no teste do usuário.

Novo Y1.0 = antigo Y2.0; novo Y1.5 = antigo Y3.0. Novo Y2.0 e Y3.0 equivalem matematicamente aos ganhos antigos Y4.0 e Y6.0, que não eram aceitos no INI anterior. A faixa atual continua 0.25–3.0. Teste o novo 1.0 antes de aumentar. Enquadramento, colisão, limites e rotação real podem mudar a percepção.

## Mira e acompanhamento do personagem

A mira usa `opção / 3` após os caminhos de curva nativa identificados, somente com câmera ativa `Precision`: 1.0 = um terço da referência rápida anterior; 2.0 = dois terços; 3.0 = referência rápida anterior, equivalente ao antigo 1.0 nesses caminhos.

As tentativas anteriores aumentavam a entrada antes da curva quadrática, tornando 2.0 rápido demais. A aplicação pós-curva fornece progressão proporcional no ponto modificado. A aceleração, os limites e outros estados do motor ainda podem afetar o movimento; não foram medidos graus/s finais globais da mira. Outros nomes de câmera não recebem esses ganhos.

Alterar só o CFG horizontal não resolvia a lentidão; outras tentativas aceleravam a arma ou giravam a câmera sem o corpo. A solução aprovada gira o personagem pela rotina nativa e calcula o ângulo da câmera a partir da direção real, com a convenção angular original. No neutro, mantém o acompanhamento original. A última normalização vertical preservou o horizontal e a mira aprovados.

## Fechamento antes do menu e verificação

O dump `SilentHill.exe.20612.dmp` identificou a exceção original `0xC0000005`: escrita pela instrução VA `0x10386303` no endereço `0x103863F8`. A flag Precision estava na seção executável protegida do SGL. A exceção final `0xC0000409` em KERNELBASE era o encerramento posterior.

A flag agora fica em dados graváveis da DLL. O SGL contém um ponteiro configurado pelo wrapper; os hooks verificam ponteiro nulo. Após aplicar constantes e ponteiro, as páginas retornam à proteção original. O SGL de disco não é regravado pela DLL.

Passaram compilação x86, teste nativo de assinatura/valores/encaminhamento e teste do detour real com `PAGE_EXECUTE_READ`, incluindo mundo nulo, Precision, Navigation e ponteiro ainda não configurado. Foram registrados 255 casos de curva/escala e 10.800 quadros de alinhamento em emulação. As rotinas internas simuladas não certificam todos os estados do jogo. Emerson confirmou abertura e bom gameplay após a correção; a normalização vertical mais recente continua aguardando comparação visual.

O log `Bin/camera_axis_fix.log` registra aplicação ou rejeição de assinaturas e `post-curve scale=value/3` da mira.

## Backup e restauração

`Files/_Backup Original/Bin/g_SilentHill.sgl` é o backup preexistente mais antigo desta instalação, SHA256 `2A7C30031A3146036115292EED7D6022C603470C257A5659BED8D4423F2DFD61`. Não é um arquivo vanilla certificado.

Feche o jogo, restaure o SGL apropriado e seus CFGs/auxiliares anteriores. Remova as duas DLLs e o INI do mod apenas se não existiam antes; arquivos próprios devem ser restaurados pelo backup pessoal.

Registro local: backup anterior à normalização em `C:/Projetos/SilentHill5-CameraFix/_backup/antes_normalizar_vertical_v1_20261012_125613`; backup anterior à correção do fechamento em `_backup/antes_correcao_fechamento_v1_20261012_012327`; build defeituosa arquivada em `_backup/falha_menu_v1_20261012`. Esses registros locais não acompanham necessariamente o pacote público.

## Fontes e documentos

`Source` contém os fontes do mod, cabeçalhos, geradores históricos do patch e testes; não contém o código-fonte do jogo. O wrapper foi recompilado a partir do pacote e os dois testes nativos passaram. Consulte [Source/README.md](Source/README.md) e [Source/README.en.md](Source/README.en.md).

Os geradores históricos ainda dependem de caminhos e backups/intermediários compatíveis. Não são um gerador portátil em um clique. Não execute instaladores históricos às cegas: eles podem instalar versões obsoletas ou defeituosas. Não publique backups ou binários originais como código-fonte. A versão pública permanece 1.0; repositório oficial no GitHub: https://github.com/Emertels/Silent-Hill-5-Camera-Fix.

Documentos pareados: [README-EN.md](README-EN.md), [AGENTS.PT-BR.md](AGENTS.PT-BR.md) e [AGENTS-EN.md](AGENTS-EN.md). [MANUAL.md](MANUAL.md) detalha opções e testes em português; [CHANGELOG.md](CHANGELOG.md) registra mudanças; `SHA256.json` identifica os arquivos.

## Créditos

**Emerson Teles — EMERSON TELES:** testes no jogo, identificação dos sintomas, escolha da calibração, validação do acompanhamento e organização. Implementação e verificação local com assistência do Codex. Silent Hill: Homecoming e Unknown Project pertencem aos respectivos autores.
