from django.db.models.signals import post_save
from django.dispatch import receiver
from import_export.signals import post_import, post_export
from django.contrib.auth.models import Group, Permission
from .models import Vendor, Order

@receiver(post_save, sender=Vendor)
def add_vendor_to_group(sender, instance, created, **kwargs):
    if created:
        # Get the group object with the desired permissions
        group = Group.objects.get(name='Vendor Permissions')

        # Add the vendor to the group
        instance.groups.add(group)

        # Get the permissions for the group
        permissions = Permission.objects.filter(group=group)

        # Assign the permissions to the vendor
        for permission in permissions:
            instance.user_permissions.add(permission)
            

@receiver(post_export, sender=Order, dispatch_uid='post_export_order')
def post_export_order(sender, **kwargs):
    order = kwargs['instance']
    # Process the exported order instance as needed
    # ...

    # Example: Print the order's primary key
    print(order.pk)