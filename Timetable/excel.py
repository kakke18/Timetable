###############################################################
# Excel関連
# load_excel: 授業を読み込む
# load_teacher: 先生を読み込む
# write_excel: Excelに書き込む
###############################################################

# インポート
import xlrd
import xlwt
import teacher
import subject


# 定数
GRADE = 7
CLASS = 5
CLASS_S = 2
DAY = 5
TIME = 5
CLASS_T = 7
TEACHERNUM = 29


class Load:
    def load_excel(self):
        ###Excel###
        book = xlrd.open_workbook('Excel\Subject_zenki.xls')
        sheet = book.sheet_by_index(0)

        ###初期化###
        sub = []
        graduation = []
        specsub = []
        choicesub = []
        simusub = []

        ###読み込み###
        for row in range(1, sheet.nrows):
            # 空欄じゃない
            if(sheet.cell(row, 1).value != ''):
                # 卒研
                if('卒研' in sheet.cell(row, 1).value):
                    self.load_graduation(sheet, row, graduation)

                # 選択教科
                elif(int((sheet.cell(row, 2).value / 100) % 10) == 6):
                    self.load_choicesub(sheet, row, choicesub)

                # 帯教科
                elif(int((sheet.cell(row, 2).value / 100) % 10) == 7):
                    self.load_simusub(sheet, row, simusub)

                # 特別教室
                elif(sheet.cell(row, 10).value != ''):
                    self.load_specsub(sheet, row, specsub)

                # その他
                else:
                    self.load_sub(sheet, row, sub)

        return graduation, choicesub, simusub, specsub, sub

    def load_graduation(self, sheet, row, graduation):
        # 引数
        args = {
            "subname": sheet.cell(row, 1).value,
            "subcode": sheet.cell(row, 2).value,
            "cont": sheet.cell(row, 11).value
        }

        # graduationに代入
        graduation.append(subject.Special(**args))

    def load_choicesub(self, sheet, row, choicesub):
        # 初期化
        choicenum = int(sheet.cell(row, 3).value)

        # リスト初期化
        choicecode = []

        # リストに代入
        for col in range(4, 4 + choicenum):
            choicecode.append(sheet.cell(row, col).value)

        # 引数
        args = {
            "subname": sheet.cell(row, 1).value,
            "subcode": sheet.cell(row, 2).value,
            "choicenum": choicenum,
            "choicecode": choicecode
        }

        # choicesubに代入
        choicesub.append(subject.Choice(**args))

    def load_simusub(self, sheet, row, simusub):
        # 初期化
        teachernum = int(sheet.cell(row, 3).value)
        simunum = int(sheet.cell(row, 12).value)

        # リスト初期化
        teachercode = []
        simucode = []

        # リストに代入
        for col in range(4, 4 + teachernum):
            teachercode.append(sheet.cell(row, col).value)
        for col in range(13, 13 + simunum):
            simucode.append(sheet.cell(row, col).value)

        # 引数
        args = {
            "subname": sheet.cell(row, 1).value,
            "subcode": sheet.cell(row, 2).value,
            "teachernum": teachernum,
            "teachercode": teachercode,
            "spec": sheet.cell(row, 10).value,
            "cont": sheet.cell(row, 11).value,
            "simunum": simunum,
            "simucode": simucode
        }

        # simusubに代入
        simusub.append(subject.Special(**args))

    def load_specsub(self, sheet, row, specsub):
        # 初期化
        teachernum = int(sheet.cell(row, 3).value)
        if(sheet.cell(row, 12).value == ''):
            simunum = 0
        else:
            simunum = int(sheet.cell(row, 12).value)

        # リスト初期化
        teachercode = []
        simucode = []

        # リストに代入
        for col in range(4, 4 + teachernum):
            teachercode.append(sheet.cell(row, col).value)
        for cok in range(13, 13 + simunum):
            simucode.append(sheet.cell(row, col).value)

        # 引数
        args = {
            "subname": sheet.cell(row, 1).value,
            "subcode": sheet.cell(row, 2).value,
            "teachernum": teachernum,
            "teachercode": teachercode,
            "spec": sheet.cell(row, 10).value,
            "cont": sheet.cell(row, 11).value,
            "simunum": simunum,
            "simucode": simucode
        }

        # specsubに代入
        specsub.append(subject.Special(**args))

    def load_sub(self, sheet, row, sub):
        # 初期化
        teachernum = int(sheet.cell(row, 3).value)
        if(sheet.cell(row, 12).value == ''):
            simunum = 0
        else:
            simunum = int(sheet.cell(row, 12).value)

        # リスト初期化
        teachercode = []

        # リストに代入
        for col in range(4, 4 + teachernum):
            teachercode.append(sheet.cell(row, col).value)

        # 引数
        args = {
            "subname": sheet.cell(row, 1).value,
            "subcode": sheet.cell(row, 2).value,
            "teachernum": teachernum,
            "teachercode": teachercode,
        }

        # データに代入
        sub.append(subject.Normal(**args))

    ###先生の読み込み###
    def load_teacher(self, data_teacher):
        ###Excel###
        book = xlrd.open_workbook('Excel\Subject_zenki.xls')
        sheet = book.sheet_by_index(1)

        ###読み込み###
        for row in range(1, sheet.nrows):
            if(sheet.cell(row, 8).value != ''):
                args = {
                    "teachername": sheet.cell(row, 10).value,
                    "charge": sheet.cell(row, 9).value,
                    "teachercode": sheet.cell(row, 8).value,
                    "part": sheet.cell(row, 11).value
                }

                data_teacher.append(teacher.Teacher(**args))


