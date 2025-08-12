from models import data
import time

# 装飾付きのモンスター名を表示する
def print_monster_name(monster_data):
    """
    モンスター名と属性記号を色付きで表示する。
    """
    # モンスターの名前と属性を取得
    monster_name = monster_data['name']
    mon_element = monster_data['element']
    symbol = data.ELEMENT_SYMBOLS[mon_element]
    mon_color = monster_data['element']
    color = data.ELEMENT_COLORS[mon_color]
    time.sleep(0.1)
    # ANSIエスケープシーケンスで色付き表示
    print(f'\033[4{color};37m{symbol}{monster_name}{symbol}\033[0m',end='')

# 記号から属性名を取得する
def get_element_name(gem_symbol):
    """
    宝石の記号から対応する属性名を返す。
    見つからない場合は「不明」を返す。
    """
    for name, symbol in data.ELEMENT_SYMBOLS.items():
        # 記号が一致した場合
        if symbol == gem_symbol:
            return name
    # 記号が見つからなかった場合
    return '不明'

# プレイヤー名と味方モンスターのリストからパーティを編成する
def organize_party(player_name,friends):
    """
    引数
        player_name : プレイヤー名
        friends : 味方モンスターのリスト
    戻り値
        編成されたパーティ情報（ディクショナリ）
    """
    hp = 0
    max_hp = 0
    dp = 0
    # 味方モンスターのHPの合計と防御力の平均を計算
    for friend in friends:
        hp += friend['hp']
        max_hp += friend['max_hp']
        dp += friend['dp']
    dp = dp / len(friends)

    # プレイヤーのパーティ情報をディクショナリとしてまとめる
    party = {
        'player_name' : player_name,
        'friends' : friends,
        'hp' : hp,
        'max_hp' : max_hp,
        'dp' : dp
    }
    return party

# 編成されたパーティの情報を表示する
def show_party(party):
    """
    編成されたパーティメンバーの各パラメータを表示する。
    """
    friends = party['friends']
    for friend in friends:
        hp = friend['hp']
        ap = friend['ap']
        dp = friend['dp']
        time.sleep(0.03)

        symbol = data.ELEMENT_SYMBOLS.get(friend['element'])
        color = data.ELEMENT_COLORS.get(friend['element'])
        print(f'\033[4{color};37m{symbol}{friend['name']}{symbol}\033[0m',end='')
        print(f'HP = {hp} 攻撃 = {ap} 防御 = {dp}')