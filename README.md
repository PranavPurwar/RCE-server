# Running

Install the dependencies first.

```py
pip3 install -r requirements.txt
```

Now for running the server

```py
python3 main.py
```

Set a custom server password by editing the .env file

```
password=new-password
```

## Note
If you decide to modify the password, edit the 'pswd' parameter to the new value while sending request.
To disable password protection, set `password_protected` environment variable to False

You can test the connection on the computer like this

```sh
curl -X POST -H "Content-Type: application/json" -d '{"command":"ls", "pswd":"sshIsAwesome"}' http://localhost:8888/
```

At the start of the session, you might need to send the request twice before getting response back. This is a bug which I wasn't able to come up with a solution for.

This should list all files in the folder where main.py is situated.
It uses a single terminal session for running all the commands at `/`.

For single-use, for example if you just need to delete a file, just do

```sh
curl -X POST -H "Content-Type: application/json" -d '{"command":"ls", "pswd":"sshIsAwesome"}' http://localhost:8888/execute
```

To kill the shell, run

```sh
curl http://localhost:8888/kill
```

To restart the shell, run

```sh
curl http://localhost:8888/restart
```
