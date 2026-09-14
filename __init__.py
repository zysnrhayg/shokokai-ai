# Import the "app" variable (or module) from the current package's "run" module
from .run import app

# Define a list called "all" and include "app" as an element in it
# This is typically used to explicitly specify which modules or variables are imported 
# when using the "*" import statement within a package
all = [app]
