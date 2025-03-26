# Solitaire

Um jogo de Solitaire desenvolvido com Python e Flet, oferecendo uma experiência interativa e funcionalidades adicionais para melhorar a jogabilidade.

## Objetivo do Jogo

O Solitaire (também conhecido como Paciência) é um jogo de cartas para um único jogador. O objetivo principal é organizar todas as cartas em quatro pilhas de fundação, uma para cada naipe (copas, ouros, paus e espadas), começando pelo Ás e terminando no Rei, em ordem crescente. O jogo é vencido quando todas as 52 cartas estiverem corretamente organizadas nas pilhas de fundação.

## Como Jogar

### Elementos do Jogo
- **Stock (Baralho)**: Pilha de cartas viradas para baixo no canto superior esquerdo.
- **Waste (Descarte)**: Área ao lado do stock onde as cartas viradas são colocadas.
- **Foundation (Fundação)**: Quatro espaços no topo direito onde as cartas são organizadas por naipe em ordem crescente (Ás a Rei).
- **Tableau (Tabuleiro)**: Sete colunas onde as cartas são organizadas em ordem decrescente e com cores alternadas.

### Regras Básicas
1. **Movimentos no Tableau**: 
   - As cartas devem ser organizadas em ordem decrescente (Rei a Ás) e com cores alternadas (vermelho sobre preto ou preto sobre vermelho).
   - Apenas Reis podem ser colocados em espaços vazios no tableau.
   - Grupos de cartas em sequência podem ser movidos juntos.

2. **Movimentos para a Fundação**:
   - Apenas Áses podem iniciar uma pilha de fundação.
   - As cartas devem ser do mesmo naipe e organizadas em ordem crescente (Ás a Rei).

3. **Utilização do Stock**:
   - Clique no stock para virar cartas para o waste.
   - As cartas no waste podem ser movidas para o tableau ou fundação, se permitido pelas regras.
   - Quando o stock estiver vazio, pode-se reciclar o waste para formar um novo stock (limitado pelo número de passagens permitidas).

### Controlos
- **Arrastar e Soltar**: Mova as cartas arrastando-as com o rato.
- **Clique Duplo**: Mova automaticamente uma carta para a fundação, se possível.

## Funcionalidades do Jogo

### Sistema de Loja (Shop)

A implementação de uma loja virtual no jogo Solitaire foi motivada pela necessidade de aumentar o envolvimento do jogador e proporcionar um sistema de recompensas que incentive a continuidade do jogo. Através da loja, os jogadores podem personalizar a sua experiência, adquirindo diferentes designs para o verso das cartas utilizando moedas ganhas durante o jogo.

#### Funcionamento Detalhado:
- **Economia do Jogo**: Os jogadores ganham 25 moedas por cada jogada bem-sucedida. Adicionalmente, perdem 30 moedas ao desfazer uma jogada (nunca ficando com saldo negativo).
- **Designs Disponíveis**: Existem quatro designs diferentes para o verso das cartas, cada um com um preço específico:
  - Design Padrão: Gratuito (disponível desde o início)
  - Design Básico: 500 moedas
  - Design Premium: 2000 moedas
  - Design Exclusivo: 9000 moedas
- **Persistência**: Os designs adquiridos e o saldo de moedas são guardados no armazenamento local do navegador, permanecendo disponíveis entre sessões de jogo.
- **Interface Adaptativa**: A loja ajusta-se automaticamente a diferentes tamanhos de ecrã, proporcionando uma experiência otimizada tanto em dispositivos móveis como em computadores.

Para aceder à loja, clique no ícone de carrinho de compras na barra superior do jogo. Na loja, os designs já adquiridos mostram a indicação "Owned", enquanto os ainda não desbloqueados mostram o seu preço em moedas. Para adquirir um design, basta clicar nele (se tiver moedas suficientes). Para seleccionar um design já adquirido, clique nele e será imediatamente aplicado ao jogo.

### Sistema de Dicas (Tip)

O sistema de dicas foi implementado para auxiliar jogadores que possam estar com dificuldades em identificar o próximo movimento possível. Esta funcionalidade é particularmente útil para jogadores iniciantes ou em situações onde o jogo parece não ter solução aparente.

#### Algoritmo de Prioridade:
O sistema analisa o estado actual do jogo e sugere movimentos seguindo uma ordem específica de prioridade:

1. **Mover um Ás para uma fundação vazia**: Esta é a prioridade máxima, pois inicia uma nova pilha de fundação.
2. **Mover uma carta do tableau para uma fundação**: Ajuda a progredir directamente para o objectivo do jogo.
3. **Mover uma carta entre colunas do tableau**: Reorganiza o tableau para revelar mais cartas ou criar sequências mais longas.
4. **Mover uma carta do waste para uma fundação**: Utiliza cartas do waste para progredir nas fundações.
5. **Mover uma carta do waste para o tableau**: Liberta cartas do waste, potencialmente revelando novas opções.
6. **Mover um Rei para um espaço vazio no tableau**: Cria novas sequências no tableau.
7. **Virar uma carta do stock**: Quando nenhum outro movimento é possível, sugere virar mais cartas.

#### Implementação Visual:
Quando uma dica é solicitada, o jogo destaca com uma borda amarela tanto a carta que pode ser movida quanto o seu destino. Este destaque visual permanece por alguns segundos, dando tempo suficiente ao jogador para compreender o movimento sugerido sem interferir excessivamente na jogabilidade.

Para solicitar uma dica, clique no ícone de lâmpada na barra superior do jogo. Note que o uso de dicas não penaliza o jogador nem afecta a pontuação ou o saldo de moedas.

### Funcionalidades Adicionais

- **Guardar e Carregar Jogo**: O estado completo do jogo pode ser guardado e posteriormente recuperado, permitindo continuar uma partida em qualquer momento.
- **Desfazer Jogada**: Permite reverter a última jogada realizada, útil para corrigir erros ou experimentar diferentes estratégias. Esta acção custa 30 moedas.
- **Limite de Passagens pelo Baralho**: O jogo limita o número de vezes que o waste pode ser reciclado para formar um novo stock, aumentando o desafio.
- **Detecção Automática de Vitória**: O jogo reconhece automaticamente quando todas as cartas foram correctamente organizadas nas fundações, apresentando uma mensagem de vitória.

## Controlos na Interface

- **Novo Jogo** (Botão "New game"): Inicia uma nova partida, reiniciando todas as cartas.
- **Guardar** (Botão "Save"): Guarda o estado actual do jogo no armazenamento local.
- **Carregar** (Botão "Load"): Recupera um jogo previamente guardado.
- **Dica** (Ícone de lâmpada): Destaca um movimento possível seguindo o algoritmo de prioridade.
- **Loja** (Ícone de carrinho): Acede à loja para comprar novos designs de cartas.
- **Desfazer** (Ícone de seta de retorno): Reverte a última jogada realizada (custa 30 moedas).

## Dicas Estratégicas

1. Tente sempre revelar cartas viradas para baixo no tableau o mais rápido possível.
2. Liberte os Reis cedo para poder criar novas sequências nos espaços vazios.
3. Pense várias jogadas à frente antes de mover cartas para as fundações.
4. Utilize o sistema de dicas quando estiver bloqueado, mas tente não depender excessivamente dele para desenvolver as suas habilidades.
5. Gerencie as suas moedas estrategicamente, decidindo entre gastar em designs de cartas ou guardar para poder desfazer jogadas.

---
