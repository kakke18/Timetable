####################################################################################################################
# コスト値算出
# judge_free: 引数で与えられた学年，クラス，曜日で途中に空きコマがあればFalse，その時間帯を返す
# calc_duplication: 同じ曜日に同系統の授業があるかを判断
# calc_penalty_hard: ハード制約算出 交換がしやすいように制約によって値を変えている
# calc_penalty_hard: ソフト制約算出．ハード制約は100倍にしている

# 「1日に2コマ以上」という制約が1~3年までにしかできていないので，改良の余地あり

# 1~3年以外の空きコマに対する制約，教員が連続して授業を担当することに対する制約，数学，物理，化学は午前中にという制約
# これらを追加できると良い
############################################################3######################################################

# インポート
import arrangement

# 定数 TEACHERNUM: 同じ時間帯に授業をする最大人数，TEACHERNUM2: 同じクラスに属する最大教員数
GRADE = 7
CLASS = 5
DAY = 5
TIME = 5
CLASS_T = 7
TEACHERNUM = 14
TEACHERNUM2 = 29


class Penalty:
    def judge_free(self, arg_timetable, grade, cla, day):
        for time in range(TIME - 1):
            # LHRがあるので3年水曜は4コマ
            if(grade == 3 and day == 2):
                if(hasattr(arg_timetable[grade][cla][day][time], 'subname') is False):
                    return False, time
            elif((hasattr(arg_timetable[grade][cla][day][time], 'subname') is False) and (time != TIME - 2)):
                return False, time
        return True, 999

    def calc_duplication(self, list):
        s = set()
        result = []
        pena = 0

        for x in list:
            if x in s:
                result.append(x)
            s.add(x)

        if len(result) != 0:
            pena += 1

        return pena

    ###ペナルティ計算(ハード制約)###
    def calc_penalty_hard(self, arg_timetable):

        # 初期化
        penalty = 0
        judge = Penalty()
        library = [[0 for i2 in range(TIME)] for i1 in range(DAY)]
        chemistry = [[0 for i2 in range(TIME)] for i1 in range(DAY)]
        pe = [[0 for i2 in range(TIME)] for i1 in range(DAY)]
        teacher = [[[0 for i3 in range(TEACHERNUM)]
                    for i2 in range(CLASS_T)] for i1 in range(2)]

        # 化学で使う教室は月2,火34は使えない
        chemistry[0][1] = 1
        chemistry[1][2] = 1
        chemistry[1][3] = 1

        for grade in range(1, GRADE + 1):
            for cla in range(1, CLASS + 1):
                for day in range(DAY):
                    for time in range(TIME):
                        if(hasattr(arg_timetable[grade][cla][day][time], 'subname')):
                            # 先生のかぶり
                            if(arg_timetable[grade][cla][day][time].over_flag):
                                penalty += 10000

                            # 図書館
                            if('英' in arg_timetable[grade][cla][day][time].subname and '図' in arg_timetable[grade][cla][day][time].subname):
                                library[day][time] += 1
                            # 化学
                            if('化学' in arg_timetable[grade][cla][day][time].subname):
                                chemistry[day][time] += 1
                            # 体育
                            if('保体' in arg_timetable[grade][cla][day][time].subname or '体育' in arg_timetable[grade][cla][day][time].subname):
                                pe[day][time] += 1

                            # 卒研
                            if day > 2 and time > 0:
                                for n in range(arg_timetable[grade][cla][day][time].teachernum):
                                    code = arg_timetable[grade][cla][day][time].teachercode[n]
                                    # 一般科目
                                    if code > 600:
                                        break

                                    if day == 3:
                                        teacher[0][int(code / 100)
                                                   ][code % 100] += 1
                                    if day == 4:
                                        teacher[1][int(code / 100)
                                                   ][code % 100] += 1

                    # 空きコマ
                    if(grade < 4):
                        flag, t = judge.judge_free(
                            arg_timetable, grade, cla, day)
                        if(flag):
                            pass
                        else:
                            penalty += 100

        for day in range(DAY):
            for time in range(TIME):
                # 図書館
                if(library[day][time] > 2):
                    penalty += 1
                # 化学
                if(chemistry[day][time] > 1):
                    penalty += 1
                # 体育
                if(pe[day][time] > 2):
                    penalty += 1

        for day in range(2):
            for cla_t in range(CLASS_T):
                for num in range(TEACHERNUM):
                    if(teacher[day][cla_t][num] > 1):
                        penalty += 1

        # penaltyを返す
        return penalty

    ###ペナルティ計算(ソフト制約)###
    def calc_penalty_soft(self, arg_timetable, arg_teacher):
        # 親クラス・ペナルティ計算
        pena = self.calc_penalty_hard(arg_timetable) * 100

        # 判定
        for grade in range(1, 4):
            for class_ in range(1, CLASS + 1):
                # リスト
                japanese = []
                pe = []
                english = []
                eng = []
                math = []
                mathA = []
                graduation = [[0 for i2 in range(TEACHERNUM)]
                              for i1 in range(CLASS_T)]

                for day in range(DAY):
                    flag = []
                    for time in range(TIME):
                        if(hasattr(arg_timetable[grade][class_][day][time], 'subname')):
                            flag.append(time)
                            if '日本' in arg_timetable[grade][class_][day][time].subname:
                                japanese.append(day)
                            if '体' in arg_timetable[grade][class_][day][time].subname:
                                pe.append(day)
                            if '英' in arg_timetable[grade][class_][day][time].subname:
                                english.append(day)
                                if '表' not in arg_timetable[grade][class_][day][time].subname:
                                    eng.append(day)
                            if '数' in arg_timetable[grade][class_][day][time].subname:
                                math.append(day)
                                if 'A' in arg_timetable[grade][class_][day][time].subname:
                                    mathA.append(day)

                            # 卒研
                            if day > 2 and time > 0:
                                for n in range(arg_timetable[grade][class_][day][time].teachernum):
                                    code = arg_timetable[grade][class_][day][time].teachercode[n]
                                    # 一般
                                    if code > 600:
                                        break
                                    # 専門
                                    if day == 3 or day == 4:
                                        graduation[int(code / 100)
                                                   ][code % 100] += 1

                    # 1日に1コマのみなら
                    if len(flag) < 2:
                        pena += 1

                #  ペナルティ計算
                pena += self.calc_duplication(japanese)
                pena += self.calc_duplication(pe)
                pena += self.calc_duplication(english)
                pena += self.calc_duplication(math)
                if mathA[0] + 1 == mathA[1]:
                    pena += 1
                if eng[0] + 1 == eng[1]:
                    pena += 1
                if grade < 3:
                    if pe[0] + 1 == pe[1]:
                        pena += 1

        for cla_t in range(CLASS_T):
            for num in range(TEACHERNUM):
                if(graduation[cla_t][num] > 1):
                    pena += 1

        # 先生
        for cla_t in range(1, CLASS_T + 1):
            for num in range(1, TEACHERNUM2 + 1):
                for day in range(DAY):
                    teacher = []
                    for time in range(TIME):
                        # シス技は除く
                        if (arg_teacher[cla_t][num][day][time] is not None) and (arg_teacher[cla_t][num][day][time] != 'シス技'):
                            teacher.append(time)

                    '''
                    # 1日に3つ and 連続
                    if len(teacher) == 3:
                        if (teacher[0] == 0) and (teacher[1] == 1) and (teacher[2] == 2):
                            pena += 1
                        if (teacher[0] == 1) and (teacher[1] == 2) and (teacher[2] == 3):
                            pena += 1
                    
                    # 1日に4連続
                    if len(teacher) == 4:
                        pena += 1
                    '''
        return pena
