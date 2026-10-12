# Patch Fix Camera 1.0 - By Emerson Teles

## Referência vertical normalizada — versão 1.0, 12/10/2026

Emerson aprovou a horizontal em1.0, a mira em1.0/2.0 e todos os modos em2.0. No comparativo posterior, escolheu a velocidade do **antigo vertical2.0** como referência mais próxima da horizontal1.0. A nova normalização aplica essa escolha: **novo VerticalCameraSpeed=1.0 equivale ao ganho do antigo2.0**.

A DLL agora multiplica somente a referência vertical por2. O fator angular de base extraído do SGL continua 1.432394498923; a referência efetiva é 2 × 1.432394498923 = **2.864788997846**. A curva linear vertical e seus limites permanecem. Os cálculos horizontal, mira e acompanhamento, o SGL e os binds não foram alterados.

Isso é uma calibração **empírica escolhida pelo usuário**, com equivalência exata entre os ganhos antigos e novos, não uma nova medição de paridade angular. Antes dos limites, a solicitação vertical no máximo agora é 3 × VerticalCameraSpeed rad/s, enquanto a horizontal continua 1.5 × HorizontalCameraSpeed. As taxas matemáticas diferem por escolha de sensação; não afirmar igualdade física somente porque o usuário considerou o movimento mais equilibrado.

Na nova escala vertical: 1.0=antigo2.0; 1.5=antigo3.0; 2.0 solicita equivalente ao antigo4.0 e 3.0 ao antigo6.0. Os antigos4/6 não eram aceitos no INI anterior; aqui são equivalências de ganho interno, não valores liberados. O INI continua aceitando **0.25..3.0**. 2.0 e3.0 ficam mais rápidos que antes no vertical, então comece pelo novo1.0 e confira antes de aumentar.

Vertical instalado foi deixado em1.0 para testar a referência escolhida. Outros valores pessoais do INI foram preservados. O pacote continua com quatro padrões1.0. A abertura e o gameplay da versão anterior já foram aprovados; a leitura desta nova referência ainda precisa ser conferida pelo usuário. Não há mudança da escala da mira nesta atualização.

Backup anterior: `C:\Projetos\SilentHill5-CameraFix\_backup\antes_normalizar_vertical_v1_20261012_125613`. Compilação x86, teste de fatores/normalização e regressão nativa com código READ/EXECUTE passaram. A flag continua em dados graváveis da DLL. Versão pública mantida em1.0.

**Atualizado em 12/10/2026 • Emerson Teles — EMERSON TELES**

Este manual explica instalação, quatro ajustes, faixa aceita, percentuais, calibração, campos antigos e restauração. O mod foi desenvolvido para esta instalação Unknown Project 3.20. Outros binários e o jogo sem esse projeto não tiveram compatibilidade comprovada.

## 1. Situação atual

O jogo voltou a abrir após a correção da flag de mira. Emerson aprovou o acompanhamento atrás do personagem, a horizontal em 1.0/2.0, a mira em 1.0/2.0 e o teste com todos em 2.0. No retorno posterior, escolheu o antigovertical2.0 como novo padrão1.0. A DLL foi normalizada para essa equivalência; o novo padrão precisa ser conferido no jogo.

O pacote usa os quatro padrões 1.0. Seu INI instalado pode ter valores pessoais diferentes. Durante esta atualização de documentos, nenhum INI, binário ou bind foi modificado.

## 2. Onde ajustar

Depois da instalação, edite **Bin/camera_axis_fix.ini**, dentro da pasta do jogo. O INI que está em `Files/Bin` pertence ao pacote manual: mudar apenas essa cópia não muda o jogo até copiá-la para o Bin.

Procedimento:

1. Feche o jogo e abra o INI instalado em um editor de texto.
2. Na seção `[Camera]`, altere o número da opção desejada. Use ponto decimal.
3. Salve mantendo o nome `camera_axis_fix.ini`, não `.ini.txt`, e abra o jogo novamente.

As opções são lidas na inicialização. Salvar enquanto o jogo está aberto não atualiza os ganhos da sessão atual.

```ini
[Camera]
HorizontalCameraSpeed=1.0
VerticalCameraSpeed=1.0
AimHorizontalSpeed=1.0
AimVerticalSpeed=1.0
```

