from models import data, party_and_monster
from . import gems
import time
# *******************バトルフィールドの表示*******************
def show_battle_field(party,monster):
    print('バトルフィールド')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.5)
    print(f'HP = {monster['hp']} / {monster['max_hp']}')
    time.sleep(0.5)
    print('------------------------')
    for positions in data.ELEMENT_POSITIONS:
        time.sleep(0.05)
        print(f'{positions}',end=' ')
    print('')
    time.sleep(0.5)
    gems.print_gems(data.gems_slot)
    print('')
    time.sleep(0.5)
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
    
# *****************スロット内の宝石を消滅させて効果を発動させる*********************
def banish_gems(banishable_groups, party, monster):
    for start, end in banishable_groups:
        for i in range(start, end + 1):
            data.gems_slot[i] = data.ELEMENT_SYMBOLS['無']

    time.sleep(0.5)
    print('消去された箇所より右側の宝石達を１マスずつ動かす')
    gems.shift_gems(data.gems_slot, party, monster)
    time.sleep(0.5)
    print('右端にできた空きスロットにランダムに宝石を発生させる')
    gems.spawn_gems()
# *******************プレイヤーターン*******************
def on_player_turn(party,monster):
    if not data.gems_slot:
        for _ in range(14):
            data.gems_slot.append(gems.fill_gems())

    time.sleep(0.5)
    print(f'【{party['player_name']}】のターン (HP = {party['hp']})')
    show_battle_field(party, monster)
    valid_command = False
    while not valid_command:
        command = input('コマンド? > ')
        valid_command = check_valid_command(command)
        if valid_command:
            gems.move_gem(command)
            # 動かした後のフィールドを再表示
            time.sleep(0.5)
            print('------------------------')
            for positions in data.ELEMENT_POSITIONS:
                time.sleep(0.05)
                print(f'{positions}',end=' ')
            print('')
            gems.print_gems(data.gems_slot)
            print('')
            time.sleep(0.5)
            print('------------------------')

    banishable_groups = gems.check_banishable(data.gems_slot)
    if banishable_groups:
        banish_gems(banishable_groups, party, monster)
    damage = 50
    # (3) 敵モンスターのHPからダメージ分の値を減らす。
    time.sleep(0.5)
    print(f'{damage}のダメージを与えた')
    monster['hp'] -= damage
    print('')
# *******************敵のターン*******************
def on_enemy_turn(party,monster):
    # (1) 「【〇〇〇のターン】(HP = XXX)を表示する。」
    time.sleep(0.5)
    print('【',end='')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.5)
    print(f'】のターン (HP = {monster['hp']})')
    # (3) プレイヤーのHPからダメージ分の値を減らす。
    time.sleep(0.5)
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
    time.sleep(0.5)
    print(f'が現れた！')
    print('')
    while party['hp'] > 0 and monster['hp'] > 0:
        on_player_turn(party,monster)
        if monster['hp'] <= 0:
            continue
        on_enemy_turn(party,monster)
    party_and_monster.print_monster_name(monster)
    time.sleep(0.5)
    print(f'を倒した！')
    return 1

# *******************ダンジョンに入る*******************
def go_dungeon(party,monster_list):
    time.sleep(0.5)
    print(f'{party['player_name']}のパーティ(HP = {party['hp']})はダンジョンに到着した')
    time.sleep(0.5)
    print('<パーティー編成>-----------------------')
    party_and_monster.show_party(party)
    time.sleep(0.5)
    print('-----------------------------------')
    monster_defeated = 0 # 倒したモンスター数
    for monster in monster_list:
        is_win = do_buttle(party,monster)
        if party['hp'] <= 0:
            time.sleep(0.5)
            print('パーティのHPは0になった')
            time.sleep(0.5)
            print(f'「{party['player_name']}はダンジョンから逃げ出した」')
            break
        else:
            time.sleep(0.5)
            print(f'「{party['player_name']}はさらに奥へと進んだ」')
            time.sleep(0.5)
            print('=====================================')
            monster_defeated += is_win

    if monster_defeated == 5:
        time.sleep(0.5)
        print(f'{party['player_name']}はダンジョンを制覇した')
        return monster_defeated
    else:
        return monster_defeated

