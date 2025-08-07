from models import data
from models import party_and_monster
from views import battle

def main():
    print('*** Puzzle & Monsters ***')
    player_name = ''
    while player_name == '':
        player_name = input('プレイヤー名を入力してください > ')
        if player_name == '':
            print('エラー：プレイヤー名を入力してください')
    monster_num = battle.go_dungeon(party_and_monster.organize_party(player_name, data.friends), data.monster_list)
    if monster_num == 5:
        print('*** GAME CLEARED!! ***')
        print(f'倒したモンスター数 = {monster_num}')
    else:
        print('*** GAME OVER!! ***')
        print(f'倒したモンスター数 = {monster_num}')
# main関数の呼び出し
main()