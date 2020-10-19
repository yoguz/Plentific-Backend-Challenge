from bisect import bisect_right, bisect_left
import json
from django.db.models import Avg
from django.http import HttpResponse
from .models import Transaction, Postcode, Date
import datetime
from dateutil.rrule import rrule, MONTHLY


def index(request):
    print("This is for Heroku debug")
    return HttpResponse("Hello, world. You're at the polls index.")


def get_postcodes(request):
    print('getting postcodes...')
    postcode_list = list()
    try:
        postcodes = Postcode.objects.all().order_by('postcode')
        print('postcode fetch completed...')

        for postcode in postcodes:
            if postcode.postcode is not None and len(postcode.postcode) > 0:
                postcode_list.append(postcode.postcode)

        print('getting postcodes SUCCESSFUL...')
    except:
        print('getting postcodes FAILED...')

    return HttpResponse(json.dumps(postcode_list))


def get_dates(request):
    print('getting dates...')
    date_list = list()
    try:
        dates = Date.objects.all().order_by('date')
        print('date fetch completed...')

        for date in dates:
            date_list.append(date.date_str)

        print('getting dates SUCCESSFUL...')
    except:
        print('getting dates FAILED...')

    return HttpResponse(json.dumps(date_list))


def get_avg_prices(request):
    print('getting avg prices...')
    result = []
    try:
        j = json.loads(request.body)
        print('querying for date_from:', j['date_from'], ', date_to:', j['date_to'], ' and postcode:', j['postcode'])

        date_from = Date.objects.filter(date_str__exact=j['date_from'])[0].date
        print('date_from fetch completed...')

        date_to = Date.objects.filter(date_str__exact=j['date_to'])[0].date
        print('date_to fetch completed...')

        postcode = Postcode.objects.filter(postcode=j['postcode'])[0]
        print('postcode fetch completed...')

        result = []
        for date in rrule(MONTHLY, dtstart=date_from, until=date_to):
            date_id = Date.objects.filter(date_str__exact=date.strftime('%b %Y'))[0].id
            objects = Transaction.objects \
                .filter(date_id=date_id, postcode_id=postcode.id)\
                .values('property_type')\
                .annotate(avg_price=Avg('price'))

            d_avg = 0
            s_avg = 0
            t_avg = 0
            f_avg = 0
            for o in objects:
                if o['avg_price'] is None:
                    continue

                if o['property_type'] == 'D':
                    d_avg = int(o['avg_price'])
                elif o['property_type'] == 'F':
                    f_avg = int(o['avg_price'])
                elif o['property_type'] == 'S':
                    s_avg = int(o['avg_price'])
                elif o['property_type'] == 'T':
                    t_avg = int(o['avg_price'])

            result.append({'Date': date.strftime('%b %Y'),
                           'd_avg': d_avg, 's_avg': s_avg, 't_avg': t_avg, 'f_avg': f_avg})

            print('result is appended for month:', date.month, ' and year:', date.year)

        print('getting avg prices SUCCESSFUL...')
    except:
        print('getting avg prices FAILED...')

    return HttpResponse(json.dumps(result))


def get_transaction_counts(request):
    print('getting transaction counts...')
    labels = []
    values = []
    try:
        j = json.loads(request.body)
        print('querying for date:', j['date'], ' and postcode:', j['postcode'])

        date = Date.objects.filter(date_str__exact=j['date'])[0]
        print('date fetch completed...')

        postcode = Postcode.objects.filter(postcode=j['postcode'])[0]
        print('postcode fetch completed...')

        prices = Transaction.objects.filter(date_id=date.id, postcode_id=postcode.id).values('price')
        print('prices fetch completed...')

        price_list = list()
        for p in prices:
            price_list.append(p['price'])
        price_list.sort()

        median = price_list[int(len(price_list) / 2)]
        q1 = price_list[int(len(price_list) / 4)]
        q3 = price_list[int((len(price_list) / 4) * 3)]
        iqr = q3 - q1
        lower_end = median - 1.5 * iqr
        upper_end = median + 1.5 * iqr
        lower = bisect_left(price_list, lower_end)
        upper = bisect_right(price_list, upper_end)

        if lower == 0 and upper == len(price_list):
            # data has no outliers
            print('data has no outliers...')
            period = int((price_list[upper-1] - price_list[lower]) / 8)
            labels.append(f'Under £{int((price_list[lower] + period) / 1000)}k')
            for i in range(1, 7):
                labels.append(
                    f'£{int((price_list[lower] + (period * i)) / 1000)}k - £{int((price_list[lower] + (period * (i + 1))) / 1000)}k')
            labels.append(f'Over £{int((price_list[lower] + period * 7) / 1000)}k')

            count_prev = 0
            for i in range(1, 8):
                count = bisect_left(price_list, price_list[0] + (period * i)) - count_prev
                values.append(count)
                count_prev += count
            values.append(len(price_list) - count_prev)

        elif lower > 0 and upper == len(price_list):
            # data has outliers in lower ends
            print('data has outliers in lower ends...')
            period = int((price_list[upper] - price_list[lower]) / 7)
            labels.append(f'Under £{int((price_list[lower]) / 1000)}k')
            for i in range(1, 7):
                labels.append(
                    f'£{int((price_list[lower] + (period * i)) / 1000)}k - £{int((price_list[lower] + (period * (i + 1))) / 1000)}k')
            labels.append(f'Over £{int((price_list[lower] + period * 7) / 1000)}k')

            count_prev = lower
            values.append(count_prev)
            for i in range(1, 7):
                count = bisect_left(price_list, price_list[0] + (period * i)) - count_prev
                values.append(count)
                count_prev += count
            values.append(len(price_list) - count_prev)

        elif lower == 0 and upper < len(price_list):
            # data has outliers in upper ends
            print('data has outliers in upper ends...')
            period = int((price_list[upper] - price_list[lower]) / 7)
            labels.append(f'Under £{int((price_list[lower] + period) / 1000)}k')
            for i in range(1, 7):
                labels.append(
                    f'£{int((price_list[lower] + (period * i)) / 1000)}k - £{int((price_list[lower] + (period * (i+1))) / 1000)}k')
            labels.append(f'Over £{int((price_list[lower] + period * 7) / 1000)}k')

            count_prev = 0
            for i in range(1, 8):
                count = bisect_left(price_list, price_list[0] + (period * i)) - count_prev
                values.append(count)
                count_prev += count
            values.append(len(price_list) - count_prev)

        elif lower > 0 and upper < len(price_list):
            # data has outliers in both ends
            print('data has outliers in both ends...')
            period = int((price_list[upper] - price_list[lower]) / 6)
            labels.append(f'Under £{int((price_list[lower]) / 1000)}k')
            for i in range(0, 6):
                labels.append(
                    f'£{int((price_list[lower] + (period * i)) / 1000)}k - £{int((price_list[lower] + (period * (i + 1))) / 1000)}k')
            labels.append(f'Over £{int((price_list[upper]) / 1000)}k')

            count_prev = lower
            values.append(count_prev)
            for i in range(1, 7):
                count = bisect_left(price_list, price_list[lower] + (period * i)) - count_prev
                values.append(count)
                count_prev += count
            values.append(len(price_list) - count_prev)

        print('getting transaction counts SUCCESSFUL...')
    except:
        print('getting transaction counts FAILED...')

    return HttpResponse(json.dumps({'labels': labels, 'values': values}))


def update_tables(request):
    update_postcodes()
    update_dates()
    return HttpResponse()


def update_postcodes():
    print('updating postcodes...')
    try:
        query = Transaction.objects.values('postcode').distinct()
    except:
        print("ERR. Something goes wrong while fetching postcodes.")

    li = list(query)
    postcode_set = set()
    for elem in li:
        postcode = elem['postcode']
        if postcode == '':
            continue

        postcode_set.add(postcode.split(' ', 1)[0])

    for p in postcode_set:
        postcode = Postcode(postcode=p)
        try:
            postcode.save()
        except:
            print("ERR. Postcode:", postcode, " can not saved.")

    print('postcodes are updated.')


def update_dates():
    print('updating dates...')

    start = end = datetime.datetime.now()
    try:
        min_date = Transaction.objects.earliest('date')
        max_date = Transaction.objects.latest('date')
        start = datetime.datetime(min_date.date.year, min_date.date.month, min_date.date.day)
        end = datetime.datetime(max_date.date.year, max_date.date.month, max_date.date.day)
    except:
        print("ERR. Something goes wrong while fetching dates.")

    for date in rrule(MONTHLY, dtstart=start, until=end):
        d = Date(date_str=date.strftime('%b %Y'), date=date)
        try:
            d.save()
        except:
            print("ERR. Date:", date, " can not saved.")

    print('dates are updated.')
