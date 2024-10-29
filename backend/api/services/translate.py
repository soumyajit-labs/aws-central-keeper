import subprocess
import os

def translate(key, text, operation):
  command_args = ['string', operation, 'AES', 'CBC', key, text]
  command_arg_str = ' '.join(command_args)
  command = 'java -cp assets/mule-secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool ' + (command_arg_str)
  print('>>>> COMMAND : ' + command)
  try:
    result = subprocess.run(command.split(), capture_output=True)
  except Exception as e: 
    print('>>>> ERROR : ' + e)
  if result.returncode == 0:
    mod = (result.stdout.decode('utf-8')).strip()
    output = ('![' + mod + ']') if (operation == 'encrypt') else (mod)
    return output
  else:
    print('Error:', result.stderr.decode('utf-8'))
    return -1