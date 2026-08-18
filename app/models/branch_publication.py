from pydantic import BaseModel


class BranchPublication(BaseModel):
    """Outcome of the optional commit-and-push step."""

    requested: bool = False
    published: bool = False
    branch: str | None = None
    remote: str = "origin"
    commit: str | None = None
    message: str = "La publicaciÃ³n de rama no fue solicitada."
