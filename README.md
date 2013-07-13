Ezlog2
============
A weibo clone

-----------------------------------------------------------
## Setup
1. install MongoDB, virtualenv(optional), pip

2. activate vitualenv

linux:
```
    virtualenv ezlog2
    cd ezlog2
    source bin/activate 
    
```

3. get source code

    git clone git@github.com:zhy0216/ezlog2.git

4. install 3rd libs

    `pip install -r pip_requirements.txt`

5. run

    `python runserver.py`
    if you need instant message push, please run tools/instant_message_push.py

7. unittest

    `nosetests`

-----------------------------------------------------------
