from django.urls import path
from . import views

app_name = 'gpf'
urlpatterns = [
    path('list', views.PermitRequestListView.as_view(), name='list'),
    path('listexterns/', views.PermitRequestListExternsView.as_view(), name='listexterns'),
    path('add/', views.actorAdd, name='actor_add'),
    path('companyadd/', views.companyAdd, name='companyadd'),
    path('actor/<int:pk>/change', views.actorChange, name='ActorChange'),
    path('actor/<int:pk>', views.genericactorview, name='genericactorview'),
    path('actor_edit_account/', views.actor_edit_account, name='actor_edit_account'),
    path('add/<int:project_owner_id>/', views.permitRequestAdd, name='permit-request-add'),
    path('change/', views.permitRequestChange, name='permit-request-change'),
    path('listexport/', views.PermitExportView.as_view(), name='listexport'),
    path('listexportexterns/', views.PermitExportViewExterns.as_view(), name='listexportexterns'),
    path('permitdetail/<int:pk>', views.permitdetail, name='permitdetail'),
    path('mapnv/<int:pk>', views.mapnv, name='mapnv'),
    path('permitdelete/<int:pk>', views.PermitRequestDelete.as_view(), name='permitdelete'),
    path('companyedit/<int:pk>', views.companyedit, name='companyedit'),
    path('sendpermit/<int:pk>', views.sendpermit, name='sendpermit'),
    path('printpermit/<int:pk>', views.printpermit, name='printpermit'),
    path('callforvalidations/<int:pk>', views.callforvalidations, name='callforvalidations'),
    path('seewaitingvalidations/<int:pk>', views.seewaitingvalidations, name='seewaitingvalidations'),
    path('serviceusers/', views.serviceusers, name='serviceusers'),
    path('waitingvalidations/<int:hours>', views.waitingvalidations, name='waitingvalidations'),
    path('endwork/<int:pk>', views.endwork, name='endwork'),
    path('documentupload/<int:permit_id>/', views.documentUpload, name='documentupload'),
    path('thanks/<int:permit_id>', views.thanks, name='thanks'),
    path('prices/', views.prices, name='prices'),
    path('file-download/<int:pk>', views.file_download, name='file-download'),
    path('signature', views.signature, name='signature'),
    ]
