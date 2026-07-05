---
title: "Infrastructure for AI-Augmented Mathematics"
speaker: "Terence Tao"
affiliation: "UCLA; SAIR Foundation"
event: "2026 Science and AI Summit"
date: 2026-06-30
timestamp: "0:33:13"
youtube_url: "https://www.youtube.com/live/i6OQ5Z3repA?t=1993"
tags: ["mathematics","AI-infrastructure","formal-verification","crowdsourcing","SAIR-Foundation"]
loomic:
  loom: sair-ucr-2026
  asserted: 2026-06-30
  source: tao-2026-infra
---

::: {#tao-2026-infra .context part_of=2026-science-and-ai-summit
     verification.external="https://www.youtube.com/live/i6OQ5Z3repA?t=1993"}
Talk by [Terence Tao]{ref=terence-tao} at the [[2026 Science and AI Summit]], UC Riverside, June 30, 2026.
:::

## Summary

::: {#tao-infra-summary .synthesis
     parents="tao-infra-transcript@paraphrased"
     confidence.textual=high confidence.interpretive=medium}

[[Terence Tao]] opened by observing that mathematics is one of the most tradition-bound disciplines in academia — mathematicians still favor blackboards, work in small groups, and produce knowledge through a slow handcrafted process that has changed little in centuries. While AI is now capable of generating vast numbers of proposed solutions to mathematical problems and can sometimes verify them automatically, [the rest of the mathematical life cycle — peer review, digestion, communication, and incorporation into textbooks — has not scaled to match]{#math-lifecycle-mismatch .claim
  tense=indexical status=open parents="tao-infra-t1@paraphrased"}. This mismatch is creating what Tao calls "[[proof indigestion]]": [traffic jams in which floods of AI-generated papers overwhelm journals and human referees, and solution repositories accumulate faster than anyone can verify them]{#proof-indigestion-claim .claim
  tense=indexical status=open parents="tao-infra-t1@paraphrased"
  refines=math-lifecycle-mismatch}.

To illustrate the structural problem, Tao offered an automobile analogy. [When cars first appeared in the 19th century, they had to share narrow cobblestone streets built for pedestrians and horses — the result was chaos. The solution was not to improve the cars but to redesign the infrastructure]{#automobile-analogy .interpretation
  parents="tao-infra-t2@paraphrased"}: dedicated roads, pedestrian walkways, traffic rules, and hybrid zones. Tao argues mathematics is at that same inflection point. [Traditional journals and conferences remain valuable but cannot absorb unrestricted AI use; new infrastructure is needed that accommodates AI contributions safely while preserving space for human mathematical work]{#infrastructure-redesign-hypothesis .hypothesis
  status=open parents="tao-infra-t2@paraphrased"
  supports=proof-indigestion-claim}.

The [[SAIR Foundation]] is developing that infrastructure through a series of crowdsourced competitions. The first, the "[[distillation challenge]]" launched on Pi Day 2026, builds on an earlier project that generated 22 million true/false questions in equational algebra. Modern frontier models can answer nearly 99% of these questions individually, but that is expensive and reveals nothing about the underlying structure. The challenge asks contestants to write a one-page "cheat sheet" — readable by both humans and cheap open-source models — that distills the essential rules governing all 22 million answers. [Early results show that the best cheat sheets lift weak-model accuracy from ~51% to ~80%]{#distillation-interim-result .experimental_result
  tense=indexical status=interim valid.from=2026-03-14
  parents="tao-infra-t3@paraphrased"
  verification.external=distillation-challenge}, and a second phase pushing toward full proofs rather than true/false answers is underway.

