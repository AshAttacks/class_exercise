from pydantic import BaseModel

class MovieInput(BaseModel):
    title: str
    release_year: int


class MovieResponse(MovieInput):
    id: int

class CSVInfo(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: list[str]
    dataset_id: int
    pass

from pydantic import BaseModel, Field

class ProcessingSettings(BaseModel):
    remove_duplicates: bool = True
    # TODO: Add drop_missing as a bool with default True.
    drop_missing: bool = True

class ProcessConfig(BaseModel):
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)

