"""Chat input panel: file/image upload, paste-image, chips, embedded buttons, spinner."""
from nicegui import ui
import asyncio

async def send_message():
    ui.notify("Message sent (stub)")

async def upload_file():
    ui.notify("File uploaded (stub)")

async def paste_image():
    ui.notify("Image pasted (stub)")

def render_chat_panel() -> None:
    """Render chat input panel with upload, paste, chips, spinner."""
    # Use mutable objects for state
    state = {
        'streaming': False,
        'uploaded_files': [],
        'selected_tools': []
    }

    def on_upload(e):
        for file in e.files:
            state['uploaded_files'].append(file.name)
        ui.refresh()

    def remove_file(name):
        state['uploaded_files'].remove(name)
        ui.refresh()

    def open_tool_dialog():
        dialog = ui.dialog()
        with dialog:
            ui.label("Select Tools").classes("text-lg font-bold mb-2")
            tools = ["kb_stub", "ocr_stub", "stream_stub1", "stream_stub2"]
            for tool in tools:
                def select_tool(t=tool):
                    if t in state['selected_tools']:
                        state['selected_tools'].remove(t)
                    else:
                        state['selected_tools'].append(t)
                    ui.refresh()
                ui.button(tool.replace("_", " ").title(), on_click=select_tool).classes("mb-2")
            ui.button("Done", on_click=dialog.close).classes("mt-4")
        dialog.open()

    def is_disabled():
        return state['streaming']

    with ui.card().classes("w-full p-4 flex flex-col items-center"):
        if state['uploaded_files']:
            with ui.row().classes("mb-2"):
                for chip in state['uploaded_files']:
                    # Fix late binding in lambda by using default argument
                    ui.chip(chip).props("removable").on("remove", lambda e, name=chip: remove_file(name))
        chat_input = ui.input("Type your message...", disabled=is_disabled()).props("rounded outlined")
        with ui.row().classes("mt-2"):
            ui.upload(on_upload, multiple=True, auto_upload=True).props("flat").props('disabled' if is_disabled() else '')
            ui.button("Paste Image", on_click=paste_image, disabled=is_disabled()).props("flat")
            ui.button("⚙️", on_click=open_tool_dialog, disabled=is_disabled()).props("flat")
            ui.button("➤", on_click=send_message, disabled=is_disabled()).props("flat")
        if state['streaming']:
            ui.spinner(size="sm", color="primary")
        ui.button(
            "Clear Current Chat History",
            on_click=lambda: ui.notify("History cleared (display-only)"),
            color="negative",
            icon="delete",
            disabled=is_disabled()
        )
