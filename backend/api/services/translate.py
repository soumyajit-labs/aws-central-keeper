import subprocess
import os
from django.conf import settings
from django.templatetags.static import static

def translate(key, text, operation):
  file_path = os.path.join(settings.BASE_DIR, static('mule-secure-properties-tool.jar'))
  command_args = ['string', operation, 'AES', 'CBC', key, text]
  command_arg_str = ' '.join(command_args)
  command = 'java -cp ' + (file_path) + ' com.mulesoft.tools.SecurePropertiesTool ' + (command_arg_str)
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