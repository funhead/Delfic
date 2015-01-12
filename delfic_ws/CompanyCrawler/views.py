from django.http import JsonResponse
from django.shortcuts import render
from CompanyCrawler.models import Company

from delfic_ws.business.data import CsvLoader
from delfic_ws.business.web import WebsiteLocator


# def index(request):
# return JsonResponse({"success": True, "message": "Site running..."})

def index(request):
    company_list = Company.objects.order_by('-Name')[:20]
    j_comps = map(lambda c: c.to_json_obj(), company_list)
    return JsonResponse(j_comps, safe=False)


def company(request, company_ref):
    f_company = Company.objects.get(pk=company_ref)
    if f_company is None:
        return JsonResponse({})
    return JsonResponse(f_company.to_json_obj())


def handle_uploaded_file(f):
    loader = CsvLoader()
    loader.handle_uploaded_file(f)


def find_company_website(request, company_ref):
    locator = WebsiteLocator()
    try:
        company_url_response = locator.find_website(company_ref)
        return JsonResponse(company_url_response)
    except Exception as ex:
        return JsonResponse({"success": False, "message": ex.message})


def find_company_links(request):
    company_url = request.GET.get('url')
    if not company_url:
        company_url = request.POST.get('url')
    locator = WebsiteLocator()
    try:
        company_url_response = locator.find_website_links(company_url)
        json_resp = company_url_response.to_json_dict()
        return JsonResponse(json_resp)
    except Exception as ex:
        return JsonResponse({"success": False, "message": ex.message})


def get_website_meta(request):
    company_url = request.GET.get('url')
    if not company_url:
        company_url = request.POST.get('url')
    locator = WebsiteLocator()
    try:
        company_url_response = locator.get_website_meta(company_url)
        json_resp = company_url_response.to_json_dict()
        return JsonResponse(json_resp)
    except Exception as ex:
        return JsonResponse({"success": False, "message": ex.message})


def get_calais_tags(request):
    company_url = request.GET.get('url')
    if not company_url:
        company_url = request.POST.get('url')
    locator = WebsiteLocator()
    try:
        company_url_response = locator.get_calais_tags(company_url)
        json_resp = company_url_response.to_json_dict()
        return JsonResponse(json_resp)
    except Exception as ex:
        return JsonResponse({"success": False, "message": ex.message})
