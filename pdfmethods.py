#!/usr/bin/python
# -*- coding: UTF-8 -*-

#Copyright (C) 2007 Adam Spencer - Free Veterinary Management Suite

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

##Contact: evetteproject@dsl.pipex.com

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm, inch, pica

pdf = Canvas("/home/adam/Desktop/evettetest.pdf")

pdf.setFont("Courier", 12)
pdf.setStrokeColorRGB(1, 0, 0)

text = pdf.beginText(inch * 1, inch * 10)

text.textLine("Fog is very handsome.")
text.textLine("Moms sucks balls.")

pdf.drawText(text)

pdf.showPage()
pdf.save()