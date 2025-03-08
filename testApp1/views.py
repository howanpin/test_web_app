from django.shortcuts import render
from django.http import HttpResponse
from .domain.shared.value_objects import Weight,Percentage
from .domain.hps_program.value_objects import HpsProgram

def one_rm_max(request):
    if request.method == "GET":
        return render(request,'one_rm_max.html')
    
    if request.method == "POST":
        # 入力値
        input_max_weight = request.POST.get('max_weight')
        input_percentage = request.POST.get('percentage')
        input_reference_weight = request.POST.get('reference_weight')

        # 最大重量
        max_weight = Weight(float(input_max_weight))
        # パーセンテージ
        percentage = Percentage(float(input_percentage))
        # 基準重量
        reference_weight = Weight(float(input_reference_weight))      

        # 重量計算
        # -------------------------------------------------------
        # n%の重量を計算
        # -------------------------------------------------------
        raw_percent_weight = Weight(max_weight.weight * percentage.convert_to_ratio())
        # -------------------------------------------------------
        # 基準重量で丸める
        # -------------------------------------------------------
        rounded_percent_weight = raw_percent_weight.round_by_referece_weight(reference_weight)

        # 戻り値設定
        context = {}
        # -------------------------------------------------------
        # 最大重量
        # -------------------------------------------------------
        context['max_weight'] = max_weight
        # -------------------------------------------------------
        # パーセンテージ
        # -------------------------------------------------------
        context['percentage'] = percentage
        # -------------------------------------------------------
        # 基準重量
        # -------------------------------------------------------
        context['reference_weight'] = reference_weight
        # -------------------------------------------------------
        # n%の重量（実測値）
        # -------------------------------------------------------
        context['raw_percent_weight'] = raw_percent_weight
        # -------------------------------------------------------
        # n%の重量（基準重量で丸め後）
        # -------------------------------------------------------
        context['rounded_percent_weight'] = rounded_percent_weight

        return render(request,'one_rm_max.html',context)
    # GET,POST以外には空のレスポンスを返す
    return HttpResponse("")
    
def hps_program(request):
    if request.method == "GET":
        return render(request,'hps_program.html')
    
    if request.method == "POST":
        # 入力値
        input = request.POST.get('max_weight')

        # 最大重量
        max_weight = Weight(float(input))

        # プログラム構築
        hps_program = HpsProgram(max_weight)

        context = {}
        # -------------------------------------------------------
        # プログラム作成
        # -------------------------------------------------------
        context['program'] = hps_program
        return render(request,'hps_program.html',context)
    # GET,POST以外には空のレスポンスを返す
    return HttpResponse("") 