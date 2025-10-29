"""
FastAPI dependencies for dependency injection.

Define dependencies here that will be injected into route handlers.

Example:
    def get_database() -> Database:
        '''Get database connection.'''
        return Database()

    def get_item_service(db: Database = Depends(get_database)) -> ItemService:
        '''Get item service with database dependency.'''
        return ItemService(database=db)

Usage in routes:
    @router.get("/items/{item_id}")
    async def get_item(
        item_id: str,
        service: ItemService = Depends(get_item_service)
    ):
        return await service.get_item(item_id)

"""
