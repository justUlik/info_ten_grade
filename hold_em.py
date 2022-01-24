from operator import itemgetter
from itertools import combinations
from collections import Counter

SUITS = ['S', 'H', 'D', 'C']
NUMBERS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
ALL_CARDS = []


def _get_straight(cards):
    numbers = list({card[0] for card in cards})
    numbers.reverse()
    len_straight, begin = 1, numbers[0]
    for number_ind in range(1, len(numbers)):
        if numbers[number_ind - 1] - numbers[number_ind] == 1:
            len_straight += 1
        else:
            len_straight = 1
            begin = numbers[number_ind]
        if len_straight == 5:
            return begin
    irregular_straight = set([14, 2, 3, 4, 5])
    for card in irregular_straight:
        if card not in numbers:
            return None
    return 5


def _get_flush(cards):
    suits_count = {}
    numbers = []
    for card in cards:
        if card[1] not in suits_count.keys():
            suits_count[card[1]] = 1
        else:
            suits_count[card[1]] += 1
    suit = ''
    for key, val in list(suits_count.items()):
        if val >= 5:
            suit = key
    if suit == '':
        return None
    cards = sorted(cards, key=lambda x: x[0], reverse=True)
    for card in cards:
        if card[1] == suit:
            numbers.append(card[0])
        if len(numbers) == 5:
            return sorted(numbers, reverse=True), suit
    return None


def _get_straight_flush(cards):
    is_got_straight = _get_straight(cards)
    is_got_flush = _get_flush(cards)

    if is_got_flush is None or is_got_straight is None:
        return None

    cards = sorted([cards[0] for cards in cards if cards[1] == is_got_flush[1]], reverse=True)
    len_straight, begin = 1, cards[0]
    for number_ind in range(1, len(cards)):
        if cards[number_ind - 1] - cards[number_ind] == 1:
            len_straight += 1
        else:
            len_straight = 1
            begin = cards[number_ind]
        if len_straight == 5:
            return begin
    irregular_straight = set([14, 2, 3, 4, 5])
    for card in irregular_straight:
        if card not in cards:
            return None
    return 5


def _get_kare(cards):
    count = list(Counter([i[0] for i in cards]).items())
    count = sorted(count, key=lambda x: (x[1], x[0]), reverse=True)
    if count[0][1] == 4:
        return [count[0][0]]
    return None


def _get_full_house(cards):
    count = list(Counter([i[0] for i in cards]).items())
    count = sorted(count, key=lambda x: (x[1], x[0]), reverse=True)
    if count[0][1] >= 3 and count[1][1] >= 2:
        return [count[0][0], count[1][0]]
    return None



def _get_three(cards):
    count = list(Counter([i[0] for i in cards]).items())
    count = sorted(count, key=lambda x: (x[1], x[0]), reverse=True)
    if count[0][1] == 3:
        return [count[0][0]]
    return None


def _get_two(cards):
    count = list(Counter([i[0] for i in cards]).items())
    count = sorted(count, key=lambda x: (x[1], x[0]), reverse=True)
    if count[0][1] == 2 and count[1][1] == 2:
        return [count[0][0], count[1][0]]
    return None


def _get_one(cards):
    count = list(Counter([i[0] for i in cards]).items())
    count = sorted(count, key=lambda x: (x[1], x[0]), reverse=True)
    if count[0][1] == 2:
        return [count[0][0]]
    return None


