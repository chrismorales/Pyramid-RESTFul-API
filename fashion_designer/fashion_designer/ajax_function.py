import views


def getBrands():
    brands = views.DBSession.query(views.Brands).order_by(
        views.Brands.brand_id.asc()).all()
    results = []
    for item in brands:
        results.append({
            "key": item.brand_id,
            "name": item.name
        })
    return results
