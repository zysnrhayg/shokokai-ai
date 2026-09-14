from typing import Any, Optional
import utils.config as app_config


def write_audit_event(action: str, *, user_id: str = "", tenant_id: str = "",
					  resource: str = "", detail: Optional[dict[str, Any]] = None,
					  outcome: str = "ok") -> str:
	"""Write one normalized audit event and return the emitted message."""
	detail = detail or {}
	msg = (f"AUDIT action={action} outcome={outcome} "
		   f"user={user_id or '-'} tenant={tenant_id or '-'} "
		   f"resource={resource or '-'} detail={detail}")
	app_config.global_log.info(msg)
	return msg
