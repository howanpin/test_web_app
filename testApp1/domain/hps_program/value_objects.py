from ..shared.value_objects import TrainingMenu, Weight, Reps, Sets
from .enums import WeekNumberEnum,MenuTypeEnum
from .constants import REFERENCE_WEIGHT
from .settings import TrainingMenuSettings

# HPSプログラムクラス　1～6週目のメニューを持つ。（1週当たりH,P,Sの3メニューで、6週分で18メニューの情報を持つ）
class HpsProgram:
    __slots__ = ["max_weight","hps_menus_for_weeks"]

    ## TODO：オブジェクトをそのまま値として格納→ブラウザのキャッシュに保存は非推奨。今回は変更コスト大のため暫定対応。
    def to_dict(self):
        return {
            "max_weight":self.max_weight,
            "hps_menus_for_weeks":self.hps_menus_for_weeks
        }

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

    def to_dict(self):
        return {
            "week_number":self.week_number.value,
            "menu_type":self.menu_type.value
        }

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

    # 重量計算
    def __choose_weight(self,max_weight:Weight):
        # 比率選択
        ratio = self.__choose_ratio()
        # 基準重量参照
        reference_weight = Weight(REFERENCE_WEIGHT)
        return Weight(max_weight.weight * ratio).round_by_referece_weight(reference_weight)
    
    # 比率選択
    def __choose_ratio(self):
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            return TrainingMenuSettings.HYPERTROPHY_WEIGHT_RATIO.get(self.week_number)  
        # パワーの場合
        if(self.__isPower()):
            return TrainingMenuSettings.POWER_WEIGHT_RATIO.get(self.week_number)  
        # 筋力の場合
        if(self.__isStrength()):
            return TrainingMenuSettings.STRENGTH_WEIGHT_RATIO.get(self.week_number)

    # レップ数選択
    def __choose_reps(self):
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            return Reps(TrainingMenuSettings.REPS.get(MenuTypeEnum.HYPERTROPHY))   
        # パワーの場合
        if(self.__isPower()):
            return Reps(TrainingMenuSettings.REPS.get(MenuTypeEnum.POWER))      
        # 筋力の場合
        if(self.__isStrength()):
            return Reps(TrainingMenuSettings.REPS.get(MenuTypeEnum.STRENGTH)) 
        
    # セット数選択
    def __choose_sets(self):
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            return Sets(TrainingMenuSettings.HYPERTROPHY_SETS.get(self.week_number))     
        # パワーの場合
        if(self.__isPower()):
            return Sets(TrainingMenuSettings.POWER_SETS.get(self.week_number))     
        # 筋力の場合
        if(self.__isStrength()):
            return Sets(TrainingMenuSettings.STRENGTH_SETS.get(self.week_number))     
    
    # 判定ロジック：トレーニング種別判定
    def __isHypertrophy(self):
        return self.menu_type == MenuTypeEnum.HYPERTROPHY 
    def __isPower(self):
        return self.menu_type == MenuTypeEnum.POWER
    def __isStrength(self):
        return self.menu_type == MenuTypeEnum.STRENGTH
