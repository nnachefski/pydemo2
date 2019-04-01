from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import datetime, os, string, random
from django.http import JsonResponse
from operator import itemgetter
from time import sleep
from django.middleware.csrf import get_token
#import opentracing

#tracer = settings.OPENTRACING_TRACER

def subdirs(path):
    for d in filter(os.path.isdir, os.listdir(path)):
        yield d
        
def files(path):
    for f in filter(os.path.isfile, os.listdir(path)):
        yield f

def test(request):
    ret = "<p>SourceIP: %s</p>"%str(request.META.get('REMOTE_ADDR'))
    ret += "<p>SessionID: %s</p>"%str(get_token(request))
    ret += "<p>Agent: %s</p>"%str(request.META['HTTP_USER_AGENT'])
                                               
    return HttpResponse(ret)

def dt(request):
    now = datetime.datetime.now()
    html = "<html><body>%s</body></html>" % now
    
    return HttpResponse(html)

def none(request):
    html = "<html><body>Sorry, nothing found for that URL</body></html>"
    
    return HttpResponseNotFound(html)

def index(request):
    return render(request, 'index.html', {'name': settings.PROJECT_NAME })

def env(request):
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": [],
 #               "extra": ''
                }
    
    for key, value in os.environ.items():
#        if key == 'PYDEMO_SERVICE_HOST':
#            ret_dict['extra'] = value[:80]
        ret_dict['data'].append((key[:30], value[:80]))
        ret_dict['recordsTotal'] += 1

    ret_dict['data'] = sorted(ret_dict['data'])
    
    return JsonResponse(ret_dict)

def proc(request):
                  
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
                }
    
    processoutput = os.popen("ps -Af").read()
    for proc in processoutput.split('\n')[1:]:
        output = proc.split()
        if output:
            name = output[7].split('/')[-1]
            if ']' in name:
                continue
            line = (name[:30], output[0], output[1], output[2], " ".join(output[8:]))
            ret_dict['data'].append(line)
            ret_dict['recordsTotal'] += 1
    
    ret_dict['data'] = sorted(ret_dict['data'],key=itemgetter(1))
   
    return JsonResponse(ret_dict)

def file(request):
    p = '.'
    html = '<ul>'
    for d in subdirs(p):
        html = html + "<li>%s</li>"%(d)
        for f in files(p+'/'+d):
            html = html + "<li>%s</li>"%(f)
            
    for f in files(p+'/'+d):
        html = html + "<li>%s</li>"%(f)
                    
    html = html + '</ul>'

    return HttpResponse(html)

def verb(request):
    out = ' '
    msg = ' '
    if request.method == 'GET':
        if 'action' in request.GET and 'seconds' in request.GET:
            msg = "Completed '%s' for '%s' seconds"%(request.GET['action'], request.GET['seconds'])
            if request.GET['action'] == 'hang':
                out = out + os.popen("kill -s STOP 1 && sleep %s && kill -s CONT 1"%request.GET['seconds']).read()
                print (out)
                
            elif request.GET['action'] == 'fileio':
                endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(request.GET['seconds']))
                while True:
                    if datetime.datetime.now() >= endTime:
                        os.popen("rm -rf testing.txt")
                        break
                    else:
                        with open('testing.txt', 'a') as out:
                            randtxt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(200))
                            out.write(randtxt + '\n')
            
            elif request.GET['action'] == 'load':
                endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(request.GET['seconds']))
                while True:
                    if datetime.datetime.now() >= endTime:
                        break
                    else:
                        x = 987239478234879 * 98723947823947
                        
        elif request.GET['action'] == 'kill':
            out = out + os.popen("kill 1").read()
            print (out)
            msg = "exiting container.... Bye!"
                
    return HttpResponse(msg+"\n"+out)