The second featured competition, developed in partnership with the L-functions and Modular Forms Database ([[LMFDB]]), targets the [[inverse Galois problem]]. Contestants search for polynomials with specific Galois groups, framed as an "Easter egg hunt" across 160,000 possible group types. Verification is automatic and nearly instantaneous, making the task well-suited to large-scale crowdsourcing and AI assistance. The competitive phase rewards teams who find rare group types that others have not yet found; a cooperative phase will follow in which all polynomials are shared openly. [The competition is producing the first large-scale empirical dataset on the distribution of Galois groups — something traditional mathematics, not being an experimental science, has lacked]{#galois-empirical-dataset .observation
  tense=indexical parents="tao-infra-t4@paraphrased"}. [Tao noted that these competitions represent a model for how AI capabilities can be directed toward tasks that are orthogonal to, rather than competitive with, traditional mathematical work]{#orthogonal-capability .interpretation
  parents="tao-infra-t4@paraphrased"}.

:::

## Transcript

::: {#tao-infra-transcript .observation
     parents="tao-2026-infra@faithful"
     verification.transcript="https://www.youtube.com/live/i6OQ5Z3repA?t=1993"
     confidence.textual=medium}

[0:33:45] Well, I will — I can probably describe my talk without the slides. Anyway, so thank you all for coming. I'm very excited. This is the third [[SAIR Foundation|SIR]] event. I've been involved in SIR for about six months now.

[0:34:19] At SAIR we've been trying to figure out ways to support and integrate AI and other modern technologies into scientific research, and in particular in my home field of mathematics.

[0:34:36] Mathematicians are very traditional. The way we do mathematics has not fundamentally changed in centuries. We still use blackboards — we're almost the last profession in academia to cling to our chalk. In fact, we favor certain special Japanese and Korean chalk. You can read a textbook from 200 years ago and it looks almost identical to the ones we use today.

[0:35:13] We work in very small groups — one-on-one, or with one postdoc and two students. We do sort of handcrafted work, one problem at a time, slowly mapping out a mathematical landscape. This has worked for centuries, but it doesn't really scale.

[0:35:31] There's a whole life cycle: we work on problems, produce solutions, slowly verify them, write them up, communicate them to the rest of the community, and eventually digest them so they appear in textbooks and teach them to the next generation of humans — and now increasingly to AI as well.

[0:36:19] AI can now generate many, many solutions. AI is allowing massive generation of proposed solutions to mathematical problems, which is great. In some cases it can even automatically verify them.

[0:37:03] The theme of my talk is that mathematics is entering the 21st century. We have worked in much the same way for centuries. Things have really not changed that much in 200 years.

[0:37:57] There's a whole life cycle where proofs slowly get generated, understood, digested, and eventually end up in textbooks and now in the training data of AI. But what AI has been doing is accelerating proof generation and to some extent proof verification — but not so much the rest of the digestion process.

