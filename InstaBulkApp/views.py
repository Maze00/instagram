from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .InstaScrapper import Scrap_it, validateProfile, getSource
import copy

def index(request):
    if request.method == 'GET':
        context = {'data': [], 'nextPage' : "", 'prevPage': "" , 'username' : "", 'Next' : False, 'DownloadAll' : False}
        return render(request, 'InstaBulkApp/index.html', context)
    
    if request.method == 'POST':
        if 'Username' in request.POST:
            username = request.POST.get('Username', None)
            if(username is None or username == ""):
                context = {'data': False, 'nextPage': "",'prevPage': "" , 'username' : "",  'Next' : False, 'DownloadAll' : False}
                return render(request, 'InstaBulkApp/index.html', context)
            
            nextpagcode = ""
            prevPage = copy.copy(nextpagcode)
            
            if(validateProfile(username) != False):
                Scrapped_data, nextpagcode = Scrap_it(username, nextpagcode)
                Next = True

            else:
                Scrapped_data = False
                Next = False
                Download = False

            context = {'data': Scrapped_data, 'nextPage': nextpagcode,'prevPage': prevPage , 'username' : username,  'Next' : Next, 'DownloadAll' : False}
            return render(request, 'InstaBulkApp/index.html', context)
            
        
        elif 'next' in request.POST:
            nextpagcode = request.POST.get('next', None)
            username = request.POST.get('currentUser', None)
            prevPage = copy.copy(nextpagcode)
            
            if(validateProfile(username) != False):
                Scrapped_data, nextpagcode = Scrap_it(username, nextpagcode)

            else:
                Scrapped_data = False
            context = {'data': Scrapped_data, 'nextPage': nextpagcode, 'prevPage': prevPage , 'username': username, 'Next': True, 'DownloadAll': False}
            return render(request, 'InstaBulkApp/index.html', context)
        
        
        elif 'downloadNext' in request.POST:
            currentPage = request.POST.get('prevPage', None)
            username = request.POST.get('downloadUser', None)
            
            Scrapped_data, nextpagcode = Scrap_it(username, currentPage)
            
            context = {'data': Scrapped_data, 'nextPage': nextpagcode, 'prevPage': currentPage, 'username': username, 'Next': True, 'DownloadAll': True}
            return render(request, 'InstaBulkApp/index.html', context)