from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from ecommerce import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('verifylogin/', views.verifylogin, name="verifylogin"),
    path('userlogout/', views.userLogout, name="userlogout"),
    path('signup/', views.signup, name="signup"),
    path('createlocalbuyer/', views.createlocalbuyer, name="createlocalbuyer"),
    path('accounthalt/', views.accountHalt, name="accounthalt"),
    path('categories/', views.login, name="categories"),
    path('userbrands/<int:cid>', views.filteredCategory, name="userbrands"),
    path('productlist/<int:bid>/', views.productlist, name="productlist"),
    path('productdetail/<int:pid>/', views.productdetail, name="productdetail"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('products/', views.products, name="products"),
    path('brands/', views.brands, name="brands"),
    path('localbuyer/', views.localbuyer, name="localbuyer"),
    path('activatelocalbuyer/<int:uid>/', views.activatelocalbuyer, name="activatelocalbuyer"),
    path('deactivatelocalbuyer/<int:uid>/', views.deactivatelocalbuyer, name="deactivatelocalbuyer"),
    path('mainbuyer/', views.mainbuyer, name="mainbuyer"),
    path('savemainbuyer', views.savemainbuyer, name="savemainbuyer"),
    path('savebrand/', views.savebrand, name="savebrand"),
    path('ajax/load-brand/', views.loadbrand, name='loadbrand'),
    path('saveproduct/', views.saveproduct, name='saveproduct'),
    path('update_item/', views.updateItem, name='update_item'),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)