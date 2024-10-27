from app.extensions import db

def add_item(model, *args):
    new_item = model()
    i = 0
    for column in new_item.__table__.columns:
        if column.name != 'id':
            setattr(new_item, column.name, args[i - 1])
        i += 1

    db.session.add(new_item)
    db.session.commit()

    return new_item
