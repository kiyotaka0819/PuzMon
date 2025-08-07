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

monster_list = [slime,goburin,ookoumori,dragon]

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

# **********宝石スロットのリスト**********
gems_slot = []