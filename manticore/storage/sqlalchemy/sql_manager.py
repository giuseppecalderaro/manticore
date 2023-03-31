from typing import Any
import sqlalchemy as sa
from sqlalchemy.orm import exc, sessionmaker


class SqlManager:
    def __init__(self, uri: str, poolclass=sa.pool.NullPool):
        self._uri = uri
        self._engine = sa.create_engine(uri, encoding='utf8', poolclass=poolclass)
        self._session_maker = sessionmaker(bind=self._engine)

    async def init(self) -> bool:
        return True

    def create(self) -> Any:
        return self._session_maker()

    @staticmethod
    def close(session):
        session.close()

    @staticmethod
    def decode_filters(obj_type, filters):
        output = {
            'filters': [],
            'needs_filtering': False,
            'needs_slicing': False,
            'needs_ordering': False
        }

        if filters:
            for key, value in filters.items():
                try:
                    field = getattr(obj_type, key)

                    if isinstance(field.type, sa.sql.sqltypes.String) and not value.isdigit():
                        output['filters'].append(field.ilike(value + '%'))
                        output['needs_filtering'] = True
                    elif isinstance(field.type, sa.sql.sqltypes.Integer) and value.isdigit():
                        output['filters'].append(field == int(value))
                        output['needs_filtering'] = True
                    else:
                        output['needs_filtering'] = False

                except AttributeError:
                    continue
                except TypeError:
                    continue

            if '_start' in filters and '_end' in filters:
                output['start'] = int(filters['_start'])
                output['end'] = int(filters['_end'])

                if output['start'] >= 0 and output['end'] >= 0 and output['start'] < output['end']:
                    output['needs_slicing'] = True

            if '_sort' in filters and '_order' in filters:
                output['sort'] = filters['_sort']
                output['order'] = sa.asc if filters['_order'].lower() == 'asc' else sa.desc

                try:
                    getattr(obj_type, output['sort'])
                    output['needs_ordering'] = True
                except AttributeError:
                    pass
                except TypeError:
                    pass

        return output

    @staticmethod
    def insert_one(session, obj_type, **kwargs):
        try:
            obj = obj_type(**kwargs)
            session.add(obj)
            session.commit()
        except:
            session.rollback()
            raise

        return obj

    @staticmethod
    def insert_many(session, docs):
        raise RuntimeError('Method insert_many() not implemented yet.')

    @staticmethod
    def find(session, obj_type, **kwargs):
        filters = SqlManager.decode_filters(obj_type, kwargs.pop('smart', None))

        objs = session.query(obj_type).filter_by(**kwargs)

        if filters['needs_filtering']:
            objs = objs.filter(*filters['filters'])

        if filters['needs_ordering']:
            ordering = filters['order']
            sorting = getattr(obj_type, filters['sort'])
            objs = objs.order_by(ordering(sorting))

        if filters['needs_slicing']:
            objs = objs.slice(filters['start'], filters['end'])

        if objs.count() == 0:
            return [], 0

        return objs, objs.count()

    @staticmethod
    def find_one(session, obj_type, **kwargs):
        try:
            obj = session.query(obj_type).filter_by(**kwargs).one()

        except exc.NoResultFound:
            return None

        except exc.MultipleResultsFound as exception:
            return exception

        return obj

    @staticmethod
    def update_one(session, obj_type, **kwargs):
        values = kwargs.get('values', {})
        del kwargs['values']

        obj = session.query(obj_type).filter_by(**kwargs)

        if obj.count() == 0:
            return 0, {obj_type.__name__: obj}

        if obj.count() > 1:
            raise RuntimeError('Multiple records found. Use update_many()')

        try:
            counter = obj.update(values)
            session.commit()
        except:
            session.rollback()
            raise

        return counter, {obj_type.__name__: obj.one().id}

    @staticmethod
    def delete(session, obj_type, **kwargs):
        objs = session.query(obj_type).filter_by(**kwargs)

        try:
            objs.delete()
            session.commit()

        except:
            session.rollback()
            raise

    def historical(self, obj_type, id, fields=None):
        """
            Method to get the historical from the temporal table
            Compatible with MariaDB only.
            :param id: (int) object id
            :param fields: (list) fields to return
            :return: list of objects
        """
        objs = []

        if not fields:
            fields = ['*']

        query = sa.text(f"SELECT {','.join(fields)} FROM {obj_type.__classname__} FOR SYSTEM_TIME ALL WHERE id = {id}")
        # Need to get the bind in order to execute the raw SQL query

        res = self._engine.execute(query)
        for value in res.fetchall():
            for item in zip(res.keys(), value):
                setattr(obj_type(), item[0], item[1])
            objs.append(obj_type())

        return objs
