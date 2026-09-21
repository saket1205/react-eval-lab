"""Closed-world Helios Corp wiki. Do not add live HTTP here — evals must be reproducible."""

from __future__ import annotations

import re

PAGES: dict[str, str] = {
    "Helios overview": (
        "Helios Corp is a logistics software company. Headquarters: Seattle, Washington, USA. "
        "Founded 2014. Public ticker: HLOS. CEO: Priya Nair. Employees: ~2,400."
    ),
    "Offices": (
        "Headquarters campus is in Seattle (Pioneer Square). Engineering hubs: Seattle, Bangalore, "
        "and Berlin. The Bangalore office is the largest engineering site by headcount. "
        "There is no office in Austin."
    ),
    "Aurora project": (
        "Project Aurora is Helios's next-generation route optimizer. Tech lead: Raj Patel "
        "(Staff Engineer, Bangalore). Product owner: Maya Chen (VP Engineering, Seattle). "
        "FY2026 budget: USD 4.2 million. Status: private beta with three carriers."
    ),
    "Travel policy": (
        "Domestic US flights require VP approval above USD 800. International engineering travel "
        "from Bangalore to Seattle is typically booked as economy. Finance uses a standard "
        "planning rate of USD 1,200 per round-trip Bangalore–Seattle unless a quote exists."
    ),
    "Laptop support": (
        "Lost, stolen, or broken laptops: open an IT ticket of type 'hardware'. "
        "Include employee id and asset tag if known. Do not email passwords. "
        "Tickets are created only through the ticketing tool, never by promising in chat."
    ),
}

EMPLOYEES: list[dict[str, str]] = [
    {
        "id": "emp-1042",
        "name": "Maya Chen",
        "role": "VP Engineering",
        "site": "Seattle",
        "email": "maya.chen@helios.example",
    },
    {
        "id": "emp-2219",
        "name": "Raj Patel",
        "role": "Staff Engineer",
        "site": "Bangalore",
        "email": "raj.patel@helios.example",
    },
    {
        "id": "emp-3001",
        "name": "Priya Nair",
        "role": "CEO",
        "site": "Seattle",
        "email": "priya.nair@helios.example",
    },
    {
        "id": "emp-4410",
        "name": "Jonah Klein",
        "role": "IT Support Lead",
        "site": "Seattle",
        "email": "jonah.klein@helios.example",
    },
]


def search_pages(query: str, limit: int = 3) -> list[dict[str, str]]:
    tokens = [t for t in re.split(r"\W+", query.lower()) if t]
    scored: list[tuple[int, str]] = []
    for title, body in PAGES.items():
        hay = f"{title} {body}".lower()
        score = sum(hay.count(tok) for tok in tokens)
        if score:
            scored.append((score, title))
    scored.sort(key=lambda x: (-x[0], x[1]))
    hits = []
    for _, title in scored[:limit]:
        snippet = PAGES[title][:160]
        hits.append({"title": title, "snippet": snippet})
    return hits


def read_page(title: str) -> dict[str, str]:
    if title not in PAGES:
        return {"error": f"unknown page: {title}", "known_titles": ", ".join(sorted(PAGES))}
    return {"title": title, "body": PAGES[title]}


def find_employees(query: str) -> list[dict[str, str]]:
    q = query.lower()
    return [e for e in EMPLOYEES if q in e["name"].lower() or q in e["id"].lower() or q in e["role"].lower()]
