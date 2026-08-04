from fastapi import APIRouter, HTTPException, status

from backend.app.schemas.notice_schemas import (
    NoticeCreate,
    NoticeDeleteResult,
    NoticeDetail,
    NoticeListItem,
    NoticeUpdate,
)
from backend.app.services import notice_service


router = APIRouter(prefix="/notices", tags=["notices"])


def _raise_http_error(error: Exception) -> None:
    """서비스 계층 예외를 API 응답으로 변환합니다."""

    if isinstance(error, notice_service.NoticeNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="공지사항을 찾을 수 없습니다.")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="공지사항 처리 중 오류가 발생했습니다.",
    )


@router.post("", response_model=NoticeDetail, status_code=status.HTTP_201_CREATED)
def create_notice(payload: NoticeCreate) -> dict:
    """제목과 본문으로 공지를 등록합니다."""

    try:
        return notice_service.create_notice(payload.title, payload.content)
    except (notice_service.NoticeDatabaseError, notice_service.NoticeNotFoundError) as error:
        _raise_http_error(error)


@router.get("", response_model=list[NoticeListItem])
def list_notices() -> list[dict]:
    """공지 ID와 제목 목록을 최신순으로 조회합니다."""

    try:
        return notice_service.list_notices()
    except notice_service.NoticeDatabaseError as error:
        _raise_http_error(error)


@router.get("/{notice_id}", response_model=NoticeDetail)
def get_notice(notice_id: int) -> dict:
    """공지 상세를 조회합니다."""

    try:
        return notice_service.get_notice(notice_id)
    except (notice_service.NoticeDatabaseError, notice_service.NoticeNotFoundError) as error:
        _raise_http_error(error)


@router.put("/{notice_id}", response_model=NoticeDetail)
def update_notice(notice_id: int, payload: NoticeUpdate) -> dict:
    """공지 제목과 본문을 수정합니다."""

    try:
        return notice_service.update_notice(notice_id, payload.title, payload.content)
    except (notice_service.NoticeDatabaseError, notice_service.NoticeNotFoundError) as error:
        _raise_http_error(error)


@router.delete("/{notice_id}", response_model=NoticeDeleteResult)
def delete_notice(notice_id: int) -> dict[str, str]:
    """공지 하나를 삭제합니다."""

    try:
        notice_service.delete_notice(notice_id)
    except (notice_service.NoticeDatabaseError, notice_service.NoticeNotFoundError) as error:
        _raise_http_error(error)
    return {"message": "삭제 되었습니다"}

