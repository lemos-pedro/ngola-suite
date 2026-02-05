"""
ZENTURY - Middleware
Rastreabilidade de requisições - Princípio 5
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable

logger = logging.getLogger(__name__)

class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware de rastreabilidade"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        method = request.method
        path = request.url.path
        query_string = request.url.query
        ip_address = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        self._log_request(
            method=method,
            path=path,
            query=query_string,
            ip=ip_address,
            user_agent=user_agent,
            status_code=response.status_code,
            process_time=process_time,
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-IP-Address"] = ip_address
        
        return response
    
    @staticmethod
    def _get_client_ip(request: Request) -> str:
        if "x-forwarded-for" in request.headers:
            return request.headers["x-forwarded-for"].split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"
    
    @staticmethod
    def _log_request(
        method: str,
        path: str,
        query: str,
        ip: str,
        user_agent: str,
        status_code: int,
        process_time: float,
    ) -> None:
        if path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return
        
        full_path = f"{path}"
        if query:
            full_path += f"?{query}"
        
        log_msg = (
            f"📝 HTTP {method} {full_path} "
            f"| Status: {status_code} "
            f"| Time: {process_time*1000:.2f}ms "
            f"| IP: {ip}"
        )
        
        if status_code >= 500:
            logger.error(log_msg)
        elif status_code >= 400:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting - Princípio 4"""
    
    def __init__(self, app, requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.requests_limit = requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ip = self._get_client_ip(request)
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        if ip not in self.requests:
            self.requests[ip] = []
        
        self.requests[ip] = [
            (ts, count) for ts, count in self.requests[ip]
            if ts > window_start
        ]
        
        total_requests = sum(count for _, count in self.requests[ip])
        
        if total_requests >= self.requests_limit:
            logger.warning(
                f"❌ RATE LIMIT EXCEDIDO: {ip} "
                f"({total_requests}/{self.requests_limit} req)"
            )
            return Response(
                content="Rate limit exceeded",
                status_code=429,
            )
        
        if self.requests[ip]:
            self.requests[ip][-1] = (self.requests[ip][-1][0], total_requests + 1)
        else:
            self.requests[ip].append((current_time, 1))
        
        return await call_next(request)
    
    @staticmethod
    def _get_client_ip(request: Request) -> str:
        if "x-forwarded-for" in request.headers:
            return request.headers["x-forwarded-for"].split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Security headers"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline';"
        )
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        
        return response