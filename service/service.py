import random
import string
from datetime import datetime

import pdfkit
import qrcode
from django.template.loader import render_to_string

from service.crud import ItemCrud


class CreateCheckService:

    def __init__(self, item_crud=ItemCrud):
        self.crud = item_crud()

    def _create_pdf(self, items: dict, check_name: str):
        data = render_to_string(template_name='service/check_template.html',
                                context=items)
        options = {
            'page-height': '526px',
            'page-width': '364px',
        }

        file_str = pdfkit.from_string(data, options=options)
        with open(f'media/check/{check_name}.pdf', 'wb') as file:
            file.write(file_str)

    def _generate_filename(self) -> str:
        letters = string.ascii_lowercase + string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for _ in range(30))
        return result_str

    def _calculate(self, list_ids: list) -> dict:
        items = self.crud.get_by_list_id(list_ids)
        data, total = [], 0
        for item in items:
            amount = list_ids.count(item.get('id'))
            total_price = item.get('price') * amount
            total += total_price
            data.append({'title': item.get('title'), 'amount': amount, 'price': total_price})
        return {'items': data, 'total': total}

    def _create_qr_code(self, qr_code_name: str, check_path: str) -> str:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(check_path)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f'media/qr/{qr_code_name}.png')
        return qr_code_name

    def execute(self, list_ids: list, scheme: str, host: str) -> str:
        items = self._calculate(list_ids)
        items.update(date=datetime.now().strftime('%d.%m.%Y %H:%M'))
        check_file_name = self._generate_filename()
        qr_code_name = self._generate_filename()
        self._create_pdf(items=items, check_name=check_file_name)
        self._create_qr_code(check_path=f'{scheme}://{host}/media/check/{check_file_name}.pdf',
                             qr_code_name=qr_code_name)
        return qr_code_name