Mantenha uma linha para cada opção; evite chaves duplicadas. Escreva comentários em linhas próprias iniciadas por `;`, sem juntar texto ao valor numérico.

## 3. O que cada opção faz

**HorizontalCameraSpeed:** giro esquerda/direita da câmera normal pelo analógico direito. Regula também a rotação do personagem que acompanha a câmera. Não aumenta a caminhada ou corrida do analógico esquerdo. O código de acompanhamento aprovado usa a direção real do personagem depois da rotação.

**VerticalCameraSpeed:** resposta cima/baixo da câmera normal. O caminho do controle usa resposta linear e fator angular calculado a partir das constantes verticais originais. Continua sujeito à zona morta e aos limites de inclinação do jogo. Não transforma a câmera vertical em giro ilimitado.

**AimHorizontalSpeed:** sensibilidade esquerda/direita da mira com arma no modo de câmera Precision. O ajuste é aplicado depois dos caminhos de curva nativa identificados. Não modifica o HorizontalCameraSpeed.

**AimVerticalSpeed:** sensibilidade cima/baixo da mira com arma no mesmo modo. Não modifica o VerticalCameraSpeed.

Você pode usar valores diferentes nos quatro campos. Por exemplo, horizontal normal=1.0, vertical normal=1.2 e mira X/Y=1.0 são ajustes independentes. Para avaliar equilíbrio entre eixos, mantenha a referência horizontal fixa durante a comparação.

## 4. Todos os valores aceitos

Não existe uma lista fechada de passos. As quatro opções aceitam **números decimais de 0.25 até 3.0**, incluindo os extremos e valores intermediários: 1.01, 1.1, 1.15, 1.2, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5 e assim por diante. A precisão é a de ponto flutuante usada pela implementação; não é necessário escrever muitas casas decimais para calibrar visualmente.

Use `1.2`, não `1,2`. Também são válidos inteiros como `1`, `2` e `3`, mas a escrita `1.0` ajuda a manter a configuração consistente.

Comportamento do leitor:

- Valor válido dentro de 0.25..3.0: usa esse valor.
- Valor numérico comum abaixo de 0.25, como 0 ou 0.1: limita a 0.25. Zero **não desliga** o mod.
- Valor numérico comum acima de 3.0, como 4.0 ou 5.0: limita a 3.0. Não há velocidade 4.0/5.0 nesta versão.
- Valor ausente ou texto inválido: usa 1.0. Não use sinal negativo, vírgula, notação científica como `1e0`, nem unidades como `1.2x`.
- Números excessivamente grandes também podem voltar ao padrão do leitor, em vez de virar 3.0. Para resultados previsíveis, use somente valores dentro da faixa documentada.

O log mostra os multiplicadores com duas casas decimais. Isso não significa que o INI só aceite passos de 0.01: um valor como 1.125 pode aparecer arredondado no texto do log, sem que o leitor tenha limitado o ajuste a duas casas.

## 5. Percentuais em relação a 1.0

Fórmula: **percentual da referência = valor × 100**. Aumento ou redução em relação a 1.0: **(valor − 1) × 100**.

- 0.25: 25% da referência, redução de 75%.
- 0.50: 50% da referência, redução de 50%.
- 0.75: 75% da referência, redução de 25%.
- 1.00: 100%, a referência padrão do mod.
- 1.10: 110%, aumento de 10%.
- 1.15: 115%, aumento de 15%.
- 1.20: 120%, aumento de 20%.
- 1.25: 125%, aumento de 25%.
- 1.50: 150%, aumento de 50%.
- 1.75: 175%, aumento de 75%.
- 2.00: 200%, aumento de 100%, ou duas vezes a referência.
- 2.25: 225%, aumento de 125%.
- 2.50: 250%, aumento de 150%.
- 2.75: 275%, aumento de 175%.
- 3.00: 300%, aumento de 200%, ou três vezes a referência.

Esses percentuais descrevem o **multiplicador aplicado no cálculo**, não uma medição garantida da velocidade visual final. Aceleração, limites, enquadramento e colisão podem mudar a sensação.

