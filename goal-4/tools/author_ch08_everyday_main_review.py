#!/usr/bin/env python3
"""Deterministically author the accepted ch08-main Stage 12 review.

The semantic projection below was derived only from the sealed ch08-main bundle
and its accepted review. At runtime this program reads only the bundle named on
the command line, verifies every sealed input, reconstructs immutable ledger
fields from the bundle CSVs, and writes only output/output.json.
"""

from __future__ import annotations

import argparse
import base64
import bz2
import csv
import hashlib
import io
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_MANIFEST_SHA256 = "db7d40b08b753c54b27ae6ef4497f1c6ae2360bb43e17584cb08f08b50dec675"
EXPECTED_PROJECTION_SHA256 = "6bdb98a4fa5ec04940a84bde2649e5e5b06022e6fe7642ce4649d9fd5e350196"
EXPECTED_OUTPUT_SHA256 = "1f301c91f9d7c8c83bb6ed03896897c30f0f1e619957066c6477f33c54f07606"

READING_HEADER = [
    "source_unit_id",
    "document_order",
    "path",
    "block_kind",
    "byte_start",
    "byte_end",
    "line_start",
    "line_end",
    "global_line_start",
    "global_line_end",
    "unit_sha256",
    "review_status",
    "review_epoch",
    "review_disposition",
    "source_status",
    "uncertainty",
    "secondary_roles",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
]
ASSET_HEADER = [
    "asset_id",
    "link_id",
    "physical_path",
    "sha256",
    "bytes",
    "source_path",
    "source_unit_id",
    "assignment_path",
    "assignment_stage",
    "assignment_basis",
    "reference_status",
    "inspection_status",
    "review_epoch",
    "visual_role",
    "source_status",
    "risk_flags",
    "original_resolution_status",
    "transcription_status",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
    "uncertainty",
]

