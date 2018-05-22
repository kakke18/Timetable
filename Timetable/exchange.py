##############################################################################################
# 近傍解を生成するために2-opt法を使用
# exchange1: 先生の重複を交換
# exchange2: 空き時間をなくすように交換
# exchange3: ランダム

# exchange3は空きコマとは交換しないようにしているが，1～3年以外は交換してもいいので，改良の余地あり
##############################################################################################

# インポート
import random
import penalty

# 定数 GRADE_S: 専攻科の学年
GRADE = 5
GRADE_S = 2
CLASS = 5
DAY = 5
TIME = 5


class Exchange:
    def exchange1(self, arg_timetable):
        excha_grade = 1
        excha_class = 1
        old_day = 0
        old_time = 0

        for grade in range(1, GRADE + 1):
            for cla in range(1, CLASS + 1):
                for day in range(DAY):
                    for time in range(TIME):
                        if(hasattr(arg_timetable[grade][cla][day][time], 'subname') and arg_timetable[grade][cla][day][time].over_flag):
                            excha_grade = grade
                            excha_class = cla
                            old_day = day
                            old_time = time

        while(True):
            new_day = random.randint(0, DAY - 1)
            new_time = random.randint(0, TIME - 2)
            if(new_day == old_day and new_time == new_day):
                continue
            elif((hasattr(arg_timetable[excha_grade][excha_class][new_day][new_time], 'subname') is False) or arg_timetable[excha_grade][excha_class][new_day][new_time].fix_flag):
                break

        # 交換
        arg_timetable_t = arg_timetable[excha_grade][excha_class][old_day][old_time]
        arg_timetable[excha_grade][excha_class][old_day][old_time] = arg_timetable[excha_grade][excha_class][new_day][new_time]
        arg_timetable[excha_grade][excha_class][new_day][new_time] = arg_timetable_t

    def exchange2(self, arg_timetable):
        pena = penalty.Penalty()

        excha_flag = True
        for grade in range(1, GRADE + 1):
            for cla in range(1, CLASS + 1):
                for day in range(DAY):
                    flag, time = pena.judge_free(arg_timetable, grade, cla, day)
                    if(flag is False):
                        if(excha_flag):
                            excha_grade = grade
                            excha_class = cla
                            old_day = day
                            old_time = time
                            excha_flag = False

        while(True):
            new_day = random.randint(0, DAY - 1)
            new_time = random.randint(0, TIME - 2)
            if(new_day == old_day and new_time == new_day):
                continue
            elif((hasattr(arg_timetable[excha_grade][excha_class][new_day][new_time], 'subname') is False) or arg_timetable[excha_grade][excha_class][new_day][new_time].fix_flag):
                break

        # 交換
        arg_timetable_t = arg_timetable[excha_grade][excha_class][old_day][old_time]
        arg_timetable[excha_grade][excha_class][old_day][old_time] = arg_timetable[excha_grade][excha_class][new_day][new_time]
        arg_timetable[excha_grade][excha_class][new_day][new_time] = arg_timetable_t


    def exchange3(self, arg_timetable):
        while True:
            excha_grade = random.randint(1, GRADE+GRADE_S)
            excha_class = random.randint(1, CLASS)
            old_day = random.randint(0, DAY - 1)
            old_time = random.randint(0, TIME - 2)
            new_day = random.randint(0, DAY - 1)
            new_time = random.randint(0, TIME - 2)

            # 同じ日・時間
            if new_day == old_day and new_time == new_day:
                continue
            # どっちかが空きコマ
            if hasattr(arg_timetable[excha_grade][excha_class][old_day][old_time], 'subname') is False or hasattr(arg_timetable[excha_grade][excha_class][new_day][new_time], 'subname') is False:
                continue
            # 移動可能
            elif arg_timetable[excha_grade][excha_class][old_day][old_time].fix_flag and arg_timetable[excha_grade][excha_class][new_day][new_time].fix_flag:
                break


        # 交換
        arg_timetable_t = arg_timetable[excha_grade][excha_class][old_day][old_time]
        arg_timetable[excha_grade][excha_class][old_day][old_time] = arg_timetable[excha_grade][excha_class][new_day][new_time]
        arg_timetable[excha_grade][excha_class][new_day][new_time] = arg_timetable_t
