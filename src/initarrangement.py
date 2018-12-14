##################################################################################
# 初期配置
# CHOICE，SIMU，SPECIALに固定時間帯を代入
# 固定時間帯をプログラムに入力するのではなく，Excelに入力した方が良い．改良の余地あり
###################################################################################

# インポート
import timetable
import subject


# 定数
GRADE = 7
CLASS = 5
CLASS_S = 2
DAY = 5
TIME = 5


class Graduation:

    def __init__(self):
        pass

    def set_(self, grad, arg_timetable):
        for num in range(len(grad)):

            # 学年・クラス算出
            a = grad[num].subcode / 100
            grade = int(a / 10)
            cla = int(a % 10)

            # 専攻科2年は水～金
            if(grade == 7):
                start = 2
            else:
                start = 3

            # 時間割配置
            for day in range(start, 5):
                for time in range(3 - grad[num].cont, 4):
                    # 引数
                    args = {
                        "subname": grad[num].subname,
                        "subcode": grad[num].subcode,
                        "fix_flag": False
                    }
                    arg_timetable[grade][cla][day][time] = timetable.Timetable(**args)


# 1年:専門1,専門2,LHR
# 2年:LHR
# 3年:選択1,LHR
# 4年:選択3,選択4
# 5年:選択7
CHOICE = [[], [5, 6, 18], [19], [14, 22], [8, 12], [7]]

class ChoiceSubject:
    def __init__(self):
        pass

    def set_(self, specsub, choicesub, arg_timetable):
        # 初期化
        count_choice = [-1 for i in range(GRADE + 1)]

        for num in range(len(choicesub)):
            # 先生
            teacher = []
            teachernum = 0

            # 学年・日付・時間計算
            grade = int(choicesub[num].subcode / 1000)
            count_choice[grade] += 1
            day = CHOICE[grade][count_choice[grade]] % DAY
            time = int(CHOICE[grade][count_choice[grade]] / DAY)

            for i in range(len(specsub)):
                for j in range(choicesub[num].choicenum):
                    if(specsub[i].subcode == choicesub[num].choicecode[j]):
                        for k in range(specsub[i].teachernum):
                            teacher.append(specsub[i].teachercode[k])
                            teachernum += 1

            for cla in range(1, CLASS + 1):
                # 引数
                args = {
                    "subname": choicesub[num].subname,
                    "subcode": choicesub[num].subcode,
                    "teachernum": teachernum,
                    "teachercode": teacher,
                    "simunum": choicesub[num].choicenum,
                    "simucode": choicesub[num].choicecode,
                    "fix_flag": False
                }
                arg_timetable[grade][cla][day][time] = timetable.Timetable(**args)


# 4年:応数A,応数A,応物Ⅰ,応物Ⅰ 5年:応数3,応数3,応物Ⅲ,応物Ⅴ,応物Ⅴ,法と倫理
# 専1年:応代数,時事英,英語演,日表文,シス技,エンデザ,流体力,水文学,材料学,ディジタル,離散数,計算機
# 専2年:代解概,科技英,シミュ工,人間工
SIMU = [[], [], [], [], [1, 14, 18, 9], [0, 1, 2, 5, 17, 6],
        [15, 5, 3, 16, 2, 6, 0, 1, 11, 11, 1, 4], [16, 6, 5, 2]]