# bzip2-compressed, Base85-encoded JSON containing only accepted mutable row
# annotations plus candidate, route, and uncertainty proposals.
_PROJECTION_B85 = (
    "LRx4!F+o`-Q&}h&@f!mK{NL?h08;P&`al2w|G)qL`bZ!MhCl!q01yCRjhpG_?;@G8qP4Gff*rZqm35<RByO0lg<8g%R+?zW#<yV9"
    "H<h?wUwr%Lm)qN`nw^tkURizgeGh#I06K(T@R!@KfPDfk;P-g|D8cQ#e4!o;3|;Sl6X$*NxH<;i&t1<k-(Fs0YkRR9z5oCK0002`"
    "IqtLE^i&^1AOZEgg6~Z3+og;xz4woy<og<ZYm+IkYfFf!tj>g<zTF#TtgV_jd5$<W+s{ti@Gi?5){^vNcy|dEN<C=$i3ycDnBeBR"
    "1AFD&SJn4$6HRus8>dY7I_p-o>mK&y4_4jWR&z=Vtw~+mbrmCQI;nI*sZ}npTMcOJmaf*&20#YqeE2rrw?2KYdY*j;$OG$6_egiK"
    "wXbSEj&clUzU^>=00-8TAj}QY&h|2JX`oDy6G0G0s&5lhN#;#c^(T@vZA}dTWM~GB3^c?LiKJBVRQy!PZ2*Rb1Z2cAGy?>{nlKV+"
    "A|hy-6C+Ji^wN*eNO@0FK=lC8wE^Wkpa2?rf=^VWl4_o0qxB%spaGx&Xa;})0000fDIows38O+{X{2eDH1eB7^$gTKr8EcW1obgA"
    "0ErMn6GUhVdYMLzCXZ30O*8?Z(?9?K&^#o7Kt3Pt{NI`W$@YE!ey`dean1iL{chK2_e;y$pZD(i4?X4XjwN$Nh7CHdE!;yPr^gr@"
    "{c^Is5=$}HhfkmH=YyK{8w+VNLY-wRHqX1aFA(k`antSlyZ+w$yU#`>Rst+R0f_+HGNa42)?M7xZJAN$^{+RZA3tu`Hf4rr^W%IT"
    "wd%~MkYOZA7BC4Q0D9vlOXJqF#5L_l8ZBUAAHlW)ixV0>#0$uEX1&$!2c2JNok+(;8xix%su|iq;iplq9}u~%y?65nQ4@q(B(Hok"
    "ZH}dnOR789rlH-FLXJ}gkN+`BlF;nhuN*@~?8JgjuZP{HIgT#S4NHLB*c${vssZ{;k})#H!S`VO_wUZK2ie9^>l)w`Kp|JZTD)mH"
    "u|IemFpy4TRvmv*-s6xkMS<FT79@45nHlFweYIHqPuzM2&l27=LxfORmX|_<uuaQ1{Vq`uJA>cu)D9y-CoEV6!m&4=z-wD4iO#wR"
    "4erC=v-`vFG=x#Y(ihH(py=AtISC~yRGzeI7}aOT!#EiV{ZzO_0L>k^hWOIpgvDxS5{X5@`De#-o#>5i;R@|kA&yl@Q}*P)T*uC0"
    "n^@Nv#>Ee>((7;l5#G;J^hC@J>1fn8#A%+S03^;E_S*3PWtbnY^{~D?-1RNv*bKS0)fCd@Tm<q%ftQ)lLE>2SF&FI{l7$LIhnIw*"
    "U?|?J<$(=8TafWn!<+V3C%?njvVd~;?cQ?-yv~sTD)Xei^E~RRjgbanP>>*i>Q9uyf>Fv!VK6Zr_N}ksKFkMQqJh~RS_L@O?*I@m"
    "MmJ%*>assp9w)>0Ut3v^UNRd5#rf_q3J2%Qx&lEUkV+CsC>V55WcEj|Sa8aWj3k7flg0$btC47<I--aVcV}+Hy*_l<C{`IMysimZ"
    "k>=-7rdtoL&wL)X6q1PZgM*S81G)7-W$I$;IJ;}80eNA-OsZ}IQ?Z)|c1OUzWrSRW4x|aiSR))mV7fDOhykLGcs+Ub$>*x;Q3{30"
    "#a`R4#BRA}(`DI%gu5}C26T$2Hwcl%z$a1_)$?XZ9vppL+vOOjs;Y{L@t$rsJ0wva0^0NsJotSZF=>86-*knI1(9qq5dZ<Jjop}1"
    "`%?C-;sWrcqo+~;0A=t=3&MC#X9n)$Y0}m59K`#P(fp&$eX}(laoS&NmaXgnJzX>F2c=!rkCHG1L_nC7OHub2*eM}9@w3`kQI9yH"
    "j<r)@BD_P&aXQpQL?B23FFu2(y^x9EBXvcSv{&8L(Feni1`s9s%9Fw(P*`W}<K(japRg?<q0PEHKP&G%h!gfiZy-4p&VjobpHTMt"
    "q6fXG!*H)^C)*=B?=PU#H+Iih;|qbW8+y}{o2Mi(8y$>g003A#oe;6cTeGf#K*?Ts)wT!Bh+?&}ro}s3AV2^X9*HTHrb}Wv4b~Pn"
    "dw;axjh+}F$Ou5>s4VSNfe(hf&e`<vAf<8J7j%yj&T;KeGwB==1LKZk)~-b{L6``UDzocZkgfS~>$r|<&3XKI;Oog&rhzjYGT~w{"
    "X<AhlEJiFXYiQ)QGXMjPcH!xFoc2#n`p-pLsok-ia6>Ut2=dzT<zOeR<9EGA${80{3^t-UehlnZBS(-R00!25q5yfKy(C($t||he"
    "0z(%p2y&`vM<kKV1pzhhDl+;lm;l5Ed)2`hXtFbH5+}1ydGj=W`yRZig9o%qB&a<D#2433!`)zO+iab$o{U5}kVpy)1IfuF<)T^v"
    "je*=LAOW4UxdF@|fGN2?nCaMvaapuPMH!l0J{lalh=Je)e9*}tkP%l;Paf8pZHoq@Q31={EQgPS3j8;mL#pCT{w(WU{cNthzf?dC"
    "ZfOt$?_M|DnHy%FNDhjBw+IJF5C8{o0-qR{p&4fQ=%bX6S38l_sRY=zK!6Kpfs{G~%{tJIpbC3YAre9+p8}ZB;<BQ$taVmoJd@`X"
    "Y|WbArJQaM1VGFs*G7D(eq1DLjo)HwY)Kc0dB>yxxD>3fppN_2YXd!(Mp0w}h(I8UQb)v&@p|v^oALI}hZ%0_s~q6?;uY)Ou!sSh"
    "lo9epc~^_aQcaI=G(pbZQJ{7&-473|L6D~zN(h+KfHeefl#+OiKEr)^c-|Q24)FrZ>`)D7yy+G8sGZ0#Sdp9nu$$~1WSCt{_ymnt"
    "I6#GQxXI5xX1mZ<Zv8U23Ng15_0~7Yg0BoYsm20?2RPqnj@+JF_Ps~2oM3EnkBlG=a~UJ?P>MG;H8rKDRtaUy%!e}MqNXNhN|YRl"
    "VW%y~B1&dbnNk~aZXpp<0vq+MO<^(V-!YZbGa&aZR7w(W)I!2obO-<g0Dwq5gbbZ^OFKTJMsX*ONJQ>7epG4*L}d*+VLBrBgzEEO"
    "+rx>*`v<3$ZV1aP=ssAvJI31IM)}WhtLhgX@NOt@b5<W$!XO9AtX}@N&%$O!01Oa0(4#^U3vCg+mRysW`s!C4@vEbRKo3^~qM!z9"
    "_`~(OgP4l;iVNoj8=f!co;@ta>qc=&HNSJh*T2>CR})_r3M)510m7i14Y)SupfMqW0EiSYWC_Er0=yR-FwuF{$TVI3$=WUC-LP}u"
    "#G#3uB3<y_vF=d@gWWzp%bktv4xAtm?qHvC^N7)zNZ^N^dAXg#>9EWd0Q8SJ69u4=OZOR(IdTn0ifPe1-X;(bNlMZKZhNrxndmR^"
    "QSgd=#Sr7sjF}Zt^2{F*0IA=N7B#r@r4a{nI;#frp=gjbL;(;NjTlgKMH7>+o$%;Rg>Zc_b$!(i!*zk&h=P$7>br6;*XS7xZ(1%N"
    "UUdU0Jj?+M!ve@be_X<Fe3fpS*o}v+vOo?I2;8Q-WwBWgzE>oHvWemvG$$@}^ni5{8F;%^Fodh$GLJz%g4GTPbFzNZKX&(}T_{WN"
    "SMt;k)EFj&4&et3$W91OCuXcM0X1>zAbbJi<kILB*f_@YcSVF-2=i`hV}rA0RVmF#r~wS@))coIGmU_9(ZyryBkxIm3&YSizpro6"
    "q1R+505RY&0C;G!ERKlVnQV|osJH-)SxE&|5EbIxkDH^ISdIL!j2qvk6Up0L5<}eVx)S__VnHO5gb)cN5+Du2vxOFVGIvdtWk)vb"
    "Q0E_?E2mAcUGbDCqBtLG3yYfc9bw|-cl6~D13&;Vql^Ylp<lBvLZ6wLAt0zFKwT2RB_s~Ph(yNV(GpAg>f;b(aQhZI<{A1poH2#("
    "P2JJpKojZrHaBZQ61uCURq&L{m*~YumDzqHg;WE5^OxKmMox;!umk`A@D2@&3m_Sk9h*RQAe|LfJNLdy0DvTEjtD8EfSEW^wEzGI"
    "vJsEWQ@}IponN>jYI((E_M+bl)qN8Lg+3Kh$Qe4=dv#UoJaw;$L42)^hmsZ?bG`-b)o0Upc<A$Xs@MQhij!j<V`k=fwuTHN;a7?4"
    "PlkjmSjRoDjOS0gH;-u6jb9CYrB#OJ8@y@ImF=xf%Naf&M^fXAP%^Z++qBP(GhYMXvG%J5t67xFAdiYmy`k-$g`xmy_}Qf)$Wsx@"
    "hi4#cr7|EFH0q^JkWYcD-q6zAtGpVw(#QdEGmRKy003O=#jRH?G3R{(YXIQ)mD4Lbs40Me0fiG*RW&^;5|9_y-nn6hKq8`5kuV4&"
    "e*^#-%9w)3f*+Dz8>Qo6w(<gb?imm^z~{0jEm??#h!4P>o_j%w4Hor~k~ewRyQ$DS8q10z73++uvaab06LNES#;I=bFG4^Q15)=k"
    "&|3=Lb1Sb8T}h?GB&_6MmMY-$(iG6H&t&scR7VFo5W=mRZ$?H<wX%2|2|5XwfB?j#Nj>pqJa@o?me-CPK@(6CS;c7AV|y`(8E8n^"
    "TO)(Z*v|Q6<7i|700IG+ePI>1e8*oF-T+5jUu#`DS#qmA-Z}k0qmVf%rUsjJw>`&+a@ca5kIZ-&*CSkb(086p6ma`njZSjS+}cf?"
    "IP)r$wg5+GzEc9{<?xMUAU-(jy6kI&keknMPwR88u<$%xv_M!MvpTU~dq4=_2xQRq<ms`W2UyRo9(7)`gYoO%Gs)j*K}Z1r1DKEi"
    "@7|8&YSX^%dNqy}FPEjBo1>?dzJxAFQGmKQ##G>m1QFRr&Awqe9x?UcF_rrVNRkj&wmlKx-`=>-ewt9gK9rH<J774ErzH3IM4%mr"
    "z{WF}p3m!|BVc&pz~f}o3Zt&6?h#peAo^D|lBmp}ETB#8SZ^5N^FPDe?DEIZ^ZEUMeNG$bBN22cTB|q%7AYkpP{tDL7MM<e*XP@@"
    "_&IQ&LYTeaPzC-T1V5Dhkx%86%m{h&@b<*NV;=}!W5lnBcktvq$eD~gy*?UvcdD!m3pI6E5v^-!f<o59NJ%5K+HjmE(`m|ZZP^1("
    "m`R|7<&&3#LB36BhN-E|?9-=$P3@Xw(ZrfvEaYoTwB_Ep$&)LPCjeGJngX|s((9d=&KD9$;cS~9+WEe_zd`YPceZJD#=V)Quv;RZ"
    "zDRxnC&wf|hg$OU8cf-=k&?n`HcV*D(PATHWo%npX2~S@iSe-#C^|F{XXlEd41PoiR51g)7avl#`aU<qyHhs!cfQ*6H3hv6BFMdg"
    "Z~@i?F&n=0{CfBI`27A}z5VX)?(XjH?(XjH?(XjH?(XjH?(XjH?(XjH?(XjH?(XjH?(XjH|7ZxG>H!i!L~%8EeCdp7hp3~VxNBRN"
    "#jDj$D(>#??(XjH?(XjH?(XjH?(XjH?(XjH?(XjH?(XjH?(Xh0oaa3A&*%^Z^%VGud__cH1qysB55az{*w)%@ehO(j`6)kJ^E{m5"
    "Byuid`+|>;Cy!&>+uIq@J<oc)ZmRQ*>vJDlnR3LW+pXHw)2ykwIj1LQP49Oo>268KH1Rw{1q4L*{FBBaDuCgj6X9r%8Wf5u!s+aI"
    "Fek7!lkWD_2kf^fE0w_A)zfD!TwgY;+Q>TNw>{jK?cB$5W@i(IZRT2L2{98qD&lJq5f?L27jrXlbwskN(wnNrEpb&<O1EZesn>eO"
    "Xu-|>(NDkQ<@Nbt`_IUa$M)-Rgp)g^55L?~U}_f@K&c{Q0+tT7E0{9LhvuLj2OhjK_#OMNrt~rDVQ-=M_C1SqzMH`<D$GK7Jbn+r"
    "ojTWd+5+sUFW#vxDnt5_Pq3(ugX29WXU1ZDXTs`7+NaXI&rHb;H57oP@)8+S1`W0$=B8oa=A0?Dt+vPUs(rL1@}ux)c{~13Z=coq"
    "{lSlK3f?8ex4pSHZP&x0&xLP*Up>O32KIF-!G7iDen9;{mp3`c%lMg2qe`@OQ~)nsc<bBS$FE-3cXxMpcXxMpc>xo`1Ow1P+qZjc"
    "`e^#8B1nBUV3X-oeu$D($fqw9Dfk8afpTE&0=cEorqSVqAxB`0hS+IO)&lV<*HBATFMIada5Ys#vjCqYQ@}11?deHT&}txI){~_*"
    "{!%COqLtvUpbOrRv_@0-((_2K>MNO2T{^#6l6l&Y7De$SG+0HDQ|Q$UVPf12!vdTD?GV@kEK$N>bwj<BkWd23#0!j$w4&Z{(JHlQ"
    "wj@|i1sp|<r4pe;$C%Ac*t&3bn9HLREwZ&V4&ehc1)6dLUGr|3j-<}<KGJ%t(N5QQno=f=2q{VsOH}~ljWaa>D(OrR5=c@ZRkTe4"
    ">{Dj+JF2;Iq7n(Q4GM_R<|XEesslMiHmow7=$>kM)a+Apxh~XqClvB7yQ8H)1v*o>@`7BG<t2)2Rft%~)lwZor9|om5hpjg-qv!U"
    "iU}indA#Eot><=%!Mxg;<*R9JYq66kJcz57#o-ePn8R4mfH+iuzFfQ|QfH#1w4Lh>4B9Vpm$^&4Os1(7(wLu?<sdeI=oEB{c06jj"
    "t(n1`=e~_-)^K7(%!!dRB20;~Q&y~ouI`0Us;jYfF2ux<GA2a8h!GJ2AVbUuh=&g0<|ahQn5q>*s;Z3&v2#|ehK1Eosufc*CT3(z"
    "$;E@yw=D_^T)1o^F$IJKSyHnx8z4avZBSxLRL&qk!#D<&>q$cn6d*$qEJ!;`39WL=dDgbmo$I3)YP_NtilXR}iHk8+CLBqjIY>%q"
    "7U5D5CIPW^Fl1{>S(4_#S!p4s7Z`-nuwWGN3a0cBk^@KuRNj%HEQ!?1mTFjyShg<P8X!z!l5s?nDM|}er8XQodeHI9zmmKheAGUM"
    "kM7kRYM1$Kw#R@ZE+;2--Pd<q;&M5*Zf0iZ2-;FwPKe>u>vE<V6m6WGmgAd|!kK9fmZ0l6WSLDAri=qBwJRf1p=dI3x@_7aA|fIp"
    "CqzU<+SuAHv1@Hy+^2TsJGXaT-MLQf$h1U6L{W2Gw>K!RZbVd3b5|lL-8UjAr*+CS?%axZZdu*A5f&?(l<wT4blkCXawv)@-8Uj4"
    "iq`UqF-Fv4jYh#yV?`Q@C@8cVyxw`;-N__N7P-43=VH6KBw4O#(W6F_QFYB@b5+YbJCYJra^0NWZfVzLP08JtEp)q`xdx|6)lpo9"
    "X=!Cbt7%XzEVQMuEn<+O(YaT5cH!9y#^&9}RY6E76(xc;*)6au29=PlBPv@$vIS_?5kf63go+ZD!Yx(>Ldcb{Et0^tfm(r9mLM`)"
    "B#R)n*=o{^3v3Flb#ohaT-&Zr<c!wkvAL3Ext7}A000000002C+iObNwe;*CG3rtI)8%eoeuihP^)d&?@_SqHe0BGHo1Z53XFqN!"
    "aFqD_Zk=6Sg@R<<%fhi!Pjz^E7ZYmvdeoidqz%-Tp7&Y06*s%wt%YeLwC;6y)0MsN5gN>T#WZ#_rgTM>vUPh%p{jc~t&F|Bsc!}o"
    "yUbV&%hqLzIPPaxHf4=5sW)?3f@4{9ceR4{&QQt|Q#R{HlFDVOs}}JgnQC5etyWfV5fDuiVT()6u%SX;V6iJP5Y;xqYGtTfnV|TY"
    "!r5lJ4>wxYx3cSd8=|G&T<ciX$VR4un@<p$LM9lH3@Mdq3=U8YfuJdNp-SZh00-U?F>MQ*h=8Wx)Z+sb5k9}K<Uj}H6^V>mIhPuh"
    "Syr{S7Up2w&hI1MTbozdm4IsK5(*R`5>r{6Uaq$>mcZBF-{JuMG;FEEta4UOL5)<GS!UXsW`)b8No{cz%%P@}twGh-3fhA*D%TCa"
    "?<sVo%1t6iMpbsq&4FC4LAzwm6uT*kT*Nsk&blda&LGw+b2w7RP;k3xqZH|Kr$spJyG0tsaB{gNcFwx3ql$Brm34)^D_XVd)z#}3"
    "Ljs7~ZB*?6Wl46@oGVf*ovtTsP~!;ABwX7w6yViSGpA%zqOz2-ldVqKn`m6L4j9;{7E-$-jt;SFQk^t~b<M?98;&Ea+Dhw0Kg_3z"
    "F|;;QEvC@b6<Mu5wYAl`sANn<5wygsHqeb|(N!q`7|M-iG?g1_l49FwmcwO(X^?*q7Nw9UU=IQ@jABnb^PY!;>HUZJ=AuqFfd0%l"
    "KXy`A&*^XLbpz%3qg{phBhCJ4{Ah^?sO2?)sqzFP0uuxA)4tXv28mhxBCt0H>8vxT3*Jxec%bB16$9~?Z`N$nC*k;wHJP*lUsOZ@"
    "0QdL97xL9-O>Vr$>~3^ihl0PbEar467*a!^KmZD&y#Ek%2mk}J0B|-?4vX-#cNsyWrEDAJ^aH8T@$0u4%$@%}-Z}5QdU^Bdp4@n^"
    "+EhjVxTobvAwrO;E@e(BkeN(VDaAQzuC|+fRxudbBNj9of{a+k3~U<K-djyoc$zIW8Zk9#HDxtrYP6cMG-zsSG-{Y>Fw$kH(Wt{J"
    ")upP^VU){BmR4FCOs8csohg+il*%}!RAo4(Q<My*L2*o}#XA(a6N+lCl+vq;X(^P+GMGy#!6@RHOiPMnggL2PQzFV`No6#vie*V<"
    "Hx-OFYgvtu%|#lG328AKY^}R%7&2+0rJ<s6O-Yo=WiTwJDU{NkRLVfgWSmn;Sxl*v*Ts2t^kq@?{1r5aCe%a@dxSiBzaO>-y{v#l"
    "_BLC;bLkAJpKuWT&!utwjzDQxT_q@1c>5V%V7r{<5CdxF77h_q)X^kl5P=1N!6Y}qtKKOCV&OTx6Z93coKgf0u>vww1*sK^<RuZ*"
    "=UHMC$1VV#u<x#pp5rj-cjNC@&&&9#OW(kJOVhr8v)DMRta0drXE=kE4?Oqu(vp5%6(4+QRK*j69DgRl<u_#UVfr0+L_}^&?<2H8"
    "zS^+^>O>=}0ucu9l&fS>u@MC2x^@T!xIircGQ%K?3KVn+E1qBKkFuWBiyA2A78eI+Nmi*`O8kh9VPRDL75UmVt#7XHtnH+hXFaEa"
    "hFD*1OP84~?sO{_E-5K98oxH@y2z6?@9v++mxOoV^f<Ly#WPBewf=JKKfFa9FPU-}k7xBeOq9oc{6rayF*0$u-lruiV1uS5o$ki6"
    "=*mhBugmSu8m@JBPk%eGY6!QvvIBD4(rjKow!#bH{lrK|2B&KnQVkP|>S*|?Pi@t+?O5!ER7f(`E_W=A@4573_kE7YGq*D%s_y&c"
    "J#%fPTA5|TO9hz^eHmc<y190<vs`L&OuDf7pJE0<B;<Ku!;-XUvv!Bc3`Cg=KK{<|4(JxL?c~L~4;pl>@hW<s-Lj3K1tUa5q1^69"
    "2$2-!;WN)l{a4f7%!Nn3oLd7I8b>U%C>4t$f#B3J<0&FBafT)#w5(VQG{V~o#R;SXOw*<;kXQ;z#VTvrLmpUHgq02VP|NV$y*5-i"
    "<`obZIBKGi^jo@c%wy7sgh_;1XND#TAmQ}3hV>c)e8&}+QjH~M*ymHD5=`XjB5dW0naGhhIFYE!7n5crnYqM{W6T+Ih1D1)hGU7a"
    "+5}RT8L0|v)#c4tqag&OO=RI&k&{CUnJP|7wNW>gBvhd8S*aOSMkJYei2T4G=7{`|fcRgyK40dkj~u7@vp<w%)2U+BW*OZBl<ZRy"
    "$i&1jqTyB8QNVm*J}BRqK!AAYzmJ!Nz>fiO`~euAkq`iY2m81?1`Gh-o_ef1{!|4ZfRqHJqIVNBGc$J8RaF&E^lt5BU4@Fnyw<gM"
    "M5U^>-fZn-irl$WLTR*8WYH4TfEUi~=cq_WF5I|j!vh%SoORa#e)-Fpj#MG#>6$rPR3ZKq&mO(~eLjB&>DSm}ZHmRB+ALVHV!>$9"
    "Y+FXf8ra$`7BxmTHpEtg8mQVRv8b$A(Lt(<Mu^poL|bEQYBq}-V`!sRG+P?Q7TDVs#j$K{8lus(MzmE$V;UmZ+BIT|qS1=6wl$)^"
    "w|$ASSuC4m){@C-Et7ABI&77a(o~j`v8y!9W;q(U{!v?$+>+d_!j|N23bi^>d0TCwy>`$_2_yn{$Fiikt5-2dGEBu<VFnP)Ri;2g"
    "LTf^;%XK0{Q9fZ&8(J3GnP9*!i4gc2DUM$4u_Tn<BNzdKGH!wgU(OI#YO1QURaI40Z&=Ib_5Qel1x)5Vx~`B&?}=-rDPT2nr1LWg"
    "mcneZ#k^_dNR@1rRD?JT0KgLw&b!WqeyQmv)(rnJf*;X6#N_Hy=sFA!hQTtqIw++ImJNeKd;w-9*r<=TFAw&`I9-~`*&K-o6ahd|"
    "!T?i(#Ice#uuK(2k20!ci&i_7-OLFSMdfBlV6Rg}njxJmC=F&5N}`gBI0YU$592dVw`8K8_uJnhWIB7E!13V(fQU@Y&3LZBB0NPC"
    "RPhy7*@)9cR)~BZyKMjll|*{kTxzwXQ+0c-);o6XvR<oQZ;PwSSNxAxLFs)8djgNSoWtA$`QKsrFR4WA9`<a40olW%$dOU?F-c<x"
    ";4QRGScM=COqr7D7>GIu5r7m(Edx`FT7|&Vj3DDi428!6m4U&6;3XIq@LmMCI25cLV2oy=3_0725{;!SFizhWcG&f@@}0b~=(qy%"
    ">Cyq?#LpPbRZK1$4~%0Kd5K_47FpzuZ%$_DsHMZRD)-6JDI+wl?xbC6ad_R>JXtEMyXg8u*e~TA`vD1DzS=2MvE9(@h|CLu)|Lz!"
    "C|U?GS}2@L9jk|w<<6SV2Mp@xOvOgXgd+elXVk`;BR!1qCx4o2MAdrLS_v2&r(FaTIzTb4RaH{mRaH$@+MI_f%B&9!mCcnr=1h)a"
    "PZ>iPE^?-%xsqm7t93I*Wj3bOvk-s|0B|#|`~X+61Q0#^CWPrXuo1&VvlR+J?kTlNgfOy75|>JzL@Q-!6A58rcf=%Iwj`+}gCmir"
    "c@rd%0Zw>s7qcuNludxZ!U3Mb46N&ls>zBKO;uR8e8S|)ygI_fJ1NT+dUwm53`^Vy1})+cq6@^~AssnSWZ6V+#1CPfeUhp|ha==C"
    "!$rBuYNV8vB7C}KR8nNE7Po^}gL?Jrnpj03PQgW#WPoyG;JH30ljY8jYQ&BOj#N*~0rb1O`sRIdrDjf6X0|4+cyY_ARMl~o+vd4@"
    "Ew+~olF61?2_{>qN?gvdj7*uj8d^g=R%i430ml7+sZ>cP$K!;DoZZ;cmP)}8RRVbCVVRcOkuxyyb(*c#f@@UMOF}5ovZWaa<B*92"
    "dkio@`au{S6Z7!jx2c#L76-5fU<2kN`I(uQ^SOG~wOZWkRmWnAs&y(#N*B24O{Lb)4HD5IX{MzRkSR4RIZ+5g9t%4!sCfX#uT~L?"
    ">5PgxWV%uen~a4Qw(x^RcQ9=rmgZ8`pq*y$)FOHZf*3ts8qn7K@#$2W1Bb{O0DG#{-m_0LGIKS(NWHx*o2t6GYFaf~mi8=BrNcQw"
    "4LY$U%)PL~&_qCi4**ud>d=y~g;Y>Yl-q@{m6%XbBoZY83GmZF7=zg?RD24f2i3Z7-Dg4+1P6i}dFs60o@Qj`Xz=rO&2yKBO}o|R"
    "s-|l~c%Eu+dZzfCr6DT`w9|Cepp$P~%yNz5=2}~6b%ZRFAY_?oD~5#-I$K*>rK+OUuY5@|VM|!`L`4S-KA)TAAAErTAq#!qF8*$x"
    "y}|VF=<EBD+CKxT0Y9nz+;2a|Hq%Z&4z}(2Z|%OPIR1~_#Xi_)@k9IlR<XU9)+^f=(w}hppXiAqLL(p$A`p{j`))|56#s;e`y~Gv"
    "PxV*$$N5schZmFkqoPmwXZb>OMLQfw>@WGm4_a6Ii9D!$Q@h+u$m`Y*H=_BLiR~euFZPj7`vB;7ztqF(Qk^N}s>0#x>rtUktS4zp"
    "P}CLf@gg}%)}jAIrl*uARrjh6DzP5wby9XuU8$;r|4TTHS~o=!cqHW1Jk<7ubxOO{j2bVsPg#HLk)wqB^(Pe{_bG_#4rTI5*sjil"
    "w-HWBn_DY6|3Zqcs4M;wAB-pEL-l&s{cp%wsb2Lz?N=LNwQSnQDHp5-^_1mRa#K*NsZS#>R*z*q&d_wfWUt0k-5)AsW4pSi(4Q;V"
    "Cz`9uSNvnVctY}1*-vOXRF~wbFU5L^?(>6+egYkp`AcRRS@cbMB+I7-$#F4#!278`FgcqWZChT>NOrE_k2+E2)IBP78kO)xJ_bCY"
    "II8(1_=Dk<CHOuR^pWPuc=V-;!_GtUsmW5j-Kd|fI}c$Gv+YyJtI<AacS-MFchWQDig%!|#F2eoN0epvQ;{B&az`DZJru|2>@26+"
    "?BY)o@Rr8pRCz~r)E(+NB*`8C<kA`w-4yVh)hYR;)j`TA@Rh495%fuk<x{ktbTic&J_XWF(NWntN{$gaReaFv=s!D@KA<bgSCawd"
    "2h~!ankn>lbrl}SeTyLKmChCLs{54n5~J=VJiu4jj|80|X?dz?d6srg%9xr+zQViDLOhXAiBslNvh$BMh~j#Ym0VPpkou~<WI1?W"
    "N*`37WS*4oL%K#mFBGh*;;YJvGLA~oka^F6jZI|5wc-=eBa)qz)!dJ?uVkGFcBd+Pj_R+i6n6n%FJ)KSofo-_OFYdSjpiZRr<$H="
    "UT=a=awm)-HdFp9=#k>RAoEkjPZX~z9tHHSQ&k3KR!5P-IFpVk%+PwpQ@X3tyqr~hkxroTB;tC-E8SZyEHWhduM|=L6#OUDL%L7V"
    "?gG6Or(TlByk3&DA6lZmU5@QDO^nkttrVJRX-iEtGiF&PnKMk)nq{S?3ah0_X-mRPRmD$#*lku-f0Tc?sxIkNnJE50+rpnO#q%7M"
    "{vYAv_^bA(=^=kvPt6(sUNQJ$&*29&8FBs}=+p7H)<u{9YRBcE&M}+Lnc8si8a~`F=dd@WJuAo<tUkDU&Z0luFDFjBb5}cOQ?<8$"
    "ocshr5EwvKNdQt`efMz$S_r=Va+1VRJEcVxREWdaM3C#-t@oSR_!xKiZ^hKOuz#EUpXUBw<tO+5H}9Em=l%sai^Q!p-`I#hQ6wNt"
    "Jwq{S!-$KuXTqXr8ES@(qF&itT`e^XT*cU-HegP8Hk=0u!NbP^!NI;qX?fo{KH>L@S~62gAfz@lU@@rJv}(m0HMiHcw6Fxt0LZm%"
    "CdIU~2FZ%7V`~+%8)`CbRI^q!sKjhqn^bAF6C#akY^1cC2xg{RO15ENU;11@(%LrKsm@bs+mN-I(%RZG7@5myZ7rP|#>{P81CnaG"
    "*D{Z__=)|DDVRUDKhC0`x>lCd+O+*jt||T1LDHR{#ttO=eczWi;l|_gc76}Z;nUduKDf=A%{I1J+fA9K)Y`S9*%>r@6F-WpDj-CD"
    "8uhd3%lr*0_3QA)nP$ellYs!_l)=;OPh|I1f5?;RQ^EES{!|~lrTK|Jr9<;83jUNI%})X!%p>~HbR)zc=77Bl%97%p)m~~(^U7pS"
    "g&3~-t*|v13Jn2*O`?lMj24Ka7P{Kk;9FW+slu{_GA$)1od*SZQI*kM%Ho|VsBM|0wr#U!)Y>-MY~m+KJt#k-o=+t@5$d6+JXAZ-"
    "dx-W#^q}ll`_esBo=BNb3TUIvL(wVX0_v)ELFiYqq`N8F?y<CB$)wGRmekn8WT|*l)`t}(le`6zoGH?sitblc4vNUHQnH?u9U*Z~"
    "@a^TqIi*_pMuyd<lPQ$cZGY9xo|tuz@6KH-`DwJ(s{Z;9{@t=BLk4t{=m{_>^QTdTK+mO&PeW{4p-2CMzPxsAu<V~l=F?c&wQE?S"
    "`Y!7AZ(iQ!#YLH>Q%sPAP=t%F<asgt4G_BzpBa%4>!<`*gt|H0pI>1eNB;KOfAszy17l#xo;*i3>mAk6nKSn1(!bfSpU=xTH$I%@"
    ")u$Vnb}j<0Ym|-@x=x#&bE6$!Apf~O>YcyweUds-cs!UXY}34xj#TEVOU!WnA@%*d>|Mr6t!J<NRTh4SHaKo*&I>h)S7?{jc4;rX"
    "Cpmdnk;n#%LU9)PU6>`LU?o-<E~=e06flz@z=Z;$W^fh0l*6sCD)46DO>L=-fC7g~7cHT<VIq!Mg9Y1g)^n{G1OkHy09G&0G+@ll"
    "sey330_Jg$aA%zWSOa=<%*;5>YUf$5d83g4iUAY@g-#XZo`8PUJze|@`jnWbd#Hh*SlK`o243wa&_pHjAR3VYDemT|bV6|VPzipX"
    "op<Xe7q!?ZDKp|Egn=JU9+P8v)VA9ZKIi*$G+q8Y&$rkyeIeYFs6%JNAkT6`!K^b3vnqQ9?I=FauI8(od4+!RmvuigRC;O)H9XJH"
    "xRdh{UObccGZrD(nR<_CHWcd!&hJxVsG$?yi(&>r3vneBQ8(3j<Q3l?5?7^FM6$$TRrC=6`n75x$-#nJPU7%^Sdt^+X2&boPS}wU"
    "eyvclDOEv17hs&viTiPEHjQek<Il4UJzV{#nGQwqrI}b>SA@Ky<deLC^ip5q*X!~pZ=_ymaaY{-3EY(ZKWkf+KDy0b{=4lkX3CY`"
    "y`rWZQ&OQysThC*<QG1CFTp(Ls;DUrFOQlps4w&8WtK>!L*OJb)hPP@%7>z?EAsX3r)%=~bwSkPdK}p~u54}Jbzdz}s>^Eq`Y6!&"
    "k|cr`$YM{I1^9S|AP}R=%fJjFXvN$?13?FHbAUi!jU8a8P(wB8j9w*YqFoTVvsXGery`Zhj0%YU=0gfUzX8YJza}S)wF!%A$><5%"
    "0H%vlf)R|^Vx$NjnpmU60E+@BCJcgdd}3k$pB8Tq<qMjfU9l~Y<e_tP&JGQtZ!{`Vn?f8F#JzFG3}L-*I1z^$qPi7uAe4v!j50~q"
    "XaqJ(qGR)6xg8m*RRDw%Iz#}(veI2jR15F09WMGn>-81$RoI_wzaQlC)@`xyO!IoEqW9~<Pha6dz{Y@(QmpzmjtH39_?bc#*aSy0"
    "4@Ei_<c0agWR{I9Adsj9K%i6C9QpoP0v!aIK%Jlc_yQN!kYt^tq??Ox{X%Jm=($10l3;Y}ot5S1LDdhgj{Z*y#?w`rWsqx*zqdFe"
    "v+YuOWS3<0sr(ASrwPsoMS@5y3k)a+YvoOFh#&09v{RbyskaLEJRwhGOPNjUS7Wso(<#|%9NQH7XI19gcB0aI>te}3lqC$+nzb}I"
    "oZ+{X?x`<zHw#DsN+CnZ=C9n|<dBer_wN5BJq2bC^T#?~9b>K^8P@>n>B<ZMSc{l4OCV!v1;kogW?an1(m}StBus%MEhr_yE@jHg"
    "azyG9OhU4lLziZ^TwX={^7XHLjj@RujV0{e$qz^g$XakI^c+wEFI78AjJbA&GTI^AypuwyfJ|hRrvX&`A{7;pcHVw!Q1(=pk5k`u"
    "@S}%!mGBU{?Zi#uK#}ZXAdWdPVgNvjcR4u@#uP)c-0$3DCIqvST-^Y0p|BvJBP0uZ$p~*_pxX|@r9g10*7SAYuTO;yb*x^swm&Vx"
    ")wOF?>t8#4svUhauS$lirB-uEw0A(W#w8r~xb3TVMB<&~47%Eb6X_$xFDovGTXzm;1<SVC+g9lnaF12iHnIU?l$d2IrZ^u$xD?`r"
    "Z~}p+eYocq*+I-#4D-*8Lo#fxIKsHXxrs=?a|jTy2%=W=Zfu%K$pb3Gbs^3ZmugmTpIPN;gTZH~qna_adismHqKGkLBhr>nZ>p07"
    "G$d|0T3;sB&r0R3$*xu1rY)W~X4EBv=uOtwYHQLRZp&(@OS^4uSxMJiXq%Tc?A3}248lwxNMxB&q9ufPDMx{;v9^_DAOZ-=Qkc=o"
    "cxBQ{HDF-isxe48K(^Fp6op0CH#}Sz@ov$*&9`8yHLar=rVtCFfmsEJDk*a7L^hJ~DJ>;n-p*IG<F?)=n=36|+TE(=)?9|T)EFzK"
    "aif~&MRYj2B5_;}AnL8HyxsvPmnQDFB-XiT0}-H-P@<)hYqz7018f0G$P^NcHZ`vU3Wl8sAh~N{I+a~#ea*Y@UV<`*6g#QmPKxOZ"
    "!jskMw^bE=5Ps?3*5zUX#(SNK2{{PHMj`El)Cz<C7<L~y#@ENcl83=w549B2$SVXmxOh{{Q_Dh0gm>dt7bR+t=g5wDv{34q?XRY6"
    "^zCx%%cqnYq27ZX?}Rv>N_y&5V|YOY?%+C!vn`4R^dgUL3gE8qJs8QGy5@^Q)^76m#@<J$EQ{DdY_>}^&COJMz**LHjfb1QV_D&U"
    "KF-%D>0d>41K+%(l8%%@2!db@5X5#2eU`J*eR%S0s<9Nrj}<{>CV{-2IykxI#Wf?|Q;y>~$^=gf^h6qZ`46k`Y>JW*vxF8LD!R0g"
    "IV2svNZ}Oa1lQvXJN!4-K@OL!lG;=1f!8A0+|74ujpOponyqExAO-P+Knt^sSOJfc5Izt+h=;7=j1qfY9dQ7Gs`K93paS$z!_Ynv"
    "-*nf}h9H=ZV2D6MH}Jj65*65<36<pVfjyK=Xu>cFzjgosUWI46!z3t2ms2oCY|Q4QGDf3Y001sG98yslX}fQ9$5_@5wb~DCu%i|l"
    "oL~vsxa6t^fB-1rN%M~Of)o(~FD73rln^vRYRw9kNCTN7846Sg00Hs8Zs?wE-nc-+7*5JO=Q*vd&2i&I;pNVUeAfz~7`#jv`u7<#"
    "Da$4qLTXa0IR)NI0Xdii07@XO=u~M{Q=WH&xVq+U@OW%$NRlI!m=13E6$uKl3rGaus1U3v*EK+J00=h0$q+N%GB_=OwSmk=6<#gq"
    "M#T<e_|2G(2!oLmh-<Y>QOq5~p5-lOv{hZA09C0V(oH5l960q))`8#0y&Q-X@av|a0DcLz6}|$VHA~g;!5f~`qCrK#S-#pjZcqs*"
    "hyd7zwJ7Ix<~j+zc#u15E=lb!3aRAlo1(mQQGzZBSLUi>yispq#0u}t2%a@wC=3Isff>(<vBI_H4bQB^phN^ff<$L*U36!HgE1@("
    "lO~?6t}75F_1_4bjC1Fr)2i%Q)$_bMw%i!wM{~M|c17DEIHxqyh3FYsg$+ds3Or3r29d}SLi{9Gx-R)gyvv%lHtm7UwJoN}u-c8B"
    "gN=Bp;vJRKO6{cEk&b4~lM|G7?4~B|PS|WIm~I=FdYa<erCAOM4oM7>0XX4RSA5}$w$)WtS2CEa!y!>Y8kE2cgm93msw!BuAU~s7"
    "=O?7Q=eCRRhyivT=8DHb>6Oe~L)Qw#!o_OPRNGC!2_zOkgkjduINsX?=;T@JHOCk^01O=E#<>m}KuZt;*%A)XP)IuVQd8EfZIfNQ"
    "rKeZFcqL=9B;Ig`1kwQ#QSBkuDb;MuJ9je0Ft1O!IWj9sNloaCC{Hx7!DTv$Izg13g;K<*%4$qjLD@-^=@Y7lr3Z4jq1Zyasu)AU"
    "pPU`aKGB!*^c<hv?g!qwpI$fD#<q7Fe_L%+)cw%a=7bY!0qo{k`p#bm*8&?9G`;Mf(lQ5x3)`o7JDr!K)v;gULEQRjJ9i;s6eLR7"
    "0DmkGA$Z>My&591YSBsxA(TK449G*}%9+3)NSJH*Ckz$cjZ4}<`GsF@7KGt|veF3t9qJ(W{SBl1{#-Wx!)^m)LlA?REAucghz35T"
    "ez!`^P!jru8<G%&2ZkV;p*~0vrneyt`%7S<uA%OSJHGmM$b~~JHSWwGN(eNq?uM3u5C8}@#;r`CQUPU3tb&P3ng&qou)XL`*v8B+"
    "x;Z)!G0x_)YZ~Enw%Z;^5*pY5I%wJe0P^NQg9kChgJrn*e*DMm5r!aMW|yv9;vc08lU_R3I!WaOIIYe%p7=OYdU{d?_aQ+!qcz?Z"
    "Lmn%g%-r8<@x555aX^6IL-c<>U%DM;rq8<eFCK4S*ZR^q5%@m}*&7X|HfNWY>Tl1Tzr#3w2iUJce6Q!#{aBRkjZeJi@qTmFBjMce"
    "UuJ&~wRh?})AR}aY*gAGS@gz#k0kH--<5gt{XWxeqhaZznAoGWA@aqvekD=z9)f$1*^2JN>yY441F_tRA)nbpYZQveNQ{F7R}iE@"
    "TEVf<U`)_iD+`w}Q{In9?bFTktG7Ov-PXU3aiH{|`CkbKI>)7c=VXpk-}PI|PGnY6l2jG6smUZEEu9dBkVWkk0)aCsewb26XGrs|"
    "j(}Rh>)Z72>P&{Fgf+Nt1TcRNGDl|f$>h0U0UDTs)kD7Wsdt;Y#h?f_DG(G3Oe5a-t?@QdPtD=SOTRq0`~7eIx|a6try!#g;6$@w"
    "$Dp7|PN|Y{RSht+8z?2_hSR+bBG$`1Y{)}RB1RO$3`9}RsZzy&8HA2vq0yB;UYYfdb8K!@HzW>i$l2*Wa<+TG4}bthnXu%0r&|jY"
    "`pT#jD1n*ErMPl-Vvz`gs5m>P+cuk4)qQ>6Tk_4RJuj2uB|9ID)ix;Ve{w~BvX@<2RPwxOw6OIW=fXu{(u#cW9r?eT`%=C1kLum$"
    "??>*i5)32vcaZ`K_{_{IHjBouuCbgNwIR*`RLL78IwRWMsSX`+f_((Z)hL@45rUb)I1FCl+8a3I6b>01PzgexNk_FwbzruYMhq5%"
    "a&rvOb=RKRho<l{)#&fRIJ>{E`Ej$gcU-vzJ{bE(qta6PbHm223#Qyq;udo%__g6ezV|EtK6rGcPotuPzg;SpIqt_oh1OdPofGp{"
    "_E1lVQ_vQ*sdrr$LMbdi3i*Np*oYld_s#W8Qc|Mw3xEm(^B@QV!Yd4;W*PAQbNDw#fB*}oD2e>)?azXXdFVU>tG&9ea<b6yuM|K4"
    "2;@K;h=Tw@09Y(wF-VJWbgXZ7Hbzx~aRuv&G-owun&KDiR~+v=Z%u%Q9>hi<5D|HXBK&dadN#2ST&G<&w6V5hd`ALt>6XIy-QU@V"
    "=<4m1USDv>MR4MrD+>Ko94p>^+IaJ8)tXRf+P2jXWv=l(6hQPwNfDd16~SC+O^yYO6=ceSbkuq}9QSgDQn1s7TToBZGe3MJokb*b"
    "S(>i@M*Bz_=BElE%z3_9+&)3CJk~OYZY~v)hug|*nn23b79bGM<@E(qj6?DZLHt7%LjL(GCp4nw4}Bf3$Bg->MfG6%s<5HK$ShJ4"
    "3Pc`5b~Vfu``r#rFBK{LuzabWicZJXI=vOV(x-x#ILme`g>}~;@hSWf%b_#H(KJG$G=7>CM=2gnSBz7J=z+7BDDjm;yA<Zs9p|om"
    "9i6oHM9AiNhn45+DD-4)D>N6PHKc7ub5PoCRbMCiJe@ptpgrIof<zdZTPU2gL_$d=j&50?Tc?}HzDvWj;yTLRJy1T`MIIS0icSf5"
    "fQiSBk%|DqMCL;B@wL3k>o}tx{@r+Y*2*&RaZk(2@!E%;#>U3mW>-@ujyR8tn>04IwSL#tNy&L@wNX?E+ck+LMy{`)TYL4hB0Sk^"
    "Y|PkvNFLHXLcW{fUs{whEmL!*Vyv@m%afgM?$ttUg|R!W)!lTExsLfRT3&Q?M$1~ZZB>d{6ICUb@1XbZ)n6BRPL=%b9rL*5?;db3"
    ">~?0Ern6gY6vYZnl$#o6N)ke%1R}9OBqTtgXe|uIh{m*Q7||Mv3u8qhQKk&TY7LCTHIr1P(yfa$)N3<k+C1JR9aos2(@3#EvT_X{"
    "MiJ~#jY9(zc(@Dg8_$nac3AH^aHWB00q9sL_2UE(rm~Yr9uK+=Jg4^UrquG@r5rs5z6gouG6Ic{n4v<P9ic(G{>=4w^-qVJYhZ0n"
    "R$f%l@iwzD;wK^E8T<RcVthxE(C0LTwlr)Q*t7`>QlOLq*its+75kLr?A-@-ddR=h=<?PR;tM3KS){L9ZIxCbrc$(dZi@kASYOm?"
    "VI*r5gDkktI&S3ea3PP8Wx57oEuGfO3G<<9L@FsnS=M_S*ahiV@#N3-NcJ)+j1+>99-n}z<s4XkQ9BgBr#EvI6`r(RmsX!;+v>nT"
    "K>-6$00u*34Imo@C4dnCz(gVdgh&KNkPs0Fqzo7l02^smt=`{7?d22A@)2DA$KyBEbmb(cC3V-GREwRjhv7Xh8OJS{+aKoQsbg(Y"
    "bPu4#5Xc~ZH_rR!R|1iNd!k*~0Cl(9x13qycoFL)k=x+!AKSDxa5f`7CzCN9S)dwp_P_#o2vgH*CbF3e-TIoN)lZpzg8G-S==`44"
    "@nMhAtEV5^B>MFGyplZn2NazC&Dl@bQr<rb?cUmCPr{*}M)^XXPOE0_ykm!^n#azm@uQ}6281{izm>@Ye16m1L+iq)2zCCW>^7;j"
    "(CH(bUy^yB&lB7F6fM=#sC}DzXV-6DI?1E}iZw^1q(vkprbF@D-;Xw9#yih=7v;FZGOiXM$usyln3(%m7!0H&B*AH;=RKV-D}j~c"
    "=;Ir#7Hu_rltI8qf|!?ZECVEJXXc<P4si%1B^y8zbLI7=%39=$cWwY}C}|n1$^x(+j6^IN<Ih$DM`7-Dhk)6k5Df={zX?mB$FB9r"
    "+P!}d$iENE^7V760sR)q2x(u@9o>5d%z^|xNemt!r)f`HzMDHKoZ^!bdH1{M>|s)oGjVQ3Q69i!^H2y-CVtfV>tcIijyAy6r?!_e"
    "<|^i_OHEfQ#cma{MOmHaIh88eU25h_oaD0yG*Y#;3t+7nTUASGwa!rrFjxdCrC=NM42+cn&F9xH#R&?k3dgvZLj@7Pp@C4I;i8x1"
    "n}2hE4>WzN@+<5PaxaHN>#k}2SvZPrv~?^J>epCul$z&TShvTOd80{IZMNGczhl#Ht^0oDKGxNX=bYOaFC@P5o7O}0=$x*pJ+W;@"
    "#?=MbUYEty+h%4ScZ*@MJ`TQy${O{O`gf0ZQ|r{Yon;Rld&E0Cb<N2Giv$y&hP&bPv?>IVjJhf%ss!OoKu`~r>=&PZuet*C3DNL6"
    "J>ba?ZvGl(%Vq?n1y}$Romq;q*d8I&2@Q7-5Kf+W6*z!AGgPc-Do`cG06SHdpq&jSB7jUaBRf$gMf=52+Ty<2<v`Tg)^ate)=&XZ"
    "Dk=s;&I|fIj8Qosj8NC*Ij9{fFQvm9Hk)~R`aU<o<%HLrC9Q{<Us?~3um4n!x1X0bqmajYu3k4v+@y-A*|yiq>#c^3L-CF@5Wr9+"
    "pM(THV51d4yOWyd-?sSs@1MH`a@@-;88t;VeaCg8qgqMbb6B@mZi_=KS+f&1TN3Vdw=A|p8B$#7v<4v7-KkpFa_mgo6dreNF`Jyt"
    "4=O}CnS>nYEGn{wFm}{{U>KCGX;q1BAp(_(A}z*}uBb6zx89?}d*|}~C{M5Q#Xl)d|5Yaux!!nX1HO)FUqS1%KpxakJ>nM?Q<Ib_"
    "7P@|Xt{+YGW>d)24!?(18hv*(<`8}en7D&?9zt?!k8MRg+;OR65<s#+D9V8#^@N^X(%qRKS)M~=iMnq1#%5b}nX4s&$s9!Fys$#d"
    "E+9xIVY<naSPCl30+eLPP+(o^&~Y{(Mkx?V-8fw8HXlAQbtHEdpu$vmnB7X=gaZNz(DpP@Uaxf4`ezJ|W6+%T>(93v9{_gezywDc"
    "E0lsi#Ue4pUJQE3!bE7(JEvb8<i#(J)uo-zWvwvF!~h9y&DFMQ7>(mi#St6hqoSm679IsDQ>gazZmYSH^=KYt^+DN4dL#81ue4}b"
    "qfDNhhb3Svi2x(r_yYTQ=_u4poBc0n)*WtVH#NDrK@$0L6>*h9pw|Nkfh3Fpb@ZL==;^@thV9x(az|%E@2F$cdR6peY90e1aDbR8"
    "!R;2+z|-x+74Z5)SK$0}W2brOL!Ntax-3bnmv?G9b7t=Ce0HlcY2D_L$qI8dU8yI^N2R!^bRxVkHAmuovn%fpY<_3h`U-$vV^j0l"
    "SCWn}a#@2T+`5#Ru;Y$2H->^jed|`3u`6j*0X1Zt)gWGwnvcm)I)&hm58^0TMxmlYmL<xT3Y4X`0vn|}cXE>)WD$uKF%1Zem}^+|"
    "BogvT3o#-&xeQ>mru8kD&BF=-M0n7&gYdZQ&(x_b>ULes=^*MqW{brp@8iMJa5TA|7Y8yr00RKwc^Lv+5f7|Vy4fXFW?FM{mZoWm"
    "sxq5;`F@lcl*;t)pGDE+@~C;s@nx|4e8(vJXr*?x=M_#U`H(s1oi@WeDb8!pxyD>Qw%(28=!whLmz?Xh&NUz@xw^%-y4%a+FAokd"
    "J@$lk*M5+>cT>qzx{XGL%%Te=6kBUo&3CM~{4Qkjf>;7<Q8%$sqAkEmCtjS{@W-n<wLBA%=Qi6mS-}vGZG@TFF50A8$yf!eR3xpe"
    "mt%7{03Zv!%iCS<)re8+7z|1Y>saIXt)gEX$%v!@`9#J3H847pHH}b6GK#2!hz=mHY~71SXrlMITganPxCm}Lg`pv;L~>tiyQ_Pc"
    "BuR)KeBEBOtJis0+$B=t0ARYP32=fDF$HQPjItQPj3JN>8D<Q`sGeI01!A%Nv-yrN2mz!{{GpxH&X#spYRNW%$xNjNfU{nADR^$A"
    "40zpEUKx1Pd^p=;?W1bz7irodBBP8}?yd+Z(G5f#K@%~oEosgOa;Pv|LB%-=+<7iuihZE)>^w;Cw%I&2Ai$~yRRV`7fEJd?ISb-L"
    "(pMXhHj|p?I4&zyDK{#+C|5eRWL5X3xFgM4(sq$^tg$(Zu5d2;T#z*@vsTDCb2lz?gzQkc&e-b-J1Dw<w`COUlsPzShhY`WRKWnl"
    "gaE)HfwEjN3knTYOx<3J?(VyG<tPQ#%ZfGIP(rC&tBA-z2&q>YTcRNGL$7v$$=@kYw~e(^YSd=DYWE019{kO0IXizavW0NJzw#fT"
    "3Uns~Zx}8p@TS#OvuK%{C|W&Zl9pRlv5om;<gT&Z081AT0+GQ$htTQm16Un!a2@RRY^WD5TuB0;C&U*DHN(!hB7jaza;vmZYOh{7"
    "J%c(^l>*#J*i{4L$(xWnz(fz(hf^Tn`iuJH><|v%c1pvW&b1FBg%}iBDp5FUyDF%RnKXrF_O{oRv;`Oe3P|L!1iTHwLBQE1)LOv0"
    "%$P`o!3;vOh+_jHET+}BIgYvv%yXS(No6{4$fywrED4Oo!ow{Kb0mNuN!y1wY&jHNn<J;}>T@>3XJrG^he=Nf2Vxym>2+ho>^KDN"
    "G*~%7#nzp(T3u5MYm}s=tW1%XKrxa5Nd^<HIh@WNZgh%Y;wrosOu9r42>FAEXPyRmC2dND3VvIe2moFh69gOWG+aS^iEXCXS(Z{("
    "0oHcyQ~LVled(jHeMvv5ev};f2y;X9P|k1jmD%6@du^LW)jLj~%}O56mwKOMPu)^|EK2e5%dXD=wd|rD2qM_L@&@m#q*@XPPzXOE"
    "&_C<h_4x@82`A0cKn(f%&QGoYud7<TN^F6BFX5-hMn`|G{;idf`1^$Jspa~bOIs#X!*4qLn8wz>99%V7TO6dF&xfZg_o(ajJa$OS"
    ">BstXTA*bkX6<}llq-A{xmwpcRS*aym77MZ2-|9#Ct7;$X*$)E*;FxBN~@|Su7uX~xT}y$QA<gg6wx$gciMGz=W4eNJ9W9UAc%tn"
    "1QBSht#7xVQK;J{+b}j-tyCH{O>4#I4?KVa<%=v`{_#TMDo_O0LtfexKCZO5@EAeU?N1}!r)>?AIkpaEYv%=j%rb%8hC0O_Us)%m"
    "T`Sb;@b!E<)p;-5pDYbvBam7v+Q1T~4MNDDCHO={Dt9FcfO@tLDa8{NN34HjOgPbQA&nT9tO=qKShsn*W(BgSvhM*KZxu@^OQ$f*"
    "tVS7$o^`7#ssKzH#(e=t4tZRYw%smqx9_0w15{J5ho*zcfL`FE_ZRYV$TjV_Ra7XO4iOiz_UeyGPSp7xwdF_CRdkPG^g5O)x`7x-"
    "PcW~NqUL?P{jpI*6Mr*aea5~W%R~T@iY@O!N(evHl4S-xf%=YqjxMkt%TudX)KhD=u2oTv>#yUq4vjO|mE3ti^K-zJ_FQmxk{i?5"
    "KN$lqD7E;**A1fC#YFZ*to)>%3JSlk-VyM8si3Q(T|JMZeO}^KkJqX5WzUWq9NbE-j?84fx_N2L$DcWy9OPtiJbiN9xRt;z0*ipF"
    "(06;ZQv>%x2gJZs&@fWi3HwwGnPQ3x1#akAqI1`(1vLo>FW^KX)YzF0FH`ZYV>PvSSjuZ5dEcw2*q+>yo$zg2SBf{XlTI{UUbTC8"
    "ZT%YK;H>J~rsqA6f903SS`*LC^L+XD9?x&)k>v3`qEnUr8f;gKvrN>-IbNQRjQprOdb(bRQN+R4ZBU5cdPFcBp1^n>8Jeo1GE}Na"
    "kCx(QR}vYCTZj^sk^xG_#J-XSq2;!&)SfSVJtW&yhn6VTEs%OH-eJTq9!23w9^a2sHra=5&`ur?2|Q{?TeqKnym-cG;sVsy%s0dR"
    "4W8%s>)Q)Zh=|n~iM3t<Qb-*{Jj7p=rHAB+^>*nteX_Z!%v3Umh#fldYXn4PQG~4$Svv?B0L>}K*O;&BpR9)Fo;$wP#XWYo{M&7;"
    "tn)ikncjMIa#Uk(v#rydakPP@qnyxMxn%2v^OBiIh}5@jE@h31cWS_+At;q)p$i*q#}Q=2t7yiuC7~^<d9ZUELmUleXw}JE3YsD}"
    "uDtTsbF0p~X;DdDU2;QcqgK|++RJH9<_Hv|21ZaRDBD4i2(pcgYDuUxk>>r2_vKx_58O|3`f5X%!(@e$5T)#84%rkajjgd{7><8H"
    "@;%6$C+`aLm!nKidC)76{ph9iW8a*5%Eomu6mdmEn5IyJ;DVY-L5l^-Je+NNgSj9*XiLVzKS(le#RXgispya}Blw6zgf%T~cVnIS"
    "bEV4L7S(B#sfDryu$DD|%RwLjg8;<ijflNZc#MASJ}2CrgroJT)9^0z?52;kkG>C@H^bWNjx$ZJF2AXIXqyYmuT?j$7vEFaO$TI6"
    "IhOCi+b?;%|9jq7PKsUn%Voa2nZ-Lp(xIi4GQJP%_m@lGh+JFZ=fO={-cp{Yf5jfF*|5A`lq`IMc`C{iqJVi<w>mxP_dMQ=wn|P("
    "I48;evD!&{2SDwufxDkq9>SP>DjQFIucC-&6w^@ddc?@;Bt#;qz?VvMSs_};DE?tD)|UeKRDESViTwn9J9XzTd2zCvab>P0iB`W8"
    "R;{79R+jtcHdfiOM>`eEtXJjjMEhgiYSD??O85<RLHNpjbOrrK=}Gz15bW<fXVGy$(RJQzK0j7nd-N&K!lJJsb@_HPRmo;-70~&V"
    "ys3TPbbZb$=~2$L#=B&;UAUZOHKw*PMcBHFj*@mIIl_<pt8$@PomQ@Ek~=;{J?~l`*<SmaCnT7gS7u&G2dZ0IQqs$(o6}CFNF!}!"
    "%)w(sghi!{W^^e+4%$lDT5Cuk1OPw)67@A|ru4Uj>f2ke05DPt{8aL*UQB%a*Tc8V$LG$m1HIId=~S5P!~ai&%^3`SR}~8ZNkYAk"
    "mmGAjWJ2YK(7?g{g{IYEQ)11eOT!!9QMi~L-L9jZ^!ZXQW}a4hN_H9Hr9IWa0fi`#m(dC`e-J&LZjgcsezr0-vNT1+=X~YGdO^<D"
    "YnV6@;RtizeN~Z;5r_gHb7^)W1fLL`=&*%?6N^XMWI(gZ7{oxs-Sy|X6Y=vi*L|!V0&-8am0W)Ok;sy0SmTD2RYVFA3<nG0F#vUf"
    "ghB!-3A}nizW$;LbR8M>oY$wPlCjyAQ?;)J{3%`eUfZ{d<5Sy<xlKUscL#mlo>qK57V{^%&P+dioswvIb<he#P&4PCzKTZAfzzS@"
    "7z>-CPcg0ea_)1nNz3K5RPCsT!yVEOdk<txRd<-?>7|M;KtUnV8{bW1ArTNDioA)11&3n;5<-n1d_4(_a4DFxH>14Sd~F|$3jmEm"
    "K|JWes^^?uCe$`m^Hn+L#sKiBE3rtRqEM$LGMrMElgx}2kA)-DtXEY*sEetpiQKNJ?xykp002F1ZCh<ErL=INNR$PE=(rTQNWw{0"
    "DaHaotYjjX7FkK8teFs$Ado?49zP(Tmk}pY25dQpF{?1lpkOgF%jrha>%mdZliL_|*SQN?nlu#SXJttlYiYss?n4o?*F1Nn;OPOr"
    "kf2uNv)j2|gI!8=s^bCmbs|EWVbskhb;X;9W#p?{F>4i;*8a?3)*!l`vs?g4I7f1TX#|i+lnO|cN&y&3?B~gJbK+h7N;0%Zv)v#b"
    "#`=)?&l&qZ|Bt|vu#Z7cJ=5dGKW4sUW$F3)_4M!~kKIA5&xLthUFb)=CwwF?o3_gpBmfpB2xe4O`L(S=cI%HoJdE{i0eW28c@FL6"
    ")!6S);W>}Kd$Z|;UkE*JsvUWsx3MRi7irB?(*g74j}ixgq+8kX@N)4-6xPw@t&xl?S);SaXD>!QIm?;MwOZ25ic=q6S`vlK7j+6K"
    "KsV}69UI!E+VKnLqErf@OIxl~kyC*{f}3sU4_m|CJL(0Dn(<S$GTQAuc4g!v(zJ&S+Bxf?_#HXpSI4mzJg;#m(C`yiRSD-+6U&D("
    "y|Ym>t#y}|aZWgQ>H_Pwf8}fIhh7)UHZqw9uEH{zKd(|Y>eW2O+vh~-f^~DZPo}Ib%L}!hcg>$*Rio`y-j9{i`eoiBs_Pt7mQ7Jt"
    "!YPv#sY=RH%6YGJ)8_Wq&E4JAq_Rnx-N4!dVLiKBD`4)^(Nni69*R!or$UL)rd_yBLOGiNr2wSHQe3;!R>iVitxG`9t)0|eoNVhP"
    "J5_lpl<n(5?pJwyHD=gUfTf8gwgCJG9rBjF=SJ5knEd|bf@IMT?+O(9@?%$!?@%L3=8!-jWSW~oNR<W73S~uBv`39go88io`6LmT"
    "nH2Cu14qFE0T9(V*`V|;cguhnkpuNPlM|#C)n>qI`h3a}_{X84eE=W;I?;FHpn{OB6md7M*5NHdN=)5fUDWE#ZgEtFL3z;dhyiet"
    "Xn{moRjuOzhNNO*@F|c0-DfW2AtWN}So=pksOPm9?A_<59AiqAnxLs7Hoc3q)2DV-4)S(z>rT2SVU*~Vb+gv3*4JBJt?9ID&J1Hn"
    "gowznSc7dW%)9N|IjH6c*%Ua(1>u-ruo9_Do%>Kxykh7=cHWI@isN>dJL?w;&9f+g6*!oOcwoM$1oA7?t_e6-bXF@O>V9>#O{{Az"
    "rqwnuY{bo8L3`5JrkQP3n>?Rq-o|MCWrrygMP`0fp2C2-JeR0ZRS{t0(Ym9w_DhTMEAkc3UpQ>#RDtE7PK{JhMI=^1Wc->lG?GA1"
    "TnY*epmq$KtdJyuRM0g|B`HeDRF>F40@Aq3qYSp0b1Oi_vR%@s6?6?kNZVkxqOep(Ac8<!R0|Xd*Tm16&U5L$o$Gs;q$OP45TPz3"
    "4ynvBDMSO4Rxk}Jq@^t~v4F}&(>X}#7LGE}2n1QOm4lv;Do%66o2dml1)k>GIbom=5dwuodxFp}tD<$mfKy=rd%pc6!PPZ+wfBvh"
    "GQz;E9D>3hIbc``iuRY?RmhX@E9O3AJiXm1->pis&y0QbvG`+Z^}DDYdsp!Ou5*Q6T*B=RWDKGKp{!#hiMxoq(ItqI=J3(BxopzX"
    "+=K)qBLJD-ah)@F;pIc)655%hwzSs5v52N<JGAutXM?pl*Id+g@4t>7urXA0!Rb8O_3pK%4S>T};L2il&DR$idUI~M9~6E@9IEh2"
    "x1a0kl<@cDKA(%(<WGvAavI|#<4?lMhl4(rPo%w838++tI0C^tch06E%&cmvUMP^&P@w^CEf=g=nT!KsSqSS*L@zNlhU&oyYBUOQ"
    "Y#r+j4xL9yQ)p?58VKlW+bM%+W@IIC&E4oBce>^oBHKf2v$I&NSk5OZgNq=PB_xuPk_upu;VTn*xMfY?!3-6{Gbu0=vl3fsWiW$n"
    "vOoj?)!ekX32*@oinJh`MKFp|NLFmwAOVc5#xqI9(z&H10T7YA*;5h`3?4hO5(i>7-5ef)+*QDNM0l-_Ohh)hO<F+Z#E)-T-l#ie"
    "yPJ);r+$Sz<F>OAn)LkK_)o8;B=d@T>W<ytQnh{5HSzIyTsgUrX#*C#DcXa!1rxpSia~r}z@$qLl>&_ir9O(Ra#PJ%ut7Z*fKx_X"
    "NW^Zu9MBjwK_b*{c&hOHD&(7l_1+vI#HLkyTVD;9NRnLQZXl*XVhK<|Hx!(b^M_w!B@#};i6<|NYYO2*vAO87I8JUk4mpap-7<<U"
    ">Yk3L+YN!m)GsYdN=s5(Mex#2$^CD)^5OR5fw?KoTC45Zj->o_jjOCU+ah<1KaVH;uU=}rm`3u&9(m;E;ytuVI?@_#QfE5vZ?d~n"
    "zHIOM{dZ7UpKSg3=A8(`IxDjDO8)&`^tGikm~%+CW0HS+_-*Pcv*JbnC#N?0bDM0{w(g$t22OlWO8c|&sm!S_Sr^!qIve5!<OTc4"
    "o4<pGYqe7tdQa%Co{nzHOm$Z|l;Pt&RF_lX6WuYz6<R*!mDX(+XIfh{8BC@|#xms{Y}T@jl!X}~0wmN<s^m2@%KrQ|on><)YRR1Z"
    "{I4RetXj~ZpyL>(QX#?ifc>M}E6$2OtM{>Sq7HL%ZKOX6ojY%C-E^X^`}@7ScHSwQMCKfGb1{jt85S`?nM^2&6w-UA&IoKWd!Iin"
    "$M8n_2}XXZ4!HeycORZcF67W<JSoQ;7}nah%*}0t-Cbq)Pc|X8iW}!wHTBWUoP`|9Lt~np_T@RQFo0spQ3(h*szy|<M@HZUVbm%_"
    ";Wvwngxa;lfR@mEaa)6;EEEn63gn-zm#@YKF=S+Rpsu$dkm}iWD5CI!B9S5jA{!3aaWaNL$-sbR10s;SMI!EjdeWvgo3u@8tF5Z8"
    "xlB_<8LrjMT7^!@r690dYqM>UaR#bI(b&h$F5aFWgY{1l>513+H*?ieTee0g&eLtS)Z%;oTc}r>53-(53Z8zOYh=vW%xqf?9u7^n"
    "iif{{8)=v;=;qdHeRXAGHl3|V>gE<~)i+_Kbx|F%RCZw>htUU^RUO)!`dMe^kxI-k>kpj#bQHlHX`>j50RZ7G#+ua}b<rf(tg#Eh"
    "GQ^+2S8D@sbBY-?ySn<7m|!O~q1FsSMge`{tQj&=uyrKl(MJ$5oHunfmRemmO~@SUOo*<EUMa?l0UaH2=$(ntGM-MkXIffPT&1=H"
    "MB|Eaq})dt$!txO+`*e?BAvLq*7L2ZqPySLL`4Yz55CaNGD|_236RPjl-S`_FazDkCEuLww>GdBbWW-qsw=3Ub=O;O+vED-`tRhL"
    "*pI)JJyX0shqZCqtHPg!NB)AB{}=l5ZL?{zO&G*zi6Y6OAvL15iDopA*>!DyH*Kp|nkls|grn+T@P5)!;Y>mP@|FsJ-z3E~T9jSC"
    "-`D+L?%(77{r_#dy$(o407(zVAEEspjEH_DCqVosbY-7>p;#g1^PiL5fBap^6yZWZpku^r"
)


