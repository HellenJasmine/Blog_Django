from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

PER_PAGE = 9

class PostListView(ListView):

    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title':'Home - ',
        })
        
        return context
    


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.get_object().title} - Post -"
        context.update({
            'page_title': page_title,
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published = True)

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.get_object().title} - Página -"
        context.update({
            'page_title': page_title,
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published = True)


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context:dict[str, Any] = {}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context["user"]
        user_full_name = user.username

        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"
        page_title = 'Posts de '+ user_full_name +' - '

        context.update({
            'page_title':page_title,
        })
        return context
    

    def get_queryset(self):
        querySet = super().get_queryset()
        querySet = querySet.filter(created_by__pk= self._temp_context['user'].pk)
        return querySet
    
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_pk = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'author_pk': author_pk,
            'user':user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        querySet = super().get_queryset()
        querySet = querySet.filter(category__slug = self.kwargs.get('slug'))
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].category.name} - Categoria - "
        context.update({
            'page_title':page_title,
        })
        return context
    

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        querySet = super().get_queryset()
        querySet = querySet.filter(tags__slug = self.kwargs.get('slug'))
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f"{self.kwargs.get('slug')} - Tag - "
       
        context.update({
            'page_title':page_title,
        })
        return context



class SearchListView(PostListView):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get("search").strip()

        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
        Q(title__icontains = search_value)|
        Q(excerpt__icontains = search_value)|
        Q(content__icontains = search_value)
    )[0:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self._search_value
        context.update({
            'page_title': f"{search_value[:30]} - Search - ",
            'search_value': search_value
        })
        return context 
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value == "":
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)