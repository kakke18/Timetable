################################################################################################################
# 時間割の情報
# search_teacher: 引数で与えられた学年，クラス，曜日，時間帯の授業が存在し，引数の教員コードが担当教員であった場合True
################################################################################################################


# 定数 MAX_TEACHER: 同じ時間に授業をする最大人数(1年の専門)
GRADE = 7
CLASS = 5
DAY = 5
TIME = 5
MAX_TEACHER = 14
MAX_SIMU = 3


class Timetable:
    def __init__(
        self, subname, subcode, teachernum=0, teachercode=[0] * MAX_TEACHER,
        simunum=0, simucode=[0] * MAX_SIMU, fix_flag=True, over_flag=False
    ):
        self.subname = subname
        self.subcode = int(subcode)
        self.teachernum = int(teachernum)

        self.teachercode = []
        for num in range(self.teachernum):
            self.teachercode.append(teachercode[num])

        self.simunum = int(simunum)
        self.simucode = []
        if(self.simunum != 1):
            for num in range(self.simunum):
                self.simucode.append(simucode[num])

        # 固定教科:False
        self.fix_flag = fix_flag
        self.over_flag = over_flag

    def search_teacher(self, arg_timetable, teachercode, grade, class_, day, time):
        if(hasattr(arg_timetable[grade][class_][day][time], 'subname')):
            for n in range(arg_timetable[grade][class_][day][time].teachernum):
                if(arg_timetable[grade][class_][day][time].teachercode[n] == teachercode):
                    return True
        return False
