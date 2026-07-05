---
title: "Emergent Kolmogorov-Arnold Geometry in Trained Neural Networks"
speaker: "Michael Mulligan"
affiliation: "UC Riverside"
event: "2026 Science and AI Summit"
date: 2026-06-30
timestamp: "7:38:27"
youtube_url: "https://www.youtube.com/live/i6OQ5Z3repA?t=27507"
tags: ["neural-networks","Kolmogorov-Arnold","interpretability","geometry","deep-learning-theory"]
keywords: ["Kolmogorov-Arnold theorem","KA geometry","Jacobian","zero row fraction","canonical alignment","vision transformers","spontaneous structure","correlated weight initialization","training efficiency","interpretability"]
loomic:
  loom: sair-ucr-2026
  asserted: 2026-06-30
  source: mulligan-2026-ka
---

::: {#mulligan-2026-ka .context part_of=2026-science-and-ai-summit
     verification.external="https://www.youtube.com/live/i6OQ5Z3repA?t=27507"}
Talk by [Michael Mulligan]{ref=michael-mulligan} at the [[2026 Science and AI Summit]], UC Riverside, June 30, 2026.
:::

## Summary

::: {#mulligan-ka-summary .synthesis
     parents="mulligan-ka-transcript@paraphrased"
     confidence.textual=high confidence.interpretive=medium}

[[Michael Mulligan]] ([[UC Riverside]]) presents work done with Matthew Van Herweg, Mike Friedman, and Keith Adams investigating whether standard neural network training spontaneously realizes geometric structures predicted by the [[Kolmogorov-Arnold theorem|Kolmogorov-Arnold]] (KA) representation theorem. The KA theorem, which predates the universal approximation theorem by roughly 20 years, states that [any continuous multivariate function can be exactly represented by a one-hidden-layer network of fixed width]{#mulligan-ka-exact-representation .claim
  tense=timeless parents="mulligan-ka-t1@paraphrased"} — a stronger result than approximation theorems, which require arbitrary width. The theorem's construction involves two composed maps: a universal "data preparation" inner map and a task-specific outer map. Mulligan focuses on the distinctive geometry of the inner map as captured by its Jacobian — how the model responds to small variations in the input data.

The KA inner map's Jacobian has a special structure: some rows are exactly zero (meaning the network is insensitive to input variations along those directions), and the remaining nonzero rows are "canonically aligned," meaning they preserve correspondences between input and hidden neurons. Mulligan introduces two measurable quantities — the zero row fraction and canonical alignment — and applies them as diagnostic probes to trained models ranging from simple one-hidden-layer networks on synthetic regression tasks and MNIST, up to pre-trained 80-million-parameter vision transformers. [In all cases, training produces a statistically significant increase in both metrics relative to random initialization, even though the magnitudes fall well short of the idealized KA construction (roughly a factor of 10 below the theoretical target)]{#mulligan-training-emergence .experimental_result
  tense=indexical parents="mulligan-ka-t2@paraphrased"}.

[The emergence of KA geometry is smooth across training steps rather than sudden, and appears most strongly in the early layers of deep models such as vision transformers]{#mulligan-early-layer-observation .observation
  tense=indexical parents="mulligan-ka-t2@paraphrased,mulligan-ka-t4@paraphrased"}, consistent with the KA interpretation that early layers perform a universal data preparation step. Interestingly, [attempts to steer the model toward KA geometry by adding a regularization term to the loss function actually degraded performance]{#mulligan-regularization-result .experimental_result
  tense=indexical parents="mulligan-ka-t3@paraphrased"}, suggesting [the geometry arises naturally at an optimal level and cannot simply be forced]{#mulligan-optimal-level-interpretation .interpretation
  parents="mulligan-ka-t3@paraphrased"}. The results motivate new interpretability observables for probing internal model structure, and suggest a future direction: [correlated weight initialization designed to give the network a "head start" toward KA geometry before training begins]{#mulligan-correlated-init-hypothesis .hypothesis
  status=open parents="mulligan-ka-t5@paraphrased"}.

:::

## Transcript

::: {#mulligan-ka-transcript .observation
     parents="mulligan-2026-ka@faithful"
     verification.transcript="https://www.youtube.com/live/i6OQ5Z3repA?t=27507"
     confidence.textual=medium}

