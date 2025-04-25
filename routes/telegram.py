import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from telethon import TelegramClient
from telethon.errors import FloodWaitError, PhoneNumberFloodError
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession

from decorators.auth_guard import auth_guard
from models.telegram.get_chats import GetChatsRequest
from models.telegram.send_code_to_number import SendCodeToPhoneRequest
from utils.db import mongodb

router = APIRouter(prefix="/telegram", dependencies=[Depends(auth_guard)])

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("session_name", API_ID, API_HASH)


@router.post('/authenticate/send-code')
async def send_code_to_phone(auth_request: SendCodeToPhoneRequest):
    """
    Send a login code to the user's phone number.
    """
    try:
        if not client.is_connected():
            await client.connect()

        # Send the login code and get the phone_code_hash
        code_request = await client.send_code_request(auth_request.phone_number)
        return {
            "message": "Code sent to the provided phone number.",
            "phone_code_hash": code_request.phone_code_hash
        }
    except PhoneNumberFloodError:
        raise HTTPException(
            status_code=429,
            detail="Too many attempts. Please wait before trying again."
        )
    except FloodWaitError as e:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Please wait {e.seconds} seconds."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send code: {str(e)}"
        )
    finally:
        await client.disconnect()


@router.post('/authenticate/verify')
async def verify_code_and_fetch_chats(auth_request: GetChatsRequest, user: dict = Depends(auth_guard), ):
    """
    Verify the code and fetch the user's chats.
    """
    try:
        # Connect to the Telegram client without prompting for input
        if not client.is_connected():
            await client.connect()

        # Verify the code using the phone_code_hash
        if auth_request.code and auth_request.phone_code_hash:
            try:
                await client.sign_in(
                    auth_request.phone_number,
                    auth_request.code,
                    phone_code_hash=auth_request.phone_code_hash
                )
            except SessionPasswordNeededError:
                # Handle 2FA
                if not auth_request.password:
                    raise HTTPException(status_code=400, detail="2FA password required.")
                await client.sign_in(password=auth_request.password)
        else:
            raise HTTPException(
                status_code=400,
                detail="Verification code and phone_code_hash are required."
            )

        active_user = await mongodb.db["users"].find_one({"email": user["email"]})
        if not active_user:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        session_string = StringSession.save(client.session)

        await mongodb.db["users"].update_one(
            {"email": user["email"]},
            {"$set": {"telegram_session": session_string}}
        )
        return {"message": "Authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify code or fetch chats: {str(e)}")
    finally:
        # Disconnect the client
        await client.disconnect()


@router.get('/chats')
async def get_user_chats(user: dict = Depends(auth_guard)):
    """
    Fetch the user's chats using the saved Telegram session.
    """
    try:
        # Retrieve the user's telegram_session from the database
        active_user = await mongodb.db["users"].find_one({"email": user["email"]})
        if not active_user or "telegram_session" not in active_user:
            raise HTTPException(
                status_code=404,
                detail="Telegram session not found. Please authenticate first."
            )

        session_string = active_user["telegram_session"]

        # Initialize the Telegram client with the saved session
        async with TelegramClient(StringSession(session_string), API_ID, API_HASH) as session_client:
            # Fetch the user's chats
            chats = [
                {"name": dialog.name, "id": dialog.id}
                async for dialog in session_client.iter_dialogs()
            ]

        return {"message": "Chats fetched successfully", "chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chats: {str(e)}")


async def health_check():
    return {"message": "/telegram is healthy."}