def _get_rank_combinations(player_cards, known_community_cards):
    all_cards = list(player_cards) + known_community_cards
    return_value = _get_straight_flush(all_cards)

    if return_value is not None:
        if return_value == 14:
            return 0, []
        else:
            return 1, return_value

    return_value = _get_kare(all_cards)
    if return_value is not None:
        rank_max_card = 0
        for card in all_cards:
            if card[0] > rank_max_card and card[0] != return_value[0]:
                rank_max_card = card[0]
        to_return = [return_value[0], rank_max_card]
        return 2, to_return


    return_value = _get_full_house(all_cards)
    if return_value is not None:
        return 3, [return_value[0], return_value[1]]

    return_value = _get_flush(all_cards)
    if return_value is not None:
        return 4, return_value[0]

    return_value = _get_straight(all_cards)
    if return_value is not None:
        return 5, return_value

    return_value = _get_three(all_cards)
    if return_value is not None:
        rank_max_card_1 = 0
        rank_max_card_2 = 0
        for card in all_cards:
            if card[0] != return_value[0] and card[0] > rank_max_card_1:
                rank_max_card_2, rank_max_card_1 = rank_max_card_1, card[0]
            elif card[0] != return_value[0] and card[0] > rank_max_card_2:
                rank_max_card_2 = card[0]
        return 6, return_value + [rank_max_card_1, rank_max_card_2]

    return_value = _get_two(all_cards)
    if return_value is not None:
        rank_max_card = 0
        for card in all_cards:
            if card[0] != return_value[0] and card[0] != return_value[1] and card[0] > rank_max_card:
                rank_max_card = card[0]
        to_return = return_value + [rank_max_card]
        return 7, to_return

    return_value = _get_one(all_cards)
    if return_value is not None:
        uni_сards = list({i[0] for i in all_cards})
        uni_сards.remove(return_value[0])
        uni_сards.reverse()
        return 8, return_value + uni_сards[:3]

    return 9, sorted([card[0] for card in all_cards], reverse=True)[:5]


def get_players_card_ranks(players_hands, known_community_cards):
    answer = []
    for player in players_hands:
        answer.append(_get_rank_combinations(player, known_community_cards))
    return answer


def get_winner(players_hands, known_community_cards):
    players_cards_ranks = get_players_card_ranks(players_hands, known_community_cards)
    players_cards_ranks_srt = sorted(players_cards_ranks, key=lambda x: x[0])
    got_the_max = []
    for player_hands in players_cards_ranks_srt:
        if player_hands[0] == players_cards_ranks_srt[0][0]:
            got_the_max.append(player_hands)
    if len(got_the_max) == 1:
        return [players_cards_ranks.index(got_the_max[0])]
    else:
        draw = []
        winner_position = max(got_the_max)
        for i in range(len(players_cards_ranks)):
            if players_cards_ranks[i] == winner_position:
                draw.append(i)
        return draw


def get_all_availlble_cards(players_hands, known_community_cards,
                            already_dropped_cards):
    global ALL_CARDS
    global SUITS
    global NUMBERS
    for suit in SUITS:
        for number in NUMBERS:
            ALL_CARDS.append(tuple([number, suit]))

    now_used_cards = []
    for player in players_hands:
        now_used_cards.append(player[0])
        now_used_cards.append(player[1])

    for card in known_community_cards:
        now_used_cards.append(card)

    if already_dropped_cards is not None:
        for card in already_dropped_cards:
            now_used_cards.append(card)
    return list(set(ALL_CARDS) - set(now_used_cards))

def convert_card(card):
    num = int(card[:-1].replace('A', '14').replace('K', '13').replace('Q', '12').replace('J', '11'))
    suit = card[-1]
    return tuple([num, suit])


def count_win_probabilities(
    players_private_cards,
    known_community_cards,
    already_dropped_cards=None):

    for i in range(len(players_private_cards)):
        players_private_cards[i] = [convert_card(players_private_cards[i][0]),
                                    convert_card(players_private_cards[i][1])]

    for i in range(len(known_community_cards)):
        known_community_cards[i] = convert_card(known_community_cards[i])

    if already_dropped_cards is not None:
        for i in range(len(already_dropped_cards)):
            already_dropped_cards[i] = convert_card(already_dropped_cards[i])
    availlble_cards = get_all_availlble_cards(players_private_cards,
                                              known_community_cards,
                                              already_dropped_cards)

    won_by_player = [0 for i in range(len(players_private_cards))]
    all_ = 0

    for comb in combinations(availlble_cards, 5 - len(known_community_cards)):
        now_known_community_cards = known_community_cards + list(comb)
        won_now = get_winner(players_private_cards, now_known_community_cards)
        if len(won_now) == 1:
            all_ += 1
            won_by_player[won_now[0]] += 1
        else:
            for person in won_now:
                all_ += 1 / len(won_now)
                won_by_player[person] += 1 / len(won_now)
    return [round(person / all_, 4) for person in won_by_player]
