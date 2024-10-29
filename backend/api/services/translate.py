import subprocess
import os

def translate(key, text, operation):
  command_args = ['string', operation, 'AES', 'CBC', key, text]
  command = f"java -cp {os.path.dirname(__file__)}\\mule-secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool {' '.join(command_args)}"
  result = subprocess.run(command.split(), capture_output=True)
  if result.returncode == 0:
    mod = (result.stdout.decode('utf-8')).strip()
    output = ('![' + mod + ']') if (operation == 'encrypt') else (mod)
    return output
  else:
    print('Error:', result.stderr.decode('utf-8'))
    return -1