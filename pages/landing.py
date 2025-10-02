from nicegui import ui

def landing_page():
    @ui.page('/')
    def land_page():
        with ui.row().classes('h-screen w-screen justify-center items-center gap-4'):
            ui.label('Welcome to Buillionaire').classes('text-2xl font-bold')
            ui.button('Login Now', on_click=lambda: ui.navigate.to('/login'))