# Camera Fix 1.0 — Código-fonte

**Mod by Emerson Teles — EMERSON TELES**. Inclui fontes reais das DLLs do mod, cabeçalhos atuais de assinatura e calibração, geradores históricos do patch SGL e testes. Não é o código-fonte do jogo.

Para recompilar o wrapper no Windows, use GCC com geração x86, dlltool e as.  Execute desta pasta:

```powershell
.\work\build_wrapper.ps1 -CompilerDirectory 'C:\caminho\gcc\bin'
```

O script usa os cabeçalhos atuais, gera build_test/xinput1_3_configurable.dll e build_test/camera_input_base.dll e executa os dois testes nativos x86. O fonte principal da entrada é src/camera_input_base.c. O nome usado na instalação é xinput1_3.dll. Preserve camera_input_base.dll. O fonte C++ do proxy também está incluído; sua recompilação exige ferramenta Windows x86 e a definição de exportação. Teste binários recompilados antes de substituir a versão funcional.

Os scripts Python preservam os caminhos e dependências do desenvolvimento. **Não são um gerador portátil de SGL em um clique.** Instale requirements.txt, revise SOURCE/OUTPUT e forneça os backups e imagens intermediárias compatíveis antes de executar. Não rode scripts históricos diretamente no jogo instalado. Para compilar o wrapper atual, não é necessário executar esses geradores. Não publique binários originais ou backups do jogo no GitHub.
