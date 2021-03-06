# Create your views here.
'''
from django.http import HttpResponse
from django.template import Context,loader

def index(request):
    t = loader.get_template('index.html')
    c = Context({})
    return HttpResponse(t.render(c))
'''
import Image, ImageDraw, ImageFont, ImageFilter
import random
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import Person,Article

def rndChar():
    return chr(random.randint(65, 90))

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def drawPIL():
    width =  30 * 4
    height = 44
    image = Image.new('RGB', (width, height), (255, 255, 255))
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 36)
    draw = ImageDraw.Draw(image)
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    a = ""
    for t in range(4):
        b = rndChar()
        a += b
        draw.text((30 * t +5, 5), b, font=font, fill=rndColor2())
    image = image.filter(ImageFilter.BLUR)
    image.save('/home/developer/Github/PublicSite/blog/static/img/validation.png', 'png');
    return a

VALIDATE = ""

def list(request):
    articles = Article.objects.all()
    return render_to_response('list.html',{'articles':articles})

def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        validation = request.POST['validation']
        global VALIDATE
        # print "mytype:%s"%validation
        # print VALIDATE
        if validation == VALIDATE:
            person = Person(username=username,password=password)
            person.save()
            return render_to_response('login.html')
        else:
            return HttpResponseRedirect('/register/')
    except:
        return render_to_response('login.html')

def register(request):
    global VALIDATE #global variable
    VALIDATE = drawPIL()
    # print "PIL:%s"%VALIDATE
    return render_to_response('register.html')

def submit(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        p = Person.objects.get(username=username,password=password)
        request.session['person_id'] = p.id
        articles = Article.objects.filter(usernameid=p.id)
        return render_to_response('index.html',{'username':username,'articles':articles})
    except:
        if request.session['person_id']:
            perid = request.session['person_id']
            username = Person.objects.get(id=perid).username
            articles = Article.objects.filter(usernameid=perid)
            return render_to_response('index.html',{'username':username,'articles':articles})
        else:
            return HttpResponse(r'<html><script type="text/javascript">alert("Error!Please check again!"); window.location="/"</script></html>')

def about(request):
    if request.session['person_id']:
        perid = request.session['person_id']
        username = Person.objects.get(id=perid).username
        return render_to_response('about.html',{'username':username})
    else:
        return HttpResponse(r'<html><script type="text/javascript">alert("Login again!"); window.location="/"</script></html>')

def add(request):
    if request.session['person_id']:
        perid = request.session['person_id']
        username = Person.objects.get(id=perid).username
        return render_to_response('add.html',{'username':username})
    else:
        return HttpResponse(r'<html><script type="text/javascript">alert("Login again!"); window.location="/"</script></html>')

def article(request):
    title = request.POST['title']
    author = request.POST['author']
    body = request.POST['body']
    usernameid = request.session['person_id']
    headImg = request.FILES['upload']
    uploadedfile(headImg)
    art = Article(title=title,author=author,body=body,usernameid=usernameid,headImg=headImg)
    art.save()
    return HttpResponseRedirect('/blog/')


def uploadedfile(f):
    path = '/home/developer/Github/PublicSite/blog/static/img/'+f.name 
    destination = open(path,'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def logout(request):
    del request.session['person_id']
    return HttpResponseRedirect('/')

def single(request,num):
    username = Article.objects.get(id=num).author
    body = Article.objects.get(id=num).body
    headImg = Article.objects.get(id=num).headImg
    try:
        perid = request.session['person_id']
        return render_to_response('single.html',{'username':username,'body':body,'num':num,'headImg':headImg})
    except:
        return render_to_response('u_single.html',{'username':username,'body':body,'num':num,'headImg':headImg})

def delete(request):
    if request.session['person_id']:
        perid = request.session['person_id']
        username = Person.objects.get(id=perid).username
        value = request.POST['value']
        deletearticle = Article.objects.get(id=value)
        deletearticle.delete()
        return render_to_response('index.html',{'username':username})
    else:
        return HttpResponse(r'<html><script type="text/javascript">alert("Login again!"); window.location="/"</script></html>')

def toedit(request,num):
    if request.session['person_id']:
        getarticle = Article.objects.get(id=num)
        title = getarticle.title
        author = getarticle.author
        body = getarticle.body
        upload = getarticle.headImg
        return render_to_response('edit.html',{'num':num,'title':title,'author':author,'body':body,'upload':upload})


def edit(request,num):
    if request.session['person_id']:
        updatearticle = Article.objects.get(id=num)
        updatearticle.title = request.POST['title']
        updatearticle.author = request.POST['author']
        updatearticle.body = request.POST['body']
        if request.FILES['upload']:
            updatearticle.headImg = request.FILES['upload']
            uploadedfile(updatearticle.headImg)
        updatearticle.save()
        return HttpResponseRedirect('/blog/')
    else:
        return HttpResponse(r'<html><script type="text/javascript">alert("Login again!"); window.location="/"</script></html>')


def consult(request):
    if request.session['person_id']:
        perid = request.session['person_id']
        username = Person.objects.get(id=perid).username
        title = request.POST['title']
        result = Article.objects.filter(title__icontains=title)
        return render_to_response('index.html',{'username':username,'articles':result})
    else:
        return HttpResponse(r'<html><script type="text/javascript">alert("Login again!"); window.location="/"</script></html>')

