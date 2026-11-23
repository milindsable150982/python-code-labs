from fastapi import FastAPI, APIRouter, Depends, HTTPException
from DataAccess.config.database import get_db
from DataAccess.members.models import Member
from DataAccess.members.schema import MemberSchema
from authentication.auth_token import verify_token

route = APIRouter()

router = APIRouter(
    prefix="/members",
    tags=["members"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}, 
               401: {"description": "Unauthorized"}, 
               402: {"description": "Payment Required"},
               400: {"description": "Bad Request"},
               500: {"description": "Internal Server Error"},
               501: {"description": "Not Implemented"}
               }
)


@router.get("/")
async def getMembers(db=Depends(get_db)):
    members = db.query(Member).all()
    return {"members": members}

@router.get("/{id}")
async def getMember(id: int, db=Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return {"member": member}

@router.post("/")
async def createMember(member: MemberSchema, db=Depends(get_db)):
    new_member = Member(
        first_name=member.first_name,
        last_name=member.last_name,
        email=member.email,
        join_date=member.join_date
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return {"member": new_member}

@router.put("/{id}")
async def updateMember(id: int, member_data: MemberSchema, db=Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.first_name = member_data.first_name
    member.last_name = member_data.last_name
    member.email = member_data.email
    db.commit()
    db.refresh(member)
    return {"member": member}

@router.delete("/{id}")
async def deleteMember(id: int, db=Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}