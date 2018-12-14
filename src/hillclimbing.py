###########################################################
# 山登り法
# 74で改善するたびに解の出力をするため2重whileにしている
###########################################################

# インポート
import copy
import arrangement
import penalty
import exchange


# 定数
MAX_STAG = 300


class HillClimbing:
    def hillclimbing(self, arg_timetable, arg_teacher, neigh):
        # 初期化 cnt:ループ回数 cnt_stag:停滞回数 penalty_history:解の記録
        cnt = 0
        cnt_stag = 0
        penalty_history = []
        
        # オブジェクト生成
        obj1 = exchange.Exchange()
        obj2 = penalty.Penalty()
        obj3 = arrangement.Arrangement()

        # 初期ペナルティ計算
        init_timetable = copy.deepcopy(arg_timetable)
        init_teacher = copy.deepcopy(arg_teacher)
        obj3.arrange_teacher(init_timetable, init_teacher)
        min_pena = obj2.calc_penalty_soft(init_timetable, init_teacher)
        print('init_penalty', min_pena)

        while True:
            while cnt_stag < MAX_STAG:
                # リスト
                pena = []
                timetable = []
                teacher = []
                
                # 近傍探索
                for x in range(neigh):
                    # 時間割
                    timetable.append(copy.deepcopy(arg_timetable))
                    # 交換
                    obj1.exchange3(timetable[x])
                    # 先生配置
                    teacher.append(copy.deepcopy(arg_teacher))
                    obj3.arrange_teacher(timetable[x], teacher[x])
                    # ペナルティ計算
                    pena.append(obj2.calc_penalty_soft(timetable[x], teacher[x]))
                
                # 表示
                if cnt % 50 == 0:
                    print('-----------step:', cnt)

                # 回数インクリメント
                cnt += 1
                cnt_stag += 1

                # ハード制約を満たし改善なら
                if min(pena) < 100 and min(pena) < min_pena:
                    min_pena = min(pena)
                    arg_timetable = copy.deepcopy(timetable[pena.index(min(pena))])
                    stagnation_cnt = 0
                    break

                # ペナルティ
                penalty_history.append(min_pena)

            # 表示
            print('penalty:', min_pena)

            if min_pena == 0 or cnt_stag > MAX_STAG:
                obj3.arrange_teacher(arg_timetable, arg_teacher)
                return arg_timetable, arg_teacher, min_pena, penalty_history
