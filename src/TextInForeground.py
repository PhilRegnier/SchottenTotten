#------------------------------------------------------------------------------------------------------
# Text format
#------------------------------------------------------------------------------------------------------
class TextInForeground(QGraphicsSimpleTextItem):
    def __init__(self, txt, parentItem):
        super().__init__()
        self.setText(txt)
        self.setFont(QFont("Helvetica [Cronyx]", 25))
        self.setBrush(QColor(255,85,0,140))
        self.setPen(QColor(21,11,127,90))
        self.setParentItem(parentItem)
        xm = (mainWindow_width - self.boundingRect().width())/2
        ym = (mainWindow_height - self.boundingRect().height())/2
        self.setPos(xm,ym)
