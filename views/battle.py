from models import data, party_and_monster

# *******************バトルフィールドの表示*******************
def show_battle_field(party,monster):
    print('バトルフィールド')
    party_and_monster.print_monster_name(monster)
    print(f'HP = {monster['hp']} / {monster['max_hp']}')
    print('------------------------')
    for positions in data.ELEMENT_POSITIONS:
        print(f'{positions}',end=' ')
    print('')
    print_gems(data.gems_slot)
    print('')
    print('------------------------')

# *******************コマンドの入力内容チェック*******************
def check_valid_command(command):
    if len(command) != 2:
        return False
    if not ('A' <= command[0] <= 'N' and 'A' <= command[1] <= 'N'):
        return False
    if command[0] == command[1]:
        return False
    else:
        return True
# *******************宝石スロットにランダムに宝石を発生させる******************
def fill_gems():
    import random
    random_num = random.randint(1, 5)
    # print(f'{data.ELEMENT_NUMBERS[random_num]}',end=' ')
    return data.ELEMENT_NUMBERS[random_num]

# *******************宝石スロット(14個分)の表示*******************
def print_gems(gems_list):
    for gem in gems_list:
    # 記号から属性を逆引き
        element = None
        for key, value in data.ELEMENT_SYMBOLS.items():
            if value == gem:
                element = key
                break
        # 属性が見つかった場合、色コードで表示
        if element and element in data.ELEMENT_COLORS:
            color = data.ELEMENT_COLORS[element]
            print(f'\033[3{color}m{gem}\033[0m', end=' ')
        else:
            print(gem, end=' ')

# *******************gemsの移動とプリント*******************
def move_gem(command):
    # ユーザーが入力したコマンドを分解
    pos1 = command[0]
    pos2 = command[1]
    # 文字を数字（インデックス）に変換する
    # リストは0から始まるから、1を引く
    index1 = data.ELEMENT_POSITIONS[pos1] - 1
    index2 = data.ELEMENT_POSITIONS[pos2] - 1

    # 宝石を入れ替える関数を呼び出す
    swap_gem(index1, index2)
# *******************gemsの隣との入れ替え*******************
def swap_gem(index1, index2):
    data.gems_slot[index1], data.gems_slot[index2] = data.gems_slot[index2], data.gems_slot[index1]
# *******************プレイヤーターン*******************
def on_player_turn(party,monster):
    if not data.gems_slot:
        for _ in range(14):
            data.gems_slot.append(fill_gems())

    print(f'【{party['player_name']}】のターン (HP = {party['hp']})')
    show_battle_field(party, monster)
    valid_command = False
    while not valid_command:
        command = input('コマンド? > ')
        valid_command = check_valid_command(command)
        if valid_command:
            move_gem(command)
            # 動かした後のフィールドを再表示
            print('------------------------')
            for positions in data.ELEMENT_POSITIONS:
                print(f'{positions}',end=' ')
            print('')
            print_gems(data.gems_slot)
            print('')
            print('------------------------')

    damage = 50
    # (3) 敵モンスターのHPからダメージ分の値を減らす。
    print(f'{damage}のダメージを与えた')
    monster['hp'] -= damage
    print('')
# *******************敵のターン*******************
def on_enemy_turn(party,monster):
    # (1) 「【〇〇〇のターン】(HP = XXX)を表示する。」
    print('【',end='')
    party_and_monster.print_monster_name(monster)
    print(f'】のターン (HP = {monster['hp']})')
    # (3) プレイヤーのHPからダメージ分の値を減らす。
    print(f'{monster['ap']}のダメージを与えた')
    party['hp'] -= monster['ap']
    print('')
# *******************プレイヤー攻撃ダメージ計算*******************
def do_attack(monster,command):
    import random
    print(random.uniform(-3,3))
# *******************敵の攻撃ダメージ計算*******************
def do_enemy_attack(party):
    print("")
# *******************戦う*******************
def do_buttle(party,monster):
    print('')
    party_and_monster.print_monster_name(monster)
    print(f'が現れた！')
    print('')
    while party['hp'] > 0 and monster['hp'] > 0:
        on_player_turn(party,monster)
        if monster['hp'] <= 0:
            continue
        on_enemy_turn(party,monster)
    party_and_monster.print_monster_name(monster)
    print(f'を倒した！')
    return 1

# *******************ダンジョンに入る*******************
def go_dungeon(party,monster_list):
    print(f'{party['player_name']}のパーティ(HP = {party['hp']})はダンジョンに到着した')
    print('<パーティー編成>-----------------------')
    party_and_monster.show_party(party)
    print('-----------------------------------')
    monster_defeated = 0 # 倒したモンスター数
    for monster in monster_list:
        is_win = do_buttle(party,monster)
        if party['hp'] <= 0:
            print('パーティのHPは0になった')
            print(f'「{party['player_name']}はダンジョンから逃げ出した」')
            break
        else:
            print(f'「{party['player_name']}はさらに奥へと進んだ」')
            print('=====================================')
            monster_defeated += is_win

    if monster_defeated == 5:
        print(f'{party['player_name']}はダンジョンを制覇した')
        return monster_defeated
    else:
        return monster_defeated