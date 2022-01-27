from django.shortcuts import render
from django.shortcuts import render, redirect
from photos import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model, authenticate, login, logout
from core.management.commands.my_email import send_email
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse
from users.forms import CustomAuthForm
from django.utils.encoding import force_bytes
from datetime import datetime
import uuid
from yookassa import Configuration, Payment as YookasaPayment
from RunPhoto.settings import API_SERVER_URL, YOOKASSA_ID, YOOKASSA_KEY


class CartView(TemplateView):

    def get(self, request, *args, **kwargs):
        if not request.user.id:
            return redirect('login')

        archive_photos_to_buy = models.PhotoToBuy.objects.filter(user=request.user, is_bought=False, is_archive=True)
        photos_to_buy = models.PhotoToBuy.objects.filter(user=request.user, is_bought=False, is_archive=False)

        photos_to_buy_ids = models.PhotoToBuy.objects.filter(user=request.user, is_bought=False).values('id')
        photos_to_buy_list = list()
        for photo in photos_to_buy_ids:
            photos_to_buy_list.append(photo['id'])

        arcive_amounts = archive_photos_to_buy.values()
        amounts = photos_to_buy.values()

        full_amount = sum(map(lambda amount: int(amount['amount']), amounts)) + \
                      sum(map(lambda amount: int(arcive_amount['amount']), arcive_amounts))

        context = {'archive_photos': archive_photos_to_buy,
                   'photos': photos_to_buy,
                   'full_amount': full_amount,
                   'photos_count': archive_photos_to_buy.count() + photos_to_buy.count(),
                   'photo_to_buy': photos_to_buy_list}
        return render(request, 'payments/cart.html', context)

    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount', None)
        photo_id = request.POST.get('photo_id', None)

        archive = request.POST.get('archive', None)
        tag_num = request.POST.get('tag_num', None)
        category_id = request.POST.get('category', None)
        # user
        print('!!!!!!!!')
        print(photo_id)
        print(amount)
        print(archive)
        print(tag_num)
        print(category_id)
        print('!!!!!!!!')

        if not request.user:
            return redirect('login')

        if not amount:
            return HttpResponse('Please add amount')
        if ',' in amount:
            amount = amount.replace(',', '.')
        try:
            amount = float(amount)
        except:
            return HttpResponse('Amount should be a float instance')
        if not photo_id and not archive:
            return HttpResponse('Please add photo or archive')

        if not tag_num:
            return HttpResponse('Please add tag number')

        try:

            tag = models.Tags.objects.get(name=tag_num)
        except:
            return HttpResponse('No such tag ' + tag_num)

        if not category_id:
            return HttpResponse('Please add category')
        try:
            category = models.Category.objects.get(id=category_id)
        except:
            return HttpResponse('No such category')
        if archive:
            photo_to_buy = models.PhotoToBuy.objects.create(
                user=request.user,
                tag=tag,
                category=category,
                is_archive=True,
                amount=amount
            )
            # return HttpResponse('OK')
            return True

        photo_to_buy = models.PhotoToBuy.objects.create(
            user=request.user,
            photo_id=photo_id,
            tag=tag,
            category=category,
            amount=amount,
        )
        print(photo_to_buy)

        photos = models.Photo.objects.filter(tags=tag, category=category).exclude(id=photo_id)

        if category.hold_date:
            hold_date = category.hold_date.strftime("%m-%d-%Y, %H:%M:%S").split(', ')[0]
        else:
            hold_date = ''

        context = {'photos': photos,
                   'tag_num': tag_num,
                   'category': category.name,
                   'created': hold_date,
                   'photos_num': photos.count(),
                   }

        #
        # context = {'category': category,
        #            'tag_num': tag_num,
        #            'photos_num': photos_num,
        #            'amount': amount}
        #
        return render(request, 'photos/search_result.html', context)
        # # return HttpResponse('OK')
        # return True


class ApproveInvoice(TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.user.id:
            return redirect('login')
        # return HttpResponse(request.user.id)
        archive_photos_to_buy = models.PhotoToBuy.objects.filter(user=request.user, is_bought=False, is_archive=True)

        photos_to_buy = models.PhotoToBuy.objects.filter(user=request.user, is_bought=False, is_archive=False)

        arcive_amounts = archive_photos_to_buy.values()
        amounts = photos_to_buy.values()

        full_amount = sum(map(lambda amount: int(amount['amount']), amounts)) + \
                      sum(map(lambda amount: int(arcive_amount['amount']), arcive_amounts))
        photos_to_buy = ' '.join(map(str, list(archive_photos_to_buy.values_list('id', flat=True))
                           + list(photos_to_buy.values_list('id', flat=True))))

        context = {'archive_photos': archive_photos_to_buy,
                   'photos': photos_to_buy,
                   'full_amount': full_amount,
                   'photos_to_buy':  photos_to_buy
                   }
        return render(request, 'payments/approve_invoice.html', context)

    def post(self, request, *args, **kwargs):
        amount = request.POST.get('full_amount')
        photos_to_buy = request.POST.get('photos_to_buy')
        # return HttpResponse(photos_to_buy)
        if not request.user.id:
            return redirect('login')
        invoice = models.Invoice.objects.create(user=request.user,
                                                amount=amount,
                                                )
        for photo_to_buy in photos_to_buy[1:-1].split(', '):
            try:
                archive_photos_to_buy = models.PhotoToBuy.objects.get(id=int(photo_to_buy))
                archive_photos_to_buy.invoice = invoice
                archive_photos_to_buy.save()
            except:
                return HttpResponse('No such photo_archive')
        # return HttpResponse('Invoice created')
        Configuration.account_id = YOOKASSA_ID
        Configuration.secret_key = YOOKASSA_KEY

        payment = YookasaPayment.create({
            "amount": {
                "value": invoice.amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": API_SERVER_URL + 'yoo-kassa-redirect/' + invoice.identify_code
            },
            "capture": True,
            "description": f"Оплата №{invoice.id}"
        }, uuid.uuid4())

        print(payment.confirmation.confirmation_url)

        return redirect(payment.confirmation.confirmation_url)


class YooKassaRedirect(TemplateView):

    def post(self, request, *args, **kwargs):

        code = kwargs.get('payment', '')
        payment = models.Invoice.objects.get(identify_code=code)
        payment.is_paid = True
        payment.save()
        return HttpResponse({'code': code})



