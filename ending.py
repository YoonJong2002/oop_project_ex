import pygame
import pickle
import opening
import class_of_text_and_image


def insert_player_in_list(player):
    """
        게임이 종료되었을 때, list_of_players 의 적절한 위치에 플레이어를 삽입함
        :param player: 이번에 플레이한 플레이어 객체
        :return: player 을 삽입한 상태의 list_of_players
    """
    f = open('ranking', 'rb')
    list_of_players = pickle.load(f)
    f.close()
    list_of_players.append(player)
    list_of_players = sorted(list_of_players, key=lambda x: (x.collected_money, x.life_left, -x.time_spent))
    for i in list_of_players:
        if i == player:
            rank_index = list_of_players.index(player)
    f = open('ranking', 'wb')
    pickle.dump(list_of_players[:10], f)
    f.close()
    return list_of_players, rank_index+1


def show_ranking(screen, list_of_players, my_rank):
    """
        정렬된 list of players 를 화면에 보여줌
        :param screen: 출력에 사용할 스크린
        :param list_of_players: 이때까지 플레이한 플레이어 객체들의 리스트
        :return: 없음
    """
    text_my_rank = class_of_text_and_image.Text('bold', 35, '하늘에서 동전이 떨어진다', 350, 50)
    if my_rank >10:
        pass
    else:
        pass
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                return
        text_my_rank.screen_text_show(screen)


def play_again(screen):
    """
        사용자가 게임을 더 플레이할 것인지 물어봄
        :param screen: 출력에 사용할 스크린
        :return: 더 플레이한다면 True, 플레이하지 않는다면 False를 반환
    """
    text_ask = class_of_text_and_image.Text('original', 20, '다시 플레이하시겠습니까? (y or n)', 350, 250)

    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                return event.unicode.lower().startswith('y')
        screen.fill((255, 255, 255))
        text_ask.screen_text_show(screen)
        pygame.display.update()


if __name__ == '__main__':
    screen = opening.set_screen()
    play_again(screen)
