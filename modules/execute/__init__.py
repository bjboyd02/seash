import seash_exceptions
import command_callbacks
import os

module_help = """
Execute Module

Using this module, you can simplify the `start` command on all of 
the VMs in your current seash target (e.g., browsegood).

Typically to run an experiment (e.g., experiment.r2py) using 
sensors and blur layers, we need to

user@target !> start dylink.r2py encasementlib.r2py sensor_layer.r2py \
               [any blur layers] experiment.r2py

Using `execute`, the command is simplified:

user@target !> execute [any blur layers] experiment.r2py
"""

# We will add these file names in front of the user-supplied args:
commands_list = ["dylink.r2py", "encasementlib.r2py", "sensor_layer.r2py"]


def simplify_command(input_dict, environment_dict):
  """This function simplifies the `start` command for the user 
  by including three libraries:
  dylink.r2py, encasementlib.r2py, and sensor_layer.r2py
  When a program is run by `execute`, these three filenames do not 
  need to be specified.

  A note on the `input_dict` argument:
  `input_dict` contains our own `command_dict` (see below), with 
  the `"[ARGUMENT]"` sub-key of `children` renamed to what 
  argument the user provided. 
  """
  # Check user input and seash state:
  # 1, Make sure there is an active user key.
  if environment_dict["currentkeyname"] is None:
    raise seash_exceptions.UserError("""Error: Please set an identity before using 'execute'!
Example:

 !> loadkeys your_user_name
 !> as your_user_name
your_user_name@ !>
""")

  # 2, Make sure there is a target to work on.
  if environment_dict["currenttarget"] is None:
    raise seash_exceptions.UserError("""Error: Please set a target to work on before using 'execute'!
Example
your_user_name@ !> on browsegood
your_user_name@browsegood !> 
""")

  try:
    user_files_and_args = input_dict["execute"]["children"].keys()[0]
  except IndexError:
    # The user didn't specify files to execute.
    raise seash_exceptions.UserError("""Error: Missing operand to 'execute'
Please specify which file(s) I should execute, e.g.
your_user_name@browsegood !> execute my_sensor_program.r2py
""")

  # `commands_list`'s first item is the filename to feed into 
  # `command_callbacks.start_remotefn`; all other items plus 
  # the user-specified filenames/args are collected here:
  filenames_and_args = " ".join(commands_list[1:]) + " " + user_files_and_args

  # Construct an input_dict containing command args for seash's 
  # `start FILENAME [ARGS]` function.
  # XXX There might be a cleaner way to do this.
  faked_input_dict = {
      "start": {"name": "start", 'callback': None,
          "children": {
              commands_list[0]: {"callback": command_callbacks.start_remotefn, 
                  "name": "filename",
                  "children": {filenames_and_args: {
                      "callback": command_callbacks.start_remotefn_arg, 
                          "children": {}, "name": "args"}}}}}}
    
  command_callbacks.start_remotefn_arg(faked_input_dict, environment_dict)




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

