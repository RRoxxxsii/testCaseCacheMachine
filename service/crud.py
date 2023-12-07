from django.db.models import QuerySet

from service.models import Item


class ItemCrud:
    model = Item

    @classmethod
    def get_all(cls) -> QuerySet[Item]:
        return cls.model.objects.all()

    @classmethod
    def get_by_list_id(cls, item_ids: list) -> QuerySet[list[dict]]:
        return cls.model.objects.filter(pk__in=item_ids).values('id', 'title', 'price')
