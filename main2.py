import random

# Definindo cartas e suas forças no truco paulista
cartas = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
naipes = ['Copas', 'Espadas', 'Ouros', 'Paus']

# Função para determinar a carta seguinte (manilha)
def carta_seguinte(carta):
    index = cartas.index(carta)
    return cartas[(index + 1) % len(cartas)]

# Criar e embaralhar o baralho
def criar_baralho():
    baralho = [(carta, naipe) for carta in cartas for naipe in naipes]
    random.shuffle(baralho)
    return baralho

# Distribuir as cartas e definir a manilha
def distribuir_cartas(baralho):
    vira = baralho.pop(0)
    manilha = carta_seguinte(vira[0])
    return [baralho[:3], baralho[3:6]], vira, manilha

# Determinar o vencedor da rodada
def determinar_vencedor(carta1, carta2, manilha):
    forca_cartas = {carta: index for index, carta in enumerate(cartas)}
    forca_cartas[manilha] = len(cartas)  # Manilha tem a força máxima

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

# Exibir as cartas de um jogador
def exibir_mao(mao):
    for index, carta in enumerate(mao):
        print(f"{index + 1}: {carta[0]} de {carta[1]}")

# Escolher uma carta da mão
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

# Adversário escolhe uma carta automaticamente
def escolher_carta_automatica(mao):
    return mao.pop(0)

# Adversário decide se aceita o truco
def adversario_aceita_truco(valor_aposta):
    if valor_aposta >= 9:
        return random.choice([True, False])
    else:
        return random.choice([True, True, False])

# Jogar uma partida (uma série de 3 rodadas)
def jogar_partida(primeiro_jogador):
    baralho = criar_baralho()
    (mao_jogador1, mao_jogador2), vira, manilha = distribuir_cartas(baralho)
    pontos_rodada_jogador1 = pontos_rodada_jogador2 = 0
    valor_rodada = 1
    jogador_atual = primeiro_jogador

    print(f"A vira é: {vira[0]} de {vira[1]}")
    print(f"A manilha é: {manilha}")

    for rodada in range(3):
        print(f"\nRodada {rodada + 1}:")

        if rodada > 0:
            pedir_truco = input("Você quer pedir truco? (s/n): ").strip().lower()
            if pedir_truco == 's':
                valor_rodada = aumentar_aposta(valor_rodada)

        if jogador_atual == 1:
            print("\nMão do Jogador 1:")
            exibir_mao(mao_jogador1)
            carta_jogador1 = escolher_carta(mao_jogador1)
            carta_jogador2 = escolher_carta_automatica(mao_jogador2)
        else:
            carta_jogador2 = escolher_carta_automatica(mao_jogador2)
            print(f"O adversário jogou: {carta_jogador2[0]} de {carta_jogador2[1]}")
            print("\nSua mão:")
            exibir_mao(mao_jogador1)
            carta_jogador1 = escolher_carta(mao_jogador1)

        print(f"\nJogador 1 joga: {carta_jogador1}")
        print(f"Jogador 2 joga: {carta_jogador2}")

        vencedor = determinar_vencedor(carta_jogador1, carta_jogador2, manilha)
        if vencedor == 1:
            pontos_rodada_jogador1 += 1
            print("Jogador 1 vence a rodada")
            jogador_atual = 1
        elif vencedor == 2:
            pontos_rodada_jogador2 += 1
            print("Jogador 2 vence a rodada")
            jogador_atual = 2
        else:
            print("Empate na rodada")
            # No caso de empate, o jogador que começou a rodada continua na próxima rodada

        if pontos_rodada_jogador1 == 2 or pontos_rodada_jogador2 == 2:
            break

    if pontos_rodada_jogador1 > pontos_rodada_jogador2:
        return valor_rodada, 1
    elif pontos_rodada_jogador2 > pontos_rodada_jogador1:
        return -valor_rodada, 2
    else:
        return 0, jogador_atual

# Aumentar a aposta
def aumentar_aposta(valor_rodada):
    for valor in [3, 6, 9, 12]:
        if valor_rodada == valor // 3:
            if adversario_aceita_truco(valor):
                print(f"O adversário aceitou! Vale {valor} pontos.")
                return valor
            else:
                print(f"O adversário recusou! Você ganha a mão com {valor_rodada} pontos.")
                return valor_rodada
    return valor

# Função principal do jogo
def jogar_truco():
    pontos_jogador1 = pontos_jogador2 = 0
    primeiro_jogador = random.choice([1, 2])

    while pontos_jogador1 < 12 and pontos_jogador2 < 12:
        print(f"\nPrimeiro jogador a jogar nesta partida: Jogador {primeiro_jogador}")
        resultado_partida, primeiro_jogador = jogar_partida(primeiro_jogador)
        if resultado_partida > 0:
            pontos_jogador1 += resultado_partida
            print("Jogador 1 ganha a partida!")
        elif resultado_partida < 0:
            pontos_jogador2 -= resultado_partida
            print("Jogador 2 ganha a partida!")
        print(f"Placar atual: Jogador 1: {pontos_jogador1} x Jogador 2: {pontos_jogador2}")

    print("Fim do jogo! Jogador 1 vence!" if pontos_jogador1 >= 12 else "Fim do jogo! Jogador 2 vence!")

# Iniciar o jogo
jogar_truco()
