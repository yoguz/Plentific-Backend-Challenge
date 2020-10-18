from . import views
from django.urls import include, path

urlpatterns = [
    path('update_tables', views.update_tables, name='index'),
    path('get_dates', views.get_dates, name='get_dates'),
    path('get_postcodes', views.get_postcodes, name='get_postcodes'),
    path('get_avg_prices', views.get_avg_prices, name='get_avg_prices'),
    path('get_transaction_counts', views.get_transaction_counts, name='get_transaction_counts'),
    path('test_lower_end', views.test_lower_end, name='test_lower_end'),
]