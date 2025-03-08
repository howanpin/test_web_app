from ..shared.value_objects import TrainingMenu, Weight, Reps, Sets
from .constants import TrainingType

# HPSプログラムクラス　1～6週目のメニューを持つ。（1週当たりH,P,Sの3メニューで、6週分で18メニューの情報を持つ）
class HpsProgram:
    __slots__ = ["max_weight","hps_menus_for_weeks"]

    FIRST_WEEK_NUMBER = 1
    SECOND_WEEK_NUMBER = 2
    THIRD_WEEK_NUMBER = 3
    FOURTH_WEEK_NUMBER = 4
    FIFTH_WEEK_NUMBER = 5
    SIXTH_WEEK_NUMBER = 6

    def __init__(self,max_weight:Weight):
        # 最大重量
        self.max_weight = max_weight
        # 1～6週目のメニュー
        self.hps_menus_for_weeks = self.__create_hps_menus_for_weeks(max_weight)


    def __create_hps_menus_for_weeks(self,max_weight):
        # TODO：マジックナンバー解消
        hps_menus_for_weeks = (
            #1週目メニュー
            HpsMenusPerWeek(max_weight,1),
            #2週目メニュー            
            HpsMenusPerWeek(max_weight,2),
            #3週目メニュー              
            HpsMenusPerWeek(max_weight,3),
            #4週目メニュー  
            HpsMenusPerWeek(max_weight,4),
            #5週目メニュー  
            HpsMenusPerWeek(max_weight,5),
            #6週目メニュー  
            HpsMenusPerWeek(max_weight,6)
            )
        return hps_menus_for_weeks


# n週目のメニュークラス（H,P,Sで3メニューの情報を持つ）
class HpsMenusPerWeek:
    __slots__ = ["max_weight","week_number","h_menu","p_menu","s_menu"]

    def __init__(self,max_weight:Weight,week_number):
       # 最大重量
       self.max_weight = max_weight
       # 何週目のメニューか
       self.week_number = week_number
       print("週目："+str(week_number))
       # 筋肥大の日のメニュー
       self.h_menu = TrainingMenuForHps(max_weight,week_number,TrainingType.TRAINING_TYPE_H)
       # パワーの日のメニュー
       self.p_menu = TrainingMenuForHps(max_weight,week_number,TrainingType.TRAINING_TYPE_P)
       # 筋力の日のメニュー
       self.s_menu = TrainingMenuForHps(max_weight,week_number,TrainingType.TRAINING_TYPE_S)
   

# HPS用メニュークラス
class TrainingMenuForHps(TrainingMenu):
    __slots__ = TrainingMenu.__slots__ + ["week_number","menu_type"]
    def __init__(self,max_weight:Weight,week_number,menu_type:TrainingType):
        # 重量
        weight = self.__choose_weight(max_weight,week_number,menu_type)
        # レップ数
        reps = self.__choose_reps(menu_type)
        # セット数
        sets = self.__choose_sets(week_number,menu_type)
        super().__init__(weight,reps,sets)

        # 何週目のメニューか
        self.week_number = week_number
        # メニュー種別
        self.menu_type = menu_type

    # 重量選択
    def __choose_weight(self,max_weight:Weight,week_number,menu_type):
        # 比率選択
        ratio = self.__choose_ratio(menu_type,week_number)
        # 基準重量設定
        reference_weight = Weight(2.5)
        return Weight(max_weight.weight * ratio).round_by_referece_weight(reference_weight)
    
    # 比率選択
    def __choose_ratio(self,menu_type,week_number):
        # 筋肥大の場合
        if(menu_type == TrainingType.TRAINING_TYPE_H):
            ratio = 0.75
            return ratio
        
        # パワーの場合
        if(menu_type == TrainingType.TRAINING_TYPE_P):
            if(week_number in (1,2)):
                ratio = 0.8
                return ratio
            elif(week_number in (3,4)):
                ratio = 0.85
                return ratio
            elif(week_number in (5,6)):
                ratio = 0.9
                return ratio
        
        # 筋力の場合
        if(menu_type == TrainingType.TRAINING_TYPE_S):
            if(week_number == 1):
                ratio = 0.85
                return ratio
            elif(week_number == 2):
                ratio = 0.875
                return ratio
            elif(week_number in (3,4)):
                ratio = 0.9
                return ratio
            elif(week_number == 5):
                ratio = 0.925
                return ratio
            elif(week_number == 6):
                ratio = 0.95
                return ratio

    # レップ数選択
    def __choose_reps(self,menu_type):
        # 筋肥大の場合
        if(menu_type == TrainingType.TRAINING_TYPE_H):
            reps = 8
            return Reps(reps)
        
        # パワーの場合
        if(menu_type == TrainingType.TRAINING_TYPE_P):
            reps = 1
            return Reps(reps)
        
        # 筋力の場合
        if(menu_type == TrainingType.TRAINING_TYPE_S):
            reps = "限界まで"
            return Reps(reps)
        
    # セット数選択
    def __choose_sets(self,week_number,menu_type):
        # 筋肥大の場合
        if(menu_type == TrainingType.TRAINING_TYPE_H):
            sets = 5
            return Sets(sets)
        
        # パワーの場合
        if(menu_type == TrainingType.TRAINING_TYPE_P):
            if(week_number in (1,2)):
                sets = 5
                return Sets(sets)
            else:
                sets = 4
                return Sets(sets)
        
        # 筋力の場合
        if(menu_type == TrainingType.TRAINING_TYPE_S):
            sets = 3
            return Sets(sets)