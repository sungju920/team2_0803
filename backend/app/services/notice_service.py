"""공지사항의 Supabase 데이터 처리 로직입니다."""

from datetime import datetime, timezone
from typing import Any

from app.core.supabase_client import get_supabase_client


TABLE_NAME = "notices"
DEFAULT_WRITER = "관리자"


class NoticeNotFoundError(Exception):
    """요청한 공지사항이 없을 때 발생합니다."""


class NoticeDatabaseError(Exception):
    """Supabase 처리 중 문제가 생겼을 때 발생합니다."""


def _data_or_database_error(response: Any) -> list[dict[str, Any]]:
    """Supabase 응답의 데이터를 안전하게 꺼냅니다."""

    data = getattr(response, "data", None)
    if data is None:
        raise NoticeDatabaseError("공지사항 데이터를 처리하지 못했습니다.")
    return data


def _get_notice(notice_id: int) -> dict[str, Any] | None:
    """공지 하나를 찾고, 없으면 None을 반환합니다."""

    try:
        response = (
            get_supabase_client()
            .table(TABLE_NAME)
            .select("*")
            .eq("id", notice_id)
            .execute()
        )
        data = _data_or_database_error(response)
    except NoticeDatabaseError:
        raise
    except Exception as error:
        raise NoticeDatabaseError("공지사항 조회 중 데이터베이스 오류가 발생했습니다.") from error

    return data[0] if data else None


def create_notice(title: str, content: str) -> dict[str, Any]:
    """작성자가 관리자 고정값인 새 공지사항을 등록합니다."""

    try:
        response = (
            get_supabase_client()
            .table(TABLE_NAME)
            .insert({"title": title, "content": content, "writer": DEFAULT_WRITER})
            .execute()
        )
        data = _data_or_database_error(response)
    except NoticeDatabaseError:
        raise
    except Exception as error:
        raise NoticeDatabaseError("공지사항 등록 중 데이터베이스 오류가 발생했습니다.") from error

    if not data:
        raise NoticeDatabaseError("등록된 공지사항을 찾을 수 없습니다.")
    return data[0]


def list_notices() -> list[dict[str, Any]]:
    """최신 등록순으로 공지 ID와 제목만 조회합니다."""

    try:
        response = (
            get_supabase_client()
            .table(TABLE_NAME)
            .select("id,title")
            .order("created_at", desc=True)
            .execute()
        )
        return _data_or_database_error(response)
    except NoticeDatabaseError:
        raise
    except Exception as error:
        raise NoticeDatabaseError("공지사항 목록 조회 중 데이터베이스 오류가 발생했습니다.") from error


def get_notice(notice_id: int) -> dict[str, Any]:
    """공지 상세 정보를 조회합니다."""

    notice = _get_notice(notice_id)
    if notice is None:
        raise NoticeNotFoundError
    return notice


def update_notice(notice_id: int, title: str, content: str) -> dict[str, Any]:
    """공지 제목과 본문을 수정하고 수정 시각을 갱신합니다."""

    get_notice(notice_id)
    try:
        response = (
            get_supabase_client()
            .table(TABLE_NAME)
            .update(
                {
                    "title": title,
                    "content": content,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            .eq("id", notice_id)
            .execute()
        )
        data = _data_or_database_error(response)
    except NoticeDatabaseError:
        raise
    except Exception as error:
        raise NoticeDatabaseError("공지사항 수정 중 데이터베이스 오류가 발생했습니다.") from error

    if not data:
        raise NoticeDatabaseError("수정된 공지사항을 찾을 수 없습니다.")
    return data[0]


def delete_notice(notice_id: int) -> None:
    """공지사항을 삭제합니다."""

    get_notice(notice_id)
    try:
        get_supabase_client().table(TABLE_NAME).delete().eq("id", notice_id).execute()
    except Exception as error:
        raise NoticeDatabaseError("공지사항 삭제 중 데이터베이스 오류가 발생했습니다.") from error