Para comparar dois valores diferentes de 1.0, use **(novo ÷ anterior − 1) × 100**. De 1.1 para 1.2, o aumento é aproximadamente 9.09%, apesar de 1.2 estar 20% acima de 1.0. De 2.0 para 2.5, o aumento é 25%, não 50%.

## 6. Referência da câmera normal

No horizontal, a taxa solicitada em deflexão máxima é `1.5 × HorizontalCameraSpeed` radianos/s, antes das limitações do corpo. Em 1.0 é aproximadamente 85.94 graus/s; em 2.0, 171.89; em 3.0, 257.83. Com inclinação parcial, a entrada do controle participa linearmente.

O código vertical original do controle usa referência de 60 graus/s. A conversão nativa para radianos identificada é 0.01745329238474369. Para aproximar a referência angular da horizontal aprovada, o mod calcula:

```text
ganho vertical = 1.5 / (60 × 0.01745329238474369)
              = 1.432394498923
```

O caminho vertical deixou de elevar a entrada ao quadrado e usa seu módulo. A normalização atual acrescenta fator2 escolhido pelo usuário: ganho efetivoY=2.864788997846 × opção. Y1.0 corresponde ao antigoY2.0. Não há agora igualdade matemática entre as taxas solicitadas X/Y; a referência foi calibrada pela sensação no jogo.

Ainda assim, o eixo vertical tem curso limitado, enquadramento e zona morta próprios; a horizontal também depende da rotação efetiva do personagem. **Não trate essa conta como prova de sensação perfeitamente igual em todo o movimento**, nem como certificação de velocidade idêntica ao jogo sem mod. O 1.0 é o padrão calibrado do mod. Emerson preferiu a sensação do antigoY2.0, que foi normalizada como novoY1.0. A aplicação dessa nova base ainda precisa ser conferida no jogo.

## 7. Referência da mira

A nova escala da mira usa **valor do INI ÷ 3**, aplicado depois das curvas nativas identificadas, mantendo fixa a entrada de referência responsiva anterior.

- Mira 1.0: um terço da referência rápida da versão anterior.
- Mira 1.5: metade daquela referência.
- Mira 2.0: dois terços daquela referência.
- Mira 2.5: cinco sextos, aproximadamente 83.33% daquela referência.
- Mira 3.0: referência rápida do antigo padrão 1.0 nos caminhos modificados.

Em relação ao **novo** padrão 1.0, mira 2.0 aplica o dobro do multiplicador e mira 3.0 aplica o triplo. São duas bases de comparação diferentes; não confundir o antigo padrão rápido com o padrão atual.

O ajuste depois da curva evita que aumentar o número do INI também amplifique o efeito de elevar a entrada ao quadrado. Porém, a mira ainda possui aceleração, limites e estados nativos. Sua velocidade final em graus/s não foi medida como igual à câmera normal. A validação do usuário foi prática: mira 1.0 e 2.0 ficaram excelentes.

## 8. Calibrar sem perder a referência

Na comparação anterior à normalização vertical:

1. Use HorizontalCameraSpeed=1.0 e VerticalCameraSpeed=1.0 como comparação inicial.
2. Teste VerticalCameraSpeed=1.1, sem mudar o horizontal ou a mira junto.
3. Se ainda estiver lento, teste 1.2; se passar do ponto, use um intermediário como 1.15.
4. Feche/reabra entre alterações. Compare na mesma área e postura, com movimentos parecidos do analógico.
5. Depois de escolher o melhor valor, confira a resposta parcial e no fim do curso, parado e andando. Confira também os demais valores que você costuma usar, como 2.0.

Esses testes1.1/1.2 ficaram como histórico. A referência escolhida posteriormente foi antigoY2.0, agora chamadoY1.0. Depois da normalização, não use comparações antigas como se a base não tivesse mudado.

Uma configuração de uso aprovada pelo usuário foi todos em 2.0. Outra foi mira em 1.0. Esses relatos ajudam a escolher uma referência, mas não obrigam todos a usar os mesmos números. Deixe a sensibilidade da mira no valor confortável para você, mesmo se a câmera normal usar outro.

## 9. Dicas práticas

