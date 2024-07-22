---
title: 'Useful tools for working on server clusters'
date: 2022-02-04T15:41:03+02:00
redirect_from:
  - /server-tools
tags:
  - server tools
---

# Monitoring jobs on slurm nodes

## check how many cpus your program is using
- Open `top` by typing `top` in the terminal.
- Press `1` (one) to display a breakdown of CPU usage for each individual CPU.
- Press `f` to enter the field management screen.
- Use the arrow keys to navigate to `P` (which stands for "Last Used CPU" or "P" as in processor) and press `d` to toggle the display of this column.
- Press `Enter` to return to the main screen.