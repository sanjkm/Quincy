#!/bin/bash
cat /home/smenon/Quincy/second_reminder_email.txt | msmtp --from=default -t sanjay.menon@gmail.com
