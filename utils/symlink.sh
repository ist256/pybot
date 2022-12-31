#!/bin/bash
cp -v ../*.py $HOME/.pybot/
ln -sf $HOME/.pybot /opt/conda/lib/python3.9/site-packages/pybot
cp -v pybot_startup.py $HOME/.pybot/utils/pybot_startup.py 
ln -sf $HOME/.pybot/utils/pybot_startup.py /opt/ipython/profile_default/startup/pybot_startup.py
