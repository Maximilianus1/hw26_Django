from django.urls import path, re_path
from .views import (index, by_rubric, BbCreateView, get_comments, get_comment_by_id, delete_comment, 
                    add_and_save, redirect_to_index, detail, redirect_to_rubric, BbByRubricView, BbDetailView, BbAddView, BbEditView, BbDeleteView, BbIndexView, BbMonthArchiveView,BbCardsView,MachineDetailsView,jsonGet,editBb,
                    BbRedirectView, book_list, magicFruit)
from .models import Bb

app_name = 'bboard'


urlpatterns = [
    path('comments/', get_comments, name='get_comments'),
    path('comments/<int:comment_id>/', get_comment_by_id, name='get_comment_by_id'),
    path('comments/delete/<int:comment_id>/', delete_comment, name='delete_comment'),

    # path('add-and-save/', add_and_save, name='add_and_save'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    # path('add/', BbAddView.as_view(), name='add'),

    path('json/', jsonGet, name='json'),

    path('<int:year>/<int:month>/<int:day>', BbMonthArchiveView.as_view(), name='month_archive'),

    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    # path('', index, name='index'),
    path('', BbIndexView.as_view(), name='index'),

    path('redirect/', redirect_to_index, name='redirect_to_index'),
    # path('detail/<int:bb_id>/', detail, name='detail'), 
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),
    path('catalog/', BbCardsView.as_view(), name='bb_card'),
    path('redirect/', redirect_to_index, name='redirect_to_index'),
    path('redirect/<int:rubric_id>/', redirect_to_rubric, name='redirect_to_rubric'),
    path('bb_edits/', editBb, name='bb_edit'),
    path('fruits/', magicFruit, name='magic_fruits'),
    path('booklist/', book_list, name='book_list'),

]



