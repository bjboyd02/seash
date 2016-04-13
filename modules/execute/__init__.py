import seash_exceptions
import command_callbacks
import os

module_help = """
Execute Module

Using this module, you can simplify the `start` command on all of 
the VMs in your current seash target (e.g., browsegood).

Typically to run an experiment (e.g., experiment.r2py) using 
security layers, we need to

user@target !> start dylink.r2py encasementlib.r2py sensor_layer.r2py \
               [any blur layers] experiment.r2py

Using `execute`, the command is simplified:

user@target !> execute [any blur layers] experiment.r2py
"""



def simplify_command(input_dict, environment_dict):
  """This function simplifies three library files specified in `start`:
  dylink.r2py, encasementlib.r2py, and sensor_layer.r2py. When a program
  is run by `execute`, these three files do not need to be specified.

  A note on the input_dict argument:
  `input_dict` contains our own `command_dict` (see below), with 
  the `"[ARGUMENT]"` sub-key of `children` renamed to what 
  argument the user provided. 
  """
  # Check user input and seash state:
  # 1, Make sure there is an active user key.
  if environment_dict["currentkeyname"] is None:
    raise seash_exceptions.UserError("""Error: Please set an identity before using 'uploaddir'!
Example:

 !> loadkeys your_user_name
 !> as your_user_name
your_user_name@ !>
""")

  # 2, Make sure there is a target to work on.
  if environment_dict["currenttarget"] is None:
    raise seash_exceptions.UserError("""Error: Please set a target to work on before using 'uploaddir'!
Example
your_user_name@ !> on browsegood
your_user_name@browsegood !> 
""")


  # Construct an input_dict containing command args for seash's 
  # `upload FILENAME` function.
  # XXX There might be a cleaner way to do this.
  faked_input_dict = {"start": {"name": "start", 
        "children": {dylink.r2py: {"name": "filename"}, 
                     encasementlib.r2py: {"name": "filename"},  
                     sensor_layer.r2py: {"name": "filename"}}}}
    
  command_callbacks.start_remotefn(faked_input_dict, environment_dict)




command_dict = {
  "execute": {
    "name": "execute",
    "callback": simplify_command,
    "summary": "Simplify the `start` command",
    "help_text": module_help,
    "children": {
      "[ARGUMENT]": {
        "name": "",
        "callback": None,
        "children": {},
      }
    }
  }
}


moduledata = {
  'command_dict': command_dict,
  'help_text': module_help,
  'url': None,
}



