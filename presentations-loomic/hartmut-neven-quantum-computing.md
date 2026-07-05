---
title: "Quantum Computing: Progress, Architecture, and AI Synergies"
speaker: "Hartmut Neven"
affiliation: "Google Quantum AI"
event: "2026 Science and AI Summit"
date: 2026-06-30
timestamp: "2:48:36"
youtube_url: "https://www.youtube.com/live/i6OQ5Z3repA?t=10116"
tags: ["quantum-computing","Google","error-correction","AI-materials","quantum-ML"]
keywords: ["quantum error correction","surface code","modular architecture","magic state cultivation","out-of-time-order correlators","quantum echoes","AlphaFold analogy","beyond-classical data","magnon","neutron scattering","diffusion neural networks","qubit coherence","T-gate"]
loomic:
  loom: sair-ucr-2026
  asserted: 2026-06-30
  source: neven-2026-quantum-computing
---

::: {#neven-2026-quantum-computing .context part_of=2026-science-and-ai-summit
     verification.external="https://www.youtube.com/live/i6OQ5Z3repA?t=10116"}
Talk by [Hartmut Neven]{ref=hartmut-neven} of [[Google Quantum AI]] at the [[2026 Science and AI Summit]], UC Riverside, June 30, 2026.
:::

## Summary

::: {#neven-summary .synthesis
     parents="neven-transcript@paraphrased"
     confidence.textual=high confidence.interpretive=medium}

[[Hartmut Neven]] of [[Google Quantum AI]] outlined the team's full-stack approach—spanning hardware fabrication in Santa Barbara through cloud interfaces and applications—and presented an accelerated road map toward a commercially relevant quantum computer. [The original six-milestone plan requiring roughly one million physical qubits has been compressed]{#neven-roadmap-compression .claim
  tense=indexical status=open parents="neven-t1@paraphrased"}: advances in error-correcting codes (particularly modular architectures that replace the plain surface code), [improvements in qubit coherence times (from 20 microseconds to ~300 microseconds with millisecond prototypes now demonstrated)]{#neven-coherence-gains .experimental_result
  tense=indexical status=interim parents="neven-t3@paraphrased"}, and algorithmic refinements have reduced the physical qubit requirement to approximately 100,000. [Google's team has already completed milestones one (beyond-classical computation) and two (demonstrated [[quantum error correction]] below break-even), and expects milestone three—a complete logical module with a full gate set including T-gates—by end of 2025, with a useful machine (milestone five) targeted by end of decade]{#neven-milestone-status .claim
  tense=indexical status=open parents="neven-t1@paraphrased,neven-t4@paraphrased"}.

A key architectural shift drives much of this progress. Moving from a monolithic surface-code sheet to a modular design—where modules of several hundred physical qubits are interconnected with higher-than-nearest-neighbor connectivity—[enables error-correcting codes that require only 52 physical qubits per logical qubit rather than ~1,000]{#neven-encoding-ratio .experimental_result
  tense=indexical status=interim parents="neven-t2@paraphrased"}. The team is also pursuing dual modalities: superconducting transmon qubits (nanosecond gate times, deep circuit capability) alongside neutral-atom qubits (flexible all-to-all connectivity via laser tweezers, but slower gate times), treating the two as complementary rather than competing platforms.

On the quantum-AI interface, [[Hartmut Neven|Neven]] described two concrete examples. First, "quantum echoes" (out-of-time-order correlators, or OTOCs): a circuit run forward, perturbed by a butterfly operator at peak entanglement, then run in reverse. Comparing the OTOC measured on a quantum processor with that from an NMR machine allows gradient-descent fitting of unknown molecular parameters—a form of [[quantum computing|quantum machine learning]] now being applied to open chemistry problems. Second, inspired by the AlphaFold precedent, [the team is using quantum simulation of magnon systems (with neutron-scattering spectroscopy as the measurement method) to generate high-quality "beyond-classical" datasets that cannot be reproduced on classical hardware, then passing those datasets to Google DeepMind's AI for Materials group to test whether quantum-derived training data improves [[foundation models|foundational models]]]{#neven-beyond-classical-data .observation
  tense=indexical parents="neven-t5@paraphrased"}.

As a final demonstration of quantum-AI synergy, [[Hartmut Neven|Neven]] described seeding diffusion neural networks (of the type used in image-generation products) with quantum noise from a quantum circuit rather than classical Gaussian noise. The same pretrained network, given quantum-structured noise as its starting tensor, produces qualitatively different outputs—raising the possibility that quantum circuit subroutines embedded in multiscale fluid-dynamics or generative simulations could improve both image quality and physical simulation fidelity.

:::

## Transcript

