# /src/shared/infrastructure/unit_of_work/__init__.py

# PY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class AsyncUnitOfWork:
    """
    Asynchronous implementation of the Unit of Work pattern.

    This class manages a SQLAlchemy asynchronous session and ensures that
    transactions are either committed or rolled back based on the outcome
    of the operations within the context block.

    It is designed to be used with Python's async
        context manager (`async with`).

    Class Args:
        async_session_db (AsyncSession): The SQLAlchemy
            async session instance.
    """

    def __init__(self, async_session_db: AsyncSession) -> None:
        """
        Initializes the unit of work with an asynchronous SQLAlchemy session.

        Args:
            async_session_db (AsyncSession): The SQLAlchemy
                async session instance.
        """
        self._async_session_db: AsyncSession = async_session_db
        self._committed = False

    async def __aenter__(self):
        """
        Enters the asynchronous context.

        Returns:
            AsyncUnitOfWork: The current instance to be used
                within the context.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore  # noqa: E501
        """
        Exits the asynchronous context.

        Commits the transaction if no exception occurred,
        otherwise rolls back the transaction.

        Args:
            exc_type: Exception type, if any.
            exc_val: Exception value, if any.
            exc_tb: Traceback object, if any.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self._async_session_db.close()

    async def commit(self) -> None:
        """
        Commits the current transaction if it hasn't been committed yet.

        If an error occurs during the commit, the transaction is rolled back
        and the exception is re-raised.

        Raises:
            SQLAlchemyError: If the commit fails.
        """
        if not self._committed:
            try:
                await self._async_session_db.commit()
                self._committed = True
            except SQLAlchemyError:
                await self.rollback()
                raise

    async def rollback(self) -> None:
        """
        Rolls back the current transaction and marks it as uncommitted.
        """
        await self._async_session_db.rollback()
        self._committed = False
