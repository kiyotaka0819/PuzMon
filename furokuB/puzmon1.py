'''
作成日：2025/07/31
作成者：天本
'''
# インポート

# グローバル変数の宣言
# **********モンスターのディクショナリ**********
slime = {
    'name':'スライム',
    'hp':100,
    'max_hp':100,
    'element':'水',
    'ap':10,
    'dp':1
}

goburin = {
    'name':'ゴブリン',
    'hp':200,
    'max_hp':200,
    'element':'土',
    'ap':20,
    'dp':5
}

ookoumori = {
    'name':'オオコウモリ',
    'hp':300,
    'max_hp':300,
    'element':'風',
    'ap':30,
    'dp':10
}

wearwolf = {
    'name':'ウェアウルフ',
    'hp':400,
    'max_hp':400,
    'element':'風',
    'ap':40,
    'dp':15
}

dragon = {
    'name':'ドラゴン',
    'hp':600,
    'max_hp':600,
    'element':'火',
    'ap':50,
    'dp':20
}

monster_list = [slime,goburin,ookoumori,wearwolf,dragon]

# **********味方モンスターのディクショナリ**********
seiryu = {
    'name':'青龍',
    'hp':150,
    'max_hp':150,
    'element':'風',
    'ap':15,
    'dp':10
}

suzaku = {
    'name':'朱雀',
    'hp':150,
    'max_hp':150,
    'element':'火',
    'ap':25,
    'dp':10
}

byakko = {
    'name':'白虎',
    'hp':150,
    'max_hp':150,
    'element':'土',
    'ap':20,
    'dp':5
}

genbu = {
    'name':'玄武',
    'hp':150,
    'max_hp':150,
    'element':'水',
    'ap':20,
    'dp':15
}

friends = [seiryu,suzaku,byakko,genbu]
# ***********属性の記号*************
ELEMENT_SYMBOLS = {
    '火':'$',
    '水':'~',
    '風':'@',
    '土':'#',
    '命':'&',
    '無':'　'
}

ELEMENT_COLORS = {
    '火':1,
    '水':6,
    '風':2,
    '土':3,
    '命':5,
    '無':7
}

ELEMENT_NUMBERS = {
    1:'$',
    2:'~',
    3:'@',
    4:'#',
    5:'&',
    }

ELEMENT_POSITIONS = {
    'A':1,
    'B':2,
    'C':3,
    'D':4,
    'E':5,
    'F':6,
    'G':7,
    'H':8,
    'I':9,
    'J':10,
    'K':11,
    'L':12,
    'M':13,
    'N':14
    }

# 関数宣言
# *******************バトルフィールドの表示*******************
def show_battle_field(party,monster):
    print('バトルフィールド')
    print_monster_name(monster)
    print(f'HP = {monster['hp']} / {monster['max_hp']}')
    print('------------------------')
    for positions in ELEMENT_POSITIONS:
        print(f'{positions}',end=' ')
    print('')
    for element in ELEMENT_POSITIONS:
        print_gems()
    print('')
    print('------------------------')

# *******************宝石スロットにランダムに宝石を発生させる******************
def fill_gems():
    import random
    random_num = random.randint(1, 5)
    print(f'{ELEMENT_NUMBERS[random_num]}',end=' ')
    return ELEMENT_NUMBERS[random_num]

# *******************宝石スロット(14個分)の表示*******************
def print_gems():
    # (1) gemsのキー記号を取得する
    fill_gems()
    # (2) 取得した記号に対応する属性を取得する
    #mon_element = monster_data['element']
    #symbol = ELEMENT_SYMBOLS[mon_element]
    # (3) 取得した属性に対応する色をELEMENT_COLORSから取得する
    #mon_color = monster_data['element']
    #color = ELEMENT_COLORS[mon_color]
    # (4) gemsを表示する
    #print(f'\033[3{color}m{symbol}{monster_name}{symbol}\033[0m',end='')
    print()
# *******************プレイヤーターン*******************
def on_player_turn(party,monster):
    print(f'【{party['player_name']}】のターン (HP = {party['hp']})')
    show_battle_field(party, monster)
    command = input('コマンド? > ')
    damage = 500
    # (3) 敵モンスターのHPからダメージ分の値を減らす。
    print(f'{damage}のダメージを与えた')
    monster['hp'] -= damage
    print('')
# *******************敵のターン*******************
def on_enemy_turn(party,monster):
    # (1) 「【〇〇〇のターン】(HP = XXX)を表示する。」
    print('【',end='')
    print_monster_name(monster)
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
    print_monster_name(monster)
    print(f'が現れた！')
    print('')
    while party['hp'] > 0 and monster['hp'] > 0:
        on_player_turn(party,monster)
        if monster['hp'] <= 0:
            continue
        on_enemy_turn(party,monster)
    print_monster_name(monster)
    print(f'を倒した！')
    return 1

# *******************ダンジョンに入る*******************
def go_dungeon(party,monster_list):
    print(f'{party['player_name']}のパーティ(HP = {party['hp']})はダンジョンに到着した')
    print('<パーティー編成>-----------------------')
    show_party(party)
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

# *******************装飾したモンスター名を返す*******************
def print_monster_name(monster_data):
    # (1) モンスターの名前をキーnameで取得する
    monster_name = monster_data['name']
    # (2) 取得した属性に対応する記号をELEMENT_SYMBOLSから取得する
    mon_element = monster_data['element']
    symbol = ELEMENT_SYMBOLS[mon_element]
    # (3) 取得した属性に対応する記号をELEMENT_COLORSから取得する
    mon_color = monster_data['element']
    color = ELEMENT_COLORS[mon_color]
    # (4) モンスター名を表示する
    print(f'\033[3{color}m{symbol}{monster_name}{symbol}\033[0m',end='')

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
        print_monster_name(friend)
    # ③ 続けて、HP・攻撃力を表示する。
        print(f'HP = {hp} 攻撃 = {ap} 防御 = {dp}')

# *******************メイン処理*******************
def main():
    print('*** Puzzle & Monsters ***')
    player_name = ''
    while player_name == '':
        player_name = input('プレイヤー名を入力してください > ')
        if player_name == '':
            print('エラー：プレイヤー名を入力してください')
    monster_num = go_dungeon(organize_party(player_name, friends),monster_list)
    if monster_num == 5:
        print('*** GAME CLEARED!! ***')
        print(f'倒したモンスター数 = {monster_num}') # {monster_number}
    else:
        print('*** GAME OVER!! ***')
        print(f'倒したモンスター数 = {monster_num}') # {monster_number}
# main関数の呼び出し
main()