- Altere **uma opção por vez**. Isso mostra qual ajuste produziu a diferença.
- Para refinamento, use passos pequenos de 0.05 ou 0.1. Para comparação ampla, 1.0, 1.5 e 2.0 são referências claras.
- Avalie tanto a inclinação leve quanto a máxima. Uma zona morta pode parecer lentidão inicial sem ser uma baixa taxa máxima.
- Compare sem estar encostado em paredes: a colisão pode deslocar a câmera e mudar a sensação.
- O eixo vertical alcança um limite de inclinação; insistir contra o limite não indica que o ganho deixou de funcionar.
- Não ajuste o mouse ou o analógico esquerdo para compensar esta câmera. Os quatro campos documentados regulam os caminhos do controle modificados.
- Não aumente também os últimos multiplicadores X/Y dos CFGs. Mantenha-os em 1.0 para que a referência do INI faça sentido.
- Guarde uma cópia do INI que você gostou antes de começar outra comparação. Repor o pacote inteiro também pode repor o INI padrão e apagar sua personalização.
- Após reinstalar qualquer versão, compare se SGL e DLL são do mesmo pacote. O wrapper rejeita assinaturas incompatíveis.

## 10. Campos antigos e opções de compatibilidade

O INI mantém campos lidos pela DLL de entrada preservada. Eles não são novos controles de velocidade da câmera corrigida. Mantenha os valores recomendados:

```ini
RightStickXExponent=1.0
RightStickYExponent=1.0
RightStickXGain=1.0
RightStickYGain=1.0
```



**RightStickXExponent/RightStickYExponent=1.0:** deixam sem alteração adicional de expoente a entrada encaminhada pela DLL anterior. Mudá-los pode alterar a resposta do controle antes dos cálculos do mod.

**RightStickXGain/RightStickYGain=1.0:** evitam ganho adicional no estado de entrada do analógico. Esses campos são limitados pelo formato do eixo XInput e não substituem os quatro ajustes atuais. Não usá-los junto com o INI para tentar duplicar o mesmo ganho.



Os números de faixa explicados neste manual (0.25..3.0) referem-se às **quatro opções principais**, não aos campos antigos. Use as quatro opções principais para regular a câmera e a mira.

## 11. Relação com os CFGs e instalação

Os arquivos `Engine/binds_pc_mjs.cfg` e `Engine/bindcfgs_pc.cfg` continuam necessários para mapear os comandos. O mod não substitui o mapeamento de controle. Nesta instalação, os dois foram ajustados para estas linhas:

```text
setbind 1 COMMAND_CAMERA_X CONTROLLER 0 AXIS_RX -1.0 1.0 1.0
setbind 1 COMMAND_CAMERA_Y CONTROLLER 0 AXIS_RY -1.0 1.0 1.0
setbind 1 COMMAND_TURNLEFT DEVICE_INVALID 0 0
setbind 1 COMMAND_TURNRIGHT DEVICE_INVALID 0 0
```

Preserve os addbind de teclado e os demais comandos. O giro do corpo está coordenado com a câmera pelo mod; TURNLEFT/TURNRIGHT do analógico não devem somar outra rotação. Localize pelos nomes: linhas 184/185 podem variar. Não foi determinado qual CFG é usado em todas as opções do Unknown Project, por isso ambos foram mantidos consistentes.

Para instalar em uma cópia compatível:

1. Feche o jogo e guarde seus arquivos do Bin e ambos os CFGs.
2. Copie os **quatro arquivos** de `Files/Bin` para o Bin do jogo e confira as linhas acima nos CFGs.
3. Abra e teste. Personalize o INI instalado e reabra após cada alteração.

Os quatro arquivos são g_SilentHill.sgl, xinput1_3.dll, camera_input_base.dll e camera_axis_fix.ini. O SGL é o único binário existente do jogo modificado. A wrapper xinput1_3.dll e o INI foram criados; camera_input_base.dll encaminha a entrada XInput nativa e aplica os ajustes opcionais do analógico. Os CFGs são alterações de configuração separadas e não são arquivos de instalação do pacote.

## 12. Logs e problemas comuns

O mod pode criar Bin/camera_axis_fix.log. `Navigation speed: ...; applied` indica aplicação dos valores normais. `Precision speed: ...; post-curve scale=value/3; applied` identifica a nova escala da mira. `rejected` indica assinatura incompatível ou falha ao alterar a memória, não necessariamente erro de sintaxe do seu INI.

