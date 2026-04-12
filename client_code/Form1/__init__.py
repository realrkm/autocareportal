from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js import window

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.repeating_panel_1.items = app_tables.users.search()       

        # Any code you write here will run before the form opens.
    def form_show(self, **event_args):
        # Calculate available height (Screen height minus some offset for headers/nav)
        screen_height = window.innerHeight
        grid_height = screen_height - 200  # Adjust '200' based on your top nav size
    
        # Apply the height dynamically to the Data Grid's container
        import anvil.js.window as window
        dom_node = anvil.js.get_dom_node(self.data_grid_1)
        container = dom_node.querySelector('.data-grid-child-panel')
        if container:
            container.style.maxHeight = f"{grid_height}px"
