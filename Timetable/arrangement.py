###########################################################
# 配置
# arrange_init_timetable: 固定授業
# arrange_timetable: 通常授業
# arrange_init_teacher: 固定授業の先生
# arrange_teacher: 通常授業の先生
############################################################

# インポート
import initarrangement
import random
import timetable

# 定数
GRADE = 7
CLASS = 5
DAY = 5
TIME = 5


class Arrangement:
    def arrange_init_timetable(self, grad, choicesub, simusub, specsub, arg_timetable):
        set1 = initarrangement.Graduation()
        set2 = initarrangement.ChoiceSubject()
        set3 = initarrangement.SimultaneousSubject()
        set4 = initarrangement.SpecialSubject()

        set1.set_(grad, arg_timetable)
        set2.set_(specsub, choicesub, arg_timetable)
        set3.set_(simusub, arg_timetable)
        set4.set_(specsub, arg_timetable)

    def arrange_timetable(self, subject, arg_timetable):
        for num in range(len(subject)):

            # 学年・クラス算出
            a = subject[num].subcode / 100
            grade = int(a / 10)
            cla = int(a % 10)

            # 選択を飛ばす
            if(grade == 8):
                continue

            while(True):
                # 乱数
                rand = random.randint(1, DAY * (TIME - 1) - 1)

                # 曜日・時間算出
                day = rand % DAY
                time = int(rand / DAY)

                # 固定授業のみ
                if(hasattr(arg_timetable[grade][cla][day][time], "fix_flag")):
                    pass
                else:
                    break

            # 引数
            args = {
                "subname": subject[num].subname,
                "subcode": subject[num].subcode,
                "teachernum": subject[num].teachernum,
                "teachercode": subject[num].teachercode
            }

            arg_timetable[grade][cla][day][time] = timetable.Timetable(**args)

    def arrange_init_teacher(self, arg_timetable, arg_teacher):
        for grade in range(1, GRADE + 1):
            for class_ in range(1, CLASS + 1):
                for day in range(DAY):
                    for time in range(TIME):
                        if(hasattr(arg_timetable[grade][class_][day][time], 'subname')):
                            for n in range(arg_timetable[grade][class_][day][time].teachernum):
                                
                                code = arg_timetable[grade][class_][day][time].teachercode[n]
                                cla = int(code / 100)
                                num = code % 100

                                # 未配置
                                if(arg_teacher[cla][num][day][time] is None):
                                    arg_teacher[cla][num][day][time] = arg_timetable[grade][class_][day][time].subname

    def arrange_teacher(self, arg_timetable, arg_teacher):
        for grade in range(1, GRADE + 1):
            for class_ in range(1, CLASS + 1):
                for day in range(DAY):
                    for time in range(TIME):
                        if(hasattr(arg_timetable[grade][class_][day][time], 'subname') and arg_timetable[grade][class_][day][time].fix_flag):
                            flag = True
                            for n in range(arg_timetable[grade][class_][day][time].teachernum):
                                code = arg_timetable[grade][class_][day][time].teachercode[n]
                                cla = int(code / 100)
                                num = code % 100

                                # 未配置
                                if(arg_teacher[cla][num][day][time] is None):
                                    arg_teacher[cla][num][day][time] = arg_timetable[grade][class_][day][time].subname
                                    if flag:
                                        arg_timetable[grade][class_][day][time].over_flag = False
                                # 被り
                                else:
                                    arg_teacher[cla][num][day][time] += arg_timetable[grade][class_][day][time].subname
                                    arg_timetable[grade][class_][day][time].over_flag = True
                                    flag = False
