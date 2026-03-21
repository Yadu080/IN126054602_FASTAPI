from fastapi import FastAPI, Query, Response, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# -------------------- DATA --------------------
members = [
    {"id": 1, "name": "Rahul", "age": 22, "plan": "monthly", "is_active": True},
    {"id": 2, "name": "Anita", "age": 25, "plan": "yearly", "is_active": True},
    {"id": 3, "name": "Kiran", "age": 30, "plan": "monthly", "is_active": False},
    {"id": 4, "name": "Arjun", "age": 23, "plan": "monthly", "is_active": True},
    {"id": 5, "name": "Sneha", "age": 27, "plan": "yearly", "is_active": True},
    {"id": 6, "name": "Vikram", "age": 35, "plan": "quarterly", "is_active": False},
    {"id": 7, "name": "Pooja", "age": 21, "plan": "monthly", "is_active": True},
    {"id": 8, "name": "Rohit", "age": 28, "plan": "yearly", "is_active": True},
    {"id": 9, "name": "Meena", "age": 32, "plan": "quarterly", "is_active": False},
    {"id": 10, "name": "Suresh", "age": 40, "plan": "yearly", "is_active": True},
]


trainers = [
    {"id": 1, "name": "John", "specialization": "Cardio"},
    {"id": 2, "name": "Mike", "specialization": "Strength"},
    {"id": 3, "name": "David", "specialization": "Crossfit"},
    {"id": 4, "name": "Ravi", "specialization": "Yoga"},
    {"id": 5, "name": "Amit", "specialization": "Bodybuilding"},
]



sessions = []
session_counter = 1

checkins = []

# -------------------- MODELS --------------------
class SessionRequest(BaseModel):
    member_id: int = Field(gt=0)
    trainer_id: int = Field(gt=0)
    duration: int = Field(gt=0, le=120)
    session_type: str = "group"  # personal / group


class NewMember(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)
    plan: str = Field(min_length=2)


# -------------------- HELPERS --------------------
def find_member(member_id):
    for m in members:
        if m["id"] == member_id:
            return m
    return None


def find_trainer(trainer_id):
    for t in trainers:
        if t["id"] == trainer_id:
            return t
    return None


def calculate_fee(duration, session_type):
    fee = duration * 100
    if session_type == "personal":
        fee += 3000
    return fee


# -------------------- DAY 1 --------------------
@app.get("/")
def home():
    return {"message": "Welcome to Gym Management System"}


@app.get("/members")
def get_members():
    return {"members": members, "total": len(members)}


@app.get("/members/summary")
def summary():
    active = sum(1 for m in members if m["is_active"])
    plans = list(set(m["plan"] for m in members))
    return {
        "total": len(members),
        "active": active,
        "inactive": len(members) - active,
        "plans": plans
    }


@app.get("/sessions")
def get_sessions():
    return {"sessions": sessions, "total": len(sessions)}


@app.get("/members/search")
def search_members(keyword: str):
    result = [
        m for m in members
        if keyword.lower() in m["name"].lower()
        or keyword.lower() in m["plan"].lower()
    ]

    if not result:
        return {"message": "No members found"}

    return {"result": result, "total": len(result)}


@app.get("/members/sort")
def sort_members(sort_by: str = "age", order: str = "asc"):
    if sort_by not in ["age", "name", "plan"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = order == "desc"
    sorted_data = sorted(members, key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted": sorted_data}


@app.get("/members/page")
def paginate_members(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    total = len(members)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "data": members[start:start + limit]
    }


@app.get("/members/filter")
def filter_members(
    plan: Optional[str] = None,
    age: Optional[int] = None,
    is_active: Optional[bool] = None
):
    result = members

    if plan is not None:
        result = [m for m in result if m["plan"].lower() == plan.lower()]

    if age is not None:
        result = [m for m in result if m["age"] == age]

    if is_active is not None:
        result = [m for m in result if m["is_active"] == is_active]

    return {"result": result, "count": len(result)}


@app.get("/members/browse")
def browse_members(
    keyword: Optional[str] = None,
    sort_by: str = "age",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    result = members

    # FILTER
    if keyword:
        result = [
            m for m in result
            if keyword.lower() in m["name"].lower()
            or keyword.lower() in m["plan"].lower()
        ]
    if sort_by not in ["age", "name", "plan"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    # SORT
    reverse = order == "desc"
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # PAGINATION
    start = (page - 1) * limit
    total = len(result)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "data": result[start:start + limit]
    }


@app.get("/members/{member_id}")
def get_member(member_id: int):
    m = find_member(member_id)
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")
    return m


@app.post("/sessions")
def create_session(req: SessionRequest):
    global session_counter

    member = find_member(req.member_id)
    trainer = find_trainer(req.trainer_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    if not member["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive member")

    total_fee = calculate_fee(req.duration, req.session_type)

    session = {
        "session_id": session_counter,
        "member": member["name"],
        "trainer": trainer["name"],
        "duration": req.duration,
        "session_type": req.session_type,
        "fee": total_fee
    }

    sessions.append(session)
    session_counter += 1

    return session


@app.post("/members")
def add_member(member: NewMember, response: Response):
    for m in members:
        if m["name"].lower() == member.name.lower():
            raise HTTPException(status_code=400, detail="Duplicate member")

    new_member = {
        "id": len(members) + 1,
        "name": member.name,
        "age": member.age,
        "plan": member.plan,
        "is_active": True
    }

    members.append(new_member)
    response.status_code = 201
    return new_member


@app.put("/members/{member_id}")
def update_member(
    member_id: int,
    plan: Optional[str] = None,
    is_active: Optional[bool] = None
):
    m = find_member(member_id)
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")

    if plan is not None:
        m["plan"] = plan
    if is_active is not None:
        m["is_active"] = is_active

    return m


@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    m = find_member(member_id)
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")

    if m["is_active"]:
        raise HTTPException(status_code=400, detail="Cannot delete active member")

    members.remove(m)
    return {"message": f"{m['name']} deleted"}


@app.post("/checkin/{member_id}")
def checkin(member_id: int):
    m = find_member(member_id)
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")
    if not m["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive member")
    # prevent duplicate check-in
    for c in checkins:
        if c["member_id"] == member_id:
            raise HTTPException(status_code=400, detail="Already checked in")
    checkins.append({"member_id": member_id})
    return {"message": "Checked in"}


@app.post("/checkout/{member_id}")
def checkout(member_id: int):
    for c in checkins:
        if c["member_id"] == member_id:
            checkins.remove(c)
            return {"message": "Checked out"}

    raise HTTPException(status_code=400, detail="Member not checked in")


@app.get("/sessions/search")
def search_sessions(member_name: str):
    result = [
        s for s in sessions
        if member_name.lower() in s["member"].lower()
    ]
    return {"result": result, "total": len(result)}


@app.get("/sessions/sort")
def sort_sessions(order: str = "asc"):
    reverse = order == "desc"
    sorted_data = sorted(sessions, key=lambda x: x["fee"], reverse=reverse)
    return {"sorted": sorted_data}


@app.get("/sessions/page")
def paginate_sessions(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    total = len(sessions)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "total": total,
        "total_pages": total_pages,
        "data": sessions[start:start + limit]
    }