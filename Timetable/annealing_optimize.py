#################################################################
# 焼きなまし法
# annealingoptimize1は手法1
# annealingoptimize2は手法2，3，4
# annealingoptimize1，2の違いは，コスト値算出でhardを使うか，softを使うか
# 47～54: コスト値の値によって，交換方法を変えている
#         詳細は，exchange.pyを参照
# 58～66: コスト値算出，時間割配置→先生配置の後でなければ算出できない
#         (先生配置時に時間割のflagを変えるから)
# 93～95: マルチスタート用，変数の値は適当に設定
#################################################################

# インポート
import math
import random
import copy
import arrangement
import penalty
import exchange


# 定数
# CLASS_S:専攻科のクラス数 TEACHERNUM:各クラスごとの先生のmax CLASS_T:先生のクラス
GRADE = 7
CLASS = 5
CLASS_S = 2
DAY = 5
TIME = 5
TEACHERNUM = 29
CLASS_T = 7

MIN_PENALTY = 0
MAX_CNT = 5000


class AnnealingOptimize:
    def annealingoptimize1(self, arg_timetable, arg_teacher, temp=10000, cool=0.99):
        # 初期化
        cnt = 0
        penal = 1000000

        # 解の記録
        penalty_history = []
        
        # オブジェクト生成
        obj1 = exchange.Exchange()
        obj2 = penalty.Penalty()
        obj3 = arrangement.Arrangement()
        
        # 探索
        while penal > MIN_PENALTY or cnt < MAX_CNT:
            # 交換
            old_timetable = copy.deepcopy(arg_timetable)
            if(penal >= 1000000):
                obj1.exchange1(arg_timetable)
            elif(penal >= 10000):
                obj1.exchange2(arg_timetable)
            else:
                obj1.exchange3(arg_timetable)

            # 先生配置
            old_teacher = copy.deepcopy(arg_teacher)
            new_teacher = copy.deepcopy(arg_teacher)
            obj3.arrange_teacher(old_timetable, old_teacher)
            obj3.arrange_teacher(arg_timetable, new_teacher)

            # ペナルティを計算
            old_pena = obj2.calc_penalty_soft(old_timetable, old_teacher)
            new_pena = obj2.calc_penalty_soft(arg_timetable, new_teacher)

            # 温度から確立を定義
            pro = pow(math.e, -abs(new_pena - old_pena) / temp)

            # コストを比較し改善 or 確率
            if(new_pena < old_pena or random.random() < pro):
                penal = new_pena
                teacher = copy.copy(new_teacher)
            else:
                arg_timetable = copy.deepcopy(old_timetable)
                penal = old_pena
                teacher = copy.copy(old_teacher)
            
            # 温度を下げる
            temp = temp * cool

            # カウントインクリメント
            cnt += 1

            # 表示
            if cnt % 100 == 0:
                print('penalty:', penal)
                print('count   :', cnt)
                print()
            
            # 探索が停滞
            if cnt > 300 and penal > 1000000:
                break

            # ペナルティ
            penalty_history.append(penal)

        # 表示
        print('----------------------')
        print('penalty: ', penal)
        print('----------------------')
        
        # 戻り値
        return arg_timetable, teacher, penal, penalty_history

    def annealingoptimize2(self, arg_timetable, arg_teacher, temp=10000, cool=0.99):
        # 初期化
        cnt = 0
        penal = 1000000

        # 解の記録
        penalty_history = []

        # オブジェクト生成
        obj1 = exchange.Exchange()
        obj2 = penalty.Penalty()
        obj3 = arrangement.Arrangement()

        while penal > MIN_PENALTY and cnt < MAX_CNT:
            # 交換
            old_timetable = copy.deepcopy(arg_timetable)
            if(penal >= 10000):
                obj1.exchange1(arg_timetable)
            elif(penal >= 100):
                obj1.exchange2(arg_timetable)
            else:
                obj1.exchange3(arg_timetable)

            # 先生配置
            old_teacher = copy.deepcopy(arg_teacher)
            new_teacher = copy.deepcopy(arg_teacher)
            obj3.arrange_teacher(old_timetable, old_teacher)
            obj3.arrange_teacher(arg_timetable, new_teacher)

            # ペナルティを計算
            old_pena = obj2.calc_penalty_hard(old_timetable)
            new_pena = obj2.calc_penalty_hard(arg_timetable)

            # 温度から確立を定義
            pro = pow(math.e, -abs(new_pena - old_pena) / temp)

            # コストを比較し改善なら or 確率
            if(new_pena < old_pena or random.random() < pro):
                penal = new_pena
                teacher = copy.copy(new_teacher)
            else:
                arg_timetable = copy.deepcopy(old_timetable)
                penal = old_pena
                teacher = copy.copy(old_teacher)

            # 温度を下げる
            temp = temp * cool

            # カウントインクリメント
            cnt += 1

            # 表示
            if cnt % 100 == 0:
                print('penalty:', penal)
                print('count   :', cnt)
                print()

            # 探索が停滞
            if cnt > 400 and penal > 10000:
                break

            # ペナルティ
            penalty_history.append(penal)

        # 表示
        print('----------------------')
        print('penalty: ', penal)
        print('----------------------')

        # 戻り値
        return arg_timetable, teacher, penal, penalty_history
