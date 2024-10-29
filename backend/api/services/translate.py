import subprocess
import requests
import os

def download_jar(url, filename):
  response = requests.get(url, stream=True)
  if response.status_code == 200:
    with open(filename, 'wb') as f:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)
    print(f'Downloaded {filename} successfully.')
  else:
    print(f'Error downloading {filename}: HTTP status code {response.status_code}')

url = 'https://docs.mulesoft.com/mule-runtime/latest/_attachments/secure-properties-tool.jar'
jar_path = './api/services/assets/mule-secure-properties-tool.jar'

def translate(key, text, operation):
  if len(os.listdir('./api/services/assets')) == 0: 
    filename = jar_path
    download_jar(url, filename)
  else:
    print('No need to download!')
  command_args = ['string', operation, 'AES', 'CBC', key, text]
  command = f"java -cp {jar_path} com.mulesoft.tools.SecurePropertiesTool {' '.join(command_args)}"
  result = subprocess.run(command.split(), capture_output=True)
  if result.returncode == 0:
    print(result.stdout.decode('utf-8'))
    mod = (result.stdout.decode('utf-8')).strip()
    output = ('![' + mod + ']') if (operation == 'encrypt') else (mod)
    return output
  else:
    print('Error:', result.stderr.decode('utf-8'))
    return -1