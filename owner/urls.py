from django.urls import path
from owner import views

urlpatterns=[
    path("owner/accounts/signup",views.UserCreationView.as_view()),
    path("owner/accounts/signin", views.SigninView.as_view()),
    path("orders/products",views.AddProductsView.as_view()),
    path("products/orders",views.OrderView.as_view())
]