class SimultaneousSubject:
    def __init__(self):
        pass

    def set_(self, simusub, arg_timetable):
        # 初期化
        count_simu = [-1 for i in range(GRADE + 1)]

        for num in range(len(simusub)):

            grade = int(simusub[num].subcode / 1000)
            count_simu[grade] += 1

            # 学年全体
            if(simusub[num].simunum == 1):

                if(grade < 6):
                    roop = CLASS
                else:
                    roop = CLASS_S

                day = SIMU[grade][count_simu[grade]] % DAY
                time = int(SIMU[grade][count_simu[grade]] / DAY)

                if(simusub[num].cont == 0):
                    for cla in range(1, roop + 1):
                        # 引数
                        args = {
                            "subname": simusub[num].subname,
                            "subcode": simusub[num].subcode,
                            "teachernum": simusub[num].teachernum,
                            "teachercode": simusub[num].teachercode,
                            "fix_flag": False
                        }
                        arg_timetable[grade][cla][day][time] = timetable.Timetable(
                            **args)
                else:
                    for time in range(simusub[num].cont + 1):
                        for cla in range(1, roop + 1):
                            # 引数
                            args = {
                                "subname": simusub[num].subname,
                                "subcode": simusub[num].subcode,
                                "teachernum": simusub[num].teachernum,
                                "teachercode": simusub[num].teachercode,
                                "fix_flag": False
                            }
                            arg_timetable[grade][cla][day][time] = timetable.Timetable(
                                **args)
            # 任意のクラス
            else:
                for n in range(simusub[num].simunum):
                    grade = int((simusub[num].simucode[n]) / 10)
                    cla = simusub[num].simucode[n] % 10
                    if(n == 0):
                        day = SIMU[grade][count_simu[grade]] % DAY
                        time = int(SIMU[grade][count_simu[grade]] / DAY)
                    # 引数
                    args = {
                        "subname": simusub[num].subname,
                        "subcode": simusub[num].subcode,
                        "teachernum": simusub[num].teachernum,
                        "teachercode": simusub[num].teachercode,
                        "fix_flag": False
                    }
                    arg_timetable[grade][cla][day][time] = timetable.Timetable(
                        **args)


# 1年
# 基情報
# 2年
# M:基工実  E:基実験,創造3  D:製図2  J:プロ1,基実験  C:CAD1
# 3年
# M:製図3,実習3,機工実  E:プロ1,実験1  D:CAD,プロ2,創設1,実験2  J:プロ3,OSS,実験1  C:CAD,景観
# 4年
# M:総英1,制情2,製図5,実験1  E:総英1,電子回,電デザ1,プロ4,実験3  D:総英1,プロ4,計算機,実験4  J:総英1,ソフト1,プロ言1,アルゴ,DB概,情報ネット,ゲーム,実験3  C:総英1,設計1,応測量,実験1
# 5年
# M:  E:電子Ⅲ  D:制御設  J:Web,メディア,ネット管  C:建情処,実験4
# 専1年
# S:ネット管
SPECIAL = [
    [],
    [[7], [2], [1], [0], [12]],
    [[12], [4, 1], [7], [2, 3], [3]],
    [[1, 10, 19], [1, 2], [15, 4, 18, 17], [0, 19, 12], [6, 15]],
    [[14, 5, 4, 11], [9, 4, 3, 17, 10], [13, 10, 0, 11],
    [13, 19, 18, 1, 0, 7, 4, 10], [18, 5, 17, 10]],
    [[], [0], [10], [4, 3, 11], [12, 11]],
    [[],[20]]
]


class SpecialSubject:
    def __init__(self):
        pass

    def set_(self, specsub, arg_timetable):
        # 初期化
        count_spec = [[-1 for i2 in range(CLASS + 1)]
                      for i1 in range(GRADE + 1)]

        for num in range(len(specsub)):
            if('英' in specsub[num].subname or int((specsub[num].subcode / 100) % 10) == 8 or int(specsub[num].subcode / 1000) == 8):
                if('総英中' in specsub[num].subname):
                    continue
                elif('総英' in specsub[num].subname):
                    pass
                else:
                    continue

            grade = int(specsub[num].subcode / 1000)
            cla = int((specsub[num].subcode / 100) % 10)
            count_spec[grade][cla] += 1
            day = SPECIAL[grade][cla - 1][count_spec[grade][cla]] % DAY
            time = int(SPECIAL[grade][cla - 1][count_spec[grade][cla]] / DAY)


            # 引数
            args = {
                "subname": specsub[num].subname,
                "subcode": specsub[num].subcode,
                "teachernum": specsub[num].teachernum,
                "teachercode": specsub[num].teachercode,
                "fix_flag": False
            }

            arg_timetable[grade][cla][day][time] = timetable.Timetable(**args)
            if(specsub[num].cont != 0):
                for roop in range(1, specsub[num].cont + 1):
                    arg_timetable[grade][cla][day][time +
                                                   roop] = timetable.Timetable(**args)
