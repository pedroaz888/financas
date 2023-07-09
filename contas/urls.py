from django.urls import path
from . import views

urlpatterns = [
    path('definir_contas/', views.definir_contas, name="definir_contas"),
    path('ver_contas/', views.ver_contas, name="ver_contas"),
    path('update_pagamento/<int:id>', views.update_pagamento, name="update_pagamento"),

]