::: {#neven-transcript .observation
     parents="neven-2026-quantum-computing@faithful"
     verification.transcript="https://www.youtube.com/live/i6OQ5Z3repA?t=10116"
     confidence.textual=medium}

[2:48:36] All right, next up will be [[Hartmut Neven]]. If you're still here, please come up.

[2:49:03] So yeah, while the slides are being brought up I wanted to thank the organizers for having me. I'm from the very west of LA and it's the first time I'm here in Riverside and I'm rather impressed by the high caliber of the conversations, the attendees, and also the facilities. I should have come earlier.

[2:49:39] I wanted to give you a little overview of what the [[Google Quantum AI]] lab has been up to. And I only have 20 minutes so it will just be a little smattering of the different areas we work on. We are what people know as a full stack operation. So we build the hardware — we have hardware labs and fabs in Santa Barbara. But then we build the operating system as well as cloud interfaces and applications for [[quantum computing|quantum computers]].

[2:50:31] The mission of the [[Google Quantum AI]] team is to build [[quantum computing]] for otherwise unsolvable problems. And the way we achieved this we formulated a road map how to get there. It has three components: hardware, software, and an access component.

[2:51:08] The main message here on the hardware track is that [[quantum computing]] is happening and it's going to happen rather soon. So we originally had a road map that had six milestones to get us what we consider to be a useful machine — which a few years ago we thought we would need about a thousand logical qubits to run some of the famous algorithms like Shor's algorithm or do some work with quantum simulation.

[2:51:56] A few years ago we saw to run the famous quantum algorithms we would need about a thousand logical qubits that can do about 10^12 operations.

