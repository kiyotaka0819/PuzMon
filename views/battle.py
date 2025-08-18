from models import data, party_and_monster
from views import gems
import time
import random
import sys
import pygame


# Pygameのミキサー機能を初期化
pygame.mixer.init()

# 効果音ファイルを読み込む
# ファイルのパスは、main.pyからの相対パスで指定
try:
    # 共通の効果音
    sound_banish = pygame.mixer.Sound('sounds/パワーチャージ.mp3') # 宝石を消す音

    # 敵モンスターごとの攻撃音を辞書に格納
    monster_attack_sounds = {
        'スライム': pygame.mixer.Sound('sounds/スライムの攻撃.mp3'),
        'ゴブリン': pygame.mixer.Sound('sounds/打撃4.mp3'),
        'オオコウモリ': pygame.mixer.Sound('sounds/ハトが飛び立つ2.mp3'),
        'ウェアウルフ': pygame.mixer.Sound('sounds/オオカミの遠吠え.mp3'),
        'ドラゴン': pygame.mixer.Sound('sounds/ドラゴンの鳴き声2.mp3'),
    }

except pygame.error as e:
    print(f"サウンドファイルの読み込みに失敗しました: {e}")
    # エラー時のフォールバック処理
    sound_banish = None
    monster_attack_sounds = {}


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

# バトルフィールドの情報を表示する
def show_battle_field(party,monster):
    """
    敵モンスターと宝石スロットの情報を表示する。
    """
    print('バトルフィールド')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.3)
    print(f'HP = {monster['hp']} / {monster['max_hp']}')
    time.sleep(0.3)
    print('------------------------')
    # ELEMENT_POSITIONSがタプルから辞書に変わったため、keys()で表示する
    for positions in data.ELEMENT_POSITIONS.keys():
        time.sleep(0.03)
        print(f'{positions}',end=' ')
    print('')
    time.sleep(0.3)
    gems.print_gems(data.gems_slot)
    print('------------------------')

# 入力されたコマンドが有効かチェックする
def check_valid_command(command):
    """
    入力されたコマンドが有効な形式（2文字のアルファベットで、同じスロットではない）かチェックする。
    """
    # コマンドが2文字でなければFalseを返す
    if len(command) != 2:
        return False
    # コマンドの文字がアルファベットA-Nの範囲内でなければFalseを返す
    if not ('A' <= command[0].upper() <= 'N' and 'A' <= command[1].upper() <= 'N'):
        return False
    # 同じ値を選択していたらFalseを返す
    if command[0].upper() == command[1].upper():
        return False
    # 上記の条件に当てはまらなければTrueを返す
    else:
        return True

# スロット内の宝石を消滅させ、コンボを処理する
def banish_combos(party, monster):
    """
    宝石の消滅とそれに続くコンボ（詰めコンボ、湧きコンボ）を処理する。
    """
    combo_count = 1
    while True:
        # 消去可能な宝石グループをチェック
        banishable_groups = gems.check_banishable(data.gems_slot)
        # 消せる宝石がなければループを抜ける
        if not banishable_groups:
            break

        # 1つのコンボグループを処理
        for group in banishable_groups:
            # 修正点: 宝石が消える音を各コンボの前に鳴らす
            if sound_banish:
                sound_banish.play()
            time.sleep(0.5)

            # 宝石を消去し、ダメージや回復効果を発動（メッセージとSEもここで出力）
            gems.banish_gems(group, party, monster, combo_count)
            combo_count += 1

        # 全てのコンボが終了してから、盤面を更新する
        gems.shift_gems(data.gems_slot)
        gems.spawn_gems()
        time.sleep(0.5)

# ダメージ量を計算する
def calculate_damage(party, gem_symbol, num_gems, combo_count):
    """
    プレイヤーの攻撃による敵へのダメージ量を計算する。
    """
    damage = 0
    gem_element = None
    # 宝石の記号から属性名を取得
    for key, value in data.ELEMENT_SYMBOLS.items():
        if value == gem_symbol:
            gem_element = key
            break

    # 同じ属性を持つ味方モンスターの攻撃力を取得し、ダメージを計算
    for friend in party['friends']:
        # 味方モンスターの属性が宝石の属性と一致した場合
        if friend['element'] == gem_element:
            base_damage = friend['ap']
            # 3個より多く消した分のボーナスを計算
            damage_multiplier = 1 + (num_gems - 3) * 0.5
            # コンボ数によるボーナスを計算
            combo_multiplier = 1 + (combo_count - 1) * 0.25
            # 全ての補正をかけてダメージに加算
            damage += base_damage * damage_multiplier * combo_multiplier
            break

    return int(damage)

