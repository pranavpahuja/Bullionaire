from nicegui import ui

def home_page():
    @ui.page('/home')
    def home_page_def():
        with ui.row().classes('h-screen w-screen justify-center items-center gap-4'):
            ui.label('Welcome to Buillionaire').classes('text-2xl font-bold')
            ui.button('Show Dashboard', on_click=lambda: ui.navigate.to('/dashboard'))