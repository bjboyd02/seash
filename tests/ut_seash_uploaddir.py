"""
Uploads a directory and runs a simple repy file to make sure no errors gets thrown.
"""

import seash
import sys
import seash_dictionary
import seash_modules
import shutil
import os
#pragma out Enabled modules: modules
seash_modules.enable_modules_from_last_session(seash_dictionary.seashcommanddict)

# Prevent printing to console by using test_results.txt as a text dump and redirecting output there
orig_stdout = sys.stdout
sys.stdout = open("test_results.txt", "w")

os.mkdir('test_dir')
os.mkdir('test_dir' + os.path.sep + 'test_subdir')

command_list = [
  'loadkeys guest0', 
  'as guest0', 
  'browse', 
  'on browsegood',
  'show modules',
  'enable uploaddir',
  'disable uploaddir',
  'enable uploaddir',
  'savestate testing_state'
  ]

seash.command_loop(command_list)

sys.stdout.close()

#pragma out Skipping sub-directory 'test_subdir'. You may upload it separately.

# Resets stdout to allow printing to console to allow UTF to catch errors printed by seash
sys.stdout = orig_stdout

command_list = [
  'loadkeys guest0', 
  'as guest0', 
  'loadstate testing_state',
  'uploaddir test_dir', 
]

seash.command_loop(command_list)

# Make sure the uploaddir module is disabled after this run.
# This is to ensure that other modules' tests are not affected by this module.
seash.command_loop(['disable uploaddir'])

shutil.rmtree('test_dir')
