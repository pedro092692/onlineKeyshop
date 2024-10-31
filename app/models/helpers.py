from app.extensions import db, slugify

def add_item(model, *args):
    new_item = model()
    i = 0
    for column in new_item.__table__.columns:
        if column.name != 'id' and column.name != 'slug':
            setattr(new_item, column.name, args[i - 1])

        if column.name == 'slug':
            slug = slugify(args[0])
            unique_slug = slug
            count = 1
            while model.check_slug(slug):
                unique_slug = f'{unique_slug}-{count}'
                count += 1

            setattr(new_item, column.name, unique_slug)

        i += 1

    db.session.add(new_item)
    db.session.commit()

    return new_item

def get_item(model, item_id):
    item = db.get_or_404(model, item_id)
    return item

def update_item(obj_item, *args):
    i = 0
    for column in obj_item.__table__.columns:
        if column.name != 'id' and column.name != 'slug':
            setattr(obj_item, column.name, args[i - 1])
        i += 1
    db.session.commit()

def delete_item(obj_item):
    db.session.delete(obj_item)
    db.session.commit()

def search_item(query, model):
    results = db.paginate(db.select(model).filter(model.name.icontains(query)), per_page=8)
    return results