[7:39:09] Okay. Hi everyone. It's great to be here and I want to thank Sarah and UCR for having me. So I'm going to tell you about some work I did with Matthew Van Herweg, Mike Friedman, and Keith Adams.

[7:39:30] The basic idea is that we're going to be inspired by an old theorem due to Kolmogorov and Arnold about representation of functions in neural networks. And I'm going to present some evidence that standard training of ordinary neural networks realizes structures present in this theorem to some extent.

[7:39:56] So I'll provide some evidence in a variety of different sorts of models and these structures — where they appear — show up in what's called the Jacobian of different sub-layer maps. So this has to do with how the model responds to small variations in the data. It's a sort of response function.

[7:40:20] At the very least, whether or not it realizes this KA construction, it motivates new observables in which to probe and interrogate our models and hopefully learn something about them. I'll leave open how we can use these observations to improve or make training more efficient.

[7:40:45] The basic context is the universal approximation theorem. Performance improves at scale — in theory any function can be approximated to any arbitrary degree as long as you have enough hidden neurons. A famous recent empirical example of this is our scaling laws: if you add enough compute and enough resources, the performance of your model predictably improves.

[7:41:20] [Now a similar result — actually 70 years ago, predating the universal approximation theorem — is a result due to Kolmogorov and Arnold. It's called their representation theorem and it tells you that given a target function you can represent it with a one-hidden-layer neural network.

[7:41:45] In contrast to the approximation theorem, this is an exact result, and it's exact with a finite or fixed width of the network. This construction has two pieces. It's a composition of two maps. There's a first map — an inner map — which is a sort of universal data preparer map. It organizes your data as it comes in, in such a way that the second layer can make use of that data.

[7:42:25] I'll be focused on this first layer map. This first layer map has a distinctive feature — a distinctive geometry — which I'll refer to as KA or [[Kolmogorov-Arnold theorem|Kolmogorov-Arnold]] geometry. It all has to do with how this map responds to small variations in the data. That's what the Jacobian measures.

[7:42:51] Within the construction, the Jacobian takes a special form. This special form says it has three zero rows — absolutely zero. That tells you that the model is insensitive to any variations in the data along those directions, those hidden neurons. And then in the remaining directions, it maps in a canonically aligned way. So it preserves directions as the data flows through — input neuron to hidden neuron preserves that.

[7:43:30] Now the values of the constants and which rows are zero can vary from point to point in the source manifold, but generically the model will respond in this simple way.]{#mulligan-ka-t1 .observation}

[7:43:49] So you naturally ask: is this directly relevant to machine learning? Well, early on — around 1989 — it was thought that this old result has no relevance. There are sort of two reasons. The first is the standard argument that although a representation exists, it doesn't mean you can find it. A stronger statement is that this universal data preparation map cannot be made completely smooth, meaning there will be derivatives which blow up — at odds with gradient descent training.

[7:44:49] Now we're going to follow some more recent work and be a little bit more optimistic. Recent work has taken inspiration from this theorem and built architectures very much mirrored on the KA construction. We're not going to do that, but we're still going to be optimistic and ask: to what extent do standard models — standard multi-layer perceptron feed-forward models all the way to transformers — exhibit characteristics of the KA construction? That is, do their sub-layer maps have that very special Jacobian form?

[7:45:41] I'll try to present some evidence that there are actually some hints of that — some degree of lineup between the two.

[7:45:54] There are two metrics I'm going to be thinking about throughout the talk. The first is the zero row fraction — you're just counting at a given data point how many zero rows the Jacobian has, something you can directly measure in your model. The other is what I'll call canonical alignment — that has to do with the mapping from input neuron to output neuron within a given layer.

[7:46:42] Here's some data. Let me start with just doing some simple toy tasks: synthetic curve regression of some nonlinear function — a particle in a box — and then MNIST.

[7:47:00] For a set of data points, we model the task with a one-hidden-layer neural network and measure the Jacobian in that first layer map. Given a set of data points and a Jacobian, you can measure the sizes of rows and just order them by increasing size and put them in a Zipf plot.

[7:47:28] [What I have here is two curves in the left panel. The grayish one is the behavior of the model at initialization — a very smooth set of row sizes. The darker blue one is the trained model. What you see is it dives down to zero, and that diving is what I want to associate with a sort of zero row fraction.

[7:48:01] A zero row in this numerical experiment is defined as follows: you take the first percentile of the initial model's rows and define that to be zero. Zero row fraction then measures how many rows in the trained model fall below this first-percentile threshold. That number happens to be around 9 to 13% in these models.

[7:48:36] So there are some hints of this emergence at least at the end of training. How does it emerge through training? It emerges rather smoothly through training. The point is not so much the magnitude — going from zero to roughly 10% — but that it's non-zero at all. There's a smooth increase from initialization to the final trained model.

[7:49:19] These curves are supposed to tell you that there's a coexistence of both zero rows and canonical alignment that training produces. It's not as much as the actual KA theorem — it's like a factor of 10 off — but it's not noise and it's statistically significant.]{#mulligan-ka-t2 .observation}

[7:49:46] Now, there are also non-examples where it doesn't work. Focusing on synthetic curve fitting: the particle in a box (an XOR-like task), a linear function, and a random function — where the output is drawn from some distribution so you can memorize but not generalize.

[7:50:22] In the linear case, there's no need for any KA geometry. In the random case, there are trace amounts — about 15% and some degree of canonical alignment. But the performance (R-squared) is low at around 16%, so even if this geometry is there, it's not being used very well.

[7:51:09] What we found is that you can train that first layer — which exhibits these sorts of numbers when we apply our metrics — then freeze those weights and add on a second nonlinear layer. The point is that single-layer training is too weak a model; it doesn't have the capacity. However, the initial data preparation from that first stage of training is useful for a second nonlinear layer to take advantage of.

[7:51:50] [Now, if KA geometry develops during training and seems to be useful, maybe we can force it — steer the model through an augmented loss. So we added a term to the loss that encouraged KA geometry and trained on a fermionic wave function in a box. We have a tuning parameter called lambda that either encourages or discourages canonical alignment.

[7:52:37] What you find is that performance peaks at lambda equal to zero and degrades whether you encourage or discourage the geometry. So somehow the model is doing its best when you don't try to steer this KA structure into it.]{#mulligan-ka-t3 .observation}

[7:53:17] [Now I've shown you very toy models — simple regression, MNIST, trivial tasks. We also looked at more respectable models: pre-trained models with around 80 million parameters, standard vision transformers — the sort of architectures which underlie our good-friend chatbots — and we measure the same sorts of metrics.

[7:53:47] The key point is that these models are much more nonlinear and have many more layers — 12 in this case. At each of those layers we measure the degree to which from one layer to another it exhibits zero row fraction or canonical alignment. What you see is the metrics are elevated at early layers and then decrease. So there seems to be this naturally-emerging, even in these larger models, initial data preparation stage.]{#mulligan-ka-t4 .observation}

[7:54:34] [I'll leave this with a future direction. We don't really know how to steer the model — we tried with a simple addition to the loss and it didn't seem to work. One idea we have, although we don't know how to implement it, is: if KA geometry develops through training, perhaps we can change the initialization of the model weights — give it a heads-up, a step up through training. This would be a non-trivial task, since typically you initialize weights in an independent way. What we'd be asking for is a correlated initialization of the model weights.

[7:55:20] It would be interesting to try that and see if it might work out.]{#mulligan-ka-t5 .observation}

[7:55:30] Let me just leave with two messages. First, gradient descent finds approximate canonical alignment or KA geometry. Second, the question is: how can we capitalize on this?

:::

## Loom nodes

::: {#mulligan-ka-capitalization .unknowledge status=open
     parents=mulligan-training-emergence}
Gradient descent finds approximate KA geometry spontaneously — how can this be capitalized on, for training efficiency or interpretability? (Mulligan's explicit closing question.)
:::

::: {#mulligan-steering-mechanism .unknowledge status=open
     parents=mulligan-regularization-result}
Why does explicitly regularizing toward KA geometry degrade performance, and is there any intervention — such as the proposed correlated weight initialization — that can push the geometry beyond the level training finds on its own?
:::
