from rest_framework.pagination import PageNumberPagination


class FilmPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 40   
    
    
class SeriesPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 40  
    
    

class CartoonPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 40  
    
class SubscriptionPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 40  

class ReviewPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 40    