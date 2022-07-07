FAIR Project (Forex Artificial Intelligence Repository)
V2.0

installing tpqoa packages when errors are present

Download git from: https://git-scm.com/downloads

If tpqoa is already intalled: pip uninstall tpqoa

If this command doesn't work, see below: pip install git+https://github.com/yhilpisch/tpqoa

ERRORS INSTALLING TPQOA:
    Verify that git is added to path. The default is: C:\Program Files\Git\cmd
    If it is added topath then go ahead and restart your computer, that is required after installing git.

    Some digging is required but you may come across a tpqoa whl (wheel) file. You can download it and place it inside
    your user folder (whatever your username is) then download it by copying the path to that file.

    Multiple python versions? Buddy that one gets a bit tricky.... Here are some steps you can take to work that out.
        python --version (shows the versions of python installed)

        python-<version> -m -pip <command> (example below)

        python-3.10 -m -pip install git+https://github.com/yhilpisch/tpqoa

        I highly recommend not dealing with multiple versions of python unless absolutely necessary.

    If none of these solutions work then post a comment, and I will find a solution for you.


Directories of note:
    Oanda
    src

Oanda
    This folder is the current AI system. There is a lot going on here and at the moment it isn't fully set up to run.
    Further explanations will be added soon.