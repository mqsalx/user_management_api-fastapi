# /src/shared/presentation/controllers/base_controller.py

from abc import ABC
from typing import Any

from src.shared.domain.repositories.base import IBaseAsyncRepository
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork


class BaseController(ABC):
    """
    BaseController is an abstract base class that provides
        common initialization
    for controllers by setting up the service handler with
        repository and unit of work.

    Subclasses must define their own handler initialization logic as needed.
    """

    def __init__(
        self,
        repository: IBaseAsyncRepository[Any],
        async_unit_of_work: AsyncUnitOfWork
    ) -> None:
        """
        Initialize the base controller with required dependencies.

        Args:
            repository (BaseAsyncRepository): Repository for domain access.
            async_unit_of_work (IAsyncUnitOfWork): Unit of work for
                transactions.
        """
        self._repository: IBaseAsyncRepository[Any] = repository
        self._async_unit_of_work: AsyncUnitOfWork = async_unit_of_work
