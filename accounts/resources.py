from import_export import resources
from accounts.models import Account

class AccountResource(resources.ModelResource):
    class meta:
        model = Account