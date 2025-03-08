from ..shared.value_objects import TrainingMenu, Weight, Reps, Sets
from ..shared.enums import WeekNumberEnum,MenuTypeEnum

# HPSプログラムクラス　1～6週目のメニューを持つ。（1週当たりH,P,Sの3メニューで、6週分で18メニューの情報を持つ）
class HpsProgram:
    __slots__ = ["max_weight","hps_menus_for_weeks"]

    def __init__(self,max_weight:Weight):
        # 最大重量
        self.max_weight = max_weight
        # 1～6週目のメニュー
        self.hps_menus_for_weeks = self.__create_hps_menus_for_weeks(max_weight)


    def __create_hps_menus_for_weeks(self,max_weight):
        hps_menus_for_weeks = (
            #1週目メニュー
            HpsMenusPerWeek(max_weight,WeekNumberEnum.FIRST),
            #2週目メニュー            
            HpsMenusPerWeek(max_weight,WeekNumberEnum.SECOND),
            #3週目メニュー              
            HpsMenusPerWeek(max_weight,WeekNumberEnum.THIRD),
            #4週目メニュー  
            HpsMenusPerWeek(max_weight,WeekNumberEnum.FOURTH),
            #5週目メニュー  
            HpsMenusPerWeek(max_weight,WeekNumberEnum.FIFTH),
            #6週目メニュー  
            HpsMenusPerWeek(max_weight,WeekNumberEnum.SIXTH)
            )
        return hps_menus_for_weeks


# n週目のメニュークラス（H,P,Sで3メニューの情報を持つ）
class HpsMenusPerWeek:
    __slots__ = ["week_number","h_menu","p_menu","s_menu"]

    def __init__(self,max_weight:Weight,week_number:WeekNumberEnum):
       # 何週目のメニューか
       self.week_number = week_number
       # 筋肥大の日のメニュー
       self.h_menu = TrainingMenuForHps(max_weight,week_number,MenuTypeEnum.HYPERTROPHY)
       # パワーの日のメニュー
       self.p_menu = TrainingMenuForHps(max_weight,week_number,MenuTypeEnum.POWER)
       # 筋力の日のメニュー
       self.s_menu = TrainingMenuForHps(max_weight,week_number,MenuTypeEnum.STRENGTH)
   

# HPS用メニュークラス
class TrainingMenuForHps(TrainingMenu):
    __slots__ = TrainingMenu.__slots__ + ["week_number","menu_type"]
    def __init__(self,max_weight:Weight,week_number:WeekNumberEnum,menu_type:MenuTypeEnum):
        # 何週目のメニューか
        self.week_number = week_number
        # メニュー種別
        self.menu_type = menu_type

        # 重量
        weight = self.__choose_weight(max_weight)
        # レップ数
        reps = self.__choose_reps()
        # セット数
        sets = self.__choose_sets()
        super().__init__(weight,reps,sets)

    # 重量選択
    def __choose_weight(self,max_weight:Weight):
        # 比率選択
        ratio = self.__choose_ratio()
        # 基準重量設定(TODO:現状は2.5kg固定)
        reference_weight = Weight(2.5)
        return Weight(max_weight.weight * ratio).round_by_referece_weight(reference_weight)
    
    # 比率選択
    def __choose_ratio(self):
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            ratio = 0.75
            return ratio
        
        # パワーの場合
        if(self.__isPower()):
            if(self.week_number in (WeekNumberEnum.FIRST,WeekNumberEnum.SECOND)):
                ratio = 0.8
                return ratio
            elif(self.week_number in (WeekNumberEnum.THIRD,WeekNumberEnum.FOURTH)):
                ratio = 0.85
                return ratio
            elif(self.week_number in (WeekNumberEnum.FIFTH,WeekNumberEnum.SIXTH)):
                ratio = 0.9
                return ratio
        
        # 筋力の場合
        if(self.__isStrength()):
            if(self.week_number == WeekNumberEnum.FIRST):
                ratio = 0.85
                return ratio
            elif(self.week_number == WeekNumberEnum.SECOND):
                ratio = 0.875
                return ratio
            elif(self.week_number in (WeekNumberEnum.THIRD,WeekNumberEnum.FOURTH)):
                ratio = 0.9
                return ratio
            elif(self.week_number == WeekNumberEnum.FIFTH):
                ratio = 0.925
                return ratio
            elif(self.week_number == WeekNumberEnum.SIXTH):
                ratio = 0.95
                return ratio

    # レップ数選択
    def __choose_reps(self):
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            reps = 8
            return Reps(reps)
        
        # パワーの場合
        if(self.__isPower()):
            reps = 1
            return Reps(reps)
        
        # 筋力の場合
        if(self.__isStrength()):
            reps = "限界まで"
            return Reps(reps)
        
    # セット数選択
    def __choose_sets(self):
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            sets = 5
            return Sets(sets)
        
        # パワーの場合
        if(self.__isPower()):
            if(self.week_number in (WeekNumberEnum.FIRST,WeekNumberEnum.SECOND)):
                sets = 5
                return Sets(sets)
            else:
                sets = 4
                return Sets(sets)
        
        # 筋力の場合
        if(self.__isStrength()):
            sets = 3
            return Sets(sets)
    
    # トレーニング種別判定(筋肥大)
    def __isHypertrophy(self):
        return self.menu_type == MenuTypeEnum.HYPERTROPHY
    
    # トレーニング種別判定(パワー)
    def __isPower(self):
        return self.menu_type == MenuTypeEnum.POWER
    
    # トレーニング種別判定(筋力)
    def __isStrength(self):
        return self.menu_type == MenuTypeEnum.STRENGTH