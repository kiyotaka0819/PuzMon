'''
作成日：2025/07/31
作成者：天本
'''
# インポート

# グローバル変数の宣言

# 関数宣言
def main():
    print('*** Puzzle & Monsters ***')
    name = input('プレイヤー名を入力してください > ')
    go_dungeon(name)

    finish_dungeon(name)

    print('*** GAME CLEARED!! ***')
    print(f'倒したモンスター数 = 5') # {monster_number}

def go_dungeon(name):
    print(f'{name}はダンジョンに到着した')

def finish_dungeon(name):
    print(f'{name}はダンジョンを制覇した')
    return True

# main関数の呼び出し
main()