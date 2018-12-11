#
# How do you automate this?
#
# Never leave an M with a non-joined G.

# Initial state:
#
#  4:
#  3:   PmG  PmM  RuG  RuM
#  2:             PuM  SrM
#  1: E TmG  TmM  PuG  SrG  ElG  ElM  DiG  DiM

# What are the legal moves?
# TmGM up  PuG up SrG up
#
# 5 steps later:
#  4:
#  3:   PmG  PmM  RuG  RuM
#  2: E TmG  TmM  PuG  PuM  SrG  SrM
#  1:                      
#
# Now we have all pairs.
# Given 3 pairs, it's always going to be
# MG1 up, M1 down, MG2 up, M2 down, MG3 up, M3 down, M12 up, M2 down.  That leaves:
#
# 21 steps:
#
# 4:    TmM-TmG  PuG  SrG
# 3:    PmG-PmM  RuG-RuM
# 2: E  PuM  SrM
#
# M23 up one. PmG-PmM up, PmM down.  RuG-RuM up, RuM down.
#
# 26 steps:
#
# 4:    TmM-TmG PuG SrG  PmG   RuG
# 3: E  PuM  SrM  PmM  RuM
#
# PuM-SrM up, PuM down, PuM-PmM up, PuM down, PuM-PuM up.
#
# 31.
#
#
# 18 steps.
#
# Give 2 pairs:
# MG1 up, M1 down, MG2 up, M2 down, M12 UP
#
# 5 steps.


#
# 25 is too low
# 33 is too high
