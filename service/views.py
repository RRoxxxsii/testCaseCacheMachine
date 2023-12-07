from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from service.crud import ItemCrud
from service.serializers import ListItemIDSerializer
from service.service import CreateCheckService


class CreateCheckPDF(GenericAPIView):
    queryset = ItemCrud.get_all()
    serializer_class = ListItemIDSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_ids = serializer.data.get('item_ids')
        scheme, host = request.scheme, request.get_host()
        file = CreateCheckService().execute(item_ids, scheme=scheme, host=host)
        image_url = f'{request.scheme}://{request.get_host()}/media/qr/{file}.png'
        return Response({'qr_code_url': image_url})
