from typing import Any, Iterable, Optional
from flask import Blueprint, jsonify, session


class AuthorizationError(PermissionError):
	pass


def get_login_user_id(session_obj: Any) -> str:
	if session_obj is None:
		return ""
	for key in ("APP_USER_ID", "USER_ID", "LOGIN_USER_ID"):
		value = session_obj.get(key) if hasattr(session_obj, "get") else None
		if value is not None and str(value).strip():
			return str(value).strip()
	return ""


def get_role_id(session_obj: Any) -> str:
	return str((session_obj.get("role_id_SES_session") if hasattr(session_obj, "get") else "") or "").strip()


def get_tenant_id(session_obj: Any) -> str:
	return str((session_obj.get("tenant_id_SES_session") if hasattr(session_obj, "get") else "") or "").strip()


def require_login(session_obj: Any) -> str:
	uid = get_login_user_id(session_obj)
	if not uid:
		raise AuthorizationError("login is required")
	return uid


def require_roles(session_obj: Any, allowed_roles: Iterable[str]) -> str:
	require_login(session_obj)
	role = get_role_id(session_obj)
	allowed = {str(item).strip() for item in allowed_roles if str(item).strip()}
	if not role or role not in allowed:
		raise AuthorizationError("permission denied")
	return role


def require_tenant(session_obj: Any) -> str:
	require_login(session_obj)
	tenant = get_tenant_id(session_obj)
	if not tenant:
		raise AuthorizationError("tenant is required")
	return tenant


def tenant_matches(session_obj: Any, requested_tenant: Optional[str]) -> bool:
	if requested_tenant is None or not str(requested_tenant).strip():
		return True
	return get_tenant_id(session_obj) == str(requested_tenant).strip()


def protect_blueprint_roles(blueprint: Blueprint, allowed_roles: Iterable[str]) -> None:
	roles = tuple(str(role).strip() for role in allowed_roles if str(role).strip())
	if not roles:
		raise ValueError("allowed roles must not be empty")

	@blueprint.before_request
	def verify_blueprint_role():
		try:
			require_roles(session, roles)
		except AuthorizationError:
			return jsonify({"error": "permission denied"}), 403
		return None
