from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.api.wallet.service import WalletService
from botocore.exceptions import ClientError

router = APIRouter()

class Wallet(BaseModel):
    address: str

wallet_service = WalletService()

@router.post("/", response_model=Wallet)
def create_new_wallet(wallet: Wallet):
    try:
        return wallet_service.create_wallet(wallet.address)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise HTTPException(status_code=400, detail="Wallet already exists")
        else:
            raise HTTPException(status_code=500, detail=e.response['Error']['Message'])

@router.get("/", response_model=List[Wallet])
def get_wallets():
    try:
        return wallet_service.get_wallets()
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response['Error']['Message'])

@router.get("/{address}", response_model=Wallet)
def get_wallet_by_address(address: str):
    try:
        return wallet_service.get_wallet_by_address(address)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))