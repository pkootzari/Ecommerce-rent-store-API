from django.urls import include, path
from rest_framework import routers
from . import views
urlpatterns = [
    path('signup/', views.CreateUser.as_view()),
    path('getuser/', views.GetUser.as_view()),
    path('profileupdate/', views.UpdateUser.as_view()),

    path('profileupdate/contactinfo/address/',
         views.CRUDAddress.as_view({'post': 'create'})),
    path('profileupdate/contactinfo/address/<int:pk>/',
         views.CRUDAddress.as_view({'put': 'update',
                                    'delete': 'destroy',
                                    'get': 'retrieve'})),
    path('profileupdate/contactinfo/phone/',
         views.CRUDPhone.as_view({'post': 'create'})),
    path('profileupdate/contactinfo/phone/<int:pk>/',
         views.CRUDPhone.as_view({'put': 'update',
                                  'delete': 'destroy',
                                  'get': 'retrieve'})),
    path('profileupdate/subscription/',
         views.CRUDSubscription.as_view({'post': 'create'})),
    path('profileupdate/picture/',
         views.CRUDCompanyImg.as_view({'post': 'create'})),
    path('profileupdate/picture/<int:pk>/',
         views.CRUDCompanyImg.as_view({'delete': 'destroy'})),

    path('product/',
         views.ProductCRUD.as_view({'post': 'create',
                                    'get': 'list'})),
    path('product/<int:pk>/',
         views.ProductCRUD.as_view({'put': 'update',
                                    'patch': 'partial_update',
                                    'delete': 'destroy',
                                    'get': 'retrieve'}), name='product-detail'),
    path('product/index/',
         views.ProductCRUD.as_view({'get': 'indexProduct'})),
    path('product/<int:pk>/rate/',
         views.ProductCRUD.as_view({'post': 'rate'})),
    path('product/<int:pk>/adddeletefee/',
         views.ProductCRUD.as_view({'post': 'addFee',
                                    'delete': 'deleteFee'})),
    path('product/<int:pk>/adddeleteimg/',
         views.ProductCRUD.as_view({'post': 'addImg',
                                    'delete': 'deleteImg'})),

    path('basket/items/',
         views.CRUDBasket.as_view({'post': 'create',
                                   'get': 'list'})),
    path('basket/items/<int:pk>/',
         views.CRUDBasket.as_view({'patch': 'partial_update',
                                   'put': 'update',
                                   'get': 'retrieve',
                                   'delete': 'destroy'})),
    path('items/',
         views.CRUDItem.as_view({'get': 'list'})),
    path('items/<int:pk>/',
         views.CRUDItem.as_view({'get': 'retrieve'})),
    # path('carts/', views.CartActions.as_view()),
    # path('carts/remove_item/', views.DeleteFromCart.as_view()),
    # path('invoice/', views.InvoiceDetail.as_view()),
    # TODO: need to be rewrite
    # path('getcategorylist/', views.GetCategoryList.as_view()),
    # path('getitems/', views.GetItem.as_view())
]


