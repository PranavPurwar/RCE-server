import pexpect
from flask import Flask, request
import os
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

sys_shell = os.environ.get('SHELL')

print('Starting shell: ' + sys_shell)

# Start a new shell session
shell = pexpect.spawn(sys_shell)
shell.expect(r'%')  # Wait for the shell prompt


@app.route('/execute', methods=['POST', 'GET'])
def exec():
    if request.method == 'POST':
        try:
            json = request.get_json()
            if os.environ.get('password_protected'):
                if 'pswd' in json and json.get('pswd') != os.environ.get('password'):
                    return 'Wrong password!'.encode()

            command = request.get_json()['command']

            # Use pexpect.run to execute the command
            output = pexpect.run(command, timeout=10)  # Adjust timeout as needed
            
            return output.decode()
        except Exception as e:
            return str(e)
    else:
        return "Send a POST request with a 'command' field.".encode()

is_first = True

def exec_command(cmd: str) -> str:
    print('Executing command: ' + cmd)

    # Send the command to the shell
    shell.sendline(cmd)

    # Wait for the command to finish
    shell.expect(r'%')

    # Get the output without the first (empty) line
    output = shell.before.decode().split('\r\n', 1)

    if len(output) > 1:
        output = output[1]
    else:
        output = shell.before.decode()

    print('Output: ' + output)

    return output

@app.route('/', methods=['POST', 'GET'])
def index():
    json = request.get_json()

    json = request.get_json()
    if os.environ.get('password_protected'):
       if 'pswd' in json and json.get('pswd') != os.environ.get('password'):
            return 'Wrong password!'.encode()

    if json == None:
        json = {
            'command': ''
        }
    
    global is_first
    print(is_first)
    print(json['command'])
    if request.method == 'POST':
        try:
            command = json['command']

            if command == None:
                command = ''

            return exec_command(command)
        except Exception as e:
            return str(e)
        
        is_first = False
    else:
        return "Send a POST request with a 'command' field."

@app.route('/kill')
def kill():
    shell.close(force=True)
    return 'Killed shell'

@app.route('/restart')
def restart():
    shell = pexpect.spawn(sys_shell)
    return 'Restarted shell'

print('Started server...')
serve(app, host='0.0.0.0', port=8888)
