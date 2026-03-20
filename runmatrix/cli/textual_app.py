from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class RunmatrixApp(App[None]):
    """Minimal first-class TUI shell for runmatrix."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("runmatrix TUI scaffold", id="body")
        yield Footer()
