from rest_framework import permissions


class CheckSubscription(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.access_type == 'Free':
            return True
        if request.user.subscription_status == 'Subscription':
            return True
        else:
            return False 




class CheckUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == obj.user








# class CheckSubscription(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):

#         # 1. Бесплатный контент — доступен всем
#         if obj.access_type == "Free":
#             return True

#         # 2. Подписочный контент — доступен только подписчикам
#         if obj.access_type == "Subscription":
#             return request.user.subscription_status == "Subscription"

#         # 3. Аренда — доступно только тем, кто оплатил
#         if obj.access_type == "Rent":
#             return self.user_has_rent_access(request.user, obj)

#         return False

#     def user_has_rent_access(self, user, film):
#      return RentHistory.objects.filter(
#         user=user,
#         film=film,
#         expires_at__gte=timezone.now()
#     ).exists()