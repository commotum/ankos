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
EXPECTED_PROJECTION_SHA256 = "7879b9160476bbe4b9955df10b7a910202e36788e1a14b6be6a5215d2b107b35"
EXPECTED_OUTPUT_SHA256 = "242f2e6f3ff31cd46ca5670b60e3abf9becdc990417b182061ca118f19b21a0b"

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
    "LRx4!F+o`-Q(2RtNGk(A;ot3G08;P&`al2w|G)qL`bZ!MfIt8k01yCRqg!6}_kr?PZ4Qp(Q)W$KseSI^sFJFPklt=mP^h7{1x+yP"
    "ASGJ>!1unZz`oyidv~6kUu|(zb249MuYd<QiU2)St&h9`*RQw-&}K8>>A3(TG`m<lkc{g&NLKIz)YIOtygR43*Jd*}u=ekG_nq6`"
    "_nqz6b#~X4R4S;Tg(49U`91dUd(F>9LwhyJZ8fbmPptc+PTOfjN`>4$jy%1wQ|YdatSTd>mUh=It(7SD)qLszbO2nX?&K#Ryy`1;"
    "D)t@5`!Id&&{z%h>WU=_kr;>(rG0mLcLc>MOYa69>`j6qsHI^QioWx?bjdGm_uo%?lrOcjHa6514_jfVR0V5W7_OGGLrREINd;Xr"
    "RW5RBJ?3-`3W|c7-+HKZpmV)W9-j14zS@#6rmps%d#>4xWW2h#VJUmL?^10-j`rv&MLuRLSt3+L?S0+o*xdMH5Xk~G5R(LHN2v6A"
    "iIXXTpaB?w3`T<p5QHR61Wh9*)M!Dq0gz}J3_*ZEVIxu`MLkWmQ_(!pO&+60)B{Zb21k+_Gt~eAr>G?LN=lxT$}(u$ho~@yo}dAM"
    "Mwtd_01Y$)K?+2T6HQE-Mv0nCrcG1IdXFjU9+1(a)Otaa)Ea1H0EHqDO;r4eh@Ofm`k$#!(@J@ipQ?I;5PFBG0imD(J$WEP2b1LZ"
    "J`3?rPk(-&-X9ss{*Uduw{*R6<$Z2n=dbh!eW=DXp4fmSS+}S-h!h2%H6X|FPKoD98JAqV`QO5D-eq8^GC?`SY~7z9Un`<}40PxH"
    "AL;S_j~T{u%MD0HFhEQsHq5B<?RA%TH5+8gRC)d}qf8Rld~s@)VW^U|>Ug%B8Gw=)sVQaxqfiGJeRS)45D6)?m`wm0BkAD593M`F"
    "oiU$gCm#FI)z{&20NQ}JmS;Bd@&@=N#mwv6Uhp!3^QYpW%!Inrif|9tGU|#QtO^xH9dUZ~11k9&^XRciP9be1^~Etl>W5bY$JH-d"
    "->G6V5}`{~0aE`?N|iM?m0mxb`1L;WckYl9!%N-F@3%9H-s@cO<#a&gmw?|J`OqGSBf<yttE49Pbpd*~j@#?5wSYe5(?CD(eAe1Y"
    "VnD+;eLHV!?~A%$fE^rMBsBcBfH$=)cW2_4AV@<5bjR63Lp4()J*e-eSsl!Ns6K+V#vkk7T&F>VT4AD4(?4ZmgEWEv<wSltHVGQL"
    "2!12@-+*<DAs7t7fXazz8Mk0HwDmjVI_NC?CSK?s?)SIuy6ksFkB?<fUA7l-=8U3BR+rNjty2!X_~U9(pTjpK2(L#EPGhe4U6F4&"
    "xZQy;bPv@&2V8HlfjCRrOb9t3Hq5}08rjvD2S2Y<9{R}ZnCh-FA0TQVQ2hTE`@V<(7q!XzNzI28(x%U{8P9uw1=a8$b~d%YUU9_f"
    "a1=OSHWT(=r>1rjeI9E5J%H8~gFdC!TULM%gdhzf{bL)!+8J^t+4i>y6j8MZyjTeo0}dvB7r?w@gJa^(Ez~i_P@cD1dNd%r*G&N="
    "oUF0cwMV>%waD<mis8Yb&ue}8%)_xBuj#(`to~I6I{`=uWTKX>X7TKH0|eP%A)%7va)xf#^yaybhB34O&vkkWa_sgM0%p}9MqCO)"
    ")x-`hc9HeKj<?69xo>VVt?gNb7)k5bsK7u+PZ0p9qKay%G<@W1-5&nY%a|0!K`%?m1WmnySYoZBLi@}}`X7Bp4Rfy;bUGadbH2+k"
    "TVt|-_1p1yTzAgL<9ZY4T-|T8il;6R^|0wChpr9|NQ4J-<o+L$ZjT?HZl-l0KJqLD8<qfK1Q`IwISthetKpr-hmMwnFQIxzLIrjE"
    "iJ_B5)B+vJV0|0sI|y0r833D$I{-l@;f82)TSc@(u9pv_q651KOAPbXwTmFOfxBuZBRjV4Aey?hYeBH~nTTriZ7)xL{VUco-h69H"
    "9(;21_VL%WMO9TvAd(3!M|VfG4I}6%hv+W*`5h}p+x}O)1G|BMO7#-7b3A$!K_r-=?qUSoe!P6Eo_l2WbIJe$GZ;w_!-rld20l+&"
    "$kMKKXV6_f=T?)aL`x_*@OU_(a@I2A3(DHEg-F7bbI8X3JeYSJ01sDCy<p?6>c^xo27w|(w4tBT9faExzflXe@icvLnp)B|HUn7+"
    "`m+x_ZMi^6hNLBFrR}}i^YlAwe621F9T*P9s7sAMzjspD^s+Eg0$^(@R}l}xS_4YIjvq*L{TG0pv5^9XkoQ_Ex2nk^JTe>H2ts;j"
    "AF93l+A1|FSP=FVwIPS$qbwtpBu}Gi7Q9ZjLtyzYuIFiOW<)K3QH_|f^QC)d(WD^`*WFc+0pb9lpU1+bXCvxgL9(SX(??-$oNVwH"
    "i57I&-HeUc^~^v75^^!sxulXd#n_U^B@eK=)}8yEPxLKA9x+e|;phUubxaUW%s>crzYDc%x21G&0VFn;hjt+4I66mI?FUtvWQqiZ"
    "&W$H0M-YIw?`si5qEpEg0)!$RL_nuKd#uCmGJau4zX|JmpH_Zy<vO{IS)ika7~slSRBAHPTP<P&!z{wnn9hVe@#jjpBd;%x+T!xp"
    "a41SXZJYMdo+_dqbjA>OOpx;W@nhdUZ6N-h_0gm5`RH+oF5p0jWb*xt@K!ZTpa>-G=Y)Y7pr1|Ko~It-t%gWQLX`mtO|3EUBtB4N"
    "9{%>nKE#RxzMGzr0TLm3+(;Vs191yRuJO3RLh9+zzYfaDhQ|2EknL?J#94Qk2b6gLzsm!ZA4l8>OQ!{R7mPozq0@4fEr9LIhtfB6"
    "+B)xKNoatPV6KwMLzSvaqd<Sh&qWYEbKq7QKmp&+IbbWO7Da(^`qvlFX0<Eo2e{xS4R(Dr38l)baJI6?d0>&hpcwaff(ZayuO_{0"
    "^C!-zP^Gz{W{|FJ;EQ{lSHpYZ478<hlZ@WHIBfJjzz|8k5X!&=5_I-)wOw3aGZ#QXW&YS8b^wA;AO>CWd1_+0(wY6!c<;Luei^M{"
    "M((=DAuJaN0#X1dg@O|gq0y;_aa9o;21peEd8C0h3DesQR*Mss3}-I^YU~5IM9t$8qMH<>es7(?1d&iSrzCNS`5@PM>U>eF=LD{5"
    "^0Xi3Ku`rV74JgPduMiO?-tWqk*_VUV#7oNB>;jPVIlk1q)&daXRqB}U^V!kdM=xJ+>gYd@8ggNB-@R}o&gSzWHHiI%hN`e#hEbb"
    "IVe=NP*2=-ih{9dcSGrWwjl>u(a<M5`x!n`f_w;k==p7XzD*B)eXHEs=1kQ!wLT&Tb@;xZir4XCJs_z<Lzn}j>%lJ9$6C(s&ssKT"
    "ALbeyGvtDsG8<OcJ}o`uGrxWvpavM*i^THh9XQZoHSprxcPX%jTU_KgBJS?YVZ#8crx630U0%1XThw0|6|!VvUPuXM*+aE~oJGW9"
    "T3#&=5h^BTL`=k{oSB)F<%p3mA;iQ;LQ{n;%()Q}D*<YxgAwMtTFom!=zF{6W6GeHW^BL`FD&Nl;v0}K(1v{CTE;{GK_?*)lIjR?"
    "vhAc?G<MDHY5;L}8oiGl5GSCJBdZNU1iJ^maCuZ#)*M!6XBOhM5s14!=u@@w-)1dIZGCl|j8(M(pC~#ypj{FKif04S9lYzU>=9q4"
    "^oF1~@0s#9Hue+<nFRsKvWpN@tjrOJGR~xBUGL?VbK9JaatN=p$mqxejMqDUx?Ut#(h>=YVt7svmA{Kt?lGd7i5RmGgn@hZ8E5qV"
    "AIRigYYP3T_`?&_o6ppIWM+r2iKynJLP7upki-Ze{Fi~vLzIuyKdKSrMRw3srhinnwMErah+WmLRqdo&BJbvXQ6oX>eY-YxNo*UP"
    "dmv0IOZ8T?i=@ah5chuJVYQa7sD7FQTVxVRzz{x=B1~8zh$DlQ&Kmy80(I_;8bDGv2-3M{M!`XHv?>mgZBgG_ymV-2C~7Ru=&nuZ"
    "-lhmiBb-<}bZ;|iS5X$oZ#0a)i&6%fB|-cnl_Kc-gjbCKoc#3-K%Iw;B?~Q8^=A*xiS2MT01`rrXyQaEMD$wq-x0Qq>t3buyxCeY"
    "04xp~!?G5#HnjPkdW!S(84jyiP$OQtfgLnB>o@}r;~7MZ{BL8?c})7hWH$4*PyzucZjQTU@i`H`TPXpv3-M>RiDnmHnFFFuUOwH7"
    "LAv+J&V@wu9;|Q}mVYiDp!9C#9KELP;-k}f)th-2j#-z}pdXMpIwG*!f<Ds)Eh2s6*0aO`?uUerfLwBcL!gsQ_7%Y99wp0A8i){K"
    "&nmk=NAKTv=fj=yUp1RTryvLpLXR_7-nx2l*)tH>5D`HHlF!OpPisIV5@2Rqq?84?NI=wP07#Lsi57|g4~34L{v>g|MqI+eQS_~I"
    "-#nRyx$)xksCU*lk_5)<CxH+KZDNE*(E3N`E;fQ3kUKM=5SV>76Nm&uUh|QwYv)sI<-4zVWAR5IXGrc}QS;v@5t`?xKrf$M&urcb"
    "dcQmf-(Ng?R{c!X6;#9(MH~mQX0~D4`P^HbmE3b&y^7NxJ64^nTteC=k--552*5pVY!^nW%mNWQeu31R)Ts5{06`|eB<GSaLHpC6"
    "sDELp^>=6*OeDa49e|OrJqSRY^cI#Z75V+DvXzf>;)UNTBwb$4fJUO<-*MKdXfP6ecQ?Cw4qK1B<vOp8%ZKS10=#$HuXF9P2cCye"
    "K<m(cdh|Q!IH%_>NWc*UpUA9a3;`g7aWjDiheJ?+T9Pm7b>L&P7O*^#Yu(L)v_Eds)dENc+U3;rvkjAtkWc~B$HqNy0!rcyALnz}"
    "8TnxD{uCV3=N+ZvHyKYh?#>bnxn?wuR=TZp_(OFPHkM|6y7l0AxfPb7!1B5kz=gK8;<}E;?$02d<u$s~ylx$B0NSY91!w2e2Vlr5"
    "Z;_qvtI1w`W!N>9z0(EFV;m9&p6w84z{fbr*S4K4t^S&49j&yftsc7Fna@SSym!917iT?ibyQ&^adqMyC(_@%)i+dB^1S-8V=wX5"
    "N5Szx{OZE0)@4FyA@ZB=Y<q>VQKSHuKB5+y5`$G-`2wp#!158H5|?}f@;5M=n@We1lejwR>ytk+uR~8E3f9m8<@K#V%m4{#c{q+E"
    "*S=pZU&$Q&ci??Ka1QT}r+sg2op-`S&4vI5;D7}Vf~0jqnQLxzq8G9oIfaORe%)jZK?2#e*~!2`4LhI!cucKi>x3huS@~|84ZHEN"
    "kPnXH0WZK!uORe6U5{Joc!r1&E;iqbW1Gor(3O47_6-hA_xF~%6AO?r347Pq9K^3i8FLb|Y+@+qH<it7KLmgzj!bno48DVgY-RPq"
    "K`iUi@3~rbr6;anm=$Gr;}r~0?Jeh(NN{tYU^>0K-A@4Hv(B%Rpdo5IKvLjxi6rg0g(+6xSDof701`!771qrl05pjqK*wQULoigJ"
    "t^lK6IOsob?YTpqxd40era%OfK}Cyw(Q)p1Ur)&ZsJ(pC=hMkd*X_23FN>Fg5FA(G_w)kY7~3OYINKUn@;hS5;t{snjuEfWJ|j){"
    ";^Ci8{6Z1g4pq^C9dDZt1aA7Mk86iK>FS2%+nvmS8HdH>ii27ie|qT)$zqpnEwp4^PEv*r&z|0Ox1H9_pu1RfricxCAC6~`pY7oR"
    "4}eq#yY<@d!7g^|+x2ZX@6fpJe@6WCe#6=62}S^w1HY^USI@4wHBjM`jam<Q<le#T83yK?DEMn{qYBDy=!S$lClnid3fYvPH7H;p"
    "hh`lgu9kE)A1<?C%I)_K#Mlu&nDU0ox&5b|BbT{W3&SKl2z&?@`SeS-wXQ(wh6XX5!L|B}dABSweL17mo1tFjggKBo&<-qze9g0B"
    "JzgJVqwISKEm}i4OQXYvLK;XtbY~d2taEJRzmbo>$ohD1Xlvi}O{MNE%=Z9(77}b^TwYC8&4AGK<C6alI$O_gVTFKxNR3zm0R;Z`"
    "fPwu-@dyL_ztqlC*n$s!{(Jck>LL=0TiWgGjKrp0i~Xeu)r-2xnbhQ8$(?IitGlYu+TOD;Ro&`HkdT641dvH1WNeHhWMLRa$k5CP"
    "3ku=2XLfKPBuwb&pq2oFl9Zbm254P`Eta<!EZNXYFsmt8(pF89whOXwjhx;ffWd)T186J?#fm3D1z-n21z-oMrcJ>zl12d9Ityg%"
    "YX&cG$$h7<$2+{+-J0_*`ETdut6^$OZ9g24{GH(^^D1H{gG~%fvXLoFLs2qpn9-S{u@SN|wj~9YRsHMxOhXV`HYo@9l~D~L^wzb?"
    "B@mA5uIsUWa4)B+<1q=Sd}k^hAmMo43&FtgEQlHaObnt*fIx%-aQd<5KHi=EeZ9SXs;a80s;a80s;a80s;a80s;a80s;a80s;a80"
    "s;a80s;a80s;a80s;a80s;aB?fKT=SOMp&9Um1$dF`Pu&R)Vbb)p*4;Oy3h#RaI40RaI40RaI40RaI40RaI40RaI40RaI40RaI40"
    "RaI40RaI3}Gcz+YRaNf*07>cqJ-vAb0#JPgL}U$s>nabR{bGV@N`9wbQB4YUcT^qzEj{k$uu6Cq=#;z?Nj&!)@H}|&7PwvqhIqp>"
    "+A(}U@pp%a+`5M4-sf6}b6KaoTvqCCmTCm8>mK*54QlO&UGbaOUUqBbe25ANh(10(PqPtJ1n-IhKW=3ej*XNwRU~g$liq863ifUN"
    "ze|kzU2=lCTn*h_HnPa1GI9$rFpC)Kp}-H*-{a@+@x-g|`75-p?=K=fYg$UGqe?ZZNljh*Z!cL@R;%7^YOCJ$YMH5-oMRHq)XJuD"
    "ifl~Hrd_I*1yw_0@n=s0pWHzs*WcsY#2-cR2=@D%2q2QTSf74yT+g@+2QjH=-m$6-wgaRa-8CRns6I&n4*j}!UHrpaw|rw5w~3bX"
    "OOiJF_3YfMJ9+O3C&N3Sd!`+Sa7b|IO~+CI06Yqa{e?tuR7dzCpNOcBsr9+IzLxL0`fDlo%ilg%o+>wFP=zm$9cAylq_vpAtTm&@"
    "yV8ngsvp%<_mBh;fI#e!Lc|eZyNx&T>Bv^~?$6%vF8;L%S5|m@o)f3C=a7DHurmzt>8=l*Y3zU=U!>J!pnjnWX$cjOkTfc-^ZETg"
    "e_yZD@B99}s;a80s;a80s~{8Hf(MXCRJylkVuz*2sUnh_r`9${*2D6XEX?Qw+2;U%FkjFYgJ+mCzAq@AW3av0h%nGi6$v7rkN^)T"
    "rnIV~APdj4`L%<Yn0L)=;X;q9Dd-o6nQQh*lkL!TC~?Ka<c%e5Lvv&PD1v__1s8x{Z~z}lf-(p|Ke<P^h%e|1kf@H0KhFa};>Z$~"
    "y?|kNDM#_%2BRitP;nap>;uvv&;l$dZ8kjM^<5Y;BDynhY6^Mf05!(kEY5VJMu}-2N-ae-M53WeWjRYVHip-CMb$FLMpG4yX`rFF"
    "K+M9>)yNbL(%dN!(j;)Ady01#unyi1M8Qsmz*NNuO$w{eJsS=+AZu8r$P%M^L^ZCFIR)uZ<m-{^GghpC$jDBFITaDX-xy@>D<C-G"
    "6zD)nQymI&smKn%8x92>sBkHOJw?&NhJbzmbg94{Ra9_O$fkgLRS69p<j8fHr-{oX-0clL|0}KUS<OKd6C-+go-<7&tihp)XrR)B"
    "&VW>b2O45xPQs`h_v#uAnA`wxf@1eBraN)2g$0!$Ui;I~ilRq>Q5h4Wz(^5FJ{4EOs_>#fFe0m<7!&Ja0J;zkRa0aDdmdZq;Hec="
    "-HKMl)P*u8But5!5~NLvnzv{}ySf!Zs;<S@yBAi4*t-`(s8v-8p;L4wCZWWMkvCUj>|Ip~p;c8%g;=?(c7!o?Ga_bYM9j>InxOIE"
    "@-ikEqUI(HC<zTP^oVK`mzh}!pb8SL(19tsg^VCEP7$b!)|)jVOcoGD0+B$4X{14^#9PUlOl3^zl#^*JL5yjPw<6L_A&Db%LXne7"
    "MBOni7*Pe&1W5|T)RiMzdaTNtz@6J{Y8n=Ch^8ze!(lkU%~S}`V7XvAsEstJOG0%s6AGpQ)r*055Ojc&mN`op5|p<ry;GMF1}ZeP"
    "E)3IH01!h7U{vyLML$FnUztk3aaOu&+x!5Y0Fbzxo!56=-E)b^;GB|oRtiNCl{5%zG=?r%iy;CCRAOQ_8DbTJ3^Jf-WkA$mNTew!"
    "qLLB-5UUE()Yh$QHB(naMDijcA|fIpA}2&dL_|bHL_|bHQX@*xil$CMW;qlVV@75?r*`C8A|fIvxvpH?q9P(Io0L&=aw4LOnz<21"
    ">A4X_JFZcucH~pLa?b6@h_PJUr*`B;JGUZ@({jbl$f78tblixDqg!jrG-8dY#-fcz!BJyH8j3V%D6|&5w=L&)cXCM*#jbA1x!A7m"
    "2^MRbG-%PJ)LnB}+^urC)2>B}2W`tcJCYSB3fW*ZjID_q3XGsw(yUyy((ZQT8l5LqMRQ!~Ml>60jR8g|izv2QOG4X5<z3y|hh!@o"
    "n|B>tpoO3`j44%-SPg|n$TcO66$Z!+OBys9)oqlewJaGfYnOLTmR#pEwXs{S?PH4ppvgwC7DfV~HJ~=5C=%u>(v_KtP$mXVE&-C}"
    "Q9F_|Tb9P=Nlxpza;FKl+jsx~0000018ug}n%i3Wn^(ttMEKDA(>r=Gbe+A!)euL^<?um#e&_l8*U<gb5ew)oO?L`*CZ;j&D^alN"
    "YIg1^!g!)B-NtWqnz1^C3St}0*5g@BL~COlUC6pqwGe{LPg8kz_nM1SxTc!bZuhsXtjZM&V>1-y?X_!lnND+etz}JXA>`gI-jv0}"
    "jk}!~yiV{<&i56ts5ZBfBQ99ptnW`j&N+d+%8TCYVAQG;cN@5Ry2!cP7NOMK?j}-g&Y~q)g+ppLt>gz;S1RQ#B=tFZtg%-cRSI`I"
    "iW$3$)7q`zi>*%P+$e~#x~*kiMx6(y^*O85$kw7>J!+sFCkQ|bBuOU-7!CjqxweJ7kPR*`Bf#(n3&L;#{D3>1CTcQjs62YL%+`j$"
    "1NQy@!2lQTL8gLm5QQyEnB{2OV{Iz5s|BuMjyIQr^c(ALKvEW71cE4_k_iD7OEK~(%c0}){J&^{_k^N=91TH;u#%ubDv0V>s2Yig"
    "LB~R(G~$362Bkp6kOxj+EeM24fD?gV{3@=M22>bSR5TKRZU}`{#em5`GjNfLtFReWauM8s=@i!Vs<>tV?oe@oZAL1r8$dA~$rOYD"
    "=y69t4jZ-#B*3@^E(#9i8a1V)Fb6R(15%5)0Tkb>tI{Tt$Y5xTZH<d6C~W`+6%pKuU@W2wn{Z9Qp@fPN3Lxb~Kn?*4D3POJDrgn~"
    "6_p24n}#Yxag_rC3IK3n71)LthM;08RWwR~y2}7mOAJudin@SM{tBFmLrN5(K`kW-AW~2RDqnCMM+pjKOhqy_n37eRu!^M7V``Lu"
    "3~5np(WI!0RTU)04VxOKh7hERLX{uX00vQ^AG`z5W@cgceb0-b{`d9Y<#xl<jRpOU*8V-s+tc@7{;<G%ze#$a-vbw~(tmuDV#X2I"
    "@wjvE2p9+%ADdqL<lK!+=j&--jE;dXw`&N70lZ`C-@$9<-hQQ>9BN!_2DC*7X<AFCOvoeoyaqdN*P;Uw!ZZYePT4WDei(@@k4Vmn"
    "#{1Kepk^iyqiR$Pes}A$Ym%;9-IK^^p1K1gXJ<nc$p`>~xrd*(`v$=k=?)xxa_QG&cosf%KTaPGoco#%E-uyaE(YFU3t&mnj3dxt"
    "&c7f$UR54DcGmX^Z^qjg0S)uK30LW~V|#}RZu=<tfCvO1{DA(Lq8I}Th~yyP3@D^lYO<}>ZrfGWWnU8%MmC73qQ-+zQHvPW1yf5@"
    "D7pcZSCo)slq4l0RF<SkVM$?SWJzF22?A13kd+`LNC+ZQks*{MB?t&sSs7VShD3%I7#RV8b^|Kt1{D#2WD@{nM1XJx0l^d?7*JdR"
    "lpF!ts^9~FGOmDO1TY2x1_6~w22~gb00c|{fM8buVGs~96>tVbU>N~M0g-oAmfF@;owib<BE|}2Gf_sPLRBUr)d6=h5Cj1vfg>tP"
    "rU1&M0|LM>fWR^X0LZ40VNgJTWm5oT6@X+$0iT8L^!ytz{C_hph=O$mP&;}AdGoEl&<A%VAOa((z;lk{(F+nS+<-v&4EjBOtblsy"
    "TsMKnlr`7!I9|}a+?~M{@@Fdaj7NX~d&YB|l{6s)EDR)tWMROVVgSG<2$y@L-tgEJ3_u8f0Lfa1XJp6|PY^CrwOpfwT|PIgV0>sZ"
    "Ku6>p<ZL<q2DEdWd-+$_<aqssL~mUHZ%W<Ie;^nus4)2M_z?E+bFt`<I%$3`NJxCN8uce2V8zkqXp%%QS_sqjVo~VWEC6z-06VsA"
    "+;`lPU#f|?=GGbMtDrsvq1u43BWP>n&2|?qH$jLPoFz1QFMu)6X^=phf&~yL2CkvQ3k|{=1{;SK865))ggF|79AJFI4ufN?-B~Ho"
    "u~zuoH5p_iQw=QC@pmTNYTjG@=vS2Kx%ThZZEapXcOZ0+Q=Q&xH4V0}p5k|bjIjRKF)^%|jn0K*$Hys|(VOp28rudGTaQ@#aeN`J"
    "<6)MYV~KaW52SnV4nAl~(z;#{bUh=@_Px=^ZTs5F_QRzM4(6sY4cr74piC|9#<J;4Y^#6I+)gU4b^1<zeZb^INR&DEh*DmkUQ8~p"
    "QUu&YML2<4j%+agqqHP7gHyMV9EC|^x|&_OmE1*KFK)+ZI;4V_c=_DI8{c!~bUHy!qGm@ctLs%79c~~^GP|}O?i%+IT&uW_kkFy&"
    "YW02fX&ClzL<9tqmf`dsAUgJK6Y8g<M00rA7eeap_it-k)miR<R6|aX{#BnCXdQIy&+bgR+)54tLWxy+y`z}qialJ$zIbK)bA>*!"
    "dCoHf^OtqI65crL0LY?-m(`GJ=U7mYHnBAi7UqDbaAs%e2bel^$BU%y0Q<=52A6X|k-xSEuBFSVa(zHEOml3kgfM`dkjNrZ4*yoA"
    "(OCq6URjmYqUfzyG7OR|oJ($u0FTp08mOmn(8kf@#ov+OfIn3JTpPQ$bqd@4KAxm}`%cl6r&5yJx_HgZ;gLBhEaiz>!J3*zak|wc"
    "t4W(oiI|m9d!m)Z%b37dh=7Fjn8kysfYYQaQ>&|;+piFT4#no@Y33Z77@}o4Su9(w|B;K<^dx6h5|-#fxoeeDjN^4UmcMt;Vh3V="
    "A%OL7<Q~uJ(0aTx{qY{k6`s)I?QCI1SS(rYEa^FPt!EOVQ@xzvJ}`a-|41N#?(U=A_IZcEZy~Yvg6VQe0D=U4{4Ilr2o3q^%;F>C"
    "fMkma2H;%wCjf~PGcz+)LMp1N)m2x!W1a2b*i);St!A$2Cg)cUFkD?_YATy<Q#GBU_?)1SMhuuRSiwL<O+{uvAAq8SL5hMQ*K~;t"
    "T2v7a?p)``9y|OV59GJhRAX(5#iH6QSg~TkXwhtH#=%B5HX~87Mzn2>qS0eiV`FSZXfdjdqKg`e#f=misI+K}Sky(fHpZi9v9>mf"
    "HDh9;i(u6nji{oFY;B8T*tRx}QE1vDS}LNkipH!_RBADbv9>nf<G!z6DApr)l_tq#*@+S)DJU3(i4OrLU@e6v$yqHWNogx3iYTI!"
    "1hf29TLQ!cu}c9)#Vi#9#i|kmN~7R8qbn55R8KV^25Fo!1qG7xVVF6s=2o>rO6yfvX&Dn*s>47*vQ6x&&1NRnM{Iu)Q5`M`rsB{r"
    "kkLpFp<)U&doTrs9+chzL|_yJ1L)x#k|crr<P4RZ=Q+-EoQkTds;bU!n5T-B^&}M3&Rk_(-%K|5t~|$}*jmiqXkdDE5dtPuMcJ&^"
    "l@~y`0e}unywBA52larD{eU8erg9H#4q`FTWbL(q<iLhfl%xs=1K`69&^lj`F86CfqCU5+f`6C?vh;Jp8Yh5aa03LvA`Et}fY8*y"
    "8eIdV*{n^EdotjG%@0;O)v+YxwZhyHqdx-!k{(Fom5dFPO|rvmBLhT|PPhes%q|KUDYjYeI{WZydWZwLu>-jn$ON*@RaboHJwPV-"
    "#!}8=*5^6bRTp#9aaA+Y>j(e<V3I)xm>#X&kVt$~>rQ6%98`h}q~dbwbC@TkFv&pVPg>q*`j2M=&bR^hRbQdU5%d86?faM9`InIT"
    "Xy}w*F5Ed-1wR9LIwDPmog#Cg3=kd;xlU|%t4spD1QQ_dOks%H22$<3*@p05o;X3@M$UNwLRp|lbPY)qB|)G}P>G<7x&((pb`i8q"
    "9dT-`tc*+?jS=ViJaadEbEG<Q^wrs}2yidS>?{E9d+$?KRhh(7)Kyk1JZm?app{dqbf9v>y+qC|aY5ZZDb#N?66Et&PkM2803JY1"
    "zR#oS51=FPkDovwgYo%tVyAQA<a!{sF3lzg%s65=62jqvm?HtT!09o~2{7^)5vMdUGonHvfH*kxZ;-4a_c-j9xAI0X5O6w7OY;$C"
    "xB;k~3=XH9068E`%*@Vd^Ho(>s;uSJ#0tE;D?8pI_jLJ&r0<o;-bm!yh+MWOTAS2V+ow{g)l@^iM)!3)S*0;mH4bgy0T4Rwy#N=m"
    "0t?^7Bq889;A|@q(XqhYMhJO0)l3=_MzASJU`#V1s*g+>#eg&^q9P=Z!hj`mF2g~l+YGWScsl#Ys{}7!BT?>tt0M^PXb2xvsnu@x"
    "-vX@-YBjB9w^hq@vmjRRTwG<=JIRF{5n7qKrvd_54n~|%n1u)=q1PVMrqfogAb|u3CJ0RvnD}wW+4{b?apjOb#`O0b$}l(|0et!z"
    "c-R~^t&OsU?PZjgNK~wXqS~%GgD`HxGj$^Cd&2;sE68D?g@OQ3j!CfWI{399J2We_5WtA!@_P>E_un&G*R5SWYIR!Hx52y3JJX4G"
    "E~4V&f+8YftDK3LnVEqNCku|Eogon7CL$^-o4T8j>BEsTD3h^biK1wMHOOgy`SbwRzJO`5RfF;IiSszb;IP9oB0;JjZEHcTVy;}w"
    ">2;cGtpqi7U}~b0(iJK+1hVF832hG33@CdM2axRP(=(?{by~zpz`z&)V2lo(W_7Bns+F5PRaL61H_mZ>ZniNzoSdwSN*P|y9OHM&"
    ">f$yx6rx-@#BMlcuB(Q$kwD|9v#2#EK<$CPotU!#bj2&n0NTPQhD;*sjV*;-I<o>Z1lF-LD)Gj&WYH5IL%>1@Lnilz97OGV@a{!`"
    "7cc<0;2jm`8cfY?PPMI0wVK~KV>Oev&Q`B8SE|&-OvB5`iLK4z+|50%W5CmFH0@MMK<YFuHVGhtliWOdH<gKyiIp@&_%1COia7va"
    "p-Tx>wX~=vvm`27&j$6Vq>vbt3qJ&kBfE7G<zgWU1F&q_0{qOz+tpPFnVE^1ntZ6u^NP*zrQPi~#M;kk50;CH-y$1O@<RzrdRHy6"
    "5ir_>;@n)s49v{IAP#hEqn|+D3d<Z)C8Z+u=3xwRt-&)KA(@Kfa=O)BY7<$D>A`T|foM3WO%Q4|W0-M;MYa~`(b@LB??1R-9Fh_N"
    "Aiq!C-=DAE;QM>`dcEHkwuaPz-;-;5S?~GA+1lS;+VuSUciUXD$Lik?-tpT5_iu;2&GDI=&yDN4pK$z7`lO_ZT0#g&lGF4=0!ScF"
    ";Rqkf5cEPr?#Vq6JLCZ93?7f{LrR1F>Hd@y&;q8+5e<O<aEJljKtH`udZ?bLaCi}Q-2mk5zEOlvL_m)x`M?!F^Z^Y4!~Ds90986R"
    "0ZAYQB?S-;9l`FXNCNvHrqM=FBtTyWAcz>C>QO)7MI|~xO)tz<ToqtLzz&sDVE2hgRbTQEf)ElGfIw4~LBx~}!k$3@&>$Qu1OW*9"
    "d#ZXOf0Yn~HK9n-CL&=9#4!N>s0MI^2>{O~42U}g*`Q6}3YdaKO#=}If6jo28bk&E$q+t>DfLi3-WUG^>H`vhdkFuiTq**VieSJL"
    "d!PXOBA6luB9I^fq*I`W!6D>RNCpq>MfxJ1L_I|z2sk(uJc4?Ua0KL4>WlugI75*E=u^O_(E!k>kJMC0=smz62Pg&#d?=x@e&k{x"
    "BxmF#_7F&PU=AySK>WZ%=BPhV0LY-KT73*e4X*$Ya-b(9pm$W#n;R4Z&;qBRBcv3;SIVIJpdO?uBk+2Pc0@TLPMw4Z7DJRk`;{;R"
    "7n5o!_zAE*6j1j))jEp3l=&ze2q%SkeUS11slp&H&{YT6>K#yr<|&8?*b@;9HiDdrLHmt>!k+9PoTuQ81mK{DNNjX~bf{@iVG!g5"
    "F(g2cQ`r<=MBqhJ@eoK=To4fCMU{pCL)<|j4wW{iagpw#M}Y|sKspdk1q3!GkQ6XLO$xqLO?-g-Tv0v|L0*)4AOPq=_z_h6QAPMR"
    "XaN(*f$R*R8c+<tUqY|U6z-~^pD_haQ9)mDL!uz)KxBCpC3yxmCdEh+R6+Lvcuv5lR8f6V2g)h2<qk#!Fi!x4D&VM(Kzs_m5d$7a"
    "-9-2hPRN7ZP83cALKRebPzh8pRp>xM6fs6Z5Dv-c2_+zqfv1!d?jjh9ZBUnhL){n9K{TR<)WuH#a4P!<2yluD`8^dw-AxPNC1hie"
    "fy6FUP}-*=oQS-hs)OJGPGLn7fPeHKaS-KR=m%j=RXI=&lukf>*ARtOh*g9-3<NL)!vJz51HcHU3ZdOzj1_!<Dro@dikK&GMFYUJ"
    "Ffb6H50!cd2!E_khuK9A1QYij5kX$a3hS~kcv0+&ARfw~zD=hDlMMt(2?9__Noq|rw56t+nX@dKX=yYmq)n4cHJTe+TCEC*!mH3h"
    "Bv%C=ABa-0tNti|)}pBJBB+ompRe-4Q_1u^p@b9o{x|&d`j74)-<2QGUOz4|^~Eo(mSj6)_y4a?%~7qzDF4yd_qrU+=K0q=yqd13"
    "&u{v?3w>&I=D^Kl_mi%6IRC)y-t_Iot>(Qo*!0ZKKfM1EAVefWpbJH>)%c<av_bRRl$Ii>vmBbLp@~01g**B0pM{=p#!qitd#Eh!"
    "W&Hog{NKg=Nq;ZwwZCWdeXOx+#qRSJUvVSyB!LG@=~~xGUf7&)<1hiya4TIkLwiChrdDLS-Bo4Ywif9~v3eK?)@Y4^gkZy%2FC0f"
    "2D|GuqdWE6IX>a{mV~Atk_sw;4UHHKYBntzu|~~p@z}LBHEE_R7Fh#AKvocCp-NJbh+0&jv}+Zq3tBR5s#&qC6==k0)tgjlv}{a@"
    "HLGPMq}WK!Otzb9U>Do`#vq1<Br22~#A$04+gYnh+i0XQnaZ-PsIUo!h$(SYF;Z7kkO}Vn08ipTDG&$pL;3_2KQvhyQkGA>R4`Ne"
    "MODzJ>VQHC@AE$VzA&)(HhoW_(9zsKQ@oKx#FP|}RFp)NtsycVgdrq6h)3=TB?}S&9@Digo*&s+t+w9Sc693EcuN6*c&yQKd#UIr"
    "fmiy(6XdDTJ=9SBfkW)7zf=`JoB=+dunYX+A^ZS(Dk1$yD1N9Rpit!i{s;g)!C_Gx0pLJ6R3GR?B}CGwkUQR00BSK66h?r-CecNr"
    "#tNb+#@B3v`YH^d4g$!EBnZd~rz#<cfz%QfpwKS>x&hD(Z9+|91Y)pa#Aw*4npF<sA^X63Iswoqcm)U)IshjEA>b4}6%(=uY#00l"
    "L&Bi+sE`jJGN7G-L%51^fCHpK*a&w8@+u>+9ynpB4N9ic+DUCTHi}q^RUSZmC>Sau3BmvjBA5W^2VlGc=~OfeC;{9S0qlYrMH~VC"
    "JL>>X^=kzZebgXIRhH9jBHCJruak@5ZQ~UOIgW+>WTBQ9_=1P}UCN0lYCEyre~2!_AK@MeG6P@AW<IuKSxAC^?xXL9%AqzVvG@?o"
    "6i^c_1s+Vm*z7pwS^|b7m?W5@WeBC|>Q7_)9wfp|Xb-IO#7KId_Q66j2caE?a0&AERSg0DB}xBp?&Jc3fFUI3lrpsk2<RdbhqX?G"
    "KP{cT+^uV9GQl}VC>jWm1#?b1Q4K1tY)H22Ms9bYgKwY%>L<XdzxI0|CY1-G`FSt_Mzx92MKod#GN_MmF#8A3_UbQKqEe~r{mqCU"
    "ywn2xqSr>~WfegRWSBun3MeK~?J34_xak7r;JScpP@9(KcXvAqg|_s_h|NHjX53WNFvJENAc!o94NS#^=nXNrDn})d8dxHM+boKU"
    "fB=ok)J@LhL<b}iQUcfxLt%lU3<6g4=$&tF-I7;4=D0dq=Vw=D)KJhsK_%2?n2}B0zy^UR(JV*=($xTHR_p*E01f~I;jlMO)#hYM"
    "<-Ow?AP^BmBtYznU@t%&!CxPk50jPXNAy$}0qxW_!Q1ZK6<}eAM)lvOX1o@JL=M-`Gb{)fHVBBTsj3|y7J=-5K(*_Be`lQU8}ZSa"
    ">?dGE2IJHeQUM<Lq1`AhP+E#WQ{X@8h=6$W%6z}Xn)?TccimKvvX{a7m&S@s?l4byb;c&+X7+40VXQwwJp!xq`9brw0AyZ*EA~}h"
    "h@Vi9Pe@c)l<Xgm2r6tngh6@f57Jg7fq*=Yvx4%L1|89#AC-Yr(vkIR0t1CZPT;Wjp$Ql?XtTGSe0T+Wck)(y{W&+i$-$u*%<1z)"
    "K>Qb51Qxry3qgZ&>&m@UGm2z>S4|HK(H|QDABQm-Lo)*cQjilPVdXz48Um1+1P^F-cjSPTe2#u$;6yMNr~)Af2cYE#p+8_Ea0sus"
    "g1_KTzf?`XAs$o=75EQCRQ(Q!Dt>>VHY$9kBt1u*pTRH!D8RGUeC18M$1IFc8IS;dfq3@vzY=^A_tX?>N2a~LWqu)_->pL{LkHjk"
    "yi^fCZ~}A8i-0fRtvdmO-|p}RjcgP#bW?FwOC_0uLe-y8_XMOy6goe{&X2A2>N>w=hP{v5ysx(f&o=G@Z3ZPgR%F$9cSAv?HJOMK"
    "2NObMX#*;OAOe3V9Y|)-AXE9usk@koR1{POC1AK*I%X9B3~bd31du`g#aT8;Khl6SIh<URH8tH43X?#=Y%f3&#6Te6f=d7}2dGtM"
    "NV))tIu%po)Eeyix&Rme;gW!^3JRcqrqMTt3Z4`NEF6{cLM+%_Oq5{BMUaK23IT2KbaJHvS=>g`*r(89fd*-U0b_SmK-p(-1Q{I)"
    "kc<){B}DU+*4^2zDS}9pSn3#k0ss<81Wth!w$8faPT;rU#8B1b&}Ta~W`5v}^O=uFI!$O*T*Cx|0TtR=X~eaoS*1|*(f}GXF}ws<"
    "e_&sAU4ne!`_JY&%~Ul(EQgRt<UIrgN5E?6B6s~%0{|qDC{s81I!9!i==~#r2+txSJVJYe;9XQ_ZlLT(Asmt@kW8R77)W#_HG!|?"
    "`v|8by1*Yx$HJz4@FXvy;)e{^`M^maEdzj|fdZreXwc)edhDVa1UpD^(aNw=O3ac#Ar2b-@vR^x&3p<cM5;Ie*;DidfE-S#!Ut^;"
    "Aqhgsu;4^I>$(SB0xSM#N>xmr02;tw0nk+k&}4E2yMSyqp!t<HFawe)=3NB3Rg|S7<Q79SNCs&sQ#F%QXsLi1i$_&F3W)dtvqYh#"
    "K+=L@or^v=E}2wO7XBO1Kg}MfivV(+W{0EOcoySQ+pyjsF5MUk(;~Q5IazC4D*!Z!yD|edPB0W@%*@QH1ggT4QzVi>L@AmhHLTV_"
    "nWRL}DvCmYuneMxJ0{i-ApUUu{lM`kRK*~nC_;~epa7m~Q0^N}%BNA@2qO5&@)k|2T0>fM9Oba~=i4hR#R)V(-3{?CiRYtq3ZffC"
    "yQZc9!kx>I89I(EJ0OA_oPp$2M?4RUUaF1(&<<Zv0W>L`^Lh{*@j*_F$OOO%zS|7~Ata}Rv)DZsZ=(W)1FOe@n%J5<9Xo3Tc~I&i"
    "P!Rx`o)rg<2-tBap;3?)uuWagH^?t@(kM=ukUT9x^spFMA$lcwilnIa08M<ML$WAH8W0E!h2~Mn1Can2)CwV<TsHx5sF<U`BCzTV"
    "XAnXZ_e42G>4!pUxB$t;PZpjkUL~}s0g490O+idRX;Twzf~mCRe3{4(I4iY54ZRACGZrJ8DM1ZDxCUZ+wY)He1g#~@y>+fzc1MfL"
    "B)o3%U=W(iN{Nb%5oTsZlqKydCdo~LD?||p#}MX#6C(j3(u)Lp`A*D|2O`Ih21r3jdU^qzWfVa)%X5Y=+8iL!EuURhQS*T^+!-oS"
    "ktRT9EblN|ajDZNR6$Kwn4A>EHHpLzH!IECs@r2F=W5%LM9IfoStjMnc-K)yE6Z;+X$+GZTBR6ExQTcxZpx_Akcz_-h8P-*D^crN"
    "xXGR38qtIyF=^*j-Q1VATI&ecHwo4nT^UnM7DI_oGPuP+G76L`%;xYw4NbEE$O<B0sEEyG_74!6m^g67DH_PLD8P;kv0X<ki3uV?"
    "9E*w>TV~`n(WoLTsdHB~$k;A`(CJZ37XUB>G%A6kM_Q`8a1wcPZtb}ywaualivke9!lMHWF&;er9P;wq^5r!!xf_%)BP7!XSsNh9"
    "H*A6m)@0&0Y9mut@JEnPfkOd9U_1cm7f7SZp!hr1gcW^|L-I~LxC|%@CGL6^U4mwr50=xIGDG|$$e#Rp?C3Q<x7idu0`#9G6(D*5"
    "Syfyd4n;evCr~PiK%vGG;NYw%0f&%K&Wr*9q%U^$85K8uxH{<Zv$6pIry?N<+8&qKK*2kTd6aWQt>FlQ?e=&MWjY{UjS2>NP*>Zz"
    "-Vl8q@J&=h+Yms4RtTfq$iuQYi2)*g6#yZj7@V>d4+sD<YBdET+~P<kC!x{$=wVGG?k<s6#{vLismqk&F_B1f8Xn~R(T8rmX1wPb"
    ";?3}xalH}f5D;ZSkW$7ECK_B5I^bjjkdT6QPaR*E!RhIt1ov-|BVRt@?`jyaW(AAYz;L8kD?5wB0aigYs({~=v9v=5aNjWRbUm}K"
    "Lj|>iQg>nBo#1@v69X#HQL@zJ{|SL^Z5<*BCN)M)fFP4=3A=(X1C$&s(HsI^gyo2Ht5TsW%8Fa*fWo@<?~v#K!b8$yA`C(7KWVQ!"
    "sDG3QB_MfVmO*O$KXSx}b|rFUfzX@v)_}`RBS^GDS?<6Di$nvlS?+OOn1E|3tfV=L@0zm)q;?;B0F%4)J?!G^o{S#Io(qA>=>ydi"
    "7??U*k_VR13Oi$b4S-ny6o5Fkw-G&c8JPkFhJY!Y?)sBe5^t*vD?!7RLZ!fJQ9WgY2s&U8N%_h5%Dhp0o!q0YAQ}ThL622b^h_(?"
    "p<_p8tQ_0WB$8!BtD!%yf)4Qffu#~d2VJl?zPbuzX%H9}T_`A&fIQcl*m@D2H2Ew8Z*C7F>&3@A;PmWrq@;O5*m%*(uz>ldDZL^i"
    "MKTM)&T_RIS3p<*Ag;`Z0uMEwXc1pIa>fn74|F0)#aiZp*pbVRo7yLUm4y+cFRer6z~TpJUtxe9N`ZlgFaZRX3;<FaZU|zcN69-f"
    "d|5NFweQ|61XN@_M{S}2UlOJ()&~Xq?BBmC`a{zC+pvqreERM{&rE@Y1qgru&e&<Mi0^5e*nbhg7VpwWyQ4vUC`1AQ_&K-?G3Nsl"
    "qq1B8EGJ(Z(RCg${T~mjJO+>sbie@AoQ{|S0D=y4>&pX4>)s8{u=>(ufLZ{gK-X~vWptOIivrOM0bx+F)EBQ&NCc<02^$3;oD5Pt"
    "j)V?C*5uq6GA9o6({01p6SpCf9hxlGo^UV|eFJ9^gOY_9dAeI3i137=u7V)G1s)+o!a!uSmAC-PfoUij0)mt%F#y7O0p$aGk=Y{T"
    "DOiLV6jG3;C~VrKiEUlVQYu8Y&2AlRI8>Y(R;f-vdI8b^yz^02an_AhW@S(V&pPo>FE!#RId$b%md_|`Lu@dF5?VyVVWNM1#^`%d"
    "8%L`Tz!6>@>@n>4z|>~B=vW?lFG+gGzSV<kE1FePlN~@6LeNCVm!41?){Fp0Lx7d^tsR|6-~eFjg3fTkhQPB@2ocy^Lc-%rLN7Z_"
    "y6<*530C6i>MHl|1iXtvRp$_cOa_u^rQAU4l?r`vxbIrks+c(e=yE)jlOnX`ClRDEFaa6_6a)amngvrpAu0~QRTu>XfMfuHWl-9n"
    "z&cb-04J0X;1>ZyV4yEbp(vrq57j{7K|V-B`@4bej+6T<&@1o;liv$~=^QG-`xPj6f)C9CUPVDpq9KR7t}_qf9fQ>RyAb73=%eFB"
    "{UwROo}vIgoEuO$U5{hAR15t|A;5g4P4|ZxFc#uETaAJd{fI%j4<;PS>!(b0sLLUyYcz^uku2~CtQ{OtA70{YHV5M--2PS;wCfg$"
    "HXh#a@9V=*#JCxIgg<Y2y_bL5eIswPhu_d`z<i531a!J@da=PEW8l%w=5swL3|nCZ&j|+wf$b8N*q?F%+&)NSpBvarYqH~XIp$yO"
    "rtU1oUB)%-5N)LbG_C4Jv;icP6s|U5DCmH;noZb5>7Il!FTt-`zcT_%Ywlrx2hsyEj}{uE5SoDLCfg97umL1R07+7qL9huWP<^?8"
    "3OmMRD^UmPK66^1fej)?CTX{;#38W((!SZd#zILIz$Ae!2~H||Lqvt^(;x`!Ai(S=#x2SaP@f+0J#(YCe>(N!zJPiK2p8Nw=k;U5"
    "`XFv4DEW_L&>ngk{67H%zzx8!!R)jlNKyku@ZGrk1^DLwx-dC@|4{q^e2DxH^#tiZNd--i5}!oC{ZGX_2#3hw=z#o4e*cBzNN^$Y"
    "RS(sK27o=&%n|-L1IN|-EdGBasuCbO1O`nahj9cvl28<f&=nKNBiID+2i^to$;0u;cSHc-_93H>?ZMK(%8{(5n0T(#q0Jq;)p>eJ"
    "ybKz0OqU=9JScWQIXTidnRDd)%#YhV=*l4jx(I1KQ4lcHotNxwK`{fz-rZ!#YH-1FTC)s}qM|vEFeWKJGXxR@;>+}mHw@t6APwgS"
    "00g-o7xLfgAhbm{K!N5Vk_a|`J@8K_Tz5U)5u{cRXyR9S8rINtt!r7<l?5FD!ia{F1rK2Kx1qD0AfkRJMjQ`0#vcHmIsXV&kbU~T"
    "06QwIr(_dnA@%5;{z8FUdB&ycT57?WQ3^dsJ5OH0#J4I5(*sJ80WrLcKQ0_ZQRhcmRM@bGH776vXdy?BlZlvyWkHCcm<X;`MvnK^"
    "&rVOeQ1}IB83T~+zNzWTX%opAl3=R5OIL6QPTmg;Bs9uA1f6aGkUdl0DJcpR_V9Ur>7^66`41?ln-8O*X;CyE(jp7^Dz3Ch3)DJ6"
    "KoRa1t;z@@N(lp!2_pV%2DJW9+MAAWLHbMI+{g1k78M!9CTviYzjfHT=-k0ZoX5`VzUu&Wx$oXhVa3Q}(47=;P9BrhSmzk$8}U<T"
    "i~xBR5rBBvbQ{-r^A}mpbIcCfa1<cHPpyZ~D_NjjCS=<khLCk<e00D=kB*oe`h2``9(g<PDj2+Ij6pFz4uN0IwCo?Y$~1>j!NEii"
    "NfCX5Pnr^kd%yr5`N_<<1Ku`PfkP2SG8OC-$Otdd#s4gFX+%?_NSl#BIN#6DJKe<lW6#eoNUC`pf|uX<CM>_s0$uv)>Qe(AZ^ZI$"
    "`(Aj)-ytuLuQUj;1B4OX$C`-ZInL^ZH!R2T&T$pd!UO=%ujm8-ejrJ!9N=1NW+Kt0i<dtFoWA4u%K($lr*1|my0{+IdPrPHI3gzi"
    "xbp9m@0_Fbuf|9K1EN6D03r!M4g~?m2pSwN&klfRRYxc@CvB7*>LhEJIEJgq!3#`3U9)sI3yy-Vu^&P2Sz6050Yl%lBOo2HMF|1~"
    "AEX_-NW?`<i(0+~TeWzNHIx8HgfRs$?F}k=+#kjR@-Kb7N{i3Jzk6V87x2<(Q$Vl_v=G2wDfA@kxhJwj3ao`KNTKKm;6(ON6WJPq"
    "M(dyuHehmcCs8{O022rY;O2A+o?M?H(C~Yq!XA7`W7Rfvap<d{1p5HT*cC-I2ndH7F^HAVnSB8joRs{u0tf~Wc3$N40rvnWv`i2v"
    "Ta$61SwREq(om2hu(l?ULOs8M$@~8x5PNiwsA)&mUFIl%L1YF>h~xq06K=z#dnuuP8AIGaB?II^+3pJtLxlj!rgsi^5@&c3{jQft"
    "XcLu@<rPoX0Qdoq3WEmI!Z`GSJ%s_~RdWb!g5ra%Vj<BK{Zui~oO7%$gqb6U>4=K(licS$ZymX<7e<VA8*xLZ^2#6`5Cf_O4I#>T"
    "k3raefju2b=}{mKz|Nz(2Z4Eq$bk7J8W18CUm_DC6rl-_2|!Q?A0c1&dYt=ldBlm#SIDqU*Lv1Y5vvG^004q>F^LfyM<*l@JeP?V"
    "K_YcHOc30uY3@P!@Bjy3r&)$bb}ZZoosS-XlAtjHm;@j_2Q=M<UjP__LG9-?&l5s~F!I1ZZXR}^dVA#10Ya1o1W3DBPO-%exkQ0Y"
    "GX0NrLBKRZb%zyb0;*|Q8X_g23=ZhLqLL~ah2(}RW+)F(MSTEH;wj|tA7p~2N>xQSb-6NwS}A7RmouGic3PlOQpj5qyBAx!=}271"
    "Uz)kK=VwbhD5Zo!U{EDhlu{;-vp5pM3Nqj*cjIo<Jza*8U90?D14IW3<KP37K!2Rs5K>e`w%8*vu%xi0sHS8vh*Ut48$}6;HWC0+"
    "Xe%=jutkh(M$wHHiVd-1jU<*Sm`a(p*re2y#Tr{}qiUmUlufCU5ZWA_5fe+u3HeBx6%7)0k%5CB!DIPgcr>7AZ)Z<I<}eq01Pk+>"
    "9e*Eg$nrZ*K<U(WrjgKqdm1~)i+k*ZRDuK;5ne;+0upqdqLP&Bdzc)69mAlX3MuWyDz1mxP{dAONHIFE@s0O7cSF?KLqfEqte|wH"
    "A<9(|5ONA~X#zlxw+Ddz!bo)zpbW`O%xohPgsioYAlivShysxzYC=W)z;tSZZHVn&748Z@*l2e$r`o%1$Ty|Wf4R-UmFc?YPjj-_"
    "h+t+JGZ`oAudcD!ucXaD(vgDsW|4?Pa}EqCGhi@aMc|<(sS;W^8ZxZT=dv6e1@^^qfg)QUJpsz~(2lxQ{*QBy@{{G@1Xu<Ef%5o1"
    "VyCJ+8xP+ngBSGUTDOw7wi?l_(taxM(SU#;fPtt010j+i0LU1~2Ej>S1VAtm2!J6H0THAG06-B4qzo7l6;)J&2#cI}<3UBI&_owM"
    "iS$bkWsF2X92M4UlvEMNQ|f#tXPCnn%rGIpfg%eHK%?E*{whid$|!w*=O>OXIqWHn8`iXDYeKJE#`$L(5#fUlZ32gY07N(FI0yH^"
    "AXJN>;QNd*!=F3c@jL;fGgyaj=|l(71|M9>W<i7p*VvU00>0oMa34bZ2Y;w}Q<g>#xe22W>jh6berHq!=SsM!Ir_%MKNVHFd<N=E"
    "hLRCa!B8XDxL{zaCiA0WQD}Nj?FVbjn6hPrBkLiAXcdG2GL=MsX8{$^W_`Se<{qjje6STTL^OXe`GHE5=rlo?3=n`=KVds3^-3Q8"
    "-@O19+p!Q2GJF|^cXZ+NtzoHLRS5_Bp>?C)!4g8?uq_OL!9N}R=3H&P-;409gMA_lp?ny^5eu*7h_Bx>VvQft4@hh(Y*20jhYfu1"
    "_Su^3!yR__7gK-DeE_$<;}pj3QR5^&&%kdnon1&B0Ha7T;OQry%HY9e5%YFNfzlix8}naP<{iZh2TyavH+N#|pdz=x#%}OQQfLe^"
    "5M3fmmbKL9mIO2_W_McB;8v&rP((Tc`~U%@Fy`+FQulrX?+4%M*!ztlkK0W|bX5CKU1z#=I0Xpyqi3wBZ4~bDBu2nvF;HX_=Z1K}"
    "HXA|2TZ>q^N}@i1dT<}Ih(>`q`?$Xn(66+E?7}XLv64`mHFGf9=G?VcHnBAsWyk=eT#8XBurUC}&0~b9t3n2*2}~ez2!(PC%tj@0"
    "XbuPiATm(}#Z3V%oNIH1qS1!6wpEtgZtd7;jS*<dQHyIytDTr+<S)~6EDk_?_06(^jLZ!A{RG+@aGiZkiiPwJhA-TmU*mp1w`EU-"
    "`hxj>U<R~{@-&CE<Pj(91Ar=8vO`G7h~qkdz!XR`K_h&*UcwRx1w~a*llzX<^A8V!5cgtPPdH={0n|t4ie1r1?}JE^=tT1aN)!~R"
    "1F;_BdJPWfh=lC&&=e;`j=co?g#v{5M1A-!u@7mO2jhA(VW4%e53Hyh@5-tiJJx1Eir~O1dUoaV)ccRee{NoMCP7m+u*oz4m!g}5"
    "RncBI$S;6D4g<KV_65Vy?0iE}?djpcxHAm{h6PZ74_n7YIXH*9AAfbFJpc!z&!~DwnGBfp-~sO{cWGW+XVZc6-fUBe1r0f)Kq=^c"
    "X{0*Hp>XD$F#55c*w#W*?H~Yg36N-5_QwQOl$g}ulLM$xT(<_LQ0gCE6O+`|DR)DdQ;*i~@2pQS6l%(vLQ+hf8}+|9ds^7#5}PoH"
    "@qv&Xlzr4ge*fta4}N;(C}IR0I>S+f4nYw}1uUw62j(qFO;moH?Z`p2#7!TfAfHuLkx=cvyk)HIwS9Rz<~2c(<iSd$q_r24-Lv6y"
    "Xs%UrT1bs&>S=XeS8j^KG-?|$GiA4(((|2d%X)RP5u3eNR(WxHblL+NIm=!UGDk>2iIpy4jT0+MP*)j=sd1)tWD-;y8Jhx8Ln0+b"
    "b0-{75Qdsj<1j>mD)hCr>u(%f?t?p>wW)N)5l#@G29QDp--Sb^;y;Jv0H??6BA;YakA*?wN*S#uB#5sP86x|Sk1&Aw!vXey)R6+G"
    "bGVp`hlla*yFKr6ARd<-kcbHpVi4Ew+W{xFl4Pi_!lFPJ3K75^0GI^lo7$NLNy97xGXjFl0xSU~NsKTskVb>DFSgO}XARaAb>%hM"
    "TqH+Z(Obl(V!O=H$Y>xG#1djqLUbb}Ao8;!XpvziZf7#3UIf#;as{&!ETS$h0R~nA07Vp$OzRQa@yr?zwcB}>Jxh{x8LWA@=Pc)-"
    "2yIb2kD=2Hy^j=(RENqC#u^aFI|65>x!x2W0bS>)D#+~Q&dCV>eIq-UuE!q`OcahCK-<|)zSqH)k8ahXGuF9_Qw(^30W&x_o?U9$"
    "TElUpe7b-{b>Fez$dhVlJb>bX;SVoz&>RFK;FJTfyY^KM5db?0{Kpylr?!Q~LrroXdk1qkO%gy8;Nd0tg62ILR7eFSFXnp*FdDKl"
    "jK<3p7{lX9lxs1lG7BvRmQWClLK$z}HiQ|Vi~#b1Y__6|2yD;+#0l)Z)qJznL)16}Ny;ilJ3Zy;wQ)`bPmKf%==VT}@IH}8<r_Ij"
    "^4nLx$m_WlF6+6pUEN@lvdn;*A0Ue)GMp!21jPUcA(hxDp6ChSEEGJVuVxN#{l8;tbkX2h`M=D23xY`{?CVnE9kAoOiutC2A&#VA"
    "fgw;ngJ?NGMFa-uYfKoB!YB*3DV|#0EHoq+kX*nE$32Z!0h|yJ8~_4153+r)vU*RTlcL%VqGDXdClux?T%Z`5b4sAlMo@y05}YFC"
    "utXM>v_R1=lUU`fjMag`5iZU*sN=ez?~<c=JP`{4M?0=di)PbK8r{5D&2gyMh+>CGQIJshaN0-IR7TJn1At`c+9C$Q;vd@x^rBsF"
    "pwO5BBaz4xf!v|x01XOlc^V5tC@0|{XMUw%W<)Y&im)*ZDJl>Rc<b&W69B-y_>XbWbabd4pTZOC4P?JRbTA!4eB=~f8M7To2?jPO"
    "Xi)bAS3AavfQ|rjC%A_T#*7~u8m{DUXctl<8hsQumKd33G=Qe&>WypK)g|TgC$)QBioS!Kj1&`LzH|yd8hQcji1GroSXr7PHcdu~"
    "t5>_)*AC6>iT>AB?t*9)I;sy|qN9X5lrXj9BQW<Me37;jlpI5_6;VSNsw0{0z%KlTaM_uIVU^T9=Um!KT+S<QdA#x@sd<ge;1~iT"
    "7kj1cuJ>y6-GjsgEDi<lj{ASZtcbPGYi?4K58o-hew^DLYBkOU#tvFYEW;sP^N7%|o#vnpXtZ;NtsBwRmbNA(N+y{NMnkEfphKDF"
    "G=&__39n|`+VHzqcWXs^nIuVwR`+7<Avdi?oPo88YZr0`&0&y+p=k(0<_<TAyh!m2o4_{-xhN`?Hi4QfbWWopJ+S~XYHmNg{{y3H"
    "it!M2dqJ`bXMG%7%%jam4NCF6L^O&*3V|R1#P)Gf<j@MZJCjQw@<MYZ=)$Q3aum9d+<1hgS9e*QK!CVLj&TP9M0lKlW=zEtFjZIq"
    "_|gby2TF@!$m84x=74l_z!D+FR1Ymm39(QP6+;JrMRW<KuI{^4KP+<QzyPI8oXioyVWC7+um#u%E^3M)P!EMC0YjBwkv1YZs9;Qi"
    ")sUmaE&?kchS>^4f?Cp|q=ujYBI<@%5<@fr9iRZ_NGO{@0KmY99fb&j*}YpKckc%XtH3M3=(O2!rwu@*z~r}h<ShkJjMOm;3vI-r"
    "##&qqlN}%?8pU^-k)i;VHtTb0N0@+nVDa=6R}+XuPg1%#-#S$(WeA?I<>VA0A0gkN$ag#k`Ngml+f5N0FX;Re>P$@`FaY>dgOM?7"
    "nN-q=fV3cmAkj)BNk}5dc0&LFjkA)p5?^Q>Mcf+^LUfMg3;^4Thq!or!Oqa<vDiJnH##y6TD8-Om^#fG3sSV7KwcDcZ+?3y5Qs_K"
    "g9Htzh!UaW4QPC*MC=9>S7Eum6%an1jvX{UB~VZ8w)1ferjN*9-v^LT@D~VVFH@5B^TwAZ3o#5@0La2Jp$uhEqJkzNih-U5O&V|v"
    "HUb!v#*`CV9Wny#bXKvfkj?8(g_O}Iq{+ffNNJ5`8B!)o7P1U=AZ3I>nW$7o0nvj+KrkgB>UB1Z4Q38zv;dH*o50Kpa+V2H2W1Fv"
    "XV+no2J;Z3ghhMfszDx65H^Y$LD1=wgxDB52vkF8+9Xne0A!F7YQtAmmS#5!p>Yygj!bE11WibxfHDee11d5x)rN!=f5kvUkaUpf"
    "Q8@!ne1niaYI;Gd%UO|u4md>rZXU^RV2d79LSaI_V?zw4gOf2+ED~bEkmMn#-qkVvX9f$QFvK%p9~=;he&zhsLk~zE;;QNp`+|gJ"
    "{eZk2{~D^0pdF@z{D>fjpgrCdJ`hv$0UuTbUY>B)&OjUwm;fEbReweepm**EI`lLKC=LlIV2WSBI|utd-{koUc>wA^&me}mPvrto"
    "^*`P~t4H5?Jff5!1MdFmJ!l|K4}<$?SVQi72&V$4U#U<dG$g7b$I7ep29#;O7S|O`vs5kuiNHRmZ|z?rPQ?6`P9Cq+lVFJf#y{Ht"
    "5Tdf6ls5dtJ=86$<+Zt5yjxY{$*Ld_LL>r&m5>sKkO~J-zF_6G<5W#%*;F<wQd<?0qy-WN5k!vT6bw~SkrZSSAQd4N5(LRRLg6*z"
    "ZEhPob+=)HF$N6;MmCFWwZ0kinvJxWOo2ly3acR?%=CL8yvP7P%#ERX{w5>2QvfcU26NZv=yHO7JE<SGj;7@A3GnSvSlKD)zDWmi"
    "fk+9JDC8{sr4|0*Bt>{d2sI+7$wfSXV7`M-2Xo-Zg<m7~k5Ujfu$}>M&dPkYBASDTtUll$*Cz&(@Kh4^&c&rwecc16PsBO4of)Gi"
    "4j}$gX`$aHoyPd&;@-9=BudMxTw-aqE{wxi+RcP$f}Q5q6xN<2h%^?lHwHLyCcN>@p~*6Um|1pno8#eCdgRtP3A09J7&Vwz?gb8&"
    "0u%ww9_M*SxEuocRbQ~bvBN``z;&HYeK5mC$ggD-@EC#F6wsbP?!5s%Qh}ilL_R^-Eh2Tv)r3S|V?Dqgq@b4>`N(<vw~zoQKU0sF"
    "&~x9^&?2#6fv49K6cB#3aH9pV1ME8d%w0%{`oigepcN_Hpk`(k{3+A>w1M2=zGa>lvIomosG0b#`8-tJy%gyZLGTEyIsjOTeuy39"
    "C`OF{kGdugA6mSk0tfZ|B77fQa5KL2TgS+Ix4`lOD+l2T_I^$%Yt97*SgHZ1h6z{RPGrb~wq#OSAt+!yJ@|E6z|O$C4CXf`Kr7(_"
    "1Iy|3;fx==Ao?2EYA__DF$n(t9Raru>7s&w&1SWMr9t%Z?t#P0w{b)-*hD4EkvfNMbAFRBMAGyaAQ_QIxcmKfVke9dQ-}hVgy^Aq"
    "DhwaYc5K-o@cIgP<i6~Q!^kXXtrlmfcMkHWkXS)E<>d3v0D2yu#6&td^8^Zsi~OXe9$k_|q!<{7J)_n=nfL_`Jq;&t(ikKGsO3=Y"
    "i0{?{90!MzdyO84yK|YCO=XOf=;bpTl!j%4T%bla0R^(N-v$I$P&-t+Q8^z(2ZTx_5DugSiCR?-<G#W;2s+?79-!^+hbSP0_iZAm"
    "fa1`KU~(En<N@YDO~P^8opN&pCnx|gGwA~Ke{n~U{xj!f%aJOJm~Kvx4#<O0c>3TU6$<!6KmcH$RYdkPhyss(T$z$U)GaI&RFo45"
    "s6;{m_XAFZ-;Q%3iX_S)a>5*63n`=mBvTJ;fpAm$Q}%*|s5#l`aS!JRcUoN^kyS9UpzabXZw%!;U}B(<R-;y!s*x3ukj#(<44H)1"
    "RyT}P&6!5LOxjtx*Idm>ux2~AH7l;#-7AgPX$DnEmnm!uWVq6{N-To4kvu7LDu!H^T{A7l(?ZLTNn=@UO%NN`UU_S)rwmQ!UAAo&"
    "lAFu7N+BCX7Ta4gs{qMnLLr6-OE?A&1ry!bQ$%RpJ2KYWO4^lDc0VNjAzknvAjj+p+#h*U`8}LY1u<1H&jzvdyltRxi!lPsX+$MM"
    "Iw-uSbOkX~`v|XKUyIO`i}1Sulb8?mqD1r!9bEXG8n+U_C6*}-rFnrbP!w}67%_vHg2fhU(K<-i2Rcem0pbw5;9B2cpUN7?sZ~HW"
    "6QM)OLA77Bs)h)JBQzUr>lirOq1Fy9NYb;K(W>(6wyy0)P0CJGjonRFh$ILT44^^oz7awXv_7fx6xaZX_<;KC_y?c|05TrzpE(1_"
    "3?5Gou)-<|eCT;N{o~#dCIRiQ05QY}A2?3{G6A(jlO?#oH|dGxF5jWGT^dzhH4IB0F*6AS*r#9wfFMwWeL(&m5zzR>5y8Cx8R!(2"
    "Zjny`$HIq!@=~Wj?4Yo5<p9j;D~Jjk1pos}>6#A;e8qcqB3O_?F-0>N1o9v8fuT`-70`jXqyvEVG-~uz$JJ2kne^(OR1<Ts$nbkf"
    "!1Sq+2~_MRtbG&Ug3xaq=58IEI^k7+P_!P{yBEl)dm^3@IzPz)Ct>Yv(!P<xl`95VaaL47pP)-EAXp0{dW=@0%v4KYxEg_ezC=^x"
    "L+mgz5TUq0JwOBj29-nTihD=^KfFJ1sp{~3RMIGNbnPhj97I-8{P)UI9{-Fw{hC1^I{GRK_EFe<`v`%_fGU~+T>-)X9aMc!g%5zi"
    "T?!@|oLSrpL%b6R1_)+?QBy>qY+a(^um^DfshA+2?O4PRSdA|jx}72zkrZ4XArbKR1U$(5Ss*wfkR>k9DB>N^Rqi89pt7Vp4##*6"
    "B!d=aPHS2zu!Lf;F`3t63`B)0AlYp-q{1K&00640h>fNIs}AARMT(;001N{n>?`Pj@T;$LkH^k_9)8}vjN>fB=bpB*0?@@JYRQA2"
    "eB%i<st5k<lRpe#LVY4^)EH11Za$aiL+9PkI2gAA2lbT<U(}-Z-;;7&L#=OX!#y(I<@mc;cW0@z9-Ha#g4xDuCiQb(OS*;9rvgWH"
    "7C;bY<<NHt2LB9NmG%q8E+Rm1QDN2I+%w3?dnlPg`9aaS?rQm~4}H&62F7}0Rh{Q^>SJRn!<Ne(eR8`#<0TEj4Kx5Gh}QWp!U*}M"
    "*_^_lF<}P)TVGBPBG7A;9OEF2UQb&2L(2O(o{+ohXO2UZ)&UFE=^Iz{{rZv7l&Dzh3^sXcERkaH9eQ9+y|YW^K=H;ZB?BO-2q^)|"
    "COPl`Nf0Zqh`z+RZLfa4tBd-VXI)cnqn1s=>&CZ0D@zAHD~(i6`e}nec3K6?v(ufgDq&BjliYLfJnBYCckyP=Rnize<#+>-XesyD"
    "d~!FKBe>FPcEBXi3d^i$AEA-*BP0ZHAc7t?29Zmo(Y89-Gf6J0;7izzAts%7m6KMk8^&i6pddCnLwoyN;CuuU2%C-YWwM}sCqq_)"
    "9apQJ3re%zq6EmPSKS%b0)FU-0Hi_<6p2WWcqCii=Uci2=rZ@ryZ805Js^to10blFsoVwu#Z?+XIy(Xo0>SA}PT;UEl|Ur~9V9BD"
    "z%QFuy;ggG0002>xmyS@3<D<7F$BOg2b4Ags~aKSRlZlP0kNQviewg9q_S%zqf$thp09`MTmDaZX&%rVLt7NAQKDKm+W^U>LXWLz"
    "j36Seqe@{P&06)tXmcPb;7Am}74#N6xq0_N+QD}b+M0R|UnUvB_Krp1`}ZON+V7sC^!*KT2<b#IK|RWa++4pxA5!B@$iY3$hg9LY"
    "R+dAv^o**#TCsZwOz`fWg<<u-hZq{hA5+$AfC=rrQxp&o*bT7SOeD~0G?@(m-OA6UUn_26|0LACA?<fe2-x3JBQu!${QjPhRM;qY"
    "03O;sau429_5u<etLxuKf0lJc2tPy+knMoHxI7@Jasc^7Gv()k!`oRRD_SQFY{1#N%Pi*~>*H?{CiRDfSCEwN3FM>z9CDZ`gy;?n"
    "t4_m!P{14|m7){p9;AGvP<()gcR&fQ$@*;-J3#FWfqTHOzff`ruOLbzc|Cdz@jWPL1{*OB(?SqHEW{@dAZZLV_aN_>85s<$$izxx"
    "Iz9XV8bh56xLnA?07I^Y=QufXY^4HX6P+`!t*b#mm<ByTuz<--U?hi;K!9R7K<*tLP~uPlf)aW`+LF;lwDCj_P!PFXMH~j<4DX=9"
    "4}{yDCH3SGapm>^5g`sxQe6Uo_7qVks4@ie0!j%QokQ0OiHm{8kN|bK{pf$S$KC^dR6bP&3joL==zx$6r|Bq#Vj2tu?~)F^<Wp>d"
    "niDtivL%pgcZ!<F4$r$EF#%W~ny&yp<DvM3I7C8MQC13w;-rEr=mkhf7EwijMPMFBp$Da$^iFd#GPIUSGh4VO(5Tg~d)832G*J>1"
    "a7j(r0oWQqPQt0+(sxuI;5<EDr(m8g$0{084FkscM06a92|&`N2Mnf4xTq8EBpnqOW)x~fLudyeFb?#GLLulE6+IiriwWS9Aqz~D"
    "kyr)pHQ5nwVa*(HswNNBdohHiDj%_dEHdZMQV?3Wz$WxT)5)e747YW3B}tIHY&&Sc)G8U##yq^%)>KRY10P8QBMwBP7c>AW6#4)H"
    "!PP|70kpu_GKI)PIdP@{p#&IT^72O1?jXit?KuJ48a|V3AZx(bWKM(-Nznl^JljKN+yzL^h8`^M&bvnmpcOTw<9KhM0(x(r4C{FI"
    ")*+HT`X0615n3wjNv#;R@!Eygo;D{OI;I{s!Y2R$V}s9K-JK$kMG~_nSM7}7Oy?>wE9lJU4DxJ}WO11#WkBhCn$Qw&X9S7?h?_Ar"
    "CY=gw2nRrjU<I@s0l*!O<ta6VQ%#sT0ZP#1FaSV+AhJ~`wJ<fyhK{X*41`D-R3b`{fhYnSBtTwtz+)zEU=S!|by71JcaadwUEM+r"
    "nxH@@q(A@&NG+;EwCvZMKu*BEL2y+}1>ryl76f!Yg_I#$2A~*FmZ+)%Dv6ZPp!yY{21zIYiaMU>&4N1O7vO9=Bmk>)`>{NLg8ZD~"
    "Fv~mCx<!LViO>&Z@C$?W1^R%w<FW-9q46MzNFcCa4cjw$gi^pz1SAy8{5Ujmu~6~^h^*{DM0A0kku$*c)`%@EZDR<77&f+z0kn#Q"
    "B#K7mjZq}UX>rVLh)V+s*Z`W=36VtFbPIr>LZUE=fdEVZ0T2NoE`7y&TdMV(HFlwp6NO=sf@(%P<Ex0s!4-QQG##z-Yfnd)sCK1T"
    "pRtB{$e@kcds(QeAXe7YqpY#N2pL-7=B}y%@C$SFCl2HsfO?QHR7cns0e&8O&lqOWPJ%)9ex4ERc*?BT8egXdJ2^RHNMLO63lJY`"
    "NLm3W(ZwZs0Qrap0t5I0`+@QW4&I@qPBcIuM{@`dpT;ImNlN#4L|0x1_x^@v0^`=!jB&V=s)q5YU6vCt0X$i#t~4$&CTZhF&MdWL"
    "8?0?25~{)hgT;hsn~V;HPf`m)L;@7aG$_F$sziuzL*M9}hSk%k))Tn`;{9Yhhy<do2s$DB77`$!4+-bNj&hoU#={s00)bd?j50*}"
    "k|a4Od2<psrO+B7^Od|q%7@G#F;}Pn1a|MFQ0XAfR?Y|<cOyZlBe5ibB*2YvP8CVz#lx^+UZ5}0MX@0ZL^OnfpacL$Bfjq?swo&&"
    "Z=A^1@S~i>q#JmS0`AFqc+tJ##j}8PCWavAj$L6A8|F;j^4@45V{OrJw3K*q!y#hp0B(z`jc*)|BzFxa!L~sWl4UMf;fPkYTmuqD"
    "hFr<KH@Qkc*7a^(M39t}flkw6urNjmf~w%c5rX2VVBifpB`0_|z;Q?>G7P)kWu-M~tT3h(>#;LUa2(>zT+C^cMrLK8SXvOSHzAgm"
    "q!c<33{*~$O`@2JWbcARS5uLyVWgeKhCJi9uNgJQ=@cSbq}Mt!-4Yu;do)maXF+NMmGT~spaY=;l|<@=A$P@43?vnDOj-yC5nRhG"
    "Ku$ZRws4BBRYMq-RT!zpfftn91vC*ORK$xD*dM5N4IZL<cm)%<ig}d{@O%Qoe9=OC2d9)UGu76p1RzCV+IW+=nStYCsq3!Dq%S%)"
    "NTiw{yA@XhUQIq!4M4U#!%uA3u&PIughzvf-4p>H$e8pv+9rlF5*CPrZo~B2N6`B?2`WJ}%NQh5U?G#gSPcx^xWIss2|}Bg5PAa0"
    "ra~#r+G2T^S}pY3*Y=!cUPTg*97*eqZBW{XY%IHuWPt)@gcyNj3ei!f5D^{#9>JyemXHh`AU$M4MG=u!m3;_BHmCD`#eD1^e9wwA"
    "1T7+%u<pP<`A6eqCOF#x`=vscQYJMhr$t%)Oi$<_@evd<vDq<EE}%r`wix7Kho}HV#?+z^6ey9Jz}B7{;S*|ZDC0dJ%^ytR0DcSv"
    "`$>@L1Rx_oyC1+)$fN2H?uP+pKwxqVf{~z9xC})8qrG@g5RW2@{bziyY|5enugK^pkVRy5@=ojbN8p2ysE?qC{342IOUf$4fbfi{"
    "srFP-=SzVQZ2^J<x_<F=cQV?b!J$maM+2mH09Q%mL3|?yA_4^c8DM2~6a%_-BSeKZ(A!H<riR^ZcudNSl!X}~0wmN<t-A>+^Gtg`"
    "!a|d9zVWC+mJ&3l-@Dw+W`cyygak)>->n&11U&we6(jk{=fFJ|)2WH`1MnqGB^7fl8j(Zp1vER}dhxvq3hck9#`hf*ia|0146-1R"
    "C?=L+2UDCTfkcGlnC_pHA<%LA6YK9@<OCnMLiPX=BkF=0!TX*JPl-u@k>hPOsaAVco1&D%VUlGn3L41NJfX=7g+L$|nOuY7LkMia"
    "K@5~YC^APp;+X~z3cIvGi9|ch2Fp9ICr}0pwCQChDRtgSb;NTO&S(=(2fsPhhoLMA9GwMtFXzSY_Snp{>oMpA1CZ*3m&KzsmKg0p"
    "0Ct25pobynXBQR#a0iEzxCn9y$P8;pq`Y=hK)mP&eLYngY9K{%5nM6}ppt@^aSVk*f<nS1l4&9ZGR$#QLBLRzL>&gg57?u={GWh*"
    "laxF3;3ogJ=pDsGZORY{<|L}RW+R|{eb;f=s`vp9kPmaAQ^%T;kcnan27r*|#H)}5^})<mNtFPvzBsuCWRZbp5{JaFupvpd5KV?c"
    "F+_uzupwLlK-?56A+k_Uk77#g8HcNp^d5e@-SWfs>WQ5rhn>FsClAsLVd4biqGE3xVue-6+%>Go%(aIaGjT^9;d6g;MF8+J<RTFN"
    "h(90!h#OhqxCJdph;kcv?W2lpu|vMiMKO>Xj~UUpIIavyK;gy`;^4r*(gLzfL^voRE+E7SiRS3l9YE);P^@BGbZ}vpl`}&Emv092"
    "_)~;U3QC<C#x*M<h~kYv0VtSap@b=7hB#vjO`@je6E@C9ow_c$Pg}lR2(E$+cI&SguLl4hhYlRwwN_!NGf}G#Ili7FIM|sllSTu^"
    "X6q@G5#doZ0GNP_q!Zx{XegTex_yv6-|`7G2z>fL?)X!b4{*}BZC8=k&f2%t+ikwL$rgiS8Ywhm5uzx`7D$X}+eK{>%xNLA>aFs1"
    "wW{%JT9kAEB6|b=C*%N$&;|fQ{1sV10)KKqlq4*Y$Vd}k4t~!?^!z*cmv1wWNoWNEdcIro`lR&`oWs6#%Ng=S8wv+bfBr7yig2MJ"
    "Cqj@`"
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
