# STEPHEN WOLFRAM A NEW KIND OF SCIENCE

# STEPHEN WOLFRAM A NEW KIND OF SCIENCE

Visit **www.wolframscience.com** for the latest information on the science in this book, related material, software and initiatives.

Send mail to contact@wolframscience.com for questions or comments. Do not send confidential or proprietary material.

See www.wolframscience.com/contact for more information.

**Author website: www.stephenwolfram.com**

#### Publisher: Wolfram Media, Inc.

*web:* www.wolfram-media.com<br>
*email:* info@wolfram-media.com<br>
*phone:* +1-217-398-9090/1-800-943-9626<br>
*fax:* +1-217-398-9095<br>
*mail:* 100 Trade Center Drive, Champaign, IL 61820, USA<br>
*international:* Wolfram Research Europe Ltd.<br>
Wolfram Research Asia Ltd.

#### Subject category: General science

#### Library of Congress Cataloging-in-Publication Data

Wolfram, Stephen, 1959 –<br>
A New Kind of Science / Stephen Wolfram.<br>
p. cm<br>
Includes index.

ISBN 1-57955-008-8 (alk. paper)

1. Cellular automata. 2. Computational complexity. I. Title.

QA267.5.C45 W67 2001

500—dc21

2001046603

CIP

Permissions information: www.wolframscience.com/nks/permissions<br>
(see below; versions of images suitable for reproduction are available)

#### Copyright © 2002 by Stephen Wolfram, LLC

All rights reserved. Except as provided below, no part of this book, whether in physical, electronic or other form, may be copied, reproduced, distributed, transmitted, publicly performed or displayed without the prior written consent of the copyright holder. Nor may derivative works such as translations be produced. Visit www.wolframscience.com/nks/permissions for further information.

The author, copyright holder and publisher wish to encourage further development of the science in this book, while maintaining its intellectual integrity and preserving the value of their substantial creative and financial investments through the maintenance of appropriate legal and other rights.

Discoveries and ideas introduced in this book, whether presented at length or not, and the legal rights and goodwill associated with them, represent valuable property of Stephen Wolfram, LLC, and when they or work based on them is described or presented, whether for scholarly purposes or otherwise, appropriate attribution should be given. For purposes of scholarly citation this book is a primary source, and should be cited accordingly.

Individual verbatim quotations of up to twenty lines of plain text may be made for scholarly purposes if this book is clearly identified and cited as the source. Visit www.wolframscience.com/nks/reprints for information on classroom reprints and copying arrangements.

Illustrations (including tables) may not be reproduced without the prior written consent of the copyright holder. Most individual illustrations in this book represent substantial original works in themselves, and their reproduction is not a fair use. Visit www.wolframscience.com/nks/images to request permission to reproduce illustrations, and for information on high-resolution and electronic versions. Permission to reproduce illustrations will normally be granted for scholarly purposes so long as the illustrations are not modified, are reproduced with satisfactory quality, are used and explained in an appropriate way, have adjacent captions or text that clearly identifies this book as their source, and specify Stephen Wolfram, LLC as the holder of their copyright. Stephen Wolfram, LLC is the owner of the full copyright to all illustrations in this book (except as indicated in the colophon), including their form of presentation and such original elements as non-obvious choices of rules and initial conditions used to create them. Scholarly discussion and development subject to restrictions of fair use is nevertheless encouraged.

This book contains many *Mathematica* programs in source code form. These represent licensed software and may be executed on any duly-licensed *Mathematica*-compatible system. Their source code may be reproduced verbatim for non-commercial purposes so long as it is identified in each instance as a *Mathematica* program and this book is cited as its source. Derivative works such as modified or translated versions may not be made available without prior written consent of the copyright holder. Consent will normally be granted for non-commercial purposes so long as the original version of each program is included, together with appropriate copyright and other notices. Visit www.wolframscience.com/nks/programs for downloadable programs, and for further licensing information. The *Mathematica* system and language is copyrighted by Wolfram Research, Inc.

Certain material in this book may be proprietary, and may for example be or become the subject of U.S. or foreign patents, pending or issued. Inclusion in this book shall not be construed as implying any license of any sort. Visit www.wolframscience.com/nks/licensing for licensing information.

There are no warranties, express or implied, made with respect to programs, specifications, models, instructions or information contained in this book.

“A New Kind of Science” and the form of the cover image of this book are trademarks of Stephen Wolfram, LLC. *Mathematica*<sup>®</sup> is a registered trademark of Wolfram Research, Inc. All other product names are trademarks of their respective owners.

See the colophon at the end of the book for production and photo information. See page 851 for explanations of cover and endpaper images.

Printed in Canada. ♾ Acid-free paper. First edition. First printing.

# STEPHEN WOLFRAM A NEW KIND OF SCIENCE

## Contents

<table>
<tbody>
<tr><td></td><td>Preface</td><td>ix</td></tr>
<tr><th scope="row">1</th><td>The Foundations for a New Kind of Science</td><td>1</td></tr>
<tr><th scope="row">2</th><td>The Crucial Experiment</td><td>23</td></tr>
<tr><th scope="row">3</th><td>The World of Simple Programs</td><td>51</td></tr>
<tr><th scope="row">4</th><td>Systems Based on Numbers</td><td>115</td></tr>
<tr><th scope="row">5</th><td>Two Dimensions and Beyond</td><td>169</td></tr>
<tr><th scope="row">6</th><td>Starting from Randomness</td><td>223</td></tr>
<tr><th scope="row">7</th><td>Mechanisms in Programs and Nature</td><td>297</td></tr>
<tr><th scope="row">8</th><td>Implications for Everyday Systems</td><td>363</td></tr>
<tr><th scope="row">9</th><td>Fundamental Physics</td><td>433</td></tr>
<tr><th scope="row">10</th><td>Processes of Perception and Analysis</td><td>547</td></tr>
<tr><th scope="row">11</th><td>The Notion of Computation</td><td>637</td></tr>
<tr><th scope="row">12</th><td>The Principle of Computational Equivalence</td><td>715</td></tr>
<tr><td></td><td>Notes</td><td>849</td></tr>
<tr><td></td><td>Index</td><td>1201</td></tr>
</tbody>
</table>

