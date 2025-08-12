from models import data, party_and_monster
from views import battle
import time
import random

# *******************宝石スロットにランダムに宝石を発生させる******************
def fill_gems():
    random_num = random.randint(1, 5)
    return data.ELEMENT_NUMBERS.get(random_num, '　')

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
            # 背景色と文字色を白に設定
            color = data.ELEMENT_COLORS.get(element)
            time.sleep(0.03)
            print(f'\033[4{color};37m{gem}\033[0m', end=' ')
        else:
            print(gem, end=' ')
    print('')

# *******************gemsの移動とプリント*******************
def move_gem(command):
    # ユーザーが入力したコマンドを分解
    if len(command) != 2:
        return
    pos1 = command[0].upper()
    pos2 = command[1].upper()
    # 文字を数字（インデックス）に変換する
    index1 = data.ELEMENT_POSITIONS.get(pos1, 0) - 1
    index2 = data.ELEMENT_POSITIONS.get(pos2, 0) - 1

    # インデックスが範囲内かチェック
    if 0 <= index1 < len(data.gems_slot) and 0 <= index2 < len(data.gems_slot):
        # 宝石を入れ替える関数を呼び出す
        if index1 < index2:
            for i in range(index1, index2):
                swap_gem(i, i+1)
                print_gems(data.gems_slot)
                time.sleep(0.1)
        elif index1 > index2:
            for i in range(index1, index2, -1):
                swap_gem(i, i-1)
                print_gems(data.gems_slot)
                time.sleep(0.1)
    else:
        print("無効なコマンドです。")

# *******************gemsの隣との入れ替え*******************
def swap_gem(index1, index2):
    gems_list = list(data.gems_slot)
    gems_list[index1], gems_list[index2] = gems_list[index2], gems_list[index1]
    data.gems_slot = tuple(gems_list)

# *******************宝石の並びを調べて消去可能な箇所を検索して返す*******************
def check_banishable(gems_slot):
    banishable_groups = []
    i = 0
    while i < len(gems_slot):
        # 消去対象外の無属性を飛ばす
        if gems_slot[i] == '　':
            i += 1
            continue
        # 同じ宝石が連続している数を数える
        current_gem = gems_slot[i]
        j = i + 1
        while j < len(gems_slot) and gems_slot[j] == current_gem:
            j += 1

        # 3個以上連続していたら、消去対象としてリストに追加
        if j - i >= 3:
            banishable_groups.append((i, j - 1))
        i = j

    return banishable_groups

# *******************宝石を消してダメージを与える*******************
def banish_gems(banishable_groups, party, monster, combo_count):
    gems_slot_list = list(data.gems_slot)
    banished_count = 0
    for start, end in banishable_groups:
        gem_symbol = gems_slot_list[start]
        for i in range(start, end + 1):
            if gems_slot_list[i] != '　':
                gems_slot_list[i] = data.ELEMENT_SYMBOLS.get('無', '　')
                banished_count += 1

        # ダメージ計算
        damage = battle.calculate_damage(party, gem_symbol, end - start + 1, combo_count)
        if damage > 0:
            monster['hp'] -= damage

            # 攻撃したモンスターの名前を取得するロジック
            attacker_name = "不明なモンスター"
            gem_element = party_and_monster.get_element_name(gem_symbol)
            for friend in party['friends']:
                if friend['element'] == gem_element:
                    attacker_name = friend['name']
                    break

            print(f"【{attacker_name}】の攻撃！ {combo_count} Combo!! {damage}のダメージを与えた")
            print(f"[42;37m敵モンスターに{damage}のダメージを与えた[0m")

    data.gems_slot = tuple(gems_slot_list)
    print_gems(data.gems_slot)
    time.sleep(0.3)
    return banished_count > 0


# *******************空きスロットの右側に並ぶ宝石を左詰めする*******************
def shift_gems(gems_slot):
    gems_slot_list = list(gems_slot)

    # 空きスロットの数だけ繰り返す
    num_empty_slots = gems_slot_list.count(' ')
    for _ in range(num_empty_slots):
        # 空きスロットを左から探す
        if ' ' in gems_slot_list:
            empty_index = gems_slot_list.index(' ')
            
            # 空きスロットをリストから取り除く
            empty_slot = gems_slot_list.pop(empty_index)
            
            # 取り除いた空きスロットを一番右に追加する
            gems_slot_list.append(empty_slot)
            
            # 変化をアニメーションとして表示する
            data.gems_slot = tuple(gems_slot_list)
            print_gems(data.gems_slot)
            time.sleep(0.05)
# *******************空きスロットにランダムな宝石を生成する*******************
def spawn_gems():
    gems_slot_list = list(data.gems_slot)
    new_gems = []

    # 無属性の数を数える
    empty_slots = gems_slot_list.count(' ')

    # コンボが発生しないように宝石を生成
    for _ in range(empty_slots):
        new_gem = fill_gems()
        # 直前の2つの宝石と同じにならないようにチェック
        while len(new_gems) >= 2 and new_gem == new_gems[-1] and new_gem == new_gems[-2]:
            new_gem = fill_gems()
        new_gems.append(new_gem)

    # 後ろから無属性の場所に新しい宝石を詰める
    new_gem_index = 0
    for i in range(len(gems_slot_list) - empty_slots, len(gems_slot_list)):
        gems_slot_list[i] = new_gems[new_gem_index]
        new_gem_index += 1

    data.gems_slot = tuple(gems_slot_list)
    print_gems(data.gems_slot)
    time.sleep(0.1)

# *******************指定した値を指定した範囲内で乱数を出す*******************
def blur_damage(value, blur_percentage):
    blur_amount = value * blur_percentage / 100
    return value + random.uniform(-blur_amount, blur_amount)

# *******************パーティーのHP回復*******************
def do_recover(party, amount):
    party['hp'] += amount
    if party['hp'] > party['max_hp']:
        party['hp'] = party['max_hp']
    return party['hp']