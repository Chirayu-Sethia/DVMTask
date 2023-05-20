from django.contrib.auth.mixins import AccessMixin

class VendorPermissionMixin:
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if request.user.is_superuser or request.user.is_staff:
            return perms
        else:
            # hide the models you don't want vendors to see
            hidden_models = ['Additional_information', 'Brand', 'Product']
            for model in hidden_models:
                perms[model] = False
            return perms