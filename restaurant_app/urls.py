from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CategoryListView,
    MenuItemCreateView, MenuItemUpdateView, MenuItemDeleteView, MenuItemListView
)

urlpatterns = [
    
    path('', views.home, name='home'),
    path('legacy/', views.legacy, name='legacy'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),

   
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/<int:item_id>/', views.menu_detail, name='menu_detail'),

  
    path('reservation/', views.reservation, name='reservation'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),

   
    path('order/', views.place_order, name='place_order'),

    
    path('submit-review/', views.submit_review, name='submit_review'),

   
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),

   path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('menuitems/', MenuItemListView.as_view(), name='menuitem_list'),
    path('menuitems/create/', MenuItemCreateView.as_view(), name='menuitem_create'),
    path('menuitems/<int:pk>/edit/', MenuItemUpdateView.as_view(), name='menuitem_update'),
    path('menuitems/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menuitem_delete'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
