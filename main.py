import random

# Definindo as cartas e suas forças no truco paulista
cartas = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
naipes = ['Copas', 'Espadas', 'Ouros', 'Paus']

# Função para determinar a carta seguinte (manilha)
def carta_seguinte(carta):
    index = cartas.index(carta)
    return cartas[(index + 1) % len(cartas)]

# Função para criar e embaralhar o baralho
def criar_baralho():
    baralho = [(carta, naipe) for carta in cartas for naipe in naipes]
    random.shuffle(baralho)
    return baralho

# Função para distribuir as cartas para dois jogadores e definir a manilha
def distribuir_cartas(baralho):
    vira = baralho.pop(0)
    manilha = carta_seguinte(vira[0])
    return [baralho[:3], baralho[3:6]], vira, manilha

# Função para determinar o vencedor da rodada
def determinar_vencedor(carta1, carta2, manilha):
    forca_cartas = {carta: index for index, carta in enumerate(cartas)}
    forca_cartas[manilha] = len(cartas)

    if carta1[0] == manilha and carta2[0] != manilha:
        return 1
    elif carta2[0] == manilha and carta1[0] != manilha:
        return 2
    elif forca_cartas[carta1[0]] > forca_cartas[carta2[0]]:
        return 1
    elif forca_cartas[carta1[0]] < forca_cartas[carta2[0]]:
        return 2
    else:
        return 0

# Função para exibir as cartas de um jogador
def exibir_mao(mao):
    for index, carta in enumerate(mao):
        print(f"{index + 1}: {carta[0]} de {carta[1]}")

# Função para escolher uma carta da mão
def escolher_carta(mao):
    while True:
        try:
            escolha = int(input("Escolha uma carta (1-3): ")) - 1
            if 0 <= escolha < len(mao):
                return mao.pop(escolha)
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Tente novamente.")

# Função para o jogador 2 escolher uma carta automaticamente
def escolher_carta_automatica(mao):
    return mao.pop(0)

# Função para o adversário decidir se aceita o truco
def adversario_aceita_truco(aposta_atual):
    return random.choice([True, False])

# Função para jogar uma partida (uma série de 3 rodadas)
def jogar_partida():
    baralho = criar_baralho()
    (mao_jogador1, mao_jogador2), vira, manilha = distribuir_cartas(baralho)

    pontos_rodada_jogador1 = 0
    pontos_rodada_jogador2 = 0
    valor_rodada = 1

    print(f"A vira é: {vira[0]} de {vira[1]}")
    print(f"A manilha é: {manilha}")

    for rodada in range(3):
        print(f"\nRodada {rodada + 1}:")

        if rodada > 0:  # Truco pode ser pedido a partir da segunda rodada
            pedir_truco = input("Você quer pedir truco? (s/n): ").strip().lower()
            if pedir_truco == 's':
                print("Você pediu truco!")
                if adversario_aceita_truco(valor_rodada):
                    valor_rodada = 3
                    print(f"O adversário aceitou o truco! Esta mão agora vale {valor_rodada} pontos.")
                    pedir_seis = input("Você quer pedir seis? (s/n): ").strip().lower()
                    if pedir_seis == 's':
                        print("Você pediu seis!")
                        if adversario_aceita_truco(valor_rodada):
                            valor_rodada = 6
                            print(f"O adversário aceitou seis! Esta mão agora vale {valor_rodada} pontos.")
                            pedir_nove = input("Você quer pedir nove? (s/n): ").strip().lower()
                            if pedir_nove == 's':
                                print("Você pediu nove!")
                                if adversario_aceita_truco(valor_rodada):
                                    valor_rodada = 9
                                    print(f"O adversário aceitou nove! Esta mão agora vale {valor_rodada} pontos.")
                                    pedir_doze = input("Você quer pedir doze? (s/n): ").strip().lower()
                                    if pedir_doze == 's':
                                        print("Você pediu doze!")
                                        if adversario_aceita_truco(valor_rodada):
                                            valor_rodada = 12
                                            print(f"O adversário aceitou doze! Esta mão agora vale {valor_rodada} pontos.")
                                        else:
                                            print(f"O adversário recusou doze! Você ganha a mão com {valor_rodada} pontos.")
                                            return valor_rodada
                                    else:
                                        print(f"Você não pediu doze. Esta mão vale {valor_rodada} pontos.")
                                else:
                                    print(f"O adversário recusou nove! Você ganha a mão com {valor_rodada} pontos.")
                                    return valor_rodada
                        else:
                            print(f"O adversário recusou seis! Você ganha a mão com {valor_rodada} pontos.")
                            return valor_rodada
                else:
                    print(f"O adversário recusou o truco! Você ganha a mão com {valor_rodada} pontos.")
                    return valor_rodada

        print("\nMão do Jogador 1:")
        exibir_mao(mao_jogador1)
        carta_jogador1 = escolher_carta(mao_jogador1)

        carta_jogador2 = escolher_carta_automatica(mao_jogador2)

        print(f"\nJogador 1 joga: {carta_jogador1}")
        print(f"Jogador 2 joga: {carta_jogador2}")

        vencedor = determinar_vencedor(carta_jogador1, carta_jogador2, manilha)
        if vencedor == 1:
            print("Jogador 1 vence a rodada")
            pontos_rodada_jogador1 += 1
        elif vencedor == 2:
            print("Jogador 2 vence a rodada")
            pontos_rodada_jogador2 += 1
        else:
            print("Empate na rodada")

        if pontos_rodada_jogador1 == 2 or pontos_rodada_jogador2 == 2:
            break

    if pontos_rodada_jogador1 > pontos_rodada_jogador2:
        return valor_rodada  # Jogador 1 ganha a partida
    elif pontos_rodada_jogador2 > pontos_rodada_jogador1:
        return -valor_rodada  # Jogador 2 ganha a partida
    else:
        return 0

# Função principal do jogo
def jogar_truco():
    pontos_jogador1 = 0
    pontos_jogador2 = 0

    while pontos_jogador1 < 12 and pontos_jogador2 < 12:
        resultado_partida = jogar_partida()
        if resultado_partida > 0:
            pontos_jogador1 += resultado_partida
            print("Jogador 1 ganha a partida!")
        elif resultado_partida < 0:
            pontos_jogador2 -= resultado_partida
            print("Jogador 2 ganha a partida!")
        else:
            print("A partida terminou empatada!")

        print(f"\nPontuação Atual:")
        print(f"Jogador 1: {pontos_jogador1} pontos")
        print(f"Jogador 2: {pontos_jogador2} pontos")

    if pontos_jogador1 >= 12:
        print("Jogador 1 vence o jogo!")
    elif pontos_jogador2 >= 12:
        print("Jogador 2 vence o jogo!")

# Executar o jogo
jogar_truco()
