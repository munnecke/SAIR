---
title: "SAIR Platform Architecture and Open Science Vision"
speaker: "SAIR Team"
affiliation: "SAIR Foundation"
event: "2026 Science and AI Summit"
date: 2026-06-30
timestamp: "0:55:54"
youtube_url: "https://www.youtube.com/live/i6OQ5Z3repA?t=3354"
tags: ["SAIR-Foundation","open-science","platform","benchmarks","research-infrastructure"]
keywords: ["SAIR platform","SID research identity","SAIR Connect","open benchmarks","science verticals","computational playground","artifact reusability"]
loomic:
  loom: sair-ucr-2026
  asserted: 2026-06-30
  source: sair-platform-2026-overview
---

::: {#sair-platform-2026-overview .context part_of=2026-science-and-ai-summit
     verification.external="https://www.youtube.com/live/i6OQ5Z3repA?t=3354"}
Platform overview by the [SAIR Foundation]{ref=sair-foundation} team at the [[2026 Science and AI Summit]], UC Riverside, June 30, 2026.
:::

## Summary

::: {#sair-platform-summary .synthesis
     parents="sair-platform-transcript@paraphrased"
     confidence.textual=high confidence.interpretive=medium}

The [[SAIR Foundation]] presented its vision for a unified open science and AI research platform, founded by Professor Terrence [[Terence Tao|Tao]], Professor [[Barry Barish]], and [[Chuck Ng]], with an advisory board including Randy Shechman, Lenor Blum, Manuel Blum, and Jeffrey Olman. The platform is designed around [a dual mandate: using AI for science (expanding the scale, speed, and reach of scientific exploration) and using science for AI (creating practical tests for reasoning, reliability, interpretability, and evaluation)]{#sair-platform-dual-mandate .concept
  parents="sair-platform-t1@paraphrased"}. The overarching goal is to build open research infrastructure where data, tools, models, benchmarks, and citations become reusable assets rather than siloed outputs.

The platform architecture connects four verticals — science, industry, builders, and capital — and is anchored by [a community of over 650,000 members with access to podcasts, live events, and interviews with leading scientists]{#sair-platform-community-scale .observation
  tense=indexical parents="sair-platform-t2@paraphrased"}. [The core research loop flows from open problem to open artifact: problems and datasets feed into competitions, competitions yield solutions tested in a computational playground, and those solutions produce open benchmarks enabling cross-team comparison]{#sair-platform-research-loop .observation
  parents="sair-platform-t3@paraphrased"}. A SAIR API underpins this pipeline and supports a contributor network for collaborative discovery.

Two identity and networking features are central to the platform. [SID (Science Identity) provides a persistent, portable research identity that records verified contributions, credits, and continuity across competitions and events]{#sair-platform-sid .observation
  parents="sair-platform-t4@paraphrased"}. SAIR Connect enables problem-based researcher discovery — matching people by their past scientific work rather than generic profiles — to facilitate targeted collaboration.

The platform explicitly targets equitable global access: [its open models, built on community data and reasoning traces from top labs with open weights and open evaluation, are intended to be accessible to scientists at every university size, in every emerging country, and to the next generation of builders]{#sair-platform-open-access .claim
  tense=indexical status=open
  parents="sair-platform-t5@paraphrased"}. The ambition is a single platform spanning mathematics, physics, biology, materials science, energy, robotics, and chemistry, providing open challenges, open data, open tools, open models, open benchmarks, and an open community.

:::

## Transcript

::: {#sair-platform-transcript .observation
     parents="sair-platform-2026-overview@faithful"
     verification.transcript="https://www.youtube.com/live/i6OQ5Z3repA?t=3354"
     confidence.textual=medium}

[0:55:51] So, I'm sure you've heard from Professor Terren a little bit, but there is a vision that we're going for here at [[SAIR Foundation]]. We want to make a platform that is for open science and AI research.

[0:56:29] I'm sure a lot of these people are very familiar to you but we have some very very important individuals with us. We have of course professor [[Terence Tao]], we have professor [[Barry Barish]] and we have [[Chuck Ng]] as our co-founders and for our advisory board we have Randy Shechman, we have Lenor Blum and we have Manuel Blum as well as Jeffrey Olman.

