from models import data, party_and_monster
from views import battle
import time
import random
import sys

# 1文字ずつゆっくり表示する関数
def print_slowly(text, end='\n'):
    """
    引数で受け取ったテキストを1文字ずつゆっくりと表示する。
    end引数で改行するかどうかを制御できる。
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print(end=end)

# 宝石スロットにランダムな宝石を1つ生成する
def fill_gems():
    """
    1から5のランダムな整数を生成し、対応する宝石の記号を返す。
    """
    # 1から5のランダムな整数を生成
    random_num = random.randint(1, 5)
    # その整数に対応する宝石の記号をデータから取得
    return data.ELEMENT_NUMBERS.get(random_num, ' ')

# 宝石スロットの宝石を色付きで表示する
def print_gems(gems_list):
    """
    宝石リストを受け取り、それぞれの宝石を対応する色で表示する。
    """
    for gem in gems_list:
        element = None
        # 宝石の記号から属性名を取得
        for key, value in data.ELEMENT_SYMBOLS.items():
            # 辞書のvalueと宝石の記号が一致した場合
            if value == gem:
                element = key
                break

        # 属性名が見つかった場合
        if element and element in data.ELEMENT_COLORS:
            color = data.ELEMENT_COLORS.get(element)
            time.sleep(0.03)
            # ANSIエスケープシーケンスで背景色と文字色を白に設定
            print(f'\033[4{color};37m{gem}\033[0m', end=' ')
        # 属性が見つからない場合（無属性など）
        else:
            print(gem, end=' ')
    print('')

# 宝石の移動を処理し、表示を更新する
def move_gem(command):
    """
    2文字のコマンド（例: 'AD'）を受け取り、宝石の移動を処理する。
    """
    # コマンドが2文字でなければ処理を中断
    if len(command) != 2:
        return
    pos1 = command[0].upper()
    pos2 = command[1].upper()

    # コマンドの文字をインデックスに変換
    index1 = data.ELEMENT_POSITIONS.get(pos1, 0) - 1
    index2 = data.ELEMENT_POSITIONS.get(pos2, 0) - 1

    # インデックスが有効範囲内かチェック（0からスロットの長さ-1）
    if 0 <= index1 < len(data.gems_slot) and 0 <= index2 < len(data.gems_slot):
        # 宝石を入れ替える処理
        # インデックス1がインデックス2より小さい場合（左から右へ移動）
        if index1 < index2:
            # 始点から終点まで隣接する宝石を順番に入れ替え
            for i in range(index1, index2):
                swap_gem(i, i+1)
                print_gems(data.gems_slot)
                time.sleep(0.1)
        # インデックス1がインデックス2より大きい場合（右から左へ移動）
        elif index1 > index2:
            # 始点から終点まで隣接する宝石を順番に入れ替え
            for i in range(index1, index2, -1):
                swap_gem(i, i-1)
                print_gems(data.gems_slot)
                time.sleep(0.1)
    # インデックスが無効な場合
    else:
        print("無効なコマンドです。")

# 隣接する2つの宝石を入れ替える
def swap_gem(index1, index2):
    """
    指定された2つのインデックスの宝石を入れ替える。
    """
    gems_list = list(data.gems_slot)
    # タプルは変更できないため、リストに変換して入れ替え
    gems_list[index1], gems_list[index2] = gems_list[index2], gems_list[index1]
    # 変更後、タプルに戻してdata.gems_slotに代入
    data.gems_slot = tuple(gems_list)

# 3つ以上連続している消去可能な宝石のグループを探す
def check_banishable(gems_slot):
    """
    3つ以上連続している同じ属性の宝石グループを検出し、その開始インデックスと終了インデックスのタプルを返す。
    """
    banishable_groups = []
    i = 0
    # 宝石スロット全体を走査
    while i < len(gems_slot):
        # 無属性(' ')は消去対象外
        if gems_slot[i] == ' ':
            i += 1
            continue

        # 同じ宝石が連続する数をカウント
        current_gem = gems_slot[i]
        j = i + 1
        while j < len(gems_slot) and gems_slot[j] == current_gem:
            j += 1

        # 3個以上連続していれば、消去グループとしてリストに追加
        if j - i >= 3:
            banishable_groups.append((i, j - 1))
        # 次のグループをチェックするためにインデックスを更新
        i = j
    return banishable_groups

# 消去可能な宝石を消し、効果を発動させる（ダメージまたは回復）
def banish_gems(banishable_group, party, monster, combo_count):
    """
    消去可能な宝石のグループを処理し、ダメージや回復の効果を適用する。
    宝石が消去された場合はTrue、そうでなければFalseを返す。
    """
    gems_slot_list = list(data.gems_slot)

    start, end = banishable_group
    gem_symbol = gems_slot_list[start]
    gem_element = party_and_monster.get_element_name(gem_symbol)
    num_gems = end - start + 1

    # 消去対象の宝石を「無」に置き換える
    for i in range(start, end + 1):
        if gems_slot_list[i] != ' ':
            gems_slot_list[i] = data.ELEMENT_SYMBOLS.get('無', ' ')

    # 宝石スロットのタプルを更新し、表示
    data.gems_slot = tuple(gems_slot_list)
    print_gems(data.gems_slot)
    time.sleep(0.3)

    # 攻撃メッセージと回復メッセージの出力
    if gem_element == '命':
        # 回復処理
        combo_multiplier = 1 + (combo_count - 1) * 0.25
        recover_amount = int(blur_damage(20 * combo_multiplier, 10))
        do_recover(party, recover_amount)

        print_slowly(f'命属性による回復！', end='')
        print_slowly(f'{combo_count} Combo!!', end='')
        time.sleep(0.3)
        print(f'\033[45;37m', flush=True)
        print_slowly(f'パーティーのHPが{recover_amount}回復した')
        print(f'\033[0m', flush=True)
    else:
        # ダメージ処理
        damage = battle.calculate_damage(party, gem_symbol, num_gems, combo_count)
        if damage > 0:
            monster['hp'] -= damage
            attacker_name = "不明なモンスター"
            attacker_symbol = " "
            for friend in party['friends']:
                if friend['element'] == gem_element:
                    attacker_name = friend['name']
                    attacker_symbol = data.ELEMENT_SYMBOLS.get(friend['element'])
                    break

            print(f'\033[4{data.ELEMENT_COLORS.get(gem_element)};37m', end='', flush=True)
            print_slowly(f"【{attacker_symbol}{attacker_name}{attacker_symbol}】", end='')
            print(f'\033[0m', end='')
            print_slowly(f"の攻撃！ {combo_count} Combo!!")
            time.sleep(0.3)
            print(f'\033[42;37m', end='', flush=True)
            print_slowly('敵モンスターに', end='')
            print_slowly(f'{damage}のダメージを与えた')
            print(f'\033[0m', flush=True)

    # 宝石が1つでも消去されたかどうかのブール値を返す
    return True

# 消滅した宝石の空きスロットを左に詰める
def shift_gems(gems_slot):
    """
    空きスロット(' ')をリストの左端に詰める。
    """
    gems_slot_list = list(gems_slot)
    # 空きスロットの数をカウント
    num_empty_slots = gems_slot_list.count(' ')
    # 空きスロットの数だけループ
    for _ in range(num_empty_slots):
        # 空きスロット(' ')が存在する場合
        if ' ' in gems_slot_list:
            empty_index = gems_slot_list.index(' ')
            empty_slot = gems_slot_list.pop(empty_index)
            # 空きスロットをリストの末尾に追加
            gems_slot_list.append(empty_slot)
            data.gems_slot = tuple(gems_slot_list)
            print_gems(data.gems_slot)
            time.sleep(0.05)

# 空きスロットにランダムな新しい宝石を生成する
def spawn_gems():
    """
    空きスロットの数だけ新しい宝石を生成し、スロットの右側に配置する。
    """
    gems_slot_list = list(data.gems_slot)
    new_gems = []
    # 空きスロットの数を数える
    empty_slots = gems_slot_list.count(' ')
    # 空きスロットの数だけ新しい宝石を生成
    for _ in range(empty_slots):
        new_gem = fill_gems()
        new_gems.append(new_gem)

    # スロットの右端から新しい宝石を埋める
    new_gem_index = 0
    for i in range(len(gems_slot_list) - empty_slots, len(gems_slot_list)):
        gems_slot_list[i] = new_gems[new_gem_index]
        new_gem_index += 1

    data.gems_slot = tuple(gems_slot_list)
    print_gems(data.gems_slot)
    time.sleep(0.1)

# 値を指定した範囲でランダムに変動させる
def blur_damage(value, blur_percentage):
    """
    指定された値にランダムなブレを加えた値を返す。
    """
    blur_amount = value * blur_percentage / 100
    # 指定された値からブレの範囲内の乱数を加算して返す
    return value + random.uniform(-blur_amount, blur_amount)

# パーティのHPを回復させる
def do_recover(party, amount):
    """
    パーティのHPを指定された量だけ回復させる。最大HPを超えることはない。
    """
    party['hp'] += amount
    # HPが最大値を超えないように調整
    if party['hp'] > party['max_hp']:
        party['hp'] = party['max_hp']
    return party['hp']