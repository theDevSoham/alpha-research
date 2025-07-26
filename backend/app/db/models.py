from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from .database import Base

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    status = Column(Text, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Company(Base):
    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
    name = Column(Text)
    domain = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Person(Base):
    __tablename__ = "people"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    full_name = Column(Text)
    email = Column(Text, unique=True)
    title = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ContextSnippet(Base):
    __tablename__ = "context_snippets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(Text)
    entity_id = Column(UUID(as_uuid=True))
    snippet_type = Column(Text, default="research")
    payload = Column(JSONB)
    source_urls = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SearchLog(Base):
    __tablename__ = "search_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    context_snippet_id = Column(UUID(as_uuid=True), ForeignKey("context_snippets.id"))
    iteration = Column(Integer)
    query = Column(Text)
    top_results = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
