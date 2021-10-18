from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="HappilyEver", docs_url="/", redoc_url="/doc")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/profiles", tags=["Create Profile"], response_model=schemas.ProfileId)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = crud.get_same_profile(db, name=profile.name, dob=profile.dob, status=profile.status)
    if db_profile:
        raise HTTPException(status_code=409, detail="Profile already exists")
    return crud.create_profile(db=db, profile=profile)


@app.get("/profiles", tags=["View Profile"], response_model=List[schemas.Profile])
# def read_profiles(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
#     profiles = crud.get_profiles(db, skip=skip, limit=limit)
def read_profiles(db: Session = Depends(get_db)):
    db_profiles = crud.get_profiles(db)
    if db_profiles is None:
        raise HTTPException(status_code=404, detail="No profiles exist!")
        # return {"message": "No profiles exist!"}
    return db_profiles


@app.get("/profiles/{profile_id}", tags=["View Profile"], response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Id doesn’t exist!")
    return db_profile


@app.get("/paused_profiles", tags=["View Profile"], response_model=List[schemas.Profile])
def read_paused_profiles(db: Session = Depends(get_db)):
    db_profiles = crud.get_paused_profiles(db)
    if db_profiles is None:
        raise HTTPException(status_code=404, detail="No profiles exist!")
    return db_profiles


@app.patch("/profiles/{profile_id}", tags=["Update Status"])
def update_status(profile_id: int, db: Session = Depends(get_db)):
    # getting the existing data
    db_profile = crud.get_profile(db, profile_id=profile_id)
    # db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).one_or_none()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Id doesn’t exist!")
    return crud.update_status(db=db, db_profile=db_profile)


@app.delete("/profiles/{profile_id}", tags=["Delete Profile"])
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    # getting the existing data
    db_profile = crud.get_profile(db, profile_id=profile_id)
    # db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).one_or_none()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Id doesn’t exist!")
    return crud.delete_profile(db=db, db_profile=db_profile)
