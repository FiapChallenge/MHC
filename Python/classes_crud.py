from api import db
from sqlalchemy.exc import IntegrityError


class GenericCRUD:
    model = None

    def __init__(self, model):
        self.model = model

    def type_of_sort(self, sort_by, direction):
        if self.model is None:
            raise ValueError("Model is not set. Please set the 'model' attribute.")
        match sort_by:
            case "ID":
                return (
                    getattr(self.model, f"id_{self.model.__tablename__.lower()}").asc()
                    if direction == "asc"
                    else getattr(
                        self.model, f"id_{self.model.__tablename__.lower()}"
                    ).desc()
                )
            case "NOME":
                return (
                    self.model.nome.asc()
                    if direction == "asc"
                    else self.model.nome.desc()
                )

    def get_all(self, sort_by="ID", direction="asc"):
        if self.model is None:
            raise ValueError("Model is not set. Please set the 'model' attribute.")
        items = self.model.query.order_by(self.type_of_sort(sort_by, direction)).all()
        return [item.json() for item in items]

    def get_by_id(self, id):
        item = db.session.get(self.model, id)
        return item.json() if item else None

    def get_by_name(self, name, start_with=False, sort_by="ID", direction="asc"):
        if self.model is None:
            raise ValueError("Model is not set. Please set the 'model' attribute.")
        filter_condition = (
            getattr(self.model, "nome").ilike(f"{name}%")
            if start_with
            else getattr(self.model, "nome").ilike(f"%{name}%")
        )
        items = (
            self.model.query.filter(filter_condition)
            .order_by(self.type_of_sort(sort_by, direction))
            .all()
        )
        return [item.json() for item in items]

    def get_by_field(
        self, field, value, start_with=False, sort_by="ID", direction="asc"
    ):
        if self.model is None:
            raise ValueError("Model is not set. Please set the 'model' attribute.")
        filter_condition = (
            getattr(self.model, field).ilike(f"{value}%")
            if start_with
            else getattr(self.model, field).ilike(f"%{value}%")
        )

        items = (
            self.model.query.filter(filter_condition)
            .order_by(self.type_of_sort(sort_by, direction))
            .all()
        )

        return [item.json() for item in items]

    def create(self, item):
        db.session.add(item)
        db.session.commit()
        return item.json()

    def update(self, id, new_item):
        item = db.session.get(self.model, id)
        if item:
            item.update(new_item)
            db.session.commit()
            return item.json()
        return None

    def delete(self, id):
        if self.model is None:
            raise ValueError("Model is not set. Please set the 'model' attribute.")
        item = db.session.get(self.model, id)
        if item:
            try:
                db.session.delete(item)
                db.session.commit()
                return item.json()
            except IntegrityError as e:
                db.session.rollback()
                raise ValueError(
                    f"Não é possível excluir {self.model.__name__} com id {id} pois está sendo utilizado no registro de uma classificação"
                )
            except Exception as e:
                db.session.rollback()
                return {"erro": f"Erro ao excluir o item: {e}"}
        return None
