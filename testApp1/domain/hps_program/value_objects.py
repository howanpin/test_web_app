from ..shared.value_objects import TrainingMenu, Weight, Reps, Sets
from .enums import WeekNumberEnum,MenuTypeEnum
from .constants import REFERENCE_WEIGHT
from .settings import TrainingMenuSettings

class HpsProgram:
    """
    HPSプログラムクラス
    
    1～6週目のメニューを持つ
    
    Attributes:
        max_weight(Weight):ユーザーが入力した最大重量
        hps_menus_for_weeks(Tuple[HpsMenuPerWeek,...]):1～6週目のメニュー（筋肥大,パワー,筋力）
    """
    def __init__(self,max_weight:Weight):
        # 最大重量
        self.max_weight = max_weight
        # 1～6週目のメニュー
        self.hps_menus_for_weeks = self.__create_hps_menus_for_weeks(max_weight)
    def to_dict(self):
        return {
            "max_weight":self.max_weight,
            "hps_menus_for_weeks":self.hps_menus_for_weeks
        }
    def __create_hps_menus_for_weeks(self,max_weight:Weight):
        """
        コンストラクタのヘルパーメソッド
        
        Args:
            max_weight(Weight):ユーザーが入力した最大重量
        Returns:
            Tuple[HpsMenuPerWeek,...]:1～6週目のメニュー（筋肥大,パワー,筋力）
        """
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


class HpsMenusPerWeek:
    """
    週ごとのメニュークラス
    
    筋肥大,パワー,筋力の3つのメニューを持つ
    
    Attributes:
        week_number(WeekNumberEnum):何週目なのかの情報
        h_menu(TrainingMenuForHps):筋肥大のメニュー
        p_menu(TrainingMenuForHps):パワーのメニュー
        s_menu(TrainingMenuForHps):筋力のメニュー
    """

    def __init__(self,max_weight:Weight,week_number:WeekNumberEnum):
       # 何週目のメニューか
       self.week_number = week_number
       # 筋肥大の日のメニュー
       self.h_menu = TrainingMenuForHps(max_weight,week_number,MenuTypeEnum.HYPERTROPHY)
       # パワーの日のメニュー
       self.p_menu = TrainingMenuForHps(max_weight,week_number,MenuTypeEnum.POWER)
       # 筋力の日のメニュー
       self.s_menu = TrainingMenuForHps(max_weight,week_number,MenuTypeEnum.STRENGTH)
    def to_dict(self):
        return {
            "week_number":self.week_number.value,
            "h_menu":self.h_menu,
            "p_menu":self.p_menu,
            "s_menu":self.s_menu
        }
   

class TrainingMenuForHps(TrainingMenu):
    """
    HPS用メニュークラス
    
    通常のトレーニングメニューの情報（重量/レップ数/セット数）に加えて、何週目なのかの情報とメニュー種別の情報を持つ
    
    Attributes:
        week_number(WeekNumberEnum):何週目なのかの情報
        menu_type(MenuTypeEnum):筋肥大,パワー,筋力のうち、どのメニューなのかの情報
        weight(Weight):重量 ※親クラスから継承
        reps(Reps):レップ数 ※親クラスから継承
        sets(Sets):セット数 ※親クラスから継承
    """

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
    def to_dict(self):
        return {
            "week_number":self.week_number.value,
            "menu_type":self.menu_type.value
        }

    def __choose_weight(self,max_weight:Weight):
        """
        セットの重量選択メソッド

        セットの重量 = ユーザーが入力した最大重量*比率
        ※算出した重量は基準重量で丸める
        
        Args:
            max_weight(Weight):ユーザーが入力した最大重量
        Returns:
            Weight:セットの重量
        """
        # 比率選択
        ratio = self.__choose_ratio()
        # 基準重量参照
        reference_weight = Weight(REFERENCE_WEIGHT)
        return Weight(max_weight.amount * ratio).round_by_referece_weight(reference_weight)
    
    def __choose_ratio(self):
        """
        比率の選択メソッド

        比率は週とメニュー種別で決まる
        
        Returns:
            float:比率
        """
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            return TrainingMenuSettings.HYPERTROPHY_WEIGHT_RATIO.get(self.week_number)  
        # パワーの場合
        if(self.__isPower()):
            return TrainingMenuSettings.POWER_WEIGHT_RATIO.get(self.week_number)  
        # 筋力の場合
        if(self.__isStrength()):
            return TrainingMenuSettings.STRENGTH_WEIGHT_RATIO.get(self.week_number)

    def __choose_reps(self):
        """
        レップ数の選択メソッド

        レップ数はメニュー種別で決まる
        
        Returns:
            Reps:レップ数
        """
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            return Reps(TrainingMenuSettings.REPS.get(MenuTypeEnum.HYPERTROPHY))   
        # パワーの場合
        if(self.__isPower()):
            return Reps(TrainingMenuSettings.REPS.get(MenuTypeEnum.POWER))      
        # 筋力の場合
        if(self.__isStrength()):
            return Reps(TrainingMenuSettings.REPS.get(MenuTypeEnum.STRENGTH)) 
        
    def __choose_sets(self):
        """
        セット数の選択メソッド

        セット数は週とメニュー種別で決まる
        
        Returns:
            Sets:セット数
        """
        # 筋肥大の場合
        if(self.__isHypertrophy()):
            return Sets(TrainingMenuSettings.HYPERTROPHY_SETS.get(self.week_number))     
        # パワーの場合
        if(self.__isPower()):
            return Sets(TrainingMenuSettings.POWER_SETS.get(self.week_number))     
        # 筋力の場合
        if(self.__isStrength()):
            return Sets(TrainingMenuSettings.STRENGTH_SETS.get(self.week_number))     
    
    def __isHypertrophy(self):
        """判定ロジック：トレーニング種別判定(筋肥大)"""
        return self.menu_type == MenuTypeEnum.HYPERTROPHY 
    def __isPower(self):
        """判定ロジック：トレーニング種別判定(パワー)"""
        return self.menu_type == MenuTypeEnum.POWER
    def __isStrength(self):
        """判定ロジック：トレーニング種別判定(筋力)"""
        return self.menu_type == MenuTypeEnum.STRENGTH
