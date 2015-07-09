from datetime import date
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def get_lafte_stylesheet():
    ss = getSampleStyleSheet()
    return ss


class HeaderFooterDocument(SimpleDocTemplate):

    title = ""

    styles = get_lafte_stylesheet()

    def header(self, d):
        return ("Låfteweb",
                self.title,
                "{}".format(date.today()))

    def footer(self, d):
        return ("",
                "Side {}".format(d.page),
                "")

    def _draw_header_footer(self, canvas, doc):
        h = self.header(doc) if callable(self.header) else self.header
        f = self.footer(doc) if callable(self.footer) else self.footer
        dh = doc.pagesize[1]
        dw = doc.pagesize[0]
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawString(cm, dh-cm
                          , h[0])
        canvas.drawCentredString(dw/2.0, dh-cm, h[1])
        canvas.drawRightString(dw-cm, dh-cm, h[2])
        canvas.drawString(cm, cm, f[0])
        canvas.drawCentredString(dw/2.0, cm, f[1])
        canvas.drawRightString(dw-cm, cm, f[2])
        canvas.restoreState()

    def build(self, flowables, **kwargs):
        heading = Paragraph(self.title, self.styles.get("Title"))
        flowables = [heading,] + flowables
        return super(HeaderFooterDocument, self).build(flowables, onFirstPage=self._draw_header_footer,
                                                       onLaterPages=self._draw_header_footer)