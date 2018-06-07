#!/bin/bash
cat /home/smenon/Quincy/first_reminder_email.txt | msmtp --from=default -t sanjay.menon@gmail.com
