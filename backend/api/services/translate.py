import subprocess
import os
jar_path = 'services/mule-secure-properties-tool.jar'

def translate(key, text, operation):
  directory_path = "services/"  # Replace with the actual path

  try:
    for filename in os.listdir(directory_path):
      filepath = os.path.join(directory_path, filename)
      print(filepath)
  except FileNotFoundError:
    print(f"Directory '{directory_path}' not found.")
  except OSError as error:
    print(f"Error accessing directory: {error}")

  command_args = ['string', operation, 'AES', 'CBC', key, text]
  command = f"java -cp {jar_path} com.mulesoft.tools.SecurePropertiesTool {' '.join(command_args)}"
  result = subprocess.run(command.split(), capture_output=True)
  if result.returncode == 0:
    mod = (result.stdout.decode('utf-8')).strip()
    output = ('![' + mod + ']') if (operation == 'encrypt') else (mod)
    return output
  else:
    print('Error:', result.stderr.decode('utf-8'))
    return -1