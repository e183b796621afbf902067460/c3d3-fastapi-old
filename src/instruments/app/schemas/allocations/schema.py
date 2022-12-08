from src.instruments.app.schemas.pools.schema import PoolORMSchema, PoolAddSchema, PoolDeleteSchema


class AllocationORMSchema(PoolORMSchema):
    pass


class AllocationAddSchema(PoolAddSchema):
    pass


class AllocationDeleteSchema(PoolDeleteSchema):
    pass
