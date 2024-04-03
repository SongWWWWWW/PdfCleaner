text = """
Table 1: CIFAR10 results. NLL measured in bits/dim.
Model
IS
FID
NLL Test (Train)
Conditional
EBM [11]
8.30
37.9
JEM [17]
8.76
38.4
BigGAN [3]
9.22
14.73
StyleGAN2 + ADA (v1) [29]
10.06
2.67
Unconditional
Diffusion (original) [53]
≤ 5.40
Gated PixelCNN [59]
4.60
65.93
3.03 (2.90)
Sparse Transformer [7]
2.80
PixelIQN [43]
5.29
49.46
EBM [11]
6.78
38.2
NCSNv2 [56]
31.75
NCSN [55]
8.87±0.12
25.32
SNGAN [39]
8.22±0.05
21.7
SNGAN-DDLS [4]
9.09±0.10
15.42
StyleGAN2 + ADA (v1) [29]
9.74 ± 0.05
3.26
Ours (L, ﬁxed isotropic Σ)
7.67±0.13
13.51
≤ 3.70 (3.69)
Ours (Lsimple)
9.46±0.11
3.17
≤ 3.75 (3.72)
Table 2: Unconditional CIFAR10 reverse
process parameterization and training objec-
tive ablation. Blank entries were unstable to
train and generated poor samples with out-of-
range scores.
Objective
IS
FID
˜µ prediction (baseline)
L, learned diagonal Σ
7.28±0.10
23.69
L, ﬁxed isotropic Σ
8.06±0.09
13.22
∥˜µ − ˜µθ∥2
–
–
ϵ prediction (ours)
L, learned diagonal Σ
–
–
L, ﬁxed isotropic Σ
7.67±0.13
13.51
∥˜ϵ − ϵθ∥2 (Lsimple)
9.46±0.11
3.17

"""
num = 0
for i in text:
    if i == '\n':
        num += 1

print(num)