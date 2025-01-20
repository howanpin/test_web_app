from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    if request.method == "POST":
        # 戻り値の辞書
        context = {}

        # TODO:floatにも対応する
        # フォームから送信された重量(str型のため変換を行う)
        max_weight = float(request.POST.get('max_weight'))

        # 閾値判定
        input_limit = 10
        if max_weight <= input_limit:
            context['return_value1'] = 0
            context['return_value2'] = 0
            return render(request,'index.html',context)

        # 重量計算
        calculated = __calculate_weight(max_weight)
        actual_eighty_percent_weight = calculated.get('actual_eighty_percent_weight')
        eighty_percent_weight = calculated.get('eighty_percent_weight')

        context['max_weight'] = max_weight
        context['return_value1'] = actual_eighty_percent_weight
        context['return_value2'] = eighty_percent_weight
        return render(request,'index.html',context)

def __calculate_weight(max_weight):
    context = {}
    # 80%の重量を計算（実測値）
    actual_eighty_percent_weight = max_weight * 0.8
    context['actual_eighty_percent_weight'] = actual_eighty_percent_weight

    # 2.5kg刻みで一番近い値を算出
    reference_weight = 2.5
    quotient = round(actual_eighty_percent_weight) // reference_weight
    lighter_weight = reference_weight * quotient
    heavier_weight = reference_weight * (quotient + 1)
    diff_lighter_weight = abs(actual_eighty_percent_weight - lighter_weight)
    diff_heavier_weight = abs(actual_eighty_percent_weight - heavier_weight)

    # 80%の重量（2.5kg刻み）
    eighty_percent_weight = lighter_weight if diff_lighter_weight <= diff_heavier_weight else heavier_weight
    context['eighty_percent_weight'] = eighty_percent_weight

    return context
