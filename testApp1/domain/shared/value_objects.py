from __future__ import annotations  # 型ヒントを遅延評価

class Weight:
    """
    重量クラス
    
    Attributes:
        amount(float):重量(kg)
    """
    amount:float

    def __init__(self,weight):
        self.amount = weight
    def to_dict(self):
        return {
            "weight":self.amount
        }
    def __str__(self):
        return str(self.amount)

    def round_by_referece_weight(self, reference_weight:Weight):
        """
        自身の重量を、引数の基準重量で丸めた値を返却するメソッド

        例）基準重量2.5kg：71kg → 70kgと72.5kgのうち、より近い70kgを返却する。
        ※軽い方と重い方が同じ差の場合、重い方を採用する。
        
        Args:
            reference_weight(Weight):基準重量
        Returns:
            Weight:基準重量で丸めた値
        """
        # 基準重量で割った商
        quotient = round(self.amount) // reference_weight.amount

        # 基準重量に則した重量のうち、より軽い方
        lighter_weight = Weight(reference_weight.amount * quotient)
        # 基準重量に則した重量のうち、より重い方
        heavier_weight = Weight(reference_weight.amount * (quotient + 1))

        # 自身の重量により近い方を戻り値として採用する（差が同じ場合は重い方を採用）
        amount_diff_lighter = abs(self.amount - lighter_weight.amount)
        amount_diff_heavier = abs(self.amount - heavier_weight.amount)
        rounded_weight = heavier_weight if amount_diff_heavier <= amount_diff_lighter else lighter_weight

        return rounded_weight

class Percentage:
    """
    パーセンテージクラス
    
    Attributes:
        amount(float):パーセンテージ
    """
    amount:float

    def __init__(self,percentage):
        self.amount = percentage
    def to_dict(self):
        return {
            "percentage":self.amount
        }
    def __str__(self):
        return str(self.amount)

    def convert_to_ratio(self):
        """
        比率変換メソッド

        自身のパーセンテージを比率に変換する
        例)90% → 0.9
        ※ユーザー入力は分かりやすいように%で受け取るが、計算の際は比率にする必要があるため実装

        Returns:
            float:比率
        """
        return self.amount * 0.01


class Sets:
    """
    セット数クラス
    
    Attributes:
        amount(int):セット数
    """
    amount:int
    
    def __init__(self,sets):
        self.amount = sets
    def to_dict(self):
        return {
            "sets":self.amount
        }
    def __str__(self):
        return str(self.amount)

class Reps:
    """
    レップ数クラス
    
    Attributes:
        amount(int):レップ数
    """
    amount:int

    def __init__(self,reps):
        self.amount = reps
    def to_dict(self):
        return {
            "reps":self.amount
        }
    def __str__(self):
        return str(self.amount)

class TrainingMenu:
    """
    トレーニングメニュークラス
    
    Attributes:
        weight(Weight):重量
        reps(Reps):レップ数
        sets(Sets):セット数
    """
    weight:Weight
    reps:Reps
    sets:Sets

    def __init__(self,weight:Weight,reps:Reps,sets:Sets):
        self.weight = weight
        self.reps = reps   
        self.sets = sets
    def to_dict(self):
        return {
            "weight":self.weight.to_dict(),
            "reps":self.reps.to_dict(),
            "sets":self.sets.to_dict()
        }