# プレイヤーのターン処理
def on_player_turn(party,monster):
    """
    プレイヤーのターンでの一連の処理（コマンド入力、宝石移動、コンボ処理など）を管理する。
    """
    # 宝石スロットが空の場合、初期宝石を配置
    if not data.gems_slot:
        data.gems_slot = tuple([gems.fill_gems() for _ in range(14)])

    time.sleep(0.3)
    print(f'【{party['player_name']}】のターン (HP = {party['hp']})')
    show_battle_field(party, monster)

    valid_command = False
    # 有効なコマンドが入力されるまでループ
    while not valid_command:
        command = input('コマンド? > ')
        valid_command = check_valid_command(command)
        if valid_command:
            gems.move_gem(command)

    banish_combos(party, monster)
    # show_battle_field(party, monster)

# 敵のターン処理
def on_enemy_turn(party,monster):
    """
    敵のターンでの一連の処理（攻撃、ダメージ表示など）を管理する。
    """
    time.sleep(0.3)
    damage_with_defense = monster['ap'] - party['dp']
    if damage_with_defense <= 0:
        damage_with_defense = 1
    damage_with_defense = int(gems.blur_damage(damage_with_defense, 10))
    if damage_with_defense <= 0:
        damage_with_defense = 1

    # カラーコードとテキストを分けて出力し、ゆっくり表示と色付けを両立させる
    # 敵のターン表示部分
    print_slowly(f"【{monster['name']}のターン(HP={monster['hp']})】", end='')
    print('')

    # 敵モンスター名で辞書から効果音を取得して再生
    enemy_name = monster['name']
    if enemy_name in monster_attack_sounds and monster_attack_sounds[enemy_name]:
        monster_attack_sounds[enemy_name].play()

    # ダメージ表示部分
    print_slowly(f'パーティーに', end='')
    print(f'\033[41;37m', end='', flush=True)
    print_slowly(f'{damage_with_defense}のダメージを与えた', end='')
    print('\033[0m', flush=True)
    print('------------------------')

    party['hp'] -= damage_with_defense

# バトル全体の流れを管理する
def do_buttle(party,monster):
    """
    1対1のバトルを管理する。どちらかのHPが0になるまでターンを繰り返す。
    """
    print('')
    party_and_monster.print_monster_name(monster)
    time.sleep(0.3)
    print_slowly(f'が現れた！')
    print('')
    # パーティか敵モンスターのHPが0になるまでターンを繰り返す
    while party['hp'] > 0 and monster['hp'] > 0:
        on_player_turn(party,monster)
        # プレイヤーの攻撃で敵を倒した場合、敵のターンをスキップ
        if monster['hp'] <= 0:
            continue
        on_enemy_turn(party,monster)

    # 敵モンスターのHPが0以下になった場合
    if monster['hp'] <= 0:
        party_and_monster.print_monster_name(monster)
        time.sleep(0.3)
        print_slowly(f'を倒した！')
        # 敵を倒したので1を返す
        return 1
    # パーティのHPが0以下になった場合
    else:
        # 負けたので0を返す
        return 0

# ダンジョンでのバトルを管理する
def go_dungeon(party,monster_list):
    """
    ダンジョン内の複数のバトルを管理する。
    """
    time.sleep(0.3)
    print_slowly(f'{party['player_name']}のパーティ(HP = {party['hp']})はダンジョンに到着した')
    time.sleep(0.3)
    print('<パーティー編成>-----------------------')
    party_and_monster.show_party(party)
    time.sleep(0.3)
    print('-----------------------------------')
    monster_defeated = 0

    # モンスターリストの各モンスターと順にバトル
    for monster in monster_list:
        is_win = do_buttle(party,monster)
        # パーティのHPが0以下になった場合
        if party['hp'] <= 0:
            time.sleep(0.3)
            print_slowly('パーティのHPは0になった')
            time.sleep(1.0)
            print_slowly(f'「{party['player_name']}はダンジョンから逃げ出した」')
            break
        # パーティのHPが残っている場合
        else:
            time.sleep(0.3)
            print_slowly(f'「{party['player_name']}はさらに奥へと進んだ」')
            print('=====================================')
            monster_defeated += is_win

    # 倒したモンスター数がモンスターリストの数と一致する場合
    if monster_defeated == len(monster_list):
        time.sleep(1.0)
        print_slowly(f'{party['player_name']}はダンジョンを制覇した')
        return monster_defeated
    # それ以外の場合
    else:
        return monster_defeated