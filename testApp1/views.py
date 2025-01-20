from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
    if request.method == "POST":
        # 戻り値の辞書
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
        calculated = __calculate_weight(max_weight)

        # 戻り値設定
        context = calculated
        context['max_weight'] = max_weight

        return render(request,'index.html',context)

# [パラメータ]最大重量の80%の重量（実値）と、それを2.5kg単位に丸めた重量を返すメソッド
def __calculate_weight(max_weight):
    context = {}
    # 80%の重量を計算（実値）
    actual_eighty_percent_weight = max_weight * 0.8
    context['actual_eighty_percent_weight'] = actual_eighty_percent_weight

    # 2.5kg刻みで一番近い値を算出
    reference_weight = 2.5
    eighty_percent_weight = __round_by_ref_weight(actual_eighty_percent_weight,reference_weight)

    context['eighty_percent_weight'] = eighty_percent_weight

    return context

# [パラメータ]最大重量のx%の重量（実値）を[パラメータ]基準重量で丸めた値を返す
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