[0:38:48] [This has started creating what I call [[proof indigestion]] — traffic jams in mathematics. And I think the same thing is happening in the other sciences too now. Journals are suddenly receiving floods of AI-generated papers; many are very low quality but some have value, and we don't have the human resources to referee all these new advances. New bottlenecks are emerging: sites devoted to solving problems where solutions are piling up and people are not able to verify them.

[0:39:32] What this tells me is that traditional frameworks for doing research in mathematics — journals, conferences — can't handle unrestricted AI use. Adding more and more AI to these infrastructures can actually be quite harmful; it can crowd out human contributions.]{#tao-infra-t1 .observation}

[0:39:59] [As an analogy, I like to think of AI as sort of like the invention of the automobile. At the end of the 19th century when automobiles came out, the only infrastructure available were streets built in the 19th century — very narrow cobblestone streets. Cars had to drive in those streets with no traffic rules, all mingled together with humans. It was pretty chaotic. And making the technology better — faster, safer, more energy efficient — still doesn't solve the congestion problem.

[0:40:43] That's kind of where mathematics and probably the sciences more broadly stand today with regard to AI. What we need is to redesign our infrastructure and create new ways to do scientific research that can accommodate AI use safely. With the automobile, we figured this out: we have roads specifically for automobiles, pedestrian walkways where no cars are allowed, and a very small number of hybrid roads where you have both. We figured out ways to have them coexist.]{#tao-infra-t2 .observation}

[0:41:41] We should keep our infrastructure of journals and traditional ways of producing research — still valuable — but we should also create new ones. That's what I've been interested in at SIR. One of the venues for this are the SAIR competitions.

[0:42:08] Mathematics has been a fairly heavily gatekept field until recently. You needed a math PhD often to even understand the problems we work on, let alone contribute to them. But now we have the capability to accept contributions from the broader community of math-adjacent people who may not have PhDs but who have new tools — AI and otherwise — and can contribute. The key is that we need to design the right problems for them to work on, for which we can safely incorporate hundreds or thousands of contributions from the public.

[0:43:05] Right now we have three competitions ongoing. None have completely finished yet, but they have all produced nice intermediate results.

[0:43:14] The first competition is what we called a [[distillation challenge]]. We launched it on Pi Day — March 14th. It built upon a previous crowdsourced project I ran about two years ago called the Equational Theories project. This was an experiment to see whether we could really do mathematics at scale with modern technologies.

[0:43:36] We created 22 million problems in algebra — whether the commutative law implies the associative law, that kind of thing. We generated this big test set of 22 million questions, most of which are not too hard individually — a graduate student in algebra working for an hour can solve any given one of them — but we have 22 million of them.

[0:44:43] About two years ago we completed this project. Many people contributed with many tools — AIs and more traditional computational tools — and we managed to settle all 22 million questions: each one gets a yes or no answer. So we have this nice dataset of algebra results.

[0:45:08] Any individual question — with modern AI, you could feed any given one of these 22 million data points to a frontier model and it will think for 30 minutes and spend a few dollars of compute and it will answer almost 99% of them correctly. But this doesn't tell you what the structure is, what the features of this dataset are, whether there's a way to describe all these answers in a condensed way.

[0:45:38] So we set up what we call a distillation challenge. If instead of using a premium expensive model you use a very cheap open-source model, it's terrible on these problems — it has a 51% chance of getting the answer right, barely better than random chance. But it turns out that if you give these open-source models a good prompt — like a one-page set of tips on how to solve algebra problems — they can do a lot better. Just like a very weak student at taking an algebra midterm may do very badly unless given a one-page cheat sheet of helpful tips.

[0:46:24] The distillation challenge was a competition to submit a one-page cheat sheet to help these very weak AI models do well at solving these 22 million true/false questions. Contestants submit a cheat sheet; we test it against a carefully selected sample of problems; they get a grade. These are cheat sheets that AIs can read but humans can read too. The idea is whether you can distill this entire knowledge of 22 million true/false questions down to a single page that explains as much of the dataset as possible.

[0:47:19] [That challenge is still ongoing. With the best cheat sheets currently, the success rate of these weak AIs has increased by 20–30 percentage points, from 50% to about 80% accuracy. The next stage is to get these weak models to not just guess true/false answers but actually write proofs and give more detailed explanations — a much more challenging task.]{#tao-infra-t3 .observation}

[0:48:14] We're running short on time, so I'll skip one competition and talk about the final one, which is quite exciting — we're checking the results every day.

[0:48:30] This is a more mainstream mathematical challenge created in cooperation with the [[LMFDB]] — the L-functions and Modular Forms Database — a major database of mathematical objects of interest in number theory, cryptography, and many other fields of mathematics. They were interested in something called the [[inverse Galois problem]].

[0:49:03] You can think of it like an Easter egg hunt. We're looking for polynomials — think of them as eggs — and each egg has a certain Galois group, like a color. We're interested in collecting eggs of various colors. Some colors are very common and some are very rare. It turns out that in this particular problem there are 160,000 colors — types of polynomials — and we want to collect one of each.

[0:50:02] Once you find a polynomial, you just type in 24 integers, and it's very easy with modern computer software to work out its color. So it's very easy to verify a submission once you have it, but we want to collect all of them. For the common ones that's very easy; there are some ultra-rare ones, and in fact there may be some for which no Easter eggs exist. The inverse Galois problem is essentially whether every single possible color is actually attainable — that's a major open question in Galois theory.

[0:51:00] We decided to make this a competition. Contestants can submit polynomials and we verify them. We have two stages: a competitive stage ongoing right now, then a cooperative stage afterwards. In the competitive stage we don't reveal the polynomials — each team has their own secret stash. If they're the first to find a certain color they get a point; if many teams have found the same color the points are shared by a somewhat complicated formula. We want to encourage people finding very difficult, hard-to-find Easter eggs.

[0:51:46] [Part of why we run this experiment is because we don't know in advance which ones are hard and which are easy. We're hoping this competition will uncover, by market forces, which Galois groups are actually very rare and which are common. We have very little empirical data about this. Mathematics traditionally has not been an experimental science, but now we can do experimental studies of mathematical objects — a really exciting new capability these tools are offering.

[0:52:24] There are many teams. Some are clearly using a lot of AI and scooting ahead for now, but the lead is not guaranteed. If somebody else can also find eggs of the same colors as the leading teams, they can steal those points. The organizers have been reporting that at math conferences in algebra, people all know about this competition — some are organizing their own private teams and are very excited. In contrast to many other AI contributions to mathematics that have a mixed reception, this is an orthogonal capability to what traditional mathematicians do, and it's a very good place to direct these new AI capabilities.]{#tao-infra-t4 .observation}

[0:53:42] Just like we have roads for humans and roads for AI, we will have competitions with heavy AI assistance but also traditional math workflows. The competition is still ongoing; I hope to report more about it at a future meeting. So far it's been very popular — there's a little community sharing tips and there are active leaderboards.

[0:54:06] [We are running three competitions on a fairly minimal budget right now — just a few engineers and some compute resources. Eventually we want to scale up to much larger competitions with much more compute and high-profile prizes. All the competitions right now are in mathematics, partly because that's where you can most easily verify submissions and score quickly. But in principle there could be other scientific competitions. If there's some big dataset someone wants to collect in a crowdsourced fashion, come talk to us. We do hope to set up a formal call for proposals in the near future.]{#tao-infra-t5 .observation}

[0:55:02] Thank you very much.

:::

## Loom nodes

::: {#frontier-math-ai-infrastructure .frontier status=active}
Infrastructure for AI-augmented mathematics: venues, verification pipelines, and digestion processes that can absorb AI-scale contribution without crowding out human work.
:::

::: {#proof-indigestion-resolution .unknowledge status=open
     parents=proof-indigestion-claim
     part_of=frontier-math-ai-infrastructure}
What digestion infrastructure — refereeing, distillation, formalization — can scale to AI-rate proof generation?
:::

::: {#distillation-to-proofs .unknowledge status=open
     parents=distillation-interim-result
     part_of=frontier-math-ai-infrastructure}
Can cheat-sheet distillation extend from true/false accuracy to full proof generation by weak models?
:::

::: {#inverse-galois-open .problem tense=timeless status=open
     ref=inverse-galois-problem}
Is every finite group realizable as a Galois group over the rationals? (Standing open problem; the LMFDB competition gathers empirical distribution data around it.)
:::

::: {#sair-competition-scaleup .future_binding status=pending
     target=sair-foundation
     trigger.event="SAIR formal call for proposals; competitions beyond mathematics"
     trigger.test="a non-mathematics SAIR competition with automatic verification launches"
     parents="tao-infra-t5@paraphrased"}
Tao's stated intent to scale competitions beyond mathematics once verification-at-scale generalizes. Resolutions should assert `resolves=sair-competition-scaleup`.
:::

::: {#tao-barish-link .interpretation
     parents="proof-indigestion-claim,barish-confidence-gap"
     confidence.interpretive=medium}
Curator's note: Tao's verification bottleneck and Barish's discovery-confidence gap are two faces of the same frontier — generation has outrun validation. Edge asserted by the loom curator, not by either speaker.
:::
