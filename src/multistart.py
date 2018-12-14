################################################################
# マルチスタート
# multistasrt1: 手法1
# multistasrt1: 手法2，3，4
################################################################


# インポート
import annealing_optimize
import arrangement
import copy

# 定数 
MIN_PENALTY1 = 10
MIN_PENALTY2 = 0

class MultiStart:
    def multistart1(self, arg_timetable, arg_teacher, sub):
        while True:
            # コピー
            timetable = copy.deepcopy(arg_timetable)
            teacher = copy.deepcopy(arg_teacher)

            # オブジェクト生成
            obj1 = arrangement.Arrangement()
            obj2 = annealing_optimize.AnnealingOptimize()

            # 時間割配置
            obj1.arrange_timetable(sub, timetable)

            # 焼きなまし
            jikanwari, teach, penalty, penalty_history = obj2.annealingoptimize1(timetable, teacher)

            if penalty <= MIN_PENALTY1:
                print('success')
                print('penalty:', penalty)
                print()
                break
            else:
                print('fault')
                print()

        return jikanwari, teach, penalty, penalty_history

    def multistart2(self, arg_timetable, arg_teacher, sub):
        while True:
            # コピー
            timetable = copy.deepcopy(arg_timetable)
            teacher = copy.deepcopy(arg_teacher)

            # オブジェクト生成
            obj1 = arrangement.Arrangement()
            obj2 = annealing_optimize.AnnealingOptimize()

            # 時間割配置
            obj1.arrange_timetable(sub, timetable)

            # 焼きなまし
            jikanwari, teach, penalty, penalty_history = obj2.annealingoptimize2(
                timetable, teacher)

            if penalty <= MIN_PENALTY2:
                print('success')
                print('penalty:', penalty)
                print()
                break
            else:
                print('fault')
                print()

        return jikanwari, teach, penalty_history
