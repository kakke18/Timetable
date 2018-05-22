#####################################################
# 授業の情報
#####################################################

# 定数 MAX_TEACHERNUM: 1つの授業の最大教員人数 MAX_SIMUNUM: 同時開講授業の最大数 MAX_CHOICENUM: 同じ時間帯の選択科目の最大数
MAX_TEACHERNUM = 6
MAX_SIMUNUM = 3
MAX_CHOICENUM = 5

class Normal:
    def __init__(self, subname, subcode, teachernum, teachercode=[] * MAX_TEACHERNUM):

        self.subname = subname
        self.subcode = int(subcode)
        self.teachernum = int(teachernum)

        self.teachercode = []
        for num in range(self.teachernum):
            self.teachercode.append(int(teachercode[num]))


class Special:
    def __init__(
        self, subname, subcode, teachernum=0, teachercode=[0] * MAX_TEACHERNUM,
        spec=0, cont=0, simunum=0, simucode=[0] * MAX_SIMUNUM
    ):

        self.subname = subname
        self.subcode = int(subcode)
        self.teachernum = int(teachernum)

        self.teachercode = []
        for num in range(self.teachernum):
            self.teachercode.append(int(teachercode[num]))

        if(spec == ''):
            self.spec = 0
        else:
            self.spec = int(spec)

        if(cont == ''):
            self.cont = 0
        else:
            self.cont = int(cont)

        self.simunum = int(simunum)

        self.simucode = []
        if(self.simunum != 1):
            for num in range(self.simunum):
                self.simucode.append(int(simucode[num]))


class Choice:
    def __init__(self, subname, subcode, choicenum, choicecode=[] * MAX_CHOICENUM):
        self.subname = subname
        self.subcode = int(subcode)
        self.choicenum = int(choicenum)

        self.choicecode = []
        for num in range(self.choicenum):
            self.choicecode.append(int(choicecode[num]))
