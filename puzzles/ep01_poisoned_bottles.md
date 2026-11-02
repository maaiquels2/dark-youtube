# Ep01 — The poisoned bottles (piloto, 9:16, EN)

Formato: enigma + narração + legenda palavra por palavra + simulação em código.
Paleta: papel milimetrado (fundo creme #f4ecd8, traço #1c1c1c, destaque vermelho #d62828, "aceso" laranja #e07a00, ok verde #2a9d5c).
Duração alvo: ~1:45 (~310 palavras, ritmo ~3 palavras/s). Revelação por volta de 0:55.

Matemática (conferida): 2^10 = 1.024 >= 1.000, então 10 testadores bastam.
Exemplo: 618 = 512+64+32+8+2 = 1001101010; dígitos 1 nas posições 1, 4, 5, 7 e 9 (da esquerda).

| Tempo | Narração | Visual |
|---|---|---|
| 0:00-0:09 | One of these 1,000 bottles is poisoned. You have one hour to find it. How many testers do you need? The answer is smaller than you think. | Grade de 1.000 pontos aparece; um fica vermelho. Título fixo no topo. Contador "TESTERS ?" |
| 0:09-0:22 | Here are the rules. The poison kills in exactly one hour. You get one round of testing, and each tester can drink from as many bottles as you like. Whoever drinks the poisoned one dies at the hour mark. | Regras entram uma a uma, cada uma com ícone simples. Relógio de 1 h. |
| 0:22-0:40 | The obvious plan is one tester per bottle. That's 1,000 testers. Too many. With a single tester, you can only split the bottles in two: the ones he drinks, and the ones he doesn't. If he dies, the poison is in the first half. If he lives, it's in the second. | 1 testador; a grade se divide em duas metades, uma acende. Ele "morre" ou "vive" e a outra metade apaga. |
| 0:40-0:57 | Add a second tester and you get four groups. Three testers, eight groups. Every new tester doubles the groups. So ten testers? Two to the tenth. 1,024 groups. That's more than 1,000 bottles. Ten testers are enough. | Contador em escada: 2, 4, 8 ... 1.024. Grade em 1, 2, 4, 8 blocos. Contador "TESTERS 10". |
| 0:57-1:22 | Here's how. Give every bottle a number in binary, ten digits long. Bottle 618 is one-zero-zero-one-one-zero-one-zero-one-zero. Tester one drinks every bottle whose first digit is a one. Tester two drinks every bottle whose second digit is a one. And so on, ten testers, ten digits. After an hour, look at who died. Dead is a one. Alive is a zero. | Cada testador, na sua vez, acende em laranja as garrafas com aquele dígito igual a 1 (como no esboço). Depois, mortos viram "x" vermelho e vivos "ok" verde. |
| 1:22-1:30 | Say testers one, four, five, seven and nine die. That spells one-zero-zero-one-one-zero-one-zero-one-zero. Convert it, and the poisoned bottle is number 618. | Dígitos 1001101010 aparecem sob os testadores; "= 618"; a garrafa 618 cresce e pulsa (maior que no esboço). |
| 1:30-1:45 | Every tester is one yes-or-no question, and ten yes-or-no questions are enough to pick one thing out of a thousand. So next time you need to find something fast, don't search one by one. Ask questions that cut the problem in half. | Testadores viram 10 interrogações; grade encolhe até 1 ponto. Tela final: nome da série + "Next: ..." |

## Notas de produção
- Voz: Brian (ElevenLabs, 0.86) ou outra a decidir; legenda palavra por palavra, palavra-chave em vermelho.
- Música: bem baixa, sem faixa cômica.
- No esboço a garrafa 618 ficou pequena no estado RESULT; no vídeo final, círculo de destaque maior.
- Pendente: nome do canal/série, idioma confirmado, plataformas confirmadas.
