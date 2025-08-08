from models import data
import time
# *******************装飾したモンスター名を返す*******************
def print_monster_name(monster_data):
    # (1) モンスターの名前をキーnameで取得する
    monster_name = monster_data['name']
    # (2) 取得した属性に対応する記号をELEMENT_SYMBOLSから取得する
    mon_element = monster_data['element']
    symbol = data.ELEMENT_SYMBOLS[mon_element]
    # (3) 取得した属性に対応する記号をELEMENT_COLORSから取得する
    mon_color = monster_data['element']
    color = data.ELEMENT_COLORS[mon_color]
    # (4) モンスター名を表示する
    time.sleep(0.1)
    # 背景色と文字色を白に設定
    print(f'\033[4{color};37m{symbol}{monster_name}{symbol}\033[0m',end='')

# *******************記号から属性名を取得するユーティリティ関数*******************
def get_element_name(symbol):
    for name, s in data.ELEMENT_SYMBOLS.items():
        if s == symbol:
            return name
    return None

# *******************記号から属性名を取得する関数*******************
def get_element_name(gem_symbol):
    for name, symbol in data.ELEMENT_SYMBOLS.items():
        if symbol == gem_symbol:
            return name
    return '不明' # 見つからなかった場合は「不明」を返す

# *******************味方モンスターの編成*******************
def organize_party(player_name,friends):
    """
    引数
        player_name : プレイヤー名
        friends : 味方モンスターをディクショナリで管理したリスト
    """
    # (1) 味方モンスターのHPの合計と防御力の平均を求める
    hp = 0
    max_hp = 0
    dp = 0
    for friend in friends:
        hp += friend['hp']
        max_hp += friend['max_hp']
        dp += friend['dp']

    dp = dp / len(friends)

    # (2) ディクショナリにパーティの情報をまとめる
    party = {
        'player_name' : player_name,
        'friends' : friends,
        'hp' : hp,
        'max_hp' : max_hp,
        'dp' : dp
    }
    # (3) ディクショナリを戻り値に指定する
    return party


# *******************パーティ情報を見る*******************
def show_party(party):
    # (1) 引数で受け取ったパーティから味方モンスターのリストを取得する。
    friends = party['friends']
    # (2) 味方モンスターのリストから味方モンスターを順に取出し、次の①~③を繰り返す。
    for friend in friends:
    # ① 味方モンスターから、名前・HP・攻撃力・防御力を取り出す
        hp = friend['hp']
        ap = friend['ap']
        dp = friend['dp']
    # ② print_monster_name関数を利用してモンスター名を表示する。
        time.sleep(0.03)
        # 属性の記号を取得
        symbol = data.ELEMENT_SYMBOLS.get(friend['element'])
        # 背景色と文字色を白に設定
        color = data.ELEMENT_COLORS.get(friend['element'])
        print(f'\033[4{color};37m{symbol}{friend['name']}{symbol}\033[0m',end='')
    # ③ 続けて、HP・攻撃力を表示する。
        print(f'HP = {hp} 攻撃 = {ap} 防御 = {dp}')

