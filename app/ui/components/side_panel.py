"""Left drawer: tools selector, recent tools chips."""
from nicegui import ui
from typing import List

def render_side_panel() -> None:
    """Render toggleable session list with search, edit, delete, and activate actions."""
    state = {
        'panel_open': True,
        'sessions': [
            {"id": 1, "name": "NiceGUI multi-agent frame..."},
            {"id": 2, "name": "Open-source chat framework"},
            {"id": 3, "name": "Chat GUI framework"},
        ],
        'active_session': 1,
        'search_text': ""
    }

    def toggle_panel():
        state['panel_open'] = not state['panel_open']
        ui.refresh()

    def activate_session(session_id):
        state['active_session'] = session_id
        ui.notify(f"Activated session {session_id}")
        ui.refresh()

    def delete_session(session_id):
        ui.notify(f"Deleted session {session_id}")
        state['sessions'] = [s for s in state['sessions'] if s['id'] != session_id]
        ui.refresh()

    def rename_session(session, new_name):
        session["name"] = new_name
        ui.notify(f"Renamed session {session['id']} to {new_name}")
        ui.refresh()

    def on_search_change(e):
        state['search_text'] = e.value
        ui.refresh()

    with ui.left_drawer().classes("bg-white w-72 p-4"):
        with ui.row().classes("justify-between items-center mb-2"):
            ui.label("Chats").classes("text-lg font-bold")
            ui.button("☰", on_click=toggle_panel).props("flat")
        if state['panel_open']:
            ui.input("Search chats", value=state['search_text'], on_change=on_search_change).props("clearable outlined dense")
            filtered_sessions = [s for s in state['sessions'] if state['search_text'].lower() in s["name"].lower()]
            for session in filtered_sessions:
                with ui.row().classes("items-center mb-2"):
                    name_input = ui.input(value=session["name"]).props("dense outlined")
                    name_input.on("change", lambda e, s=session: rename_session(s, e.value))
                    ui.button("🖉", on_click=lambda s=session: name_input.focus()).props("flat")
                    ui.button("🗑️", on_click=lambda s=session: delete_session(s["id"])).props("flat")
                    ui.button(
                        "Activate",
                        on_click=lambda s=session: activate_session(s["id"]),
                        disabled=state['active_session'] == session["id"]
                    ).props("flat")