###書き込み###
class Write:
    def write_excel(self, timetable, teacher, arg_str, penalty_history, penalty=0, ):
        # Excel
        book = xlwt.Workbook()
        newsheet1 = book.add_sheet('Student')
        newsheet2 = book.add_sheet('Teacher')
        newsheet3 = book.add_sheet('Penalty')

        # オブジェクト生成
        obj = Write()

        # ペナルティ
        newsheet1.write(0, 0, penalty)

        # 学生
        obj.write_student(newsheet1, timetable)

        # 先生
        obj.write_teacher(newsheet2, teacher)

        # ペナルティ
        obj.write_penalty(newsheet3, penalty_history)

        # セーブ
        book.save(arg_str)

    def write_student(self, sheet, timetable):
        # スタイル
        pat1 = xlwt.Pattern()
        pat1.pattern = xlwt.Pattern.SOLID_PATTERN
        pat1.pattern_fore_colour = 0x0A
        style1 = xlwt.XFStyle()
        style1.pattern = pat1
        pat2 = xlwt.Pattern()
        pat2.pattern = xlwt.Pattern.SOLID_PATTERN
        pat2.pattern_fore_colour = 0x0B
        style2 = xlwt.XFStyle()
        style2.pattern = pat2
        pat3 = xlwt.Pattern()
        pat3.pattern = xlwt.Pattern.SOLID_PATTERN
        pat3.pattern_fore_colour = 0x0C
        style3 = xlwt.XFStyle()
        style3.pattern = pat3

        for grade in range(GRADE):
            # クラス数
            if(grade < 5):
                classnum = CLASS
            else:
                classnum = CLASS_S

            for cla in range(classnum):
                # クラス
                if(grade == 0):
                    chr1 = str(grade + 1) + '-' + str(cla + 1)
                elif(grade < 5):
                    if(cla == 0):
                        depart = 'M'
                    elif(cla == 1):
                        depart = 'E'
                    elif(cla == 2):
                        depart = 'D'
                    elif(cla == 3):
                        depart = 'J'
                    else:
                        depart = 'C'
                    chr1 = depart + str(grade + 1)
                else:
                    if(cla == 0):
                        depart = 'P'
                    else:
                        depart = 'S'
                    chr1 = depart + str(grade - 4)

                sheet.write(grade * 9 + 1, cla * 7, chr1)

                # 時間
                for time in range(TIME):
                    chr2 = str(time + 1) + '時限'
                    sheet.write(grade * 9 + time + 3, cla * 7, chr2)

            # 曜日
            for col in range(0, classnum * 7):
                if(col % 7 == 0):
                    chr3 = '時/曜'
                elif(col % 7 == 1):
                    chr3 = '月'
                elif(col % 7 == 2):
                    chr3 = '火'
                elif(col % 7 == 3):
                    chr3 = '水'
                elif(col % 7 == 4):
                    chr3 = '木'
                elif(col % 7 == 5):
                    chr3 = '金'
                elif(col % 7 == 6):
                    chr3 = ''
                sheet.write(grade * 9 + 2, col, chr3)

        # 時間割
        for grade in range(1, GRADE + 1):
            for cla in range(1, CLASS + 1):
                for day in range(DAY):
                    for time in range(TIME):
                        if(hasattr(timetable[grade][cla][day][time], 'subname')):
                            if(timetable[grade][cla][day][time].fix_flag is False and timetable[grade][cla][day][time].over_flag):
                                sheet.write((grade - 1) * 9 + time + 3, day + (cla - 1)
                                            * 7 + 1, timetable[grade][cla][day][time].subname, style3)
                            elif(timetable[grade][cla][day][time].fix_flag is False):
                                sheet.write((grade - 1) * 9 + time + 3, day + (cla - 1)
                                            * 7 + 1, timetable[grade][cla][day][time].subname, style2)
                            elif(timetable[grade][cla][day][time].over_flag):
                                sheet.write((grade - 1) * 9 + time + 3, day + (cla - 1)
                                            * 7 + 1, timetable[grade][cla][day][time].subname, style1)
                            else:
                                sheet.write((grade - 1) * 9 + time + 3, day + (
                                    cla - 1) * 7 + 1, timetable[grade][cla][day][time].subname)

    def write_teacher(self, sheet, teacher):
        # スタイル
        pat1 = xlwt.Pattern()
        pat1.pattern = xlwt.Pattern.SOLID_PATTERN
        pat1.pattern_fore_colour = 0x0A
        style1 = xlwt.XFStyle()
        # 曜日
        col = 2
        for day in range(DAY):
            for time in range(TIME + 1):
                if(time == 5):
                    chr4 = ''
                elif(day == 0):
                    chr4 = '月'
                elif(day == 1):
                    chr4 = '火'
                elif(day == 2):
                    chr4 = '水'
                elif(day == 3):
                    chr4 = '木'
                elif(day == 4):
                    chr4 = '金'
                sheet.write(0, col, chr4)
                if(time != 5):
                    sheet.write(1, col, time + 1)
                col += 1

        # 代入
        data_teacher = []
        excel = Load()
        excel.load_teacher(data_teacher)

        for t_num in range(len(data_teacher)):
            cla_t = int(data_teacher[t_num].teachercode / 100)
            num = data_teacher[t_num].teachercode % 100

            # 先生のコード・名前
            sheet.write(t_num + 2, 0, data_teacher[t_num].teachercode)
            sheet.write(t_num + 2, 1, data_teacher[t_num].teachername)

            char = Write()

            # 教科
            for day in range(DAY):
                for time in range(TIME):
                    if(teacher[cla_t][num][day][time] is not None):
                        if(len(teacher[cla_t][num][day][time]) > 5):
                            sheet.write(t_num + 2, day * 6 + time + 2,
                                        teacher[cla_t][num][day][time], style1)
                        else:
                            sheet.write(t_num + 2, day * 6 + time + 2,
                                        teacher[cla_t][num][day][time])
    
    def write_penalty(self, sheet, penalty_history):
        # 書き込み
        for row in range(len(penalty_history)):
            # ペナルティ計算
            penalty = 0
            num = penalty_history[row]
            num1 = 0
            num2 = 0
            num3 = 0

            # ハード制約
            if num >= 1000000:
                num1 = int(num / 1000000)
                num = num % 1000000
            if num >= 10000:
                num2 = int(num / 10000)
                num = num % 10000
            if num >= 100:
                num3 = int(num / 100)
                num = num % 100
            hard = num1 + num2 + num3
            penalty = hard * 100

            # ソフト制約
            penalty += num

            sheet.write(row, 0, penalty)
    
    '''
    def write_place(self, sheet, timetable):
        library = [[0 for i2 in range(TIME)] for i1 in range(DAY)]
        chemistry = [[0 for i2 in range(TIME)] for i1 in range(DAY)]
        pe = [[0 for i2 in range(TIME)] for i1 in range(DAY)]

        # 化学で使う教室は月2,火34は使えない
        chemistry[0][1] = 1
        chemistry[1][2] = 1
        chemistry[1][3] = 1

        for grade in range(1, GRADE + 1):
            for class_ in range(1, CLASS + 1):
                for day in range(DAY):
                    for time in range(TIME):
                        if(hasattr(timetable[grade][class_][day][time], 'subname')):
                            if '英' in timetable[grade][class_][day][time].subname and '図' in timetable[grade][class_][day][time].subname:
                                library[day][time] += 1
                            if '化学' in timetable[grade][class_][day][time].subname:
                                chemistry[day][time] += 1
                            if('保体' in timetable[grade][class_][day][time].subname or '体育' in timetable[grade][class_][day][time].subname):
                                pe[day][time] += 1

        for day in range(DAY):
            for time in range(TIME):
                col = day * (DAY + 1) + time + 1
                if(library[day][time] > 2):
                    sheet.write(2, col, '○')
                if(chemistry[day][time] > 1):
                    sheet.write(3, col, '○')
                if(pe[day][time] > 2):
                    sheet.write(4, col, '○')

                if(time == 5):
                    chr5 = ''
                elif(day == 0):
                    chr5 = '月'
                elif(day == 1):
                    chr5 = '火'
                elif(day == 2):
                    chr5 = '水'
                elif(day == 3):
                    chr5 = '木'
                elif(day == 4):
                    chr5 = '金'
                sheet.write(0, col, chr5)
                sheet.write(1, col, time + 1)
        sheet.write(2, 0, '図書館')
        sheet.write(3, 0, '化学')
        sheet.write(4, 0, '体育館')
    '''
