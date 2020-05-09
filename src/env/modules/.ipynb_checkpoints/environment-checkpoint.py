# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
class Environment():
    deinit__(self):
        self.obj = []
        self.contact = []
    
    def add_obj(self, new_obj):
        self.obj.append(new_obj)
        
    def add_contact(self, new_contact):
        self.contact.append(new_contact)
    
    
# -


