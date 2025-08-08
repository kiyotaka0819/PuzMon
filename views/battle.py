from models import data, party_and_monster
from . import gems
import time
import random

# *******************バトルフィールドの表示*******************
def show_battle_field(party,monster):
    print('バトルフィールド')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.3)
    print(f'HP = {monster['hp']} / {monster['max_hp']}')
    time.sleep(0.3)
    print('------------------------')
    for positions in data.ELEMENT_POSITIONS:
        time.sleep(0.03)
        print(f'{positions}',end=' ')
    print('')
    time.sleep(0.3)
    gems.print_gems(data.gems_slot)
    print('------------------------')

# *******************コマンドの入力内容チェック*******************
def check_valid_command(command):
    if len(command) != 2:
        return False
    if not ('A' <= command[0].upper() <= 'N' and 'A' <= command[1].upper() <= 'N'):
        return False
    if command[0].upper() == command[1].upper():
        return False
    else:
        return True

# *****************スロット内の宝石を消滅させて効果を発動させる*********************
def banish_combos(party, monster):
    combo_count = 1
    while True:
        banishable_groups = gems.check_banishable(data.gems_slot)
        if not banishable_groups:
            break

        gems_banished = gems.banish_gems(banishable_groups, party, monster, combo_count)
        if not gems_banished:
            break

        gems.shift_gems(data.gems_slot)
        gems.spawn_gems()
        combo_count += 1
        time.sleep(0.5)

# *******************ダメージを計算する関数*******************
def calculate_damage(party, gem_symbol, num_gems, combo_count):
    # ダメージ計算のロジック
    damage = 0
    # 宝石の属性に対応する攻撃力を取得
    gem_element = None
    for key, value in data.ELEMENT_SYMBOLS.items():
        if value == gem_symbol:
            gem_element = key
            break

    for friend in party['friends']:
        if friend['element'] == gem_element:
            base_damage = friend['ap']
            # 宝石の数ボーナス
            damage_multiplier = 1 + (num_gems - 3) * 0.5
            # コンボボーナス
            combo_multiplier = 1 + (combo_count - 1) * 0.25
            damage += base_damage * damage_multiplier * combo_multiplier
            break

    return int(damage)

# *******************プレイヤーターン*******************
def on_player_turn(party,monster):
    if not data.gems_slot:
        data.gems_slot = tuple([gems.fill_gems() for _ in range(14)])

    time.sleep(0.3)
    print(f'【{party['player_name']}】のターン (HP = {party['hp']})')
    show_battle_field(party, monster)
    valid_command = False
    while not valid_command:
        command = input('コマンド? > ')
        valid_command = check_valid_command(command)
        if valid_command:
            gems.move_gem(command)

    banish_combos(party, monster)

# *******************敵のターン*******************
def on_enemy_turn(party,monster):
    # (1) 「【〇〇〇のターン】(HP = XXX)を表示する。」
    time.sleep(0.3)
    print('【',end='')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.3)
    print(f'】のターン (HP = {monster['hp']})')
    # (3) プレイヤーのHPからダメージ分の値を減らす。
    time.sleep(0.3)
    # ダメージを受けた時の背景色を変更する処理
    print(f'\033[41;37m{monster['ap']}のダメージを与えた\033[0m')
    party['hp'] -= monster['ap']
    print('')

# *******************プレイヤー攻撃ダメージ計算*******************
def do_attack(party, monster, element_name, num_banished, combo_count):
    total_damage = 0
    # 消去した宝石の数に応じてコンボボーナスを計算
    combo_bonus = 1.0 + max(0, num_banished - 3) * 0.2
    for member in party['friends']:
        if member['element'] == element_name:
            attribute_boost = data.ELEMENT_BOOST.get(member['element'], {}).get(monster['element'], 1.0)
            damage = (member['ap'] - monster['dp']) * attribute_boost * combo_bonus
            damage = int(gems.blur_damage(damage, 10))
            if damage <= 0:
                damage = 1

            total_damage += damage
            party_and_monster.print_monster_name(member)
            if combo_count > 1:
                print(f'の攻撃！ {combo_count} Combo!! {damage}のダメージを与えた')
            else:
                print(f'の攻撃で{damage}のダメージを与えた')
            print('')

    return total_damage

# *******************敵の攻撃ダメージ計算*******************
def do_enemy_attack(party):
    print("")

# *******************戦う*******************
def do_buttle(party,monster):
    print('')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.3)
    print(f'が現れた！')
    print('')
    while party['hp'] > 0 and monster['hp'] > 0:
        on_player_turn(party,monster)
        if monster['hp'] <= 0:
            continue
        on_enemy_turn(party,monster)

    if monster['hp'] <= 0:
        party_and_monster.print_monster_name(monster)
        time.sleep(0.3)
        print(f'を倒した！')
        return 1
    else:
        return 0

# *******************ダンジョンに入る*******************
def go_dungeon(party,monster_list):
    time.sleep(0.3)
    print(f'{party['player_name']}のパーティ(HP = {party['hp']})はダンジョンに到着した')
    time.sleep(0.3)
    print('<パーティー編成>-----------------------')
    party_and_monster.show_party(party)
    time.sleep(0.3)
    print('-----------------------------------')
    monster_defeated = 0 # 倒したモンスター数
    for monster in monster_list:
        is_win = do_buttle(party,monster)
        if party['hp'] <= 0:
            time.sleep(0.3)
            print('パーティのHPは0になった')
            time.sleep(1.0)
            print(f'「{party['player_name']}はダンジョンから逃げ出した」')
            break
        else:
            time.sleep(0.3)
            print(f'「{party['player_name']}はさらに奥へと進んだ」')
            print('=====================================')
            monster_defeated += is_win

    if monster_defeated == len(monster_list):
        time.sleep(1.0)
        print(f'{party['player_name']}はダンジョンを制覇した')
        return monster_defeated
    else:
        return monster_defeated