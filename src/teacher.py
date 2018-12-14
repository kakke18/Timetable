#########################
# 教員の情報
########################

class Teacher:
    def __init__(self, teachername, charge, teachercode, part=False):
        self.teachername = teachername
        self.charge = charge
        self.teachercode = int(teachercode)
        self.part = bool(part)
