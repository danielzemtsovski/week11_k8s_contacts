import data_interactor
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI(title="Contact Manager API", version="1.0.0")


class CreateContact(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

@app.get("/contacts")
def get_contact():
    try:
        contacts = data_interactor.get_all_contacts()
        return contacts
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"you have an error: {e}")


@app.post("/contacts")
def create_contact(contact: CreateContact):
    try:
        new_id = data_interactor.create_contact(contact.dict())
        return {"message": "Contact created successfully", "id": new_id}
    except Exception:
        raise HTTPException(status_code=400, detail="contact creation failed")


@app.put("/contacts/{id}")
def update_contact(id: str, contact: CreateContact):
    success = data_interactor.update_contact(id, contact.dict())
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact updated successfully"}


@app.delete("/contacts/{id}")
def delete_contact(id: str):
    success = data_interactor.delete_contact(id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)