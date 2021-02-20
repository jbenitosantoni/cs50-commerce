from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name="new_listing"),
    path("auction/<str:auction>", views.list_auction, name="auction"),
    path("watchlist/add/<str:auction>", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<str:auction>", views.remove_watchlist, name="remove_watchlist"),
    path("bid/<str:auction>", views.new_vid, name="bid"),
    path("close/<str:auction>", views.close, name="close"),
]
