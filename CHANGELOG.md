# Changelog — Camera Fix

## 1.0 — 12/10/2026

- Giro horizontal responsivo com a câmera acompanhando a direção real do personagem; comportamento horizontal aprovado pelo usuário.
- Resposta vertical linear no caminho do controle, em lugar da entrada ao quadrado; referência angular pareada ao horizontal por fator calculado a partir das constantes do SGL original.
- Quatro opções no INI: câmera normal X/Y e mira X/Y, faixa 0.25..3.0, com padrão 1.0.
- Escala da mira aplicada depois da curva nativa: 3.0 corresponde à referência rápida anterior, 2.0 a dois terços e 1.0 a um terço no ponto de aplicação.
- Preservação dos limites nativos, encaminhamento do controle, conferência de assinatura e logs.
- Pacote manual com quatro arquivos, backup original, README, MANUAL, AGENTS e manifesto SHA256.
- Cópia completa da versão anterior antes de instalar; créditos de Emerson Teles preservados.

Compilação e testes locais passaram. A resposta vertical e a escala de mira desta atualização ainda aguardam confirmação em gameplay. A versão 1.0 identifica o pacote organizado para futura publicação; não implica validação de todos os estados do jogo.

### Correção de memória antes da publicação

- Corrigida escrita indevida da flag PrecisionMode na seção protegida do SGL, confirmada no dump.
- Estado movido para dados graváveis da DLL; ponteiro nulo tratado nos hooks.
- Acrescentado teste nativo com páginas READ/EXECUTE reais.
- Refinamentos vertical/mira reinstalados com os mesmos cálculos; INI e binds pessoais preservados.
- O usuário confirmou abertura, acompanhamento e boa resposta da mira; teste com todos em2.0 aprovado nesta instalação.

### Documentação e retorno dos testes — 12/10/2026

- Confirmadas pelo usuário a abertura após a correção, a câmera atrás do personagem e a mira em1.0/2.0; todos os modos em2.0 agradaram.
- Manual completo de opções, faixa decimal0.25..3.0, percentuais, referência atual/antiga da mira, campos legados, instalação, logs, dicas e restauração.
- Vertical em1.0 ainda com pequena diferença percebida; teste pessoal em1.1/1.2 pendente. Sem mudança de INI, binário, bind ou cálculo nesta atualização documental.
- Versão pública mantida em1.0, créditos EMERSON TELES preservados.

### Normalização vertical pelo retorno do usuário — 12/10/2026

- Novo Y1.0 corresponde ao antigo Y2.0; referência interna vertical multiplicada por2, por escolha empírica do usuário.
- Preservados cálculo horizontal, mira, acompanhamento, SGL e binds. Apenas DLL de configuração, referência Y do INI e documentação atualizados.
- Faixa continua0.25..3.0; Y2.0/Y3.0 agora solicitam mais velocidade que antes. Testar primeiroY1.0.
- Mantida versão pública1.0. Backup e testes de normalização/proteção registrados.
