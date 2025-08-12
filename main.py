from models import data, party_and_monster
from views import battle

# メインの処理を実行する関数
def main():
    print('*** Puzzle & Monsters ***')
    player_name = ''
    # プレイヤー名が入力されるまでループ
    while player_name == '':
        player_name = input('プレイヤー名を入力してください > ')
        # プレイヤー名が空文字の場合
        if player_name == '':
            print('エラー：プレイヤー名を入力してください')

    # パーティ編成を行い、ダンジョンに挑戦
    # 倒したモンスターの数を戻り値として受け取る
    monster_num = battle.go_dungeon(party_and_monster.organize_party(player_name, data.friends), data.monster_list)

    # 倒したモンスターの数が5体の場合
    if monster_num == 5:
        print('*** GAME CLEARED!! ***')
        print(f'倒したモンスター数 = {monster_num}')
    # 倒したモンスターの数が5体でない場合
    else:
        print('*** GAME OVER!! ***')
        print(f'倒したモンスター数 = {monster_num}')

# このスクリプトが直接実行された場合にmain関数を呼び出す
if __name__ == '__main__':
    main()