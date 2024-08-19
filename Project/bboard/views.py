from django.forms.forms import BaseForm
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, Http404, StreamingHttpResponse, FileResponse
from .models import Bb, Rubric, Comment, Machine, Spare, AdvUser, Book, Author
from django.template import loader
from .forms import BbForm, BbCheckForm,MagicFruitForm
from django.urls import reverse_lazy, reverse
from django.template.loader import get_template, render_to_string
from django.views.decorators.http import require_http_methods
from django.views.decorators.gzip import gzip_page
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, DayArchiveView, DateDetailView
from django.views.generic.detail import SingleObjectMixin
import requests
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
def get_comments(request):
    comments = Comment.objects.all().values('id', 'text', 'created_at')
    return JsonResponse(list(comments), safe=False)

def get_comment_by_id(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return JsonResponse({'id': comment.id, 'text': comment.text, 'created_at': comment.created_at})

def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'status': 'success'})
    except Comment.DoesNotExist:
        return HttpResponseNotFound({'status': 'comment not found'})


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    # success_url = '/bboard/detail/{rubric_id}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

def redirect_to_index(request):
    return HttpResponseRedirect(reverse('bboard:index'))
    # return HttpResponsePermanentRedirect('https://www.instagram.com/')

def jsonGet(request):
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)
    data = response.json()
    all_posts = len(data)
    if 'page' in request.GET:
        page_num = int(request.GET['page'])
    else:
        page_num=1
    num_of_posts = 3
    start_index = (page_num - 1) * num_of_posts
    end_index = start_index + num_of_posts
    paginated_data = data[start_index:end_index]
    page_range = range(1, (all_posts // num_of_posts+all_posts % num_of_posts) + 1)
    context = {'posts': paginated_data, 'page': page_num, 'page_range': page_range}
    return render(request, 'bboard/JsonInfo.html', context)


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    url1 = reverse('bboard:index')
    # print(request.headers['Content-Language'])
    context = {'bbs': bbs, 'rubrics': rubrics, 'url1': url1}
    return render(request, 'bboard/index.html', context)

    # date = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
    # return JsonResponse(date, json_dumps_params={'ensure_ascii': False})


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    url = reverse('bboard:by_rubric', args=(current_rubric.pk,))

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric, 'url': url}
    return render(request, 'bboard/by_rubric.html', context)

def redirect_to_rubric(request, rubric_id):
    return redirect('bboard:by_rubric', rubric_id=rubric_id)


@require_http_methods(['GET', 'POST'])
def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


def detail(request, bb_id):
    bb = get_list_or_404(Bb, pk=bb_id)
    return HttpResponse(f'Название: {bb.title}, Описание: {bb.content}, Дата публикации: {bb.published}')

# class BbByRubricView(ListView):
#     template_name = 'bboard/by_rubric.html'
#     context_object_name = 'bbs'

#     def get_queryset(self):
#         return Bb.objects.filter(rubric=self.kwargs['rubric_id'])


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
#         return context


# class BbDetailView(DetailView):
#     model = Bb

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubric'] = Rubric.objects.all()
#         return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})



class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['url1'] = reverse_lazy('bboard:index')
        return context


class BbMonthArchiveView(DayArchiveView):
    model = Bb
    date_field = 'published'
    month_format = '%m'
    template_name = 'bboard/bb_archive_month.html'



class BbDetailView(DateDetailView):
    model = Bb
    date_field = 'published'
    month_format = '%m'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


class BbRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Используем reverse для получения правильного URL-адреса
        return reverse('bboard:detail', kwargs={'pk': self.kwargs['pk']})

# def jsonInfo(request):
#     url = 'https://jsonplaceholder.typicode.com/posts'
#     rubrics = Rubric.objects.all()
#     url1 = reverse('bboard:index')
#     # print(request.headers['Content-Language'])
#     context = {'bbs': bbs, 'rubrics': rubrics, 'url1': url1}
#     return render(request, 'bboard/index.html', context)



class BbByRubricView(SingleObjectMixin ,ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    def get_queryset(self):
        return self.object.bb_set.all()


class BbCheckRedirectView(RedirectView):
    form_class = BbCheckForm
    permanent = False
    query_string = True
    pattern_name = 'bboard:index'

    def get_redirect_url(self, *args, **kwargs):
        form = self.form_class(self.request.GET or None)
        if form.is_valid():
            # Делаем что-то с данными формы, например, проверяем их
            field1 = form.cleaned_data['field1']
            field2 = form.cleaned_data['field2']
            # Далее можете делать что-то с данными, например, проверять их на соответствие в базе данных

            # Возвращаем URL для редиректа
            return reverse(self.pattern_name)

        # Если данные формы не проходят валидацию, возвращаем None,
        # что приведет к редиректу на текущую страницу (без изменения URL)
        return None

    def get(self, request, *args, **kwargs):
        # Вызываем метод get_context_data() для получения контекста
        context = self.get_context_data()
        # В данном примере не требуется отображение формы,
        # так как она проверяется в методе get_redirect_url()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return render(r'bboard:')

class BbCardsView(ListView):
    model = Bb
    template_name = 'bboard/catalog.html'
    ordering = ['-published']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.all()
        return context
class MachineDetailsView(DetailView):
     model = Machine
     template_name = 'bboard/Machine.html'
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         machine = self.get_object()
         context['spares'] = machine.spares.all()
         return context
#
# def editAdvUser(request,pk):
#     au = AdvUser.objects.get(pk=pk)
#     if request.method == 'POST':
#         auf = AdvUserForm(request.POST,instance=au)
#         if auf.is_valid():
#             if auf.has_changed():
#                 auf.save()
#                 return HttpResponseRedirect(reverse('bboard:index'))
#             else:
#                 context= {'form': auf}
#                 return render(request, 'bboard/create.html', context)
#         else:
#             auf = AdvUserForm(request.POST, instance=au)
#             context = {'form': auf}
#             return render(request, 'bboard/create.html', context)

def editBb(request):
    BbFormSet = modelformset_factory(Bb, fields=('kind', 'title', 'content', 'price'), can_delete=True, can_order=True)
    if request.method == 'POST':
        formset = BbFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    bb = form.save(commit=False)
                    bb.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    bb.save()
            return redirect('bboard:index')
    formset = BbFormSet(queryset=Bb.objects.all())
    return render(request, 'bboard/bbEdit.html', {'formset': formset})


def book_list(request):
    books = Book.objects.prefetch_related('authors').only('title').all()
    context = {
        'books': books
    }
    return render(request, 'bboard/book_list.html', {'books': books})
def magicFruit(request):
    if request.method == 'POST':
        form = MagicFruitForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'bboard/fruit_success.html', {'form': form})
        else:
            return render(request, 'bboard/fruit_unsuccess.html', {'form': form})
    form = MagicFruitForm()
    return render(request, 'bboard/fruit_form.html', {'form': form})