###################################################################################
# メイン
# 入力によって使用する手法を変更
# hybrid all: 同しハード制約を満たした時間割に対して，3つのハイブリッド手法を実行
###################################################################################

# インポート
import copy
import excel
import arrangement
import multistart
import hillclimbing
import greatdeluge


# 定数
GRADE = 7
CLASS = 5
DAY = 5
TIME = 5
CLASS_T = 7
TEACHERNUM = 29


# 初期化
arg_timetable = [[[[None for i4 in range(TIME)] for i3 in range(DAY)]
                for i2 in range(CLASS + 1)] for i1 in range(GRADE + 1)]
arg_teacher = [[[[None for i4 in range(TIME)] for i3 in range(DAY)]
                for i2 in range(TEACHERNUM + 1)] for i1 in range(CLASS_T + 1)]

# オブジェクト生成
obj1 = excel.Load()
obj2 = arrangement.Arrangement()
obj3 = multistart.MultiStart()
obj4 = excel.Write()
obj5 = hillclimbing.HillClimbing()
obj6 = greatdeluge.GreatDeluge()

# 手法選択
while True:
    print('0:SA 1:SA+HC 2:SA+GD 3:SA+GD(LS) 4:hybrid all')
    method = int(input('method >> '))
    if method in range(5):
        break

# 読み込み
grad, choicesub, simusub, specsub, sub = obj1.load_excel()

# 初期時間割配置
obj2.arrange_init_timetable(grad, choicesub, simusub, specsub, arg_timetable)

# 初期先生配置
obj2.arrange_init_teacher(arg_timetable, arg_teacher)

if method == 0:
    # SA
    # 焼きなまし法
    jikanwari, teacher, penalty, penalty_history = obj3.multistart1(arg_timetable, arg_teacher, sub)
    # 書き込み
    obj4.write_excel(jikanwari, teacher,'Excel\SA\Timetable.xls', penalty_history, penalty)

else:
    # 焼きなまし法
    jikanwari1, teacher1, penalty_history = obj3.multistart2(arg_timetable, arg_teacher, sub)

    if method == 1:
        # 書き込み1
        obj4.write_excel(jikanwari1, teacher1, 'Excel\HC\Timetable_hard.xls', penalty_history)
        # 山登り法
        jikanwari2, teacher2, penalty, penalty_history = obj5.hillclimbing(jikanwari1, arg_teacher, 5)
        # 書き込み2
        obj4.write_excel(jikanwari2, teacher2, 'Excel\HC\Timetable_soft.xls', penalty_history, penalty)
    elif method == 2:
        # 書き込み1
        obj4.write_excel(jikanwari1, teacher1, 'Excel\GD\Timetable_hard.xls', penalty_history)
        # 大洪水法(2-opt)
        jikanwari2, teacher2, penalty, penalty_history = obj6.greatdeluge2opt(jikanwari1, arg_teacher)
        # 書き込み2
        obj4.write_excel(jikanwari2, teacher2,'Excel\GD\Timetable_soft.xls', penalty_history, penalty)
    elif method == 3:
        # 書き込み1
        obj4.write_excel(jikanwari1, teacher1, 'Excel\GDLS\Timetable_hard.xls', penalty_history)
        # 大洪水法(LocalSearch)
        jikanwari2, teacher2, penalty, penalty_history = obj6.greatdelugels(jikanwari1, arg_teacher)
        # 書き込み2
        obj4.write_excel(jikanwari2, teacher2, 'Excel\GDLS\Timetable_soft.xls', penalty_history, penalty)
    else:
        # 書き込み1
        obj4.write_excel(jikanwari1, teacher1, 'Excel\ALL\Timetable_hard.xls', penalty_history)
        # コピー
        arg_jikanwari2 = copy.deepcopy(jikanwari1)
        arg_jikanwari3 = copy.deepcopy(jikanwari1)
        arg_jikanwari4 = copy.deepcopy(jikanwari1)
        arg_teacher1 = copy.deepcopy(arg_teacher)
        arg_teacher2 = copy.deepcopy(arg_teacher)
        arg_teacher3 = copy.deepcopy(arg_teacher)
        # 山登り法
        jikanwari2, teacher2, penalty, penalty_history = obj5.hillclimbing(arg_jikanwari2, arg_teacher1, 5)
        # 書き込み2
        obj4.write_excel(jikanwari2, teacher2,'Excel\ALL\Timetable_soft_HC.xls', penalty_history, penalty)
        # 大洪水法(2-opt)
        jikanwari3, teacher3, penalty, penalty_history = obj6.greatdeluge2opt(arg_jikanwari3, arg_teacher2)
        # 書き込み3
        obj4.write_excel(jikanwari3, teacher3, 'Excel\ALL\Timetable_soft_GD.xls', penalty_history, penalty)
        # 大洪水法(LocalSearch)
        jikanwari4, teacher4, penalty, penalty_history = obj6.greatdelugels(arg_jikanwari4, arg_teacher3)
        # 書き込み4
        obj4.write_excel(jikanwari4, teacher4, 'Excel\ALL\Timetable_soft_GDLS.xls', penalty_history, penalty)

