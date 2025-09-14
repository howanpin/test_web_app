from .enums import WeekNumberEnum,MenuTypeEnum
# トレーニングメニュー用設定値
class TrainingMenuSettings:

    # 重量比率{n週目,比率}
    HYPERTROPHY_WEIGHT_RATIO = {
        WeekNumberEnum.FIRST:0.75,
        WeekNumberEnum.SECOND:0.75,
        WeekNumberEnum.THIRD:0.75,
        WeekNumberEnum.FOURTH:0.75,
        WeekNumberEnum.FIFTH:0.75,
        WeekNumberEnum.SIXTH:0.75
    }
    POWER_WEIGHT_RATIO = {
        WeekNumberEnum.FIRST:0.8,
        WeekNumberEnum.SECOND:0.8,
        WeekNumberEnum.THIRD:0.85,
        WeekNumberEnum.FOURTH:0.85,
        WeekNumberEnum.FIFTH:0.9,
        WeekNumberEnum.SIXTH:0.9
    }
    STRENGTH_WEIGHT_RATIO = {
        WeekNumberEnum.FIRST:0.85,
        WeekNumberEnum.SECOND:0.875,
        WeekNumberEnum.THIRD:0.9,
        WeekNumberEnum.FOURTH:0.9,
        WeekNumberEnum.FIFTH:0.925,
        WeekNumberEnum.SIXTH:0.95
    }
    # レップ数{種別,レップス数}
    REPS = {
        MenuTypeEnum.HYPERTROPHY:8,
        MenuTypeEnum.POWER:1,
        MenuTypeEnum.STRENGTH:"限界まで"
    }
    # セット数{n週目,セット数}
    HYPERTROPHY_SETS = {
        WeekNumberEnum.FIRST:5,
        WeekNumberEnum.SECOND:5,
        WeekNumberEnum.THIRD:5,
        WeekNumberEnum.FOURTH:5,
        WeekNumberEnum.FIFTH:5,
        WeekNumberEnum.SIXTH:5
    }
    POWER_SETS = {
        WeekNumberEnum.FIRST:5,
        WeekNumberEnum.SECOND:5,
        WeekNumberEnum.THIRD:4,
        WeekNumberEnum.FOURTH:4,
        WeekNumberEnum.FIFTH:4,
        WeekNumberEnum.SIXTH:4
    }
    STRENGTH_SETS = {
        WeekNumberEnum.FIRST:3,
        WeekNumberEnum.SECOND:3,
        WeekNumberEnum.THIRD:3,
        WeekNumberEnum.FOURTH:3,
        WeekNumberEnum.FIFTH:3,
        WeekNumberEnum.SIXTH:3
    }