from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Inventory
from datetime import date
import pandas as pd
import os
import matplotlib.pyplot as plt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add_item/")
def add_item(item_name: str, quantity: int, unit_price: float, added_date: date = date.today(), db: Session = Depends(get_db)):
    new_item = Inventory(item_name=item_name, quantity=quantity, unit_price=unit_price, added_date=added_date)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"msg": "Item added", "item_id": new_item.id}

@router.get("/report/")
def generate_report(db: Session = Depends(get_db)):
    items = db.query(Inventory).all()
    data = [{"item_name": i.item_name, "quantity": i.quantity, "unit_price": i.unit_price, "added_date": i.added_date} for i in items]
    df = pd.DataFrame(data)

    os.makedirs('/data/reports', exist_ok=True)
    csv_path = f"/data/reports/inventory_report.csv"
    df.to_csv(csv_path, index=False)

    # Plot example
    plt.figure(figsize=(10,5))
    df.groupby("added_date")["quantity"].sum().plot(kind="bar", color="#2E86AB")
    plt.title("Daily Inventory Added")
    plt.xlabel("Date")
    plt.ylabel("Quantity")
    plot_path = f"/data/reports/inventory_plot.png"
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

    return {"csv": csv_path, "plot": plot_path}
