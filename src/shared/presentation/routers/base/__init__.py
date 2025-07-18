# /src/shared/presentation/routes/base/__init__.py

# PY
from typing import Generic, Type, TypeVar
from fastapi import APIRouter, Depends

# Shared
from src.shared.domain.repositories.base import IBaseAsyncRepository
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork
from src.shared.presentation.controllers.base import BaseController
from src.shared.presentation.dependencies.base import BaseDependency

Controller = TypeVar("Controller", bound=BaseController)
Repository = TypeVar("Repository", bound=IBaseAsyncRepository)


class BaseRouter(Generic[Controller, Repository]):
    """
    BaseRoutes is a generic base class for building routers with automatic
        dependency injection.

    This class allows derived classes (e.g. UserRouter) to inherit
        the initialization logic of the controller with the `repository`
        and `unit_of_work` dependencies resolved via FastAPI's `Depends`.


    Class Args:
        router (APIRouter): FastAPI router where the routes
            will be defined.
        controller (Type[Controller]): Type of the controller
            to be instantiated.
        repository (IUserRepository): Injected repository.
        unit_of_work (AsyncUnitOfWork): Unit of work injected.
    """

    def __init__(
        self,
        router: APIRouter,
        controller: Type[Controller],
        repository: Repository = Depends(
            dependency=BaseDependency().get_repository
        ),
        async_unit_of_work: AsyncUnitOfWork = Depends(
            dependency=BaseDependency().get_async_unit_of_work
        ),
    ) -> None:
        """
        The Constructor method initializes the use case with a session of the
            database and an instance of the repository.

        Args:
            router (APIRouter): FastAPI router where the routes
                will be defined.
            controller (Type[Controller]): Type of the controller
                to be instantiated.
            repository (IUserRepository): Injected repository.
            unit_of_work (AsyncUnitOfWork): Unit of work injected.
        """
        self._router: APIRouter = router
        self._controller: Controller = controller(
            repository=repository,
            async_unit_of_work=async_unit_of_work,
        )
