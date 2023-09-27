from app.extensions import db


class BASE:
    def create(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

    @classmethod
    def update(cls, id, **kwargs):
        cls.query.filter_by(id=id).update(kwargs)
        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()
