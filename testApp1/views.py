from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
    if request.method == "POST":
        context = {}

        # 最大重量(str型のため変換を行う)
        max_weight = float(request.POST.get('max_weight'))

        # 重量計算
        reference_weight = 2.5
        calculated = __calculate_weight(max_weight,reference_weight)

        # 戻り値設定
        context = calculated.copy()
        context['max_weight'] = max_weight

        return render(request,'index.html',context)

# 最大重量の80%/70%について、実値と基準重量で丸めた値を返却する
# [パラメータ] max_weight       最大重量
# [パラメータ] reference_weight 基準重量
# [戻り値] {80%重量（実値）,80%重量（丸め後）,70%重量（実値）,70%重量（丸め後）}
def __calculate_weight(max_weight,reference_weight):
    context = {}

    # 80%の重量を計算（実値）
    raw_80_percent_weight = max_weight * 0.8
    # 基準重量で一番近い値を算出
    rounded_80_percent_weight = __round_by_ref_weight(raw_80_percent_weight,reference_weight)
    # 70%の重量を計算（実値）
    raw_70_percent_weight = max_weight * 0.7
    # 基準重量で一番近い値を算出
    rounded_70_percent_weight = __round_by_ref_weight(raw_70_percent_weight,reference_weight)

    # 戻り値設定
    context['raw_80_percent_weight'] = raw_80_percent_weight
    context['rounded_80_percent_weight'] = rounded_80_percent_weight
    context['raw_70_percent_weight'] = raw_70_percent_weight
    context['rounded_70_percent_weight'] = rounded_70_percent_weight

    return context

# 引数1番目の重量を基準重量で丸めた値を返却する
# [パラメータ] target_weight    丸めたい重量
# [パラメータ] reference_weight 基準重量
# [戻り値] 基準重量で丸めた値
def __round_by_ref_weight(target_weight,reference_weight):

    # 実値を基準重量で割った商
    quotient = round(target_weight) // reference_weight

    # 基準重量に則した重量のうち、target_weightより軽い方
    lighter_weight = reference_weight * quotient
    # 基準重量に則した重量のうち、target_weightより重い方
    heavier_weight = reference_weight * (quotient + 1)

    # より近い重量を採用する（差が同じ場合は重い方を採用）
    diff_lighter_weight = abs(target_weight - lighter_weight)
    diff_heavier_weight = abs(target_weight - heavier_weight)
    rounded_weight = heavier_weight if diff_heavier_weight <= diff_lighter_weight else lighter_weight

    return rounded_weight