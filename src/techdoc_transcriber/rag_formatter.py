from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class RagSection:
    title: str
    level: int
    content: List[str]


def build_rag_document(
    text: str,
    source_name: str,
    generated_at: datetime | None = None,
    keywords: Iterable[str] | None = None,
) -> str:
    """Build a RAG-optimized Markdown string from Docling output."""
    generated_at = generated_at or datetime.utcnow()
    generated_at = _normalize_timestamp(generated_at)

    source_display = Path(source_name).name or "document"
    metadata = [
        "---",
        f"source: {source_display}",
        f"generated_at: {generated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}",
    ]
    if keywords:
        metadata.append(f"keywords: {', '.join(sorted({kw.strip() for kw in keywords if kw}))}")
    metadata.append("---")

    sections = _extract_sections(text)
    if not sections:
        sections = [RagSection(title="Overview", level=1, content=[])]

    formatted_sections = [_format_section(section) for section in sections]

    return "\n".join(metadata + [""] + formatted_sections)


def _normalize_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _extract_sections(text: str) -> List[RagSection]:
    lines = text.splitlines()
    sections: List[RagSection] = []
    current_section: RagSection | None = None

    heading_pattern = re.compile(r"^(#{1,6})\s+(.*)$")

    for line in lines:
        match = heading_pattern.match(line)
        if match:
            if current_section:
                sections.append(current_section)
            level = len(match.group(1))
            title = match.group(2).strip() or "Untitled Section"
            current_section = RagSection(title=title, level=level, content=[])
            continue

        if current_section is None:
            current_section = RagSection(title="Overview", level=1, content=[])

        current_section.content.append(line.rstrip())

    if current_section:
        sections.append(current_section)

    # remove empty trailing sections
    sections = [sec for sec in sections if sec.content or sec.title]
    return sections


def _format_section(section: RagSection) -> str:
    heading = "##" if section.level == 1 else "#" * min(section.level + 1, 6)
    builder: List[str] = [f"{heading} {section.title}"]

    content_lines = [line for line in section.content if line.strip()]
    if content_lines:
        builder.extend(content_lines[:3])
    else:
        builder.append("_No extracted content._")

    facts = _extract_facts(content_lines)
    if facts:
        builder.extend(["", "**Facts:**"] + [f"- {fact}" for fact in facts])

    return "\n".join(builder)


def _extract_facts(lines: Sequence[str]) -> List[str]:
    facts: List[str] = []
    for line in lines:
        trimmed = line.strip(" \t-*")
        if not trimmed or trimmed.startswith("#"):
            continue
        if ":" not in trimmed:
            continue
        facts.append(trimmed)
        if len(facts) >= 5:
            break
    return facts