[0:56:56] [So what do we aim to do as a platform? We want SAIR to be a space where we can turn science and AI into some sort of open collaboration platform. We want to use AI for science where AI can expand the scale, speed, and reach of scientific exploration. We want there to be science for AI where scientific tasks can create practical tests for reasoning, reliability, interpretability, and evaluation. And with all this, we want to create an open research infrastructure that allows data, tools, models, benchmarks, and citations to become reusable.]{#sair-platform-t1 .observation}

[0:57:34] And how do we do this? We want to connect four verticals together to make this possible. We want to connect the science, of course, we want to connect the industry, we want to connect the builders, and we want to connect capital.

[0:57:48] [Already we have an open community that is focused on distribution and education. We want the world to grow together and to do that we have an online community of over 650,000 members where we have podcasts, live events and interviews with some of the world's leading scientists.]{#sair-platform-t2 .observation}

[0:58:07] We have a global network that connects every part of the world with our SAIR events and like we do now we have summits and events that really need to connect the community in person because being online doesn't really get the point across all the time.

[0:58:28] [And so how does a research loop work? We want to go from an open problem to an open artifact. And to do that, we first take the open problem or data. We form competitions around those problems. Through playgrounds, we'll find solutions. And with those solutions, we'll create an open benchmark for people to compare their works and see what has improved and what has not.]{#sair-platform-t3 .observation}

[0:58:52] To host this, like Professor Terren introduced earlier, we have the SAIR API. And with that, we'll create a contributor network that can help people find each other to work together because science really is a cooperative effort.

[0:59:09] So let's talk a bit more about competitions. We have public problems and statements, data sets, etc. We have runnable tasks with reproducible evaluation. And the goal is that we want submissions to become reusable research artifacts, not just results. And this is not just for the key fields where AI is most prevalent right now. We want to make it applicable to other fields as well.

[0:59:40] And so we have a playground to help with this. It's a shared environment for testing ideas, inspecting outputs, comparing methods and such where we can run solvers and baselines. You can inspect logs, proofs, lean certificates and failures. And then the point is to compare outputs in a common evaluation frame against other results. Thus, we turn experiments into reusable artifacts.

[1:00:11] And so open benchmarks — the point is to make progress measurable. We want there to be comparable results across models, setups, and teams. We want there to be comparisons to see what the community can improve on and what fails. And again, the point of this is to go back and iterate because you're not guaranteed success the first time around.

[1:00:38] [To help with this, we've come up with the process of SID and SAIR Connect where SID is a persistent research identity where verified contribution records, portable credit and continuity across competitions, events and such are recorded. And then we have SAIR Connect which allows for people to interact with each other and to allow for problem-based discovery based on your past work rather than just generic profiles, which is very important.]{#sair-platform-t4 .observation}

[1:01:13] And so with this we will create an open model and that is our goal — to create an open model for global science that is accessible to every scientist everywhere.

[1:01:23] Now SAIR builds frontier scientific models trained on community data. Reasoning traces from top labs are used to fuel this and we have open weights and open evaluation.

[1:01:37] [Now I think one of the biggest questions when it comes to science discovery is who gets access. For us we want to make sure that it's accessible to every scientist globally, we want it to be accessible to universities of every size, we want it to be accessible to researchers of every emerging country, and we want it to be accessible to the next generation of builders.

[1:02:00] And the reason this matters so much is because science and scientific discovery in large multiplies when you have all of this information that is openly accessible to everyone. And with that we're able to accelerate the rate at which we can make discoveries.]{#sair-platform-t5 .observation}

[1:02:18] So our plan is to make one platform that can cover many scientific frontiers. We want to create open challenges, open data, open tools, open models, open benchmarks, and of course an open community. We want this to be applicable to mathematics, physics, biology, materials, energy, robotics, chemistry, and other fields as well.

[1:02:43] So if you don't mind, I would love for all of us to participate in this together. You can participate in challenges, you can contribute to our infrastructure, you can join our network, and you can help us create programs.

[1:02:59] Thank you and I hope you'll join us on our journey.

:::

## Loom nodes

::: {#sair-platform-benchmark-rigor-open .unknowledge status=open
     parents=sair-platform-research-loop}
Can the platform's open benchmarks and inspectable artifacts — logs, proofs, lean certificates, reproducible evaluation — reach the level of rigor at which the scientific community would accept results built on them as validated discoveries?
:::

::: {#sair-platform-access-equity-open .unknowledge status=open
     parents=sair-platform-open-access}
Will open weights and open evaluation translate into usable access for scientists at small universities and in emerging countries, given the compute, bandwidth, and institutional-support constraints that open licensing alone does not remove?
:::

::: {#sair-platform-barish-link .interpretation
     parents="sair-platform-research-loop,barish-confidence-gap"
     confidence.interpretive=medium}
Curator's note: the platform's playground artifacts (inspectable proofs, lean certificates) and open-benchmark loop are candidate machinery for the discovery-confidence framework [Barry Barish]{ref=barry-barish} demands in his closing talk ([the confidence gap]{ref=barish-confidence-gap}, part of [the AI discovery-confidence frontier]{ref=frontier-ai-discovery-confidence}) — but the platform talk makes no such validation claim itself. Edge asserted by the loom curator, not by either speaker.
:::
