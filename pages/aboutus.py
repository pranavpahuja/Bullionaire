from nicegui import ui

def register_about():
    @ui.page('/about')
    def about_page():
        with ui.column().classes('items-center p-4'):
            ui.label('ℹ️ About Page').classes('text-2xl font-bold')
            ui.button('Back to Home', on_click=lambda: ui.navigate.to('/'))