from models import data
import time
from views import battle
# *******************宝石スロットにランダムに宝石を発生させる******************
def fill_gems():
    import random
    random_num = random.randint(1, 5)
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
            time.sleep(0.05)
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
    if index1 < index2:
        for i in range(index1, index2):
            swap_gem(i, i+1)
            print_gems(data.gems_slot)
            print()
            time.sleep(0.5)
    elif index1 > index2:
        for i in range(index1, index2, -1):
            swap_gem(i, i-1)
            print_gems(data.gems_slot)
            print()
            time.sleep(0.5)
# *******************gemsの隣との入れ替え*******************
def swap_gem(index1, index2):
    data.gems_slot[index1], data.gems_slot[index2] = data.gems_slot[index2], data.gems_slot[index1]

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
            print(f'{current_gem}が{j - i}個連続です　デバック用確認後消去')
        i = j

    return banishable_groups
# *******************空きスロットの右側に並ぶ宝石を左詰めする*******************
def shift_gems(gems_slot):
    write_index = 0
    for read_index in range(len(gems_slot)):
        # 空きスロットじゃない宝石があった時
        if gems_slot[read_index] != data.ELEMENT_SYMBOLS['無']:
            # 宝石を移動させる必要があれば
            if read_index != write_index:
                # 宝石を入れ替える
                gems_slot[write_index], gems_slot[read_index] = gems_slot[read_index], gems_slot[write_index]
                # 画面を再表示してアニメーションを見せる
                battle.show_battle_field(party, monster)
                time.sleep(0.5)
            # 宝石を書き込む場所を次に進める
            write_index += 1

    return gems_slot



# *******************空きスロットにランダムな宝石を生成する*******************

