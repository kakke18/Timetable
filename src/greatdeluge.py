###################################################################################
# 大洪水法
# 福島誠"大学時間割問題のためのハイブリッドアルゴリズム"の疑似アルゴリズムを参考に修正
# greatdeluge2opt: 文献を参考にしたもの
# greardelugels: 文献のものに局所探索を併用したもの
# 53～62: 2-opt
# 132～152: ls
###################################################################################

# インポート
import copy
import arrangement
import penalty
import exchange


# 定数 1は2-opt，2はLS
# MAX_STAG: 最大許容停滞回数，DEC_WATER: 水位減少量，FREQ_RERISE: 再上昇頻度，RERISE: 再上昇水位
MAX_STAG1 = 2000
MAX_STAG2 = 300
DEC_WATER1 = 0.5
DEC_WATER2 = 0.25
FREQ_RERISE1 = 100
FREQ_RERISE2 = 50
RERISE1 = 1
RERISE2 = 1

class GreatDeluge:
    def greatdeluge2opt(self, arg_timetable, arg_teacher):
        # 初期化 cnt_stag:停滞回数 penalty_history:解の記録
        cnt_stag = 0
        penalty_history = []

        # オブジェクト生成
        obj1 = exchange.Exchange()
        obj2 = penalty.Penalty()
        obj3 = arrangement.Arrangement()

        # 先生配置
        teacher = copy.deepcopy(arg_teacher)
        obj3.arrange_teacher(arg_timetable, teacher)
        # ペナルティ計算  
        cost_current = obj2.calc_penalty_soft(arg_timetable, teacher)

        # 最小ペナルティ
        min_cost = cost_current
        # 初期水位
        water_level = cost_current

        # ペナルティ記録
        penalty_history.append(cost_current)

        # ループ
        while min_cost > 0 and cnt_stag < MAX_STAG1:
            ### 2-opt ###
            # コピー
            timetable = copy.deepcopy(arg_timetable)
            teacher = copy.deepcopy(arg_teacher)
            # 交換
            obj1.exchange3(timetable)
            # 先生配置
            obj3.arrange_teacher(timetable, teacher)
            # 現在のペナルティ
            cost_neigh = obj2.calc_penalty_soft(timetable, teacher)

            # 改善 or 水位以下
            if cost_current >= cost_neigh or water_level >= cost_neigh:
                # 交換を許可
                arg_timetable = copy.deepcopy(timetable)
                cost_current = cost_neigh

                # 改善
                if cost_current < min_cost:
                   # ペナルティ
                    min_cost = cost_current
                    min_timetable = copy.deepcopy(arg_timetable)
                    cnt_stag = 0

                # 水位以下
                if cost_current < water_level:
                    # 水位を下げる
                    water_level -= DEC_WATER1

                # 同じ
                if cost_current == min_cost or cost_current == water_level:
                    cnt_stag += 1
            else:
                cnt_stag += 1

            # 再上昇
            if cnt_stag % FREQ_RERISE1 == 0:
                water_level += RERISE1

            # 表示
            print('min_pena', min_cost)
            print('cur_pena', cost_current)
            print('water_level', water_level)
            print('cnt_stag', cnt_stag)
            print()
            # ペナルティ記録
            penalty_history.append(cost_current)

        obj3.arrange_teacher(min_timetable, arg_teacher)
        return arg_timetable, teacher, min_cost, penalty_history

    def greatdelugels(self, arg_timetable, arg_teacher):
        # 初期化 cnt_stag:停滞回数
        cnt_stag = 0
        penalty_history = []

        # オブジェクト生成
        obj1 = exchange.Exchange()
        obj2 = penalty.Penalty()
        obj3 = arrangement.Arrangement()

        # 先生配置
        teacher = copy.deepcopy(arg_teacher)
        obj3.arrange_teacher(arg_timetable, teacher)
        # ペナルティ計算
        cost_current = obj2.calc_penalty_soft(arg_timetable, teacher)

        # 最小ペナルティ
        min_cost = cost_current
        # 初期水位
        water_level = cost_current

        # ペナルティ記録
        penalty_history.append(cost_current)

        # ループ
        while min_cost > 0 and cnt_stag < MAX_STAG2:
            ### LocalSearch ###
            # リスト
            penal = []
            timetable = []
            teacher = []
            # 近傍探索
            for x in range(5):
                # コピー
                timetable.append(copy.deepcopy(arg_timetable))
                # 交換
                obj1.exchange3(timetable[x])
                # 先生配置
                teacher.append(copy.deepcopy(arg_teacher))
                obj3.arrange_teacher(timetable[x], teacher[x])
                # 現在のペナルティ
                penal.append(obj2.calc_penalty_soft(timetable[x], teacher[x]))
            # 最小要素
            min_element = penal.index(min(penal))
            timetable = copy.deepcopy(timetable[min_element])
            teacher = copy.deepcopy(teacher[min_element])
            cost_neigh = min(penal)

            # 改善 or 水位以下
            if cost_current >= cost_neigh or water_level >= cost_neigh:
                # 交換を許可
                arg_timetable = copy.deepcopy(timetable)
                cost_current = cost_neigh

                # 改善
                if cost_current < min_cost:
                   # ペナルティ
                    min_cost = cost_current
                    min_timetable = copy.deepcopy(arg_timetable)
                    cnt_stag = 0

                # 水位以下
                if cost_current < water_level:
                    # 水位を下げる
                    water_level -= DEC_WATER2

                # 同じ
                if cost_current == min_cost or cost_current == water_level:
                    cnt_stag += 1  
            else:
                cnt_stag += 1

            # ペナルティ
            penalty_history.append(cost_current)

            # 再上昇
            if cnt_stag % FREQ_RERISE2 == 0:
                water_level += RERISE2

            # 表示
            print('min_pena', min_cost)
            print('cur_pena', cost_current)
            print('water_level', water_level)
            print('cnt_stag', cnt_stag)
            print()
            # ペナルティ記録
            penalty_history.append(cost_current)

        obj3.arrange_teacher(min_timetable, arg_teacher)
        return min_timetable, arg_teacher, min_cost, penalty_history
