"""
1.table和标题紧跟着后面就是table的文字描述内容
（从table这一行的下一行开始，如果行的内容大于50，找到第一个低于50的行，如果这个行以句号结尾，则从下一行开始找到大于50的行，如果不是句号结尾就从这一行开始找到
大于50的行）
(从table最后的一个字符开始，如果这一行还有文字，则从下一行开始找，一直找到小于50的行如果这一行是句号结尾，那么从下一行开始是表格，否则这一行是)
2.两个table紧紧挨着
（用两个或多个table将一页分开，（按照table和紧跟文字描述处理））
3.table可能在前面，也可能在后面，table在前面
4.table在前面，标题后有文字
5.表格的内容分到两个页

"""

"""
pdf:
1:
Table 1: Diffusion training strategies comparison
<re.Match object; span=(73, 122), match='Table 1: Diffusion training strategies comparison>
Table 2: Segmentation performance comparison to non-diffusion models
<re.Match object; span=(557, 625), match='Table 2: Segmentation performance comparison to n>
Table 3: Diffusion with different number of sampling steps
<re.Match object; span=(10, 68), match='Table 3: Diffusion with different number of sampl>
Table 4: Diffusion model performance across different inference seeds
<re.Match object; span=(686, 755), match='Table 4: Diffusion model performance across diffe>
Table 5: Segmentation performance without Transformer
<re.Match object; span=(1220, 1273), match='Table 5: Segmentation performance without Transfo>
Table 6: Training Hyper-parameters
<re.Match object; span=(1285, 1319), match='Table 6: Training Hyper-parameters'>
Table 7: Network Size
<re.Match object; span=(758, 779), match='Table 7: Network Size'>
Table 8: Per class Dice score comparison
<re.Match object; span=(73, 113), match='Table 8: Per class Dice score comparison'>
Table 9: Per class Hausdorff distance comparison “No diff
<re.Match object; span=(73, 130), match='Table 9: Per class Hausdorff distance comparison >
Table 10: Diffusion with different training variance schedule
<re.Match object; span=(31, 92), match='Table 10: Diffusion with different training varia>
2:

3:

4:


"""







"""
Table 1: Diffusion training strategies comparison. “Diff.” represents standard diffusion.
“Diff. sc. xt” and “Diff. sc. xt+1” represents self-conditioning from Chen et al. (2022b)
and Watson et al. (2023), respectively. “Diff. rec. xt+1” and “Diff. rec. xT ” represents
recycling from Fu et al. (2023) and the proposed recycling in this work, respectively. The
best results are in bold and underline indicates the difference to the second best is significant
with p-value < 0.05.
Method
DDPM
DDIM
DS ↑
HD ↓
DS ↑
HD ↓
Diff.
86.60 ± 12.38
41.11 ± 35.48
86.18 ± 12.41
42.31 ± 35.82
Diff. sc. xt
86.35 ± 14.14
40.42 ± 37.53
85.96 ± 13.78
42.00 ± 36.76
Diff. sc. xt+1
87.14 ± 11.48

"""

"""
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






"""
InstructGPT w/ AR
175B
60.5
62.2
71.3
44.7
69.7
43.3
InstructGPT w/ AARContriever (Ours)
175B
61.5
64.5
73.1
45.0
69.9
43.9
InstructGPT w/ AARANCE (Ours)
175B
62.2
62.0
72.0
49.2
70.7
52.0
Table 1: Main results on MMLU and PopQA. We group the methods by the parameters. Our Ls is Flan-T5Base.
AARContriever: AAR initialized from Contriever; AARANCE: AAR initialized from ANCE; FT: fine-tuning; AR:
adaptive retrieval. Unspecified methods represent direct prompting. The score marked in bold represents the highest
performance achieved among the models in the zero-shot setting.
"""