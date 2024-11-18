__package__ = 'archivebox.api'

from uuid import UUID
from typing import List, Any
from datetime import datetime


from ninja import Router, Schema

from .auth import API_AUTH_METHODS

router = Router(tags=['Workers and Tasks'], auth=API_AUTH_METHODS)


class TaskSchema(Schema):
    TYPE: str
    
    id: UUID
    abid: str
    description: str

    status: str
    retry_at: datetime | None
    
    created_at: datetime
    modified_at: datetime
    created_by_id: int
    
    @staticmethod
    def resolve_description(obj) -> str:
        return str(obj)


class ActorSchema(Schema):
    # TYPE: str = 'actors.actor.ActorType'

    # name: str
    #pid: int | None
    idle_count: int
    launch_kwargs: dict[str, Any]
    mode: str
    
    model: str
    statemachine: str
    STATE_FIELD_NAME: str
    # ACTIVE_STATE: str
    FINAL_STATES: list[str]
    EVENT_NAME: str
    CLAIM_ORDER: list[str]
    CLAIM_FROM_TOP_N: int
    CLAIM_ATOMIC: bool
    MAX_TICK_TIME: int
    MAX_CONCURRENT_ACTORS: int
    
    queue: list[TaskSchema]
    past: list[TaskSchema]
    
    @staticmethod
    def resolve_model(obj) -> str:
        return obj.Model.__name__
    
    @staticmethod
    def resolve_statemachine(obj) -> str:
        return obj.StateMachineClass.__name__
    
    @staticmethod
    def resolve_name(obj) -> str:
        return str(obj)

    # @staticmethod
    # def resolve_ACTIVE_STATE(obj) -> str:
    #     return str(obj.ACTIVE_STATE)
    
    @staticmethod
    def resolve_FINAL_STATES(obj) -> list[str]:
        return [str(state) for state in obj.FINAL_STATES]

    @staticmethod
    def resolve_queue(obj) -> list[TaskSchema]:
        return [obj for obj in obj.qs.filter(obj.pending_q | obj.future_q | obj.active_q | obj.stalled_q).order_by('-retry_at')]

    @staticmethod
    def resolve_past(obj) -> list[TaskSchema]:
        return [obj for obj in obj.qs.filter(obj.final_q).order_by('-modified_at')]


class OrchestratorSchema(Schema):
    # TYPE: str = 'actors.orchestrator.Orchestrator'

    #pid: int | None
    exit_on_idle: bool
    mode: str

    actors: list[ActorSchema]
    
    @staticmethod
    def resolve_actors(obj) -> list[ActorSchema]:
        return [actor() for actor in obj.actor_types.values()]


@router.get("/orchestrators", response=List[OrchestratorSchema], url_name="get_orchestrators")
def get_orchestrators(request):
    """List all the task orchestrators (aka Orchestrators) that are currently running"""

    from actors.orchestrator import Orchestrator
    orchestrator = Orchestrator()

    return [orchestrator]


@router.get("/actors", response=List[ActorSchema], url_name="get_actors")
def get_actors(request):
    """List all the task consumer workers (aka Actors) that are currently running"""

    from actors.orchestrator import Orchestrator
    orchestrator = Orchestrator()
    return orchestrator.actor_types.values()