[2:52:13] [But due to advances in algorithms and [[quantum error correction]] and also hardware architecture and computer architecture, these numbers have come down. So initially we thought we would need a million physical qubits to realize such good logical qubits but due to architecture we think 100,000 is already enough. On the algorithm side we have made progress. 10 to the 12 operations are not really needed anymore — it's now less than 10 to the 10 operations. So with these improvements we think our road map can stop at milestone five which is a commercially relevant quantum computer. And I should say we already did the first two of these five milestones. Our team was the first to show computations that could run much faster on quantum computers than on any classical computer. We were also the first team to show that [[quantum error correction]] — an important technique to build logical qubits out of physical qubits — works in practice. And hopefully later this year we will achieve milestone three which is essentially a module within a modular architecture that will make up milestone five. And if everything goes according to plan by the end of this decade we will have milestone five.

[2:53:49] So our own slogan is that milestone 5 is a new milestone six. That's all we need: a 100,000 physical qubit machine.]{#neven-t1 .observation}

[2:54:04] [Let me walk you through some of the improvements that have happened that enable this acceleration. One is computer architecture. Originally we thought our computer would essentially be a large sheet of silicon with transmon superconducting transmon qubits imprinted on it in a square lattice nearest neighbor connectivity architecture. But since then this has evolved to a modular architecture where each module will have several hundred physical qubits and then those modules are connected in a higher degree than the nearest neighbor checkerboard surface code architecture to other modules. And that allows for more potent error correcting codes than the standard technique which is a surface code. So while with surface code to make qubits that can participate in 10^10 operations you need about an encoding ratio of thousand to one — meaning you need thousand physical qubits to make one really good logical qubit — with these modular codes that can live on a modular architecture, you only need 52. So that's over an order of magnitude improvement.]{#neven-t2 .observation}

[2:55:32] We also start to differentiate these modules. So there will be modules that are good for compute, then some that are for hot storage like SRAM, and then for cold storage. So even though the von Neumann architecture of quantum computers hasn't been developed, you see the emergence of that.

[2:55:54] [Then the raw hardware has improved quite a bit. The coherence times — essentially the key metric of the quality of your qubit, measuring how long does a superposition state stay alive — these times have increased recently by over a factor of 10. So what used to be 20 microseconds we are now in 300 microsecond coherence times and we are actually having first prototypes of qubits that are approaching a millisecond of coherence time. So more coherence time than our road map will need for completion.

[2:57:08] And what we keep checking on is how well our error correction is working. We were the first team that showed the idea of [[quantum error correction]] — you introduce redundancy, you have more physical qubits than a single one orchestrated to one better performing logical qubit — and the idea is the more physical qubits you have the more redundancy the better your logical qubit would become. And in 2023 we showed this for the first time. The community wasn't that impressed because we just improved it by a few percent even though it was the break even point. But since then we did better. So now as you go larger in code distance it improves by over a factor of two. That made many quantum startups rich — I don't know whether you watch the stock market for quantum listed companies, it went up after this 2024 result significantly. But since then it hasn't stopped. It's not published yet but now the error suppression factor — that shows how the error rates come down as you increase the number of qubits — has now gotten up to what we call lambda 4, and our milestone three which we hope to achieve later this year would require a lambda of six according to our own goals.]{#neven-t3 .observation}

[2:58:51] [Our milestone 3 is not just a memory qubit. It's a complete module and modular architecture. So you don't only want to show that it acts as a memory qubit but you also want to show you have a complete gate set including one gate that is very difficult to make — it's a T-gate that is made in a protocol called [[magic state cultivation|magic state injection]]. And for this you need to make [[magic state cultivation|magic states]], and it used to be that making [[magic state cultivation|magic states]] in a quantum computer used to be very expensive using a process called T-state distillation. But our team member Greg Gitney had developed a new protocol called [[magic state cultivation]] — cultivation not distillation — which is better by orders of magnitude. We actually just had a paper for the first time showing experimentally that T-gates were made in the quantum computer. So you see all the pieces you need to build a large useful quantum computer are falling into place rather rapidly.]{#neven-t4 .observation}

[3:00:00] One mistake I want you to prevent from making is if you just look at some algorithmic benchmark — what's the largest number you have factored — and find oh it's still not even 21, so I have time, it will take us another decade to get to a useful machine. But that's not correct because once you have a single module that's like laying the first mile of a freeway and the next ones will follow rather quickly. The single modules have improved in quality dramatically. They're almost ready to click together into the large machine. So the progress will not be smooth but will go through a rather steep jump.

[3:00:58] We also recently decided we go dual threat. Our team used to do superconducting [[quantum computing]] because this is a rather complete technology, but another modality — neutral atom computing — has recently made some good progress as well and we didn't want to be beaten on the final stretch to a useful quantum computer. So to not take any risk we decided to do neutral atom computing as well. If you look at the scorecards of these two approaches: superconducting are very fast — physical gate times are measured in nanoseconds versus microseconds for neutral atoms. We have also shown deep circuits with millions of cycles because microwave control is very stable and the superconducting qubits don't go anywhere. The superpowers for neutral atom computing are that they have a flexible connectivity grid — the atoms that realize their qubits are held in laser tweezers and you can move them such that any two qubits that want to talk to each other can be brought into proximity and a gate can be executed there.

[3:02:50] For neutral atoms it's easier to scale in the space direction — they are already working with arrays on the order of 10,000 qubits while superconducting [[quantum computing]] is more in the 1,000 order of magnitude. But in circuit depths, computations have been run with 10^10 cycles — very deep in the time direction — while neutral atom architectures the record-holding circuits are only 100 cycles long. So not long enough for complex algorithms. The question is: is it easier for neutral atoms to scale in the time direction or is it easier for superconducting to scale in the space direction? We will find out.

[3:04:24] Since the topic here is AI, let me focus on quantum algorithms that have a bearing on AI. Another point of pride for our team is that last year we had on the cover of Nature an article about the first practical verifiable quantum algorithm. This algorithm is called quantum echoes and the technical term is an out-of-time-order correlator. This is an observable that you can measure on a system like an NMR machine. How this works is that you run your circuit forward for some time — for example initializing all your qubits in the zero state and then you evolve your qubits under a Hamiltonian that describes a molecule — and then you stop and you run this circuit in reverse. If you had no noise in your quantum processor you would come back to the start state. To make it more interesting, in the middle of the circuit, when you have a deeply entangled state, you sort of tickle one of your qubits with a butterfly operator because it's related to chaos. This effect of the butterfly operator will then spread through your system, you won't come back exactly to the start state, and this is measured by an out-of-time-order correlator. You can use a nuclear magnetic resonance machine and run this protocol there, and run this protocol on your quantum processor, and this allows you to — if you think you know the molecule in your NMR machine but may not know it perfectly — leave a few free parameters and then like traditional machine learning do gradient descent to make the OTOC you measure on your quantum processor match the OTOC you see in your NMR machine. When these two match then you know what your free parameters should be. This is an example for quantum machine learning and we are actually starting to tackle proper open chemistry questions with this.

[3:07:24] [Another example — I'm often asked how does AI relate to [[quantum computing]] and how will [[quantum computing]] enhance AI. The marvelous success of AlphaFold rested on essentially 50 years of collection of data. The protein database used in AlphaFold was started in the 1970s. It's very expensive to make such data. So with quantum processors you can accelerate making high quality datasets. For example, it's often said AI can help us hasten nuclear fusion. But today to create experimentally the conditions in plasma that are conducive to fusion reactions, one second worth of fusion data would cost you a trillion dollars to produce. But you can try to simulate these conditions in a quantum computer. We did a little bit of this recently for material science where we simulate magnon systems and we simulate on our machine measurement methods such as neutron scattering spectroscopy. We are able to make datasets of that high quality that we now feel emboldened to hand those to our colleagues at Google DeepMind that have an AI for Materials research group and say: can you experiment with this, maybe tell us whether this data has reached the quality where if you train a [[foundation models|foundational model]] with it will be better than if you didn't have access to this beyond-classical data — because all these algorithms I'm showing you could not be run anymore on classical machines.]{#neven-t5 .observation}

[3:09:21] Another fun example of how [[quantum computing]] could enhance AI — the area we picked is diffusion neural networks. You may know that products like Midjourney use diffusion neural networks to generate images. How this works essentially is you start with a noise tensor or a noise image and then these neural networks have been trained to sculpt a pretty image from this noise, and typically this noise is just classical Gaussian noise — every pixel is picked from a Gaussian distribution. But we asked the question: in nature there are many patterns we see — when you look at the W-map or the picture of the largest object we know, the universe as a whole, and look at the microwave background radiation picture, there's structure in there. And then if you go to an astronomer or a cosmologist and say why are these structures in there, they will say oh these are frozen-out quantum fluctuations from the early universe. This process — where quantum fluctuations get amplified from the microscopic to macroscopic scale — happens often, for example in weather. The butterfly effect was famously discovered when studying weather patterns. So we asked ourselves: can we reproduce this — instead of giving our quantum diffusion neural networks noise that is classical, let's produce noise patterns with a quantum circuit and see whether something changes. We did this for image generation. The network was the same, just on the left side it's seeded with classical noise and on the right side it's seeded with quantum noise. You can judge which ones you like better. But the thing I wanted to convey is that if you do a multiscale fluid dynamics simulation, maybe having a quantum circuit as a subroutine under the hood from which you can take samples may not only improve the quality of images but also improve the quality of simulations.

[3:12:20] Okay, with this I will stop.

:::

## Loom nodes

::: {#neven-frontier-beyond-classical-data .frontier status=active}
Quantum-generated "beyond-classical" training data for AI: using quantum processors to produce datasets — magnon simulations with simulated neutron-scattering spectroscopy, OTOC measurements, quantum-structured noise — that classical machines cannot generate, as fuel for [[foundation models]] in materials, chemistry, and generative simulation.
:::

::: {#neven-modality-scaling .unknowledge status=open
     parents="neven-2026-quantum-computing@motivated"}
Is it easier for neutral-atom architectures to scale in the time direction (circuit depth beyond ~100 cycles) or for superconducting architectures to scale in the space direction (beyond ~1,000 qubits)? Neven's own framing: "We will find out."
:::

::: {#neven-quantum-data-value .unknowledge status=open
     parents=neven-beyond-classical-data
     part_of=neven-frontier-beyond-classical-data}
Does training a foundation model on beyond-classical quantum-generated datasets measurably improve it over training without that data? (The open experiment Neven describes handing to Google DeepMind's AI for Materials group.)
:::

::: {#neven-quantum-noise-generative .unknowledge status=open
     parents="neven-2026-quantum-computing@motivated"
     part_of=neven-frontier-beyond-classical-data}
Does seeding diffusion neural networks with quantum-circuit noise rather than classical Gaussian noise measurably improve generated images — or, as Neven speculates, the fidelity of multiscale physical simulations with quantum-circuit subroutines?
:::

::: {#neven-milestone-three .future_binding status=pending
     target=google-quantum-ai
     trigger.event="Google Quantum AI milestone three: a complete logical module with full gate set including T-gates, at error suppression lambda ~6"
     trigger.test="published demonstration of a complete module meeting Google's stated lambda=6 goal"
     parents="neven-t1@paraphrased,neven-t4@paraphrased"}
Neven's stated expectation of achieving milestone three "later this year" (current error suppression: lambda 4, unpublished at talk time). Resolutions should assert `resolves=neven-milestone-three`.
:::

::: {#neven-milestone-five .future_binding status=pending
     target=google-quantum-ai
     trigger.event="commercially relevant quantum computer (milestone five, ~100,000 physical qubits) by end of decade"
     trigger.test="a useful machine running quantum algorithms of ~10^10 operations on high-quality logical qubits"
     parents="neven-t1@paraphrased"
     depends=neven-milestone-three}
"Milestone 5 is a new milestone six": Neven's end-of-decade target for a useful, commercially relevant machine. Resolutions should assert `resolves=neven-milestone-five`.
:::

::: {#neven-anandkumar-link .interpretation
     parents="neven-beyond-classical-data,anandkumar-quantum-dot-chip-test"
     confidence.interpretive=medium}
Curator's note: the loop runs both ways at this summit — Anandkumar's neural operators are designing quantum-dot hardware, while Neven's quantum processors generate training data for AI models. Edge asserted by the loom curator, not by either speaker.
:::
