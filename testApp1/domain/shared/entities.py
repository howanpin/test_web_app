from __future__ import annotations  # 型ヒントを遅延評価
# 重量クラス
class Weight:
    def __init__(self,weight):
        # TODO:完全コンストラクタにする
        self.weight = weight
    def __str__(self):
        return str(self.weight)

    # 基準重量の倍数のうち、self.weightに最も近いものを返却する。
    # 最も近いものが2つある場合は、より重い方の数値を採用する。
    #
    # [パラメータ] reference_weight 基準重量
    # [戻り値] 丸めた値
    def round_by_referece_weight(self, reference_weight):

        # 基準重量で割った商
        quotient = round(self.weight) // reference_weight.weight

        # 基準重量に則した重量のうち、より軽い方
        lighter_weight = Weight(reference_weight.weight * quotient)
        # 基準重量に則した重量のうち、より重い方
        heavier_weight = Weight(reference_weight.weight * (quotient + 1))

        # より近い重量を採用する（差が同じ場合は重い方を採用）
        diff_lighter_weight = abs(self.weight - lighter_weight.weight)
        diff_heavier_weight = abs(self.weight - heavier_weight.weight)
        rounded_weight = heavier_weight if diff_heavier_weight <= diff_lighter_weight else lighter_weight

        return rounded_weight
    
    # パラメータの重量に自身の重量を足した合計重量を返却する
    #
    # [パラメータ] weights 加算対象の重量
    # [戻り値] 合計重量
    def add_all(self,*weights:Weight):
        total_weight = self.weight + sum(w.weight for w in weights)
        return Weight(total_weight)


# セット数クラス
class Sets:
    def __init__(self,sets):
        # TODO:完全コンストラクタにする
        self.sets = sets
    def __str__(self):
        return str(self.sets)

# レップ数クラス
class Reps:
    def __init__(self,reps):
        # TODO:完全コンストラクタにする
        self.reps = reps
    def __str__(self):
        return str(self.reps)

# トレーニングメニュークラス
class TrainingMenu:
    def __init__(self,weight:Weight,reps:Reps,sets:Sets):
        # TODO:完全コンストラクタにする
        self.weight = weight
        self.reps = reps   
        self.sets = sets

    def calculate_total_weight(self):
        return Weight(self.weight.weight * self.reps.reps * self.sets.sets)