class AuthoringError(RuntimeError):
    """Raised when a supplied bundle cannot reproduce the accepted review."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuthoringError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _inside_bundle(bundle: Path, path: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(bundle)
    except (FileNotFoundError, ValueError):
        return False
    return True


def _read_csv(data: bytes, expected_header: list[str], label: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8"), newline=""))
    _require(reader.fieldnames == expected_header, label + " header differs from sealed contract")
    rows = list(reader)
    _require(all(None not in row for row in rows), label + " contains malformed rows")
    return rows


def _verify_bundle(bundle_arg: str) -> tuple[Path, dict[str, Any], dict[str, bytes]]:
    bundle = Path(bundle_arg).expanduser().resolve(strict=True)
    _require(bundle.is_dir(), "bundle argument is not a directory")

    manifest_path = bundle / "allowed-manifest.json"
    _require(_inside_bundle(bundle, manifest_path), "allowed-manifest.json is missing or escapes bundle")
    manifest_bytes = manifest_path.read_bytes()
    _require(
        _sha256(manifest_bytes) == EXPECTED_MANIFEST_SHA256,
        "supplied bundle manifest is not the accepted ch08-main manifest",
    )
    manifest = json.loads(manifest_bytes)
    _require(manifest.get("worker_id") == "ch08-main", "unexpected worker_id")
    _require(manifest.get("stage") == 12, "unexpected stage")
    _require(manifest.get("discovery_epoch") == 2, "unexpected discovery epoch")
    _require(manifest.get("source_unit_count") == 385, "unexpected source-unit count")
    _require(manifest.get("asset_count") == 45, "unexpected asset count")

    retained: dict[str, bytes] = {}
    for entry in manifest.get("allowed_inputs", []):
        rel_text = entry.get("path")
        _require(isinstance(rel_text, str) and rel_text != "", "invalid allowed input path")
        rel = PurePosixPath(rel_text)
        _require(
            not rel.is_absolute() and all(part not in ("", ".", "..") for part in rel.parts),
            "unsafe allowed input path: " + rel_text,
        )
        path = bundle.joinpath(*rel.parts)
        _require(_inside_bundle(bundle, path), "allowed input is missing or escapes bundle: " + rel_text)
        data = path.read_bytes()
        _require(len(data) == entry.get("bytes"), "byte count mismatch: " + rel_text)
        _require(_sha256(data) == entry.get("sha256"), "sha256 mismatch: " + rel_text)
        if rel_text in ("input/reading-input.csv", "input/asset-input.csv"):
            retained[rel_text] = data

    _require(
        set(retained) == {"input/reading-input.csv", "input/asset-input.csv"},
        "sealed ledger inputs are missing",
    )
    return bundle, manifest, retained


def _decode_projection() -> dict[str, Any]:
    compressed = base64.b85decode("".join(_PROJECTION_B85))
    raw = bz2.decompress(compressed)
    _require(_sha256(raw) == EXPECTED_PROJECTION_SHA256, "embedded semantic projection is corrupt")
    projection = json.loads(raw)
    _require(
        list(projection) == ["reading", "assets", "candidates", "routes", "uncertainties"],
        "embedded semantic projection has an unexpected shape",
    )
    return projection


def _merge_annotations(
    rows: list[dict[str, str]],
    annotations: Any,
    mutable_header: list[str],
    label: str,
) -> None:
    _require(isinstance(annotations, list), label + " annotations are not a list")
    _require(len(rows) == len(annotations), label + " annotation count mismatch")
    for ordinal, (row, annotation) in enumerate(zip(rows, annotations)):
        _require(isinstance(annotation, dict), label + " annotation is not an object")
        _require(
            list(annotation) == mutable_header,
            label + " annotation fields differ at ordinal " + str(ordinal),
        )
        row.update(annotation)


def author(bundle_arg: str) -> tuple[Path, str]:
    bundle, manifest, inputs = _verify_bundle(bundle_arg)
    projection = _decode_projection()

    reading = _read_csv(inputs["input/reading-input.csv"], READING_HEADER, "reading-input.csv")
    assets = _read_csv(inputs["input/asset-input.csv"], ASSET_HEADER, "asset-input.csv")
    _merge_annotations(reading, projection["reading"], READING_HEADER[11:], "reading")
    _merge_annotations(assets, projection["assets"], ASSET_HEADER[11:], "asset")

    output = {
        "allowed_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "asset_updates": assets,
        "bundle_sha256": manifest["content_set_sha256"],
        "candidate_proposals": projection["candidates"],
        "prohibited_input_nonuse": True,
        "prompt_sha256": manifest["prompt_sha256"],
        "reading_updates": reading,
        "route_proposals": projection["routes"],
        "schema_sha256": manifest["schema_sha256"],
        "uncertainties": projection["uncertainties"],
        "worker_id": manifest["worker_id"],
    }
    rendered = (json.dumps(output, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output_sha256 = _sha256(rendered)
    _require(
        output_sha256 == EXPECTED_OUTPUT_SHA256,
        "reconstructed output differs from the accepted canonical review",
    )

    output_dir = bundle / "output"
    output_dir.mkdir(exist_ok=True)
    _require(_inside_bundle(bundle, output_dir), "output directory escapes bundle")
    output_path = output_dir / "output.json"
    _require(not output_path.is_symlink(), "output/output.json must not be a symlink")
    output_path.write_bytes(rendered)
    return output_path, output_sha256


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Author the accepted deterministic ch08-main Stage 12 review."
    )
    parser.add_argument("bundle", help="path to the sealed ch08-main worker bundle")
    args = parser.parse_args(argv)
    try:
        output_path, output_sha256 = author(args.bundle)
    except (AuthoringError, OSError, ValueError, json.JSONDecodeError, EOFError) as exc:
        print("author_ch08_everyday_main_review.py: " + str(exc), file=sys.stderr)
        return 2
    print(str(output_path) + " sha256=" + output_sha256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

