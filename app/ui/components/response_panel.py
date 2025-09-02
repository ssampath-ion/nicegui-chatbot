"""Response panel: final LLM response display."""
from nicegui import ui

def render_response_panel() -> None:
    """Render response panel."""
    with ui.card().classes("w-full p-4 mt-2"):
        show_thinking = {'value': False}
        def on_switch(e):
            show_thinking['value'] = e.value
            ui.refresh()
        ui.switch("Show Thinking", value=show_thinking['value'], on_change=on_switch).classes("mb-2")
        thoughts = [
            "Plan: run selected tools in parallel.",
            "[kb_stub] Knowledge Base:",
            "[stream_stub1] StreamStub1 output chunk 1"
        ]
        if show_thinking['value']:
            with ui.column().classes("mb-2"):
                for thought in thoughts:
                    ui.label(thought).classes("text-sm")
        ui.label("Response:").classes("font-semibold mb-2")
        ui.label("[Final response will appear here]").classes("text-lg")
