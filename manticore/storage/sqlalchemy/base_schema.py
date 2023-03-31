import datetime
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method


class BaseSchema:
    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP, default=sa.func.current_timestamp())
    modified_at = sa.Column(sa.TIMESTAMP, onupdate=sa.func.current_timestamp())

    @hybrid_method
    def last_update_older_than(self, seconds: int) -> bool:
        last_update = self.modified_at if self.modified_at else self.created_at
        return (datetime.datetime.now() - last_update).total_seconds() > seconds
