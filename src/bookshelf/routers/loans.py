"""Endpoints for managing loans (borrowing and returning books)."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from bookshelf.database import get_session
from bookshelf.models import Book, Loan, LoanCreate, LoanRead

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("", response_model=list[LoanRead])
def list_loans(
    active_only: bool = False, session: Session = Depends(get_session)
) -> list[Loan]:
    statement = select(Loan)
    if active_only:
        statement = statement.where(Loan.returned_on.is_(None))  # type: ignore[union-attr]
    return list(session.exec(statement).all())


@router.post("", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanCreate, session: Session = Depends(get_session)) -> Loan:
    book = session.get(Book, payload.book_id)
    if book is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=f"Book {payload.book_id} does not exist"
        )

    active_loan = session.exec(
        select(Loan).where(Loan.book_id == payload.book_id, Loan.returned_on.is_(None))  # type: ignore[union-attr]
    ).first()
    if active_loan is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="Book is already on loan"
        )

    loan = Loan.model_validate(payload)
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan


@router.post("/{loan_id}/return", response_model=LoanRead)
def return_loan(loan_id: int, session: Session = Depends(get_session)) -> Loan:
    loan = session.get(Loan, loan_id)
    if loan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Loan not found")
    if loan.returned_on is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="Loan has already been returned"
        )
    loan.returned_on = datetime.now(timezone.utc).date()
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan
