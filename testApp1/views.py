from django.shortcuts import render
from django.http import HttpResponse
from .domain.shared.entities import Weight
from .domain.hps_program.entities import HpsProgram

def one_rm_max(request):
    if request.method == "GET":
        return render(request,'one_rm_max.html')
    
    if request.method == "POST":
        # 入力値
        input = request.POST.get('max_weight')

        # 最大重量
        max_weight = Weight(float(input))

        # 重量計算
        # -------------------------------------------------------
        # 基準重量
        # -------------------------------------------------------
        reference_weight = Weight(2.5)
        # -------------------------------------------------------
        # 実値(90%,80%,70%)
        # -------------------------------------------------------
        raw_90_percent_weight = Weight(max_weight.weight * 0.9)
        raw_80_percent_weight = Weight(max_weight.weight * 0.8)
        raw_70_percent_weight = Weight(max_weight.weight * 0.7)
        # -------------------------------------------------------
        # 基準重量で丸める
        # -------------------------------------------------------
        rounded_90_percent_weight = raw_90_percent_weight.round_by_referece_weight(reference_weight)
        rounded_80_percent_weight = raw_80_percent_weight.round_by_referece_weight(reference_weight)
        rounded_70_percent_weight = raw_70_percent_weight.round_by_referece_weight(reference_weight)

        # 戻り値設定
        context = {}
        # -------------------------------------------------------
        # 最大重量
        # -------------------------------------------------------
        context['max_weight'] = max_weight
        # -------------------------------------------------------
        # 90%
        # -------------------------------------------------------
        context['raw_90_percent_weight'] = raw_90_percent_weight
        context['rounded_90_percent_weight'] = rounded_90_percent_weight
        # -------------------------------------------------------
        # 80%
        # -------------------------------------------------------
        context['raw_80_percent_weight'] = raw_80_percent_weight
        context['rounded_80_percent_weight'] = rounded_80_percent_weight
        # -------------------------------------------------------
        # 70%
        # -------------------------------------------------------
        context['raw_70_percent_weight'] = raw_70_percent_weight
        context['rounded_70_percent_weight'] = rounded_70_percent_weight

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
        # 最大重量
        # -------------------------------------------------------
        context['program'] = hps_program
        return render(request,'hps_program.html',context)
    # GET,POST以外には空のレスポンスを返す
    return HttpResponse("") 