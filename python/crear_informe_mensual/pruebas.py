from pptx import Presentation
from pptx.util import Inches, Pt

archivo = 'PLANTILLA INFORME DESARROLLO2.pptx'

ppt = Presentation(archivo)

print(len(ppt.slides))


