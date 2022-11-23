from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutUser, name='logout'),

    path('master/staff/', views.masterStaff, name='staff'),
    path('master/account/', views.masterAccount, name='account'),
    path('master/vendor/', views.masterVendor, name='vendor'),

    path('master/staff/creates_staff/', views.createStaff, name='creates_staff'),    
    path('master/staff/update_staff/<str:pk>/',
         views.updateStaff, name='update_staff'),
    path('master/staff/delete_staff/<str:pk>/',
         views.deleteStaff, name='delete_staff'),
    
    path('master/account/creates_account/', views.createAccount, name='creates_account'),
    path('master/account/', views.masterAccount, name='search_account'),
    path('master/account/import/', views.importAccount, name='import_account'),
    path('master/account/export/csv', views.exportAccount, name='export_account'),
    path('master/account/export/pdf', views.exportPdf, name='export_pdf'),
    path('master/account/export/view-pdf', views.viewPdf, name='viewPdf'),
    path('master/account/export/view-pdf/print', views.print_pdf, name='print_pdf'),
    path('master/account/export/view-purchase', views.viewPurchase, name='viewPurchase'),
    path('master/account/export/view-purchase/print', views.printPurchase, name='printPurchase'),
    path('master/account/update_account/<str:pk>/',
         views.updateAccount, name='update_account'),
    path('master/account/delete_account/<str:pk>/',
         views.deleteAccount, name='delete_account'),
    
    # staff #
    path('user/', views.userPage, name='user_page'),
    path('user/purchase-request/', views.purchaseRequest, name='purchase_request'),
    path('user/purchase-request/create', views.createPurchase, name='create_purchase'),
    path('user/purchase-request/create', views.createPurchase, name='search_item'),
    path('user/purchase-request/create/cart', views.cartPurchase, name='cart_purchase'),
    path('user/purchase-request/create/cart/checkout', views.checkoutPurchase, name='checkout_purchase'),
    

]
