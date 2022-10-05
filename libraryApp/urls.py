from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("callRecordForm", views.callRecordFrom, name="callRecordForm"),
    path("addRecord", views.addRecord, name="addRecord"),

    path("callReturnForm", views.callReturnForm, name="callReturnForm"),
    path("deleteRecord", views.deleteRecord, name="deleteRecord"),

    path("callUpdateForm", views.callUpdateForm, name="callUpdateForm"),
    path("updateRecord", views.updateRecord, name="updateRecord"),
]