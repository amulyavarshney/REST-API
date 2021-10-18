from typing import List, Optional
from datetime import date
from pydantic import BaseModel

#comman attributes
class ProfileBase(BaseModel):
    name: str
    dob: date
    status: Optional[str] = "ACTIVE"

# additional attributes while posting a Profile
class ProfileCreate(ProfileBase):
    pass

# additional attributes in the database
class Profile(ProfileBase):
    id: int
    # created: datetime = datetime.now()

    class Config:
        orm_mode = True

# to return after posting a Profile
class ProfileId(BaseModel):
    id: int

    class Config:
        orm_mode = True

# to pause the profile status
class ProfilePause(BaseModel):
    status = "PAUSED"

    class Config:
        orm_mode = True

# to activate the profile status
class ProfileActivate(BaseModel):
    status = "ACTIVE"

    class Config:
        orm_mode = True