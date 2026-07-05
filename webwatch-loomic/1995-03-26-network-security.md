---
title: "Network Security"
author: "Tom Munnecke"
publication: "Web Watch column, San Diego Daily Transcript"
date: 1995-03-26
loomic:
  loom: webwatch-1995
  asserted: 1995-03-26
---
Storeowners tolerate a certain level of shoplifting, knowing that to do searches on customers would cost more than it would save. Computer networks face a similar situation, in that that too much security paraphernalia can cause people to avoid their networks.

The stakes in network security can be very high, however.  The press is full of stories of some hacker breaking into sites around the world.  For each story told publicly, there are hundreds of intrusions that go untold or unknown.  Most network administrators, if asked if their systems have been penetrated, will answer “Perhaps, but I am not certain.”

[Just as networks can multiply beneficial behavior, they can multiply intrusive or criminal behavior.]{#ww-security-multiplier .claim tense=timeless}  A set of user passwords can be posted around the world in a matter of minutes.  Even if the penetrated system takes actions to protect itself, it is quite likely that those passwords are used on other computers.  Users tend to use the same passwords on all their systems.

[As we move to ever greater dependence on computer networks, they become part of our infrastructure, like our roads, electricity grid, and water supply. Terrorist attacks against networks are not unthinkable.]{#ww-security-infrastructure .hypothesis status=open}

[As I wrote the last sentence, I asked myself, “Am I contributing to the spread of this terrible idea by mentioning it publicly?  Or am I warning people to be cautious and guard against it?”  I decided that I was doing both, but on the whole, the positive outweighed the negative.]{#ww-security-dual-use .observation}

A group on the Internet has approached this issue quite aggressively.  They will be freely distributing a program to the network called SATAN (Security Analysis Tool for Auditing Networks).  This program can be run from anywhere on the network, against any other computer.  Its purpose it to probe remote computers to find holes in their security system.  Ostensibly, the program was written to allow systems administrators to see if they have security exposures with their systems.  It also gives the novice Internet user the ability to probe for possible security leaks anywhere on the network.

The authors say that they take a conservative approach to the design of their program, and do not automatically intrude when they see a security opening.  In the Internet culture, however, this is a to challenge two thousands of people to do just that, merely for the intellectual challenge of it.  In order to be recognized for their prowess, they will circulate their enhancements for others to use.

This process is equivalent to circulating an instruction sheet, telling people how to unobtrusively try doors and windows to see if they are unlocked.  The sheet would also list the 10 most likely places where people would stash their valuables, and then tell the reader of the sheet not to go in the house to steal the valuables.  The authors then defend their sheet as a way of protecting homeowners, to insure that they lock their doors and windows.

The SATAN program is scheduled for general release from the Netherlands on April 5, 1995.  Some sites plan to pull their computers off their UNIX computers off the network in order to see what the program will do to them internally first.

It should be pointed out that most of the security problems one reads about with regard to Internet security are related to the UNIX operating system.  UNIX originated 25 years ago in an academic and research setting, when security was contrary to their goals.  One industry wag calls UNIX “A virus with a user interface.” There is still a radical faction that feels that all information should be free, and anyone has the right to access what is on your computer.

[Over time, security has become a very big issue, but is still subject to the “one last bug” syndrome.]{#ww-security-one-last-bug .concept}  As each hole in the original UNIX design is patched, another one will inevitably arise.  This cat and mouse game keeps UNIX systems administrators around the world gainfully, if not productively employed.

Other operating systems with more modern roots, such as Windows NT, have built in a security from the onset of their design.  These are more difficult to crack, and have been less susceptible to penetration.  It is important to separate the issue of security from the particular culture that has grown up around the UNIX operating system.

The networks of today provide a giant shopping mall for anyone wishing to “shoplift” information from our computers. We all need to be aware of this risk, and protect against it.

## Loom nodes

::: {#ww-security-2026 .resolution asserted=2026-07-04 asserted_by=claude-curator resolves=ww-security-infrastructure}
Attacks on network infrastructure moved from not unthinkable to routine instruments of state policy; pipelines, hospitals, and power grids have all been hit. The column's aside about SATAN — wondering in print whether describing a dual-use tool spreads the harm or the warning — is now a central, unresolved question of AI publication policy, asked in nearly the same words.
:::
