Ezlog2
============
A weibo clone based on flask, bootstrap and mongodb.

-----------------------------------------------------------
## Setup

1. install Python2.7, MongoDB, virtualenv(optional), pip
2. activate vitualenv  
linux:
```
    virtualenv ezlog2
    cd ezlog2
    source bin/activate 
```

3. get source code

    `git clone git@github.com:zhy0216/ezlog2.git`

4. install 3rd libs

    `pip install -r pip_requirements.txt`

5. run

    `python runserver.py`
    if you need instant message push, please run tools/instant_message_push.py

7. unittest

    `nosetests`

-----------------------------------------------------------

## Folder Organize

```
├─aunittest  ------------------------ unittest stuff
├─ezlog2  --------------------------- the main source
│  ├─blueprints --------------------- some sub-apps
│  ├─config     --------------------- some config for site and mongodb
│  ├─controllers  ------------------- route define here
│  ├─libs   ------------------------- some lib I wrote for myself
│  ├─model  ------------------------- model define here
│  ├─static ------------------------- css, js, pic asserts here
│  │  ├─lib   ----------------------- web framework here(bootstrap)
│  │  └─theme ----------------------- some bootstrap theme
│  ├─templates ---------------------- Tempaltes here
│  └─util --------------------------- some helper function define here
└─tools  ---------------------------- some helpful tools
```

## TO-DO

* auto search index, so far you have to make index by hand 
* better template organize
* better UI
* add js template(mustache.js?)
* add front route















