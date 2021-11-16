from django.shortcuts import render, redirect
from .models import Category, Photo,  Tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tag_finder import TagFinder
from django.http import HttpResponse


# Create your views here.


def view_gallery(request):
    category = request.GET.get('category')
    tags = Tags.objects.all()
    categories = Category.objects.all()
    photos = Photo.objects.all()
    paginator = Paginator(photos, 20)  # Show 25 contacts per page

    if category is None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)


    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        photos = paginator.page(paginator.num_pages)

    context = {'categories': categories, 'photos': photos}



    return render(request, 'photos/gallery.html', context)


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {'photo': photo}

    return render(request, 'photos/photo.html', context)

def base(request):
    photo = Photo.objects.all()
    context = {'photo': photo}

    return render(request, 'photos/base.html', context)

def home(request):
    categories = Category.objects.all()
    photo = Photo.objects.all()
    context = {
        'photo': photo,
        'categories': categories
    }

    return render(request, 'photos/home.html', context)


def add_photo(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        tags = request.POST.get('tags')
        tags = tags.split(', ')

        # Check Category
        if 'category' in data:
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        for image in images:
            img = Photo.objects.create(
                name=data['name'], category=category,
                price=data['price'],
                image=image)

            for tag in tags:
                img.tags.add(Tags.objects.get_or_create(name=tag)[0])

        return redirect('gallery')

    context = {'categories': categories}

    return render(request, 'photos/add.html', context)


def search(request):
    if request.method == "POST":
        tag_num = request.POST.get('tag_num', True)
        category = request.POST.get('category_id', True)
        try:
            tag = Tags.objects.get(name=tag_num)
            category = Category.objects.get(id=category)
        except:
            return render(request,
                          'photos/search_result.html',
                          )

        photos = Photo.objects.filter(tags=tag, category=category)

        context = {'photos': photos,
                   'tag_num': tag_num}

        return render(request,
                      'photos/search_result.html',
                      context)
    else:
        return render(request,
                      'photos/search_result.html',
                      )


def profile(request):
    return render(request, 'photos/user_profile.html', )


def login(request):
    return render(request, 'photos/login.html')


def tags_list(request):
    tags = Tags.objects.all()
    return render(request, 'photos/tags_list.html',
                  context={'tags': tags}
                  )

def cart(request):
    return render(request, 'photos/cart.html', )


