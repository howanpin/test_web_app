from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
    if request.method == "POST":
        context = {}

        # フォームから送信された重量(str型のため変換を行う)
        max_weight = float(request.POST.get('max_weight'))

        # 閾値判定
        input_limit = 10
        if max_weight <= input_limit:
            # 戻り値設定
            context['max_weight'] = 0
            context['actual_eighty_percent_weight'] = 0
            context['eighty_percent_weight'] = 0
            return render(request,'index.html',context)

        # 重量計算
        reference_weight = 2.5
        calculated = __calculate_weight(max_weight,reference_weight)

        # 戻り値設定
        context = calculated
        context['max_weight'] = max_weight

        return render(request,'index.html',context)

# 最大重量の80%/70%について、実値と基準重量で丸めた値を返却する
# [パラメータ] max_weight       最大重量
# [パラメータ] reference_weight 基準重量
# [戻り値] {80%重量（実値）,80%重量（丸め後）,70%重量（実値）,70%重量（丸め後）}
def __calculate_weight(max_weight,reference_weight):
    context = {}

    # 80%の重量を計算（実値）
    actual_eighty_percent_weight = max_weight * 0.8
    # 基準重量で一番近い値を算出
    eighty_percent_weight = __round_by_ref_weight(actual_eighty_percent_weight,reference_weight)
    # 70%の重量を計算（実値）
    actual_seventy_percent_weight = max_weight * 0.7
    # 基準重量で一番近い値を算出
    seventy_percent_weight = __round_by_ref_weight(actual_seventy_percent_weight,reference_weight)

    # 戻り値設定
    context['actual_eighty_percent_weight'] = actual_eighty_percent_weight
    context['eighty_percent_weight'] = eighty_percent_weight
    context['actual_seventy_percent_weight'] = actual_seventy_percent_weight
    context['seventy_percent_weight'] = seventy_percent_weight

    return context

# 実値を基準重量で丸めた値を返却する
# [パラメータ] actual_weight    実値の重量
# [パラメータ] reference_weight 基準重量
# [戻り値] 実値を基準重量で丸めた値
def __round_by_ref_weight(actual_weight,reference_weight):

    # 実値を基準重量で割った商
    quotient = round(actual_weight) // reference_weight

    # 基準重量に則した重量のうち、actual_weightより軽い方
    lighter_weight = reference_weight * quotient
    # 基準重量に則した重量のうち、actual_weightより重い方
    heavier_weight = reference_weight * (quotient + 1)

    # actual_weightに近い方を採用
    diff_lighter_weight = abs(actual_weight - lighter_weight)
    diff_heavier_weight = abs(actual_weight - heavier_weight)
    rounded_weight = lighter_weight if diff_lighter_weight <= diff_heavier_weight else heavier_weight

    return rounded_weight