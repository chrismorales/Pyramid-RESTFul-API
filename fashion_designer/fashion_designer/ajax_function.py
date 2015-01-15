from pyramid.view import view_config

from .models import (
    DBSession,
    Brands,
)


@view_config(route_name='ajax', renderer='json')
def ajaxFunc(request):
    if request.GET:
        # call function for retrieving data
        if request.params['function'] == 'getBrands':
            result = getBrands()
            return result
    elif request.POST:
        # call function for inserting or updating data
        print "POST Function"


def getBrands():
    brands = DBSession.query(Brands).order_by(Brands.brand_id.asc()).all()
    results = []
    for item in brands:
        results.append({
            "key": item.brand_id,
            "name": item.name
        })
    return results
