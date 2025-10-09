#!/usr/bin/env python3
"""
Authentication and Authorization Module
JWT token-based authentication with secure session management
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    scopes: list = []

class User(BaseModel):
    user_id: str
    email: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    created_at: str
    rate_limit_tier: str = "free"  # free, basic, premium

# Authentication utilities
class AuthService:
    """Authentication service for JWT token management"""
    
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        
        # In-memory token blacklist (use Redis in production)
        self.token_blacklist = set()
        
        # In-memory user store (use DynamoDB in production)
        self.users: Dict[str, User] = {}
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    def create_access_token(
        self, 
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            data: Token payload data
            expires_delta: Optional expiration time delta
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "jti": secrets.token_urlsafe(16)  # JWT ID for revocation
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> TokenData:
        """
        Decode and validate JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            TokenData with user information
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            # Check if token is blacklisted
            if token in self.token_blacklist:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Decode token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            user_id: str = payload.get("sub")
            session_id: str = payload.get("session_id")
            scopes: list = payload.get("scopes", [])
            
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return TokenData(
                user_id=user_id,
                session_id=session_id,
                scopes=scopes
            )
            
        except JWTError as e:
            logger.error(f"JWT decode error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def revoke_token(self, token: str):
        """Add token to blacklist"""
        self.token_blacklist.add(token)
        logger.info(f"Token revoked")
    
    def create_user(
        self, 
        user_id: str, 
        email: Optional[str] = None,
        rate_limit_tier: str = "free"
    ) -> User:
        """
        Create new user
        
        Args:
            user_id: User identifier
            email: Optional email address
            rate_limit_tier: Rate limit tier (free, basic, premium)
            
        Returns:
            User object
        """
        user = User(
            user_id=user_id,
            email=email,
            is_active=True,
            is_admin=False,
            created_at=datetime.now(timezone.utc).isoformat(),
            rate_limit_tier=rate_limit_tier
        )
        
        self.users[user_id] = user
        logger.info(f"User created: {user_id}")
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def authenticate_user(self, user_id: str) -> Optional[User]:
        """
        Authenticate user (simplified for hackathon)
        
        In production, this would verify credentials against a database
        """
        user = self.get_user(user_id)
        
        if not user:
            # Auto-create user for hackathon demo
            user = self.create_user(user_id)
        
        if not user.is_active:
            return None
        
        return user
    
    def create_session_token(
        self, 
        user_id: str, 
        session_id: str,
        scopes: list = None
    ) -> Token:
        """
        Create session token for user
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            scopes: Optional permission scopes
            
        Returns:
            Token object with access token
        """
        if scopes is None:
            scopes = ["agent:create", "agent:read", "agent:export"]
        
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        
        access_token = self.create_access_token(
            data={
                "sub": user_id,
                "session_id": session_id,
                "scopes": scopes
            },
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.access_token_expire_minutes * 60
        )

# Global auth service instance
_auth_service: Optional[AuthService] = None

def get_auth_service() -> AuthService:
    """Get authentication service instance"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service

# Dependency for protected endpoints
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenData:
    """
    Dependency to get current authenticated user
    
    Args:
        credentials: HTTP Bearer credentials
        auth_service: Authentication service
        
    Returns:
        TokenData with user information
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    token_data = auth_service.decode_token(token)
    
    # Verify user exists and is active
    user = auth_service.get_user(token_data.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data

# Optional authentication (for public endpoints with optional auth)
async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[TokenData]:
    """
    Optional authentication dependency
    
    Returns None if no token provided, otherwise validates token
    """
    if not authorization:
        return None
    
    if not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    
    try:
        return auth_service.decode_token(token)
    except HTTPException:
        return None

# Scope verification
def require_scope(required_scope: str):
    """
    Dependency factory for scope verification
    
    Args:
        required_scope: Required permission scope
        
    Returns:
        Dependency function
    """
    async def verify_scope(
        token_data: TokenData = Depends(get_current_user)
    ) -> TokenData:
        if required_scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required scope: {required_scope}"
            )
        return token_data
    
    return verify_scope