Se o valor não parecer mudar, confira se editou o INI do Bin correto, salvou, fechou/reabriu e usou ponto decimal. Confira se não há `.ini.txt` ou opções duplicadas. Se o ganho voltar inesperadamente ao padrão, reveja se o texto era numérico válido.

Se só o começo do movimento parecer lento, compare a zona morta e a inclinação parcial. Se parar perto do limite vertical, compare em outra posição. Se o log rejeitar a assinatura, não misture builds nem copie esse SGL para outro binário.

O fechamento antes do menu da tentativa anterior foi confirmado no dump como escrita em código protegido. A flag foi movida para dados graváveis da DLL, com teste nativo de proteção real, e o usuário confirmou que o jogo voltou a abrir. Isso não tem relação com seus créditos ou a tradução. Preserve logs e backups se aparecer uma falha nova.

## 13. Restaurar e preservar seus arquivos

Para retornar ao estado anterior, feche o jogo e use seu backup completo do SGL, CFGs e auxiliares próprios. O README informa os caminhos de backup desta instalação.

`Files/_Backup Original/Bin/g_SilentHill.sgl` é a cópia preexistente mais antiga desta instalação Unknown Project 3.20; não é certificação de SGL vanilla. Ele não restaura sozinho seus CFGs. Retire as DLLs/INI do mod somente se esses nomes não existiam antes; se já existiam, restaure seus arquivos próprios.

Não publique saves, logs pessoais, dumps ou o jogo completo junto com o mod. O conteúdo de instalação continua limitado aos quatro arquivos documentados em `Files/Bin`, com o backup em `Files/_Backup Original`, a documentação organizada e os créditos preservados. Repositório oficial no GitHub: https://github.com/Emertels/Silent-Hill-5-Camera-Fix.

## Créditos

**Emerson Teles — EMERSON TELES:** testes, identificação das diferenças de resposta, validação do acompanhamento e da mira, organização do pacote. Implementação e verificação local com assistência do Codex. Silent Hill: Homecoming e Unknown Project pertencem aos respectivos autores.

## Idiomas, créditos e opções do INI — 12/10/2026

Versão pública **1.0**. Créditos: **Mod by Emerson Teles — EMERSON TELES**. O INI instalado e o do pacote têm comentários em inglês; as chaves e os valores pessoais foram preservados. README-PT-BR.md e AGENTS.PT-BR.md estão em português; README-EN.md e AGENTS-EN.md estão em inglês.

- `HorizontalCameraSpeed`: câmera normal horizontal e giro do personagem; referência de 1.5 rad/s em 1.0.
- `VerticalCameraSpeed`: câmera normal vertical; novo 1.0 equivale ao antigo 2.0, conforme teste e escolha do usuário. Ganho efetivo 2.864788997846 vezes a opção. Não representa igualdade física comprovada entre X e Y.
- `AimHorizontalSpeed`: sensibilidade horizontal da mira Precision, aplicada após a curva original.
- `AimVerticalSpeed`: sensibilidade vertical independente da mira Precision, aplicada após a curva original. Na mira, 3.0 equivale à referência rápida anterior; 1.0 aplica um terço dela.
- `RightStickXExponent`: curva antiga da entrada horizontal; manter 1.0.
- `RightStickYExponent`: curva antiga da entrada vertical; manter 1.0.
- `RightStickXGain`: ganho antigo da entrada horizontal bruta; manter 1.0 para não somar ganho.
- `RightStickYGain`: ganho antigo da entrada vertical bruta; manter 1.0 para não somar ganho.

A faixa 0.25 a 3.0 refere-se às quatro opções principais. Use ponto: 1.2, 1.5, 2.5. Em relação a 1.0, 1.5 é +50%, 2.0 é +100% e 3.0 é +200% de ganho; limites e animações podem mudar a velocidade visual final. Texto inválido retorna a 1.0; valores usuais fora da faixa são limitados. Zero não desativa o mod. Reinicie o jogo após editar.

Os fontes estão em Source. São fontes do mod e dos geradores de patch, não o código-fonte do jogo. O guia de compilação distingue o wrapper recompilável dos scripts históricos que ainda exigem caminhos e binários locais. Não publicar Backup Original ou binários do jogo como